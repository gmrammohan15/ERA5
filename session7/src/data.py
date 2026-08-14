from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterator

import numpy as np
import torch

from session2.bpe import BPETokenizer


REPO_ROOT = Path(__file__).resolve().parents[2]
TOKENIZER_PATH = REPO_ROOT / "session2" / "artifacts" / "tokenizer.json"
CORPUS_DIR = REPO_ROOT / "session2" / "data"
LANGUAGES = ("en", "hi", "te", "kn")


@dataclass
class DataBundle:
    vocab: list[str]
    tokenizer: BPETokenizer
    token_ids: dict[str, dict[str, np.ndarray]]
    byte_lengths: np.ndarray
    observed_length_stats: dict[str, dict[str, float | int]]


def _load_tokenizer(path: Path = TOKENIZER_PATH) -> tuple[list[str], BPETokenizer]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    vocab = list(payload["vocab"])
    merges = [tuple(pair) for pair in payload["merges"]]
    return vocab, BPETokenizer(vocab, merges)


def _split_text(text: str) -> dict[str, str]:
    n = len(text)
    first = int(n * 0.80)
    second = int(n * 0.90)
    return {
        "train": text[:first],
        "validation": text[first:second],
        "test": text[second:],
    }


def load_data_bundle() -> DataBundle:
    vocab, tokenizer = _load_tokenizer()
    token_ids: dict[str, dict[str, np.ndarray]] = {
        split: {} for split in ("train", "validation", "test")
    }
    observed: dict[str, dict[str, float | int]] = {}

    for language in LANGUAGES:
        text = (CORPUS_DIR / f"{language}.md").read_text(encoding="utf-8")
        parts = _split_text(text)
        all_ids: list[int] = []
        for split, content in parts.items():
            ids = np.asarray(tokenizer.encode(content), dtype=np.int64)
            token_ids[split][language] = ids
            all_ids.extend(ids.tolist())
        lengths = [len(vocab[idx].encode("utf-8")) for idx in all_ids]
        over = sum(length > 32 for length in lengths)
        observed[language] = {
            "tokens": len(lengths),
            "over_32_tokens": over,
            "over_32_fraction": over / max(1, len(lengths)),
            "maximum_bytes": max(lengths, default=0),
        }

    byte_lengths = np.asarray([len(token.encode("utf-8")) for token in vocab], dtype=np.int64)
    return DataBundle(vocab, tokenizer, token_ids, byte_lengths, observed)


class BalancedBatcher:
    """Deterministic equal-language random-window sampler."""

    def __init__(
        self,
        language_ids: dict[str, np.ndarray],
        batch_size: int,
        context_length: int,
        seed: int,
    ) -> None:
        self.language_ids = language_ids
        self.languages = tuple(sorted(language_ids))
        self.batch_size = batch_size
        self.context_length = context_length
        self.rng = np.random.default_rng(seed)

    def next(self) -> tuple[torch.Tensor, torch.Tensor, list[str]]:
        rows: list[np.ndarray] = []
        languages: list[str] = []
        for row in range(self.batch_size):
            language = self.languages[row % len(self.languages)]
            ids = self.language_ids[language]
            if len(ids) <= self.context_length:
                raise ValueError(f"{language} split is too short for context {self.context_length}")
            start = int(self.rng.integers(0, len(ids) - self.context_length - 1))
            rows.append(ids[start : start + self.context_length + 1])
            languages.append(language)
        batch = torch.from_numpy(np.stack(rows)).long()
        return batch[:, :-1], batch[:, 1:], languages


def fixed_eval_batches(
    language_ids: dict[str, np.ndarray],
    context_length: int,
    token_budget_per_language: int,
    batch_size: int,
) -> Iterator[tuple[str, torch.Tensor, torch.Tensor]]:
    for language in sorted(language_ids):
        ids = language_ids[language]
        usable = min(len(ids) - 1, token_budget_per_language)
        starts = list(range(0, max(0, usable - context_length), context_length))
        rows: list[np.ndarray] = []
        for start in starts:
            row = ids[start : start + context_length + 1]
            if len(row) == context_length + 1:
                rows.append(row)
            if len(rows) == batch_size:
                batch = torch.from_numpy(np.stack(rows)).long()
                yield language, batch[:, :-1], batch[:, 1:]
                rows = []
        if rows:
            batch = torch.from_numpy(np.stack(rows)).long()
            yield language, batch[:, :-1], batch[:, 1:]


def byte_length_bucket(length: int) -> str:
    if length <= 8:
        return "<=8"
    if length <= 16:
        return "9-16"
    if length <= 32:
        return "17-32"
    if length <= 64:
        return "33-64"
    return "65-128"

