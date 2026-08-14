from __future__ import annotations

from collections import defaultdict
import math
import statistics
import time

import torch

from .config import ExperimentConfig
from .data import DataBundle, byte_length_bucket, fixed_eval_batches
from .decoders import TokenByteCodec
from .transformer import ReverseKroneckerLM


def edit_distance(a: bytes, b: bytes) -> int:
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, left in enumerate(a, start=1):
        current = [i]
        for j, right in enumerate(b, start=1):
            current.append(
                min(
                    current[-1] + 1,
                    previous[j] + 1,
                    previous[j - 1] + (left != right),
                )
            )
        previous = current
    return previous[-1]


def _empty_group() -> dict[str, float | int]:
    return {
        "tokens": 0,
        "nll_sum": 0.0,
        "bytes": 0,
        "exact": 0,
        "predictions": 0,
        "valid_utf8": 0,
        "known_vocab": 0,
        "byte_errors": 0,
    }


def _finalize(group: dict[str, float | int]) -> dict[str, float | int | None]:
    tokens = int(group["tokens"])
    predictions = int(group["predictions"])
    byte_count = int(group["bytes"])
    mean_nll = float(group["nll_sum"]) / max(1, tokens)
    return {
        "tokens": tokens,
        "mean_token_nll": mean_nll,
        "perplexity": math.exp(min(mean_nll, 20.0)),
        "bits_per_utf8_byte": float(group["nll_sum"]) / max(1, byte_count) / math.log(2),
        "exact_accuracy": int(group["exact"]) / max(1, predictions),
        "valid_utf8_rate": int(group["valid_utf8"]) / max(1, predictions),
        "known_vocab_rate": int(group["known_vocab"]) / max(1, predictions),
        "byte_error_rate": int(group["byte_errors"]) / max(1, byte_count),
        "predictions": predictions,
    }


@torch.no_grad()
def evaluate_language_model(
    model: ReverseKroneckerLM,
    data: DataBundle,
    codec: TokenByteCodec,
    config: ExperimentConfig,
    split: str = "validation",
) -> dict:
    model.eval()
    overall = _empty_group()
    short_only = _empty_group()
    per_language: dict[str, dict] = defaultdict(_empty_group)
    per_bucket: dict[str, dict] = defaultdict(_empty_group)
    peak_logits_bytes = 0
    beam_hits = 0
    beam_total = 0
    examples: list[dict] = []

    for language, input_ids, target_ids in fixed_eval_batches(
        data.token_ids[split],
        config.context_length,
        config.eval_tokens_per_language,
        config.batch_size,
    ):
        hidden = model.hidden(input_ids).reshape(-1, config.d_model)
        targets = target_ids.reshape(-1)
        loss_result = model.head.loss(hidden, targets, codec)
        peak_logits_bytes = max(peak_logits_bytes, loss_result.peak_logits_bytes)
        lengths = loss_result.byte_lengths.detach().cpu().tolist()
        nll = loss_result.token_nll.detach().cpu().tolist()

        predict_count = min(len(targets), 512)
        predicted = model.head.greedy_bytes(hidden[:predict_count], codec)
        target_ids_list = targets.detach().cpu().tolist()
        target_bytes = [codec.bytes_for_id(int(idx)) for idx in target_ids_list[:predict_count]]

        for row, (length, value_nll) in enumerate(zip(lengths, nll)):
            target_id = int(target_ids_list[row])
            bucket = byte_length_bucket(int(length))
            groups = [overall, per_language[language], per_bucket[bucket]]
            if length <= 32:
                groups.append(short_only)
            for group in groups:
                group["tokens"] += 1
                group["nll_sum"] += float(value_nll)
                group["bytes"] += int(length)
            if row < predict_count:
                guess = predicted[row]
                truth = target_bytes[row]
                exact = guess == truth
                valid = codec.valid_utf8(guess)
                known = codec.id_for_bytes(guess) is not None
                errors = edit_distance(guess, truth)
                for group in groups:
                    group["predictions"] += 1
                    group["exact"] += int(exact)
                    group["valid_utf8"] += int(valid)
                    group["known_vocab"] += int(known)
                    group["byte_errors"] += errors
                if len(examples) < 30 and (not exact or row < 3):
                    examples.append(
                        {
                            "language": language,
                            "target_id": target_id,
                            "target": data.vocab[target_id],
                            "predicted_hex": guess.hex(),
                            "predicted_text": guess.decode("utf-8", errors="replace"),
                            "exact": exact,
                            "byte_length": length,
                        }
                    )

        remaining_beam = config.beam_eval_examples - beam_total
        if remaining_beam > 0 and hasattr(model.head, "topk_bytes"):
            count = min(remaining_beam, len(targets), 32)
            candidates = model.head.topk_bytes(hidden[:count], codec, config.beam_width)
            for row, candidate_list in enumerate(candidates):
                truth = codec.bytes_for_id(int(target_ids_list[row]))
                beam_hits += int(truth in candidate_list)
                beam_total += 1

    benchmark_hidden = torch.randn(64, config.d_model)
    timings: list[float] = []
    for _ in range(7):
        started = time.perf_counter()
        model.head.greedy_bytes(benchmark_hidden, codec)
        timings.append((time.perf_counter() - started) * 1000 / len(benchmark_hidden))
    timings.sort()

    return {
        "split": split,
        "overall": _finalize(overall),
        "short_tokens_only": _finalize(short_only),
        "per_language": {key: _finalize(value) for key, value in per_language.items()},
        "per_byte_length": {key: _finalize(value) for key, value in per_bucket.items()},
        "beam_width": config.beam_width,
        "beam_examples": beam_total,
        "beam_exact_accuracy": beam_hits / max(1, beam_total),
        "peak_eval_logits_bytes": peak_logits_bytes,
        "greedy_latency_ms_per_token_p50": statistics.median(timings),
        "greedy_latency_ms_per_token_p95": timings[-1],
        "examples": examples,
    }

