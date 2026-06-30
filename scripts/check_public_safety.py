from __future__ import annotations

import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from baby_fugu.public_safety import scan_public_safety


def main() -> int:
    parser = argparse.ArgumentParser(description="Check public repository safety.")
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument("--max-file-bytes", type=int, default=1_000_000)
    args = parser.parse_args()

    issues = scan_public_safety(args.root, max_file_bytes=args.max_file_bytes)
    for issue in issues:
        print(f"{issue.kind}: {issue.path}: {issue.detail}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
