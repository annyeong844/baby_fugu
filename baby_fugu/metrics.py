from __future__ import annotations


def accuracy(correct: int, total: int) -> float:
    if total < 0 or correct < 0:
        raise ValueError("counts must be non-negative")
    if correct > total:
        raise ValueError("correct cannot exceed total")
    return correct / total if total else 0.0
