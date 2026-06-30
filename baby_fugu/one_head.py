from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

import numpy as np

from baby_fugu.dataset import ROUTE_LABELS, read_jsonl, validate_eval_row


@dataclass(frozen=True)
class OneHeadModel:
    labels: tuple[str, ...]
    weights: list[list[float]]
    bias: list[float]
    vector_normalization: str = "l2"

    def predict_proba(self, vector: list[float]) -> dict[str, float]:
        logits = np.asarray(vector, dtype=np.float64) @ np.asarray(self.weights, dtype=np.float64).T
        logits = logits + np.asarray(self.bias, dtype=np.float64)
        probs = _softmax(logits)
        return {label: float(prob) for label, prob in zip(self.labels, probs, strict=True)}

    def predict(self, vector: list[float]) -> str:
        probabilities = self.predict_proba(vector)
        return max(probabilities, key=probabilities.get)

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "algorithm": "baby-fugu-one-head-softmax",
            "labels": list(self.labels),
            "weights": self.weights,
            "bias": self.bias,
            "vector_normalization": self.vector_normalization,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, object]) -> "OneHeadModel":
        labels = tuple(str(label) for label in payload["labels"])  # type: ignore[index]
        return cls(
            labels=labels,
            weights=[[float(value) for value in row] for row in payload["weights"]],  # type: ignore[index]
            bias=[float(value) for value in payload["bias"]],  # type: ignore[index]
            vector_normalization=str(payload.get("vector_normalization", "l2")),
        )

    @classmethod
    def load(cls, path: Path) -> "OneHeadModel":
        return cls.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")


def train_one_head(
    dataset_path: Path,
    *,
    epochs: int = 250,
    learning_rate: float = 0.2,
    l2: float = 0.001,
) -> OneHeadModel:
    rows = read_jsonl(dataset_path)
    for row in rows:
        validate_eval_row(row)
    if not rows:
        raise ValueError("dataset is empty")

    labels = tuple(ROUTE_LABELS)
    label_index = {label: index for index, label in enumerate(labels)}
    vectors = np.asarray([row["vector"] for row in rows], dtype=np.float64)
    targets = np.zeros((len(rows), len(labels)), dtype=np.float64)
    for row_index, row in enumerate(rows):
        targets[row_index, label_index[row["label"]]] = float(row.get("semantic_confidence", 1.0))
        remainder = 1.0 - targets[row_index].sum()
        if remainder > 0:
            targets[row_index] += remainder / len(labels)

    weights = np.zeros((len(labels), vectors.shape[1]), dtype=np.float64)
    bias = np.zeros(len(labels), dtype=np.float64)
    for _ in range(epochs):
        probabilities = _softmax_matrix(vectors @ weights.T + bias)
        error = probabilities - targets
        weights -= learning_rate * ((error.T @ vectors) / len(rows) + l2 * weights)
        bias -= learning_rate * error.mean(axis=0)

    return OneHeadModel(
        labels=labels,
        weights=weights.tolist(),
        bias=bias.tolist(),
    )


def evaluate_one_head(model: OneHeadModel, dataset_path: Path) -> dict[str, object]:
    rows = read_jsonl(dataset_path)
    correct = 0
    confusion: dict[str, int] = {}
    for row in rows:
        validate_eval_row(row)
        prediction = model.predict(row["vector"])
        gold = row["label"]
        if prediction == gold:
            correct += 1
        key = f"{gold} -> {prediction}"
        confusion[key] = confusion.get(key, 0) + 1
    total = len(rows)
    return {
        "record_count": total,
        "accuracy": correct / total if total else 0.0,
        "correct": correct,
        "confusion": confusion,
    }


def _softmax(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits)
    exp = np.exp(shifted)
    return exp / exp.sum()


def _softmax_matrix(logits: np.ndarray) -> np.ndarray:
    shifted = logits - np.max(logits, axis=1, keepdims=True)
    exp = np.exp(shifted)
    return exp / exp.sum(axis=1, keepdims=True)
