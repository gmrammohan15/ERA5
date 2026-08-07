from __future__ import annotations

import argparse
from pathlib import Path

from v5.common import ROOT
from v5.demo import run_demo
from v5.training import training_worker


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the complete V5 training-data execution demonstration.")
    parser.add_argument("--output", type=Path, default=ROOT / "submission_artifacts")
    parser.add_argument("--worker", choices=("crash", "resume"), help=argparse.SUPPRESS)
    parser.add_argument("--artifact-root", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        if args.artifact_root is None:
            parser.error("--artifact-root is required for worker mode")
        return training_worker(args.artifact_root.resolve(), args.worker)
    return run_demo(args.output)


if __name__ == "__main__":
    raise SystemExit(main())
