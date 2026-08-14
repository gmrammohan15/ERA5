from __future__ import annotations

from hashlib import sha256
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import torch


REPO_ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = REPO_ROOT / "session7" / "artifacts"


def clean_json(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): clean_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean_json(item) for item in value]
    if isinstance(value, np.ndarray):
        return clean_json(value.tolist())
    if isinstance(value, torch.Tensor):
        return clean_json(value.detach().cpu().tolist())
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating, float)):
        result = float(value)
        return round(result, 8) if math.isfinite(result) else None
    if isinstance(value, Path):
        return str(value)
    return value


def write_json(filename: str, payload: dict) -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    path = ARTIFACT_DIR / filename
    path.write_text(
        json.dumps(clean_json(payload), indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


def read_json(filename: str) -> dict:
    return json.loads((ARTIFACT_DIR / filename).read_text(encoding="utf-8"))


def state_fingerprint(state: dict[str, torch.Tensor]) -> str:
    digest = sha256()
    for key in sorted(state):
        digest.update(key.encode("utf-8"))
        tensor = state[key].detach().cpu().contiguous()
        digest.update(tensor.numpy().tobytes())
    return digest.hexdigest()[:16]

