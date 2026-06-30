from baby_fugu.route_envelope import render_route_envelope, route_envelope_request_digest


def test_route_envelope_excludes_label_fields() -> None:
    row = {
        "request_digest": "sha256:abc",
        "text": "그 조건만 정리해줘.",
        "prior_context_available": True,
        "prior_context_summary": "환불 예외 정책",
        "semantic_label": "strong_profile_required",
        "why": "secret label rationale",
    }

    rendered = render_route_envelope(row)

    assert "그 조건만 정리해줘." in rendered
    assert "환불 예외 정책" in rendered
    assert "strong_profile_required" not in rendered
    assert "secret label rationale" not in rendered


def test_route_envelope_digest_changes_with_source_digest() -> None:
    row = {"request_digest": "sha256:a", "text": "안내문 써줘."}
    other = {"request_digest": "sha256:b", "text": "안내문 써줘."}

    assert route_envelope_request_digest(row) != route_envelope_request_digest(other)
