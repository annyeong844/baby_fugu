from __future__ import annotations

import hashlib
from typing import Any


LABEL_FIELDS = {
    "label",
    "semantic_label",
    "semanticLabel",
    "semantic_confidence",
    "semanticConfidence",
    "route_reward_vector",
    "why",
}


def render_route_envelope(row: dict[str, Any]) -> str:
    """Render a label-free route decision envelope."""

    request = _string(row, "text", default="")
    prior_available = _bool(row.get("prior_context_available"))
    prior_summary = _string(row, "prior_context_summary", default="")
    artifact_state = _string(row, "artifact_state", default="unspecified")
    intent_clarity = _string(row, "intent_clarity", default="unspecified")
    current_info = _string(row, "current_request_information", default="")
    missing_inputs = _string_list(row.get("missing_inputs"))

    prior_line = "available" if prior_available else "not_available"
    if prior_summary:
        prior_line = f"{prior_line}; summary={prior_summary}"

    current_line = current_info or ("user_request_text_only" if request else "empty_request")
    missing_line = ", ".join(missing_inputs) if missing_inputs else "none"

    return "\n".join(
        [
            "[라우팅 입력]",
            f"사용자 요청: {request}",
            f"현재 요청에 포함된 정보: {current_line}",
            f"이전 세션/프로젝트 맥락: {prior_line}",
            f"첨부/파일/외부자료 상태: {artifact_state}",
            f"의도 명확성: {intent_clarity}",
            f"부족한 핵심 입력: {missing_line}",
        ]
    )


def route_envelope_request_digest(row: dict[str, Any]) -> str:
    source_digest = _string(row, "request_digest", default="")
    envelope = render_route_envelope(_without_label_fields(row))
    payload = f"route-envelope-v1|{source_digest}|{envelope}"
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _without_label_fields(row: dict[str, Any]) -> dict[str, Any]:
    cleaned = dict(row)
    for field in LABEL_FIELDS:
        cleaned.pop(field, None)
    return cleaned


def _string(row: dict[str, Any], field: str, *, default: str) -> str:
    value = row.get(field, default)
    if value is None:
        return default
    return str(value)


def _bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in {"1", "true", "yes", "available"}
    return bool(value)


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    return [str(value)]
