from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
import json
from pathlib import Path

import torch

from session7.src.artifacts import ARTIFACT_DIR, state_fingerprint, write_json
from session7.src.config import ExperimentConfig
from session7.src.data import byte_length_bucket, load_data_bundle
from session7.src.decoders import TokenByteCodec
from session7.src.evaluation import evaluate_language_model
from session7.src.reconstruction import run_reconstruction_experiment
from session7.src.training import train_language_model
from session7.src.transformer import initial_backbone_state


HEADS = ("vocabulary", "parallel_byte", "autoregressive_byte")


def analyze(profile: str) -> dict:
    config = ExperimentConfig.smoke() if profile == "smoke" else ExperimentConfig()
    data = load_data_bundle()
    codec = TokenByteCodec(data.vocab, config.output_max_bytes)
    buckets = Counter(byte_length_bucket(int(value)) for value in data.byte_lengths.tolist())
    payload = {
        "profile": profile,
        "config": config.as_dict(),
        "config_fingerprint": config.fingerprint(),
        "vocabulary_items": len(data.vocab),
        "codec_roundtrip": codec.roundtrip_ok(),
        "vocabulary_max_bytes": int(data.byte_lengths.max()),
        "vocabulary_over_32": int((data.byte_lengths > 32).sum()),
        "vocabulary_length_buckets": dict(sorted(buckets.items())),
        "observed_token_lengths": data.observed_length_stats,
    }
    write_json("data_analysis.json", payload)
    return payload


def reconstruct(profile: str) -> dict:
    config = ExperimentConfig.smoke() if profile == "smoke" else ExperimentConfig()
    data = load_data_bundle()
    codec = TokenByteCodec(data.vocab, config.output_max_bytes)
    payload = {
        "profile": profile,
        "config": config.as_dict(),
        "config_fingerprint": config.fingerprint(),
        "result": run_reconstruction_experiment(data, codec, config, seed=config.seeds[0]),
    }
    write_json("reconstruction_results.json", payload)
    return payload


def language_models(profile: str, save_checkpoints: bool = True) -> dict:
    config = ExperimentConfig.smoke() if profile == "smoke" else ExperimentConfig()
    data = load_data_bundle()
    codec = TokenByteCodec(data.vocab, config.output_max_bytes)
    pilot_records: list[dict] = []
    selected_lr: dict[str, float] = {}

    pilot_eval_config = replace(
        config,
        eval_tokens_per_language=min(4_096, config.eval_tokens_per_language),
        beam_eval_examples=0,
    )
    for head_name in HEADS:
        if len(config.learning_rates) == 1:
            selected_lr[head_name] = config.learning_rates[0]
            continue
        candidates: list[tuple[float, float]] = []
        for learning_rate in config.learning_rates:
            state = initial_backbone_state(data.vocab, config, config.seeds[0])
            trained = train_language_model(
                data,
                codec,
                config,
                head_name,
                config.seeds[0],
                learning_rate,
                state,
                steps=config.pilot_steps,
            )
            metrics = evaluate_language_model(
                trained.model, data, codec, pilot_eval_config, "validation"
            )
            mean_nll = float(metrics["overall"]["mean_token_nll"])
            candidates.append((mean_nll, learning_rate))
            pilot_records.append(
                {**trained.record, "validation": metrics, "pilot": True}
            )
        selected_lr[head_name] = min(candidates)[1]

    runs: list[dict] = []
    checkpoint_dir = ARTIFACT_DIR / "checkpoints"
    if save_checkpoints:
        checkpoint_dir.mkdir(parents=True, exist_ok=True)

    for seed in config.seeds:
        shared_state = initial_backbone_state(data.vocab, config, seed)
        shared_hash = state_fingerprint(shared_state)
        for head_name in HEADS:
            trained = train_language_model(
                data,
                codec,
                config,
                head_name,
                seed,
                selected_lr[head_name],
                shared_state,
            )
            validation = evaluate_language_model(
                trained.model, data, codec, config, "validation"
            )
            test = evaluate_language_model(trained.model, data, codec, config, "test")
            record = {
                **trained.record,
                "shared_initialization_hash": shared_hash,
                "validation": validation,
                "test": test,
            }
            runs.append(record)
            if save_checkpoints and seed == config.seeds[0]:
                torch.save(
                    {
                        "architecture": head_name,
                        "seed": seed,
                        "config": config.as_dict(),
                        "model_state": trained.model.state_dict(),
                    },
                    checkpoint_dir / f"{head_name}_seed_{seed}.pt",
                )

    payload = {
        "profile": profile,
        "config": config.as_dict(),
        "config_fingerprint": config.fingerprint(),
        "selected_learning_rates": selected_lr,
        "pilots": pilot_records,
        "runs": runs,
    }
    write_json("language_model_results.json", payload)
    return payload


def build_report() -> None:
    from session7.build_report import build

    build()


def main() -> None:
    parser = argparse.ArgumentParser(description="Problem 5 reverse-Kronecker proof")
    parser.add_argument(
        "command", choices=("analyze", "reconstruct", "lm", "report", "all")
    )
    parser.add_argument("--profile", choices=("smoke", "full"), default="full")
    parser.add_argument("--no-checkpoints", action="store_true")
    args = parser.parse_args()

    if args.command in ("analyze", "all"):
        print(json.dumps(analyze(args.profile), indent=2, ensure_ascii=False))
    if args.command in ("reconstruct", "all"):
        result = reconstruct(args.profile)
        print(f"reconstruction: {len(result['result']['models'])} models")
    if args.command in ("lm", "all"):
        result = language_models(args.profile, save_checkpoints=not args.no_checkpoints)
        print(f"language-model runs: {len(result['runs'])}")
    if args.command in ("report", "all"):
        build_report()


if __name__ == "__main__":
    main()

