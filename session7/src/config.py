from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json


@dataclass(frozen=True)
class ExperimentConfig:
    """Decision-complete defaults for the CPU-rigorous proof."""

    vocab_size: int = 10_000
    input_max_bytes: int = 32
    output_max_bytes: int = 128
    d_model: int = 128
    n_layers: int = 2
    n_heads: int = 4
    ffn_dim: int = 512
    context_length: int = 128
    batch_size: int = 16
    train_tokens: int = 1_000_000
    pilot_tokens: int = 250_000
    eval_tokens_per_language: int = 24_576
    byte_embedding_dim: int = 64
    decoder_hidden_dim: int = 128
    parallel_hidden_dim: int = 128
    weight_decay: float = 0.01
    warmup_fraction: float = 0.05
    grad_clip: float = 1.0
    learning_rates: tuple[float, float] = (3e-4, 1e-3)
    seeds: tuple[int, int, int] = (7, 17, 29)
    beam_width: int = 5
    beam_eval_examples: int = 256
    reconstruction_steps: int = 500
    reconstruction_batch_size: int = 128
    noise_levels: tuple[float, float, float, float] = (0.0, 0.01, 0.05, 0.10)

    @property
    def steps(self) -> int:
        return max(1, self.train_tokens // (self.batch_size * self.context_length))

    @property
    def pilot_steps(self) -> int:
        return max(1, self.pilot_tokens // (self.batch_size * self.context_length))

    def as_dict(self) -> dict:
        value = asdict(self)
        value["learning_rates"] = list(self.learning_rates)
        value["seeds"] = list(self.seeds)
        value["noise_levels"] = list(self.noise_levels)
        value["steps"] = self.steps
        value["pilot_steps"] = self.pilot_steps
        return value

    def fingerprint(self) -> str:
        payload = json.dumps(self.as_dict(), sort_keys=True, separators=(",", ":"))
        return sha256(payload.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def smoke(cls) -> "ExperimentConfig":
        return cls(
            d_model=64,
            n_layers=1,
            n_heads=4,
            ffn_dim=128,
            context_length=32,
            batch_size=4,
            train_tokens=8_192,
            pilot_tokens=2_048,
            eval_tokens_per_language=1_024,
            byte_embedding_dim=32,
            decoder_hidden_dim=64,
            parallel_hidden_dim=64,
            learning_rates=(1e-3,),
            seeds=(7,),
            beam_eval_examples=32,
            reconstruction_steps=20,
            reconstruction_batch_size=32,
            noise_levels=(0.0, 0.05),
        )

