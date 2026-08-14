from __future__ import annotations

from collections import defaultdict
import math

import numpy as np
import torch
from torch import nn

from .config import ExperimentConfig
from .data import DataBundle, byte_length_bucket
from .decoders import TokenByteCodec, make_head, parameter_count, relative_noise
from .encoders import K32Encoder


class ReconstructionModel(nn.Module):
    def __init__(
        self, data: DataBundle, codec: TokenByteCodec, config: ExperimentConfig, head_name: str
    ) -> None:
        super().__init__()
        self.encoder = K32Encoder(data.vocab, config.d_model, config.input_max_bytes)
        self.head = make_head(
            head_name,
            config.d_model,
            len(data.vocab),
            config.byte_embedding_dim,
            config.decoder_hidden_dim,
            config.parallel_hidden_dim,
            config.output_max_bytes,
        )
        self.codec = codec

    def loss(self, token_ids: torch.Tensor):
        hidden = self.encoder(token_ids)
        return self.head.loss(hidden, token_ids, self.codec)


def stratified_vocabulary_split(
    data: DataBundle, seed: int, test_fraction: float = 0.20
) -> tuple[np.ndarray, np.ndarray]:
    groups: dict[str, list[int]] = defaultdict(list)
    for token_id, length in enumerate(data.byte_lengths.tolist()):
        groups[byte_length_bucket(int(length))].append(token_id)
    rng = np.random.default_rng(seed)
    train: list[int] = []
    test: list[int] = []
    for values in groups.values():
        rng.shuffle(values)
        count = max(1, int(len(values) * test_fraction))
        test.extend(values[:count])
        train.extend(values[count:])
    rng.shuffle(train)
    rng.shuffle(test)
    return np.asarray(train, dtype=np.int64), np.asarray(test, dtype=np.int64)


@torch.no_grad()
def _decode_metrics(
    model: ReconstructionModel,
    token_ids: torch.Tensor,
    hidden: torch.Tensor,
    codec: TokenByteCodec,
    chunk_size: int = 128,
) -> dict:
    predicted: list[bytes] = []
    for start in range(0, len(token_ids), chunk_size):
        predicted.extend(model.head.greedy_bytes(hidden[start : start + chunk_size], codec))
    targets = [codec.bytes_for_id(int(idx)) for idx in token_ids.cpu().tolist()]
    exact = sum(left == right for left, right in zip(predicted, targets))
    valid = sum(codec.valid_utf8(value) for value in predicted)
    known = sum(codec.id_for_bytes(value) is not None for value in predicted)
    short_rows = [i for i, idx in enumerate(token_ids.cpu().tolist()) if len(targets[i]) <= 32]
    long_rows = [i for i in range(len(targets)) if i not in set(short_rows)]

    def subset(rows: list[int]) -> dict:
        return {
            "tokens": len(rows),
            "exact_accuracy": sum(predicted[i] == targets[i] for i in rows) / max(1, len(rows)),
        }

    return {
        "tokens": len(targets),
        "exact_accuracy": exact / max(1, len(targets)),
        "valid_utf8_rate": valid / max(1, len(targets)),
        "known_vocab_rate": known / max(1, len(targets)),
        "short_tokens": subset(short_rows),
        "long_tokens": subset(long_rows),
    }


@torch.no_grad()
def _codebook_accuracy(
    noisy_test: torch.Tensor,
    clean_all: torch.Tensor,
    test_ids: torch.Tensor,
    chunk_size: int = 256,
) -> float:
    test_norm = noisy_test / noisy_test.norm(dim=-1, keepdim=True).clamp_min(1e-8)
    all_norm = clean_all / clean_all.norm(dim=-1, keepdim=True).clamp_min(1e-8)
    correct = 0
    for start in range(0, len(test_norm), chunk_size):
        scores = test_norm[start : start + chunk_size] @ all_norm.T
        predicted = scores.argmax(dim=-1)
        correct += int((predicted == test_ids[start : start + chunk_size]).sum().item())
    return correct / max(1, len(test_ids))


def run_reconstruction_experiment(
    data: DataBundle, codec: TokenByteCodec, config: ExperimentConfig, seed: int = 7
) -> dict:
    train_ids_np, test_ids_np = stratified_vocabulary_split(data, seed)
    train_ids = torch.from_numpy(train_ids_np).long()
    test_ids = torch.from_numpy(test_ids_np).long()
    rng = np.random.default_rng(seed)
    records: list[dict] = []

    for offset, head_name in enumerate(("parallel_byte", "autoregressive_byte")):
        torch.manual_seed(seed + offset * 100)
        model = ReconstructionModel(data, codec, config, head_name)
        optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3, weight_decay=0.01)
        curve: list[dict] = []
        model.train()
        log_every = max(1, config.reconstruction_steps // 10)
        for step in range(config.reconstruction_steps):
            sampled = rng.choice(
                train_ids_np,
                size=min(config.reconstruction_batch_size, len(train_ids_np)),
                replace=False,
            )
            batch = torch.from_numpy(sampled).long()
            optimizer.zero_grad(set_to_none=True)
            output = model.loss(batch)
            output.loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            if step == 0 or (step + 1) % log_every == 0 or step + 1 == config.reconstruction_steps:
                curve.append({"step": step + 1, "loss": float(output.loss.detach().item())})

        model.eval()
        with torch.no_grad():
            clean_test = model.encoder(test_ids)
            all_ids = torch.arange(len(data.vocab))
            clean_all_parts = []
            for start in range(0, len(all_ids), 512):
                clean_all_parts.append(model.encoder(all_ids[start : start + 512]))
            clean_all = torch.cat(clean_all_parts)

        generator = torch.Generator().manual_seed(seed + 909)
        noise_results: dict[str, dict] = {}
        for sigma in config.noise_levels:
            noisy = relative_noise(clean_test, sigma, generator)
            metrics = _decode_metrics(model, test_ids, noisy, codec)
            metrics["codebook_cosine_accuracy"] = _codebook_accuracy(
                noisy, clean_all, test_ids
            )
            noise_results[str(sigma)] = metrics

        records.append(
            {
                "architecture": head_name,
                "train_vocabulary_items": len(train_ids),
                "held_out_vocabulary_items": len(test_ids),
                "encoder_parameters": parameter_count(model.encoder),
                "head_parameters": parameter_count(model.head),
                "curve": curve,
                "noise_results": noise_results,
            }
        )

    short_test = int((data.byte_lengths[test_ids_np] <= 32).sum())
    return {
        "seed": seed,
        "train_vocabulary_items": len(train_ids),
        "held_out_vocabulary_items": len(test_ids),
        "held_out_short_items": short_test,
        "direct_k32_prefix_reconstruction_accuracy": short_test / max(1, len(test_ids)),
        "note": (
            "Direct K32 inversion is exact only for held-out forms of at most 32 bytes. "
            "Cosine codebook recovery stores and searches all vocabulary vectors; it is an "
            "accuracy upper baseline, not a head-free solution."
        ),
        "models": records,
    }

