from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol, runtime_checkable


@dataclass(frozen=True)
class CurriculumStage:
    """Data-driven curriculum stage; stages are configuration, not subclasses."""

    name: str
    index: int
    weights: dict[str, float]

    @classmethod
    def from_mapping(cls, value: dict[str, Any]) -> "CurriculumStage":
        return cls(name=value["name"], index=value["index"], weights=dict(value["weights"]))


@runtime_checkable
class TokenizerProtocol(Protocol):
    pad_id: int
    bos_id: int
    eos_id: int
    vocab_size: int
    tokenizer_hash: str

    def encode(self, text: str) -> list[int]: ...

    def decode(self, tokens: Iterable[int]) -> str: ...


@runtime_checkable
class PackingPolicyProtocol(Protocol):
    def policy_for(self, lane: str) -> str: ...


@runtime_checkable
class SampleSelectorProtocol(Protocol):
    def select(self, artifact_root: Path, model: Any, rows: list[dict[str, Any]], lane_slots: dict[str, Any]) -> Any: ...


@runtime_checkable
class LedgerStoreProtocol(Protocol):
    def read(self) -> list[dict[str, Any]]: ...

    def append(self, record: dict[str, Any]) -> None: ...

    def verify(self) -> tuple[bool, str]: ...


@runtime_checkable
class CheckpointStoreProtocol(Protocol):
    def save(self, name: str, state: dict[str, Any]) -> Path: ...

    def load(self, checkpoint: Path) -> dict[str, Any]: ...
