from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from baby_fugu.one_head import train_one_head


def main() -> int:
    parser = argparse.ArgumentParser(description="Train a Baby Fugu one-head router.")
    parser.add_argument("dataset", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--epochs", type=int, default=250)
    parser.add_argument("--learning-rate", type=float, default=0.2)
    parser.add_argument("--l2", type=float, default=0.001)
    args = parser.parse_args()

    model = train_one_head(
        args.dataset,
        epochs=args.epochs,
        learning_rate=args.learning_rate,
        l2=args.l2,
    )
    model.save(args.output)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
