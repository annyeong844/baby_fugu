from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterable


ROUTE_LABELS = (
    "mini_ok",
    "strong_profile_required",
    "inconclusive",
    "neither_profile_sufficient",
)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    count = 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
            count += 1
    return count


def l2_normalize_vector(vector: list[float]) -> list[float]:
    norm = sum(value * value for value in vector) ** 0.5
    if norm == 0.0:
        return [0.0 for _ in vector]
    return [float(value) / norm for value in vector]


def validate_eval_row(row: dict[str, Any]) -> None:
    if "request_digest" not in row:
        raise ValueError("row missing request_digest")
    if row.get("label") not in ROUTE_LABELS:
        raise ValueError(f"unsupported label: {row.get('label')}")
    vector = row.get("vector")
    if not isinstance(vector, list) or not vector:
        raise ValueError("row vector must be a non-empty list")
    if not all(isinstance(value, int | float) for value in vector):
        raise ValueError("row vector must contain only numbers")
