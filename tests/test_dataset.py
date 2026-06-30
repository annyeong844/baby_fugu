import pytest

from baby_fugu.dataset import l2_normalize_vector, validate_eval_row


def test_l2_normalize_vector() -> None:
    assert l2_normalize_vector([3.0, 4.0]) == [0.6, 0.8]


def test_validate_eval_row_rejects_unknown_label() -> None:
    with pytest.raises(ValueError, match="unsupported label"):
        validate_eval_row({"request_digest": "x", "label": "bad", "vector": [1.0]})
