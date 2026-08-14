"""Core components for the Problem 5 proof."""

from .config import ExperimentConfig
from .data import DataBundle, load_data_bundle
from .decoders import AutoregressiveByteHead, ParallelByteHead, TokenByteCodec, VocabularyHead
from .encoders import K32Encoder
from .transformer import ReverseKroneckerLM, SharedBackbone

__all__ = [
    "AutoregressiveByteHead",
    "DataBundle",
    "ExperimentConfig",
    "K32Encoder",
    "ParallelByteHead",
    "ReverseKroneckerLM",
    "SharedBackbone",
    "TokenByteCodec",
    "VocabularyHead",
    "load_data_bundle",
]

