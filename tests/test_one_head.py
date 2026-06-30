from pathlib import Path

from baby_fugu.one_head import OneHeadModel, evaluate_one_head, train_one_head


def test_train_one_head_fits_tiny_fixture(tmp_path: Path) -> None:
    model = train_one_head(Path("fixtures/ko_route_signal_tiny.eval-ready.jsonl"), epochs=300)

    result = evaluate_one_head(model, Path("fixtures/ko_route_signal_tiny.eval-ready.jsonl"))

    assert result["record_count"] == 4
    assert result["accuracy"] == 1.0


def test_one_head_round_trips(tmp_path: Path) -> None:
    model = train_one_head(Path("fixtures/ko_route_signal_tiny.eval-ready.jsonl"), epochs=300)
    output = tmp_path / "head.json"

    model.save(output)
    loaded = OneHeadModel.load(output)

    assert loaded.predict([1.0, 0.0, 0.0, 0.0]) == "mini_ok"
