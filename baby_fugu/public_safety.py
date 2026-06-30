from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


IGNORED_DIRS = {
    ".git",
    ".pytest_cache",
    ".ruff_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "__pycache__",
}

FORBIDDEN_PATH_PATTERNS = (
    re.compile(r"(^|/)\.env(\.|$)"),
    re.compile(r"(^|/)outputs(/|$)"),
    re.compile(r"(^|/)models(/|$)"),
    re.compile(r"(^|/)id_rsa($|[./])"),
    re.compile(r"(^|/)id_ed25519($|[./])"),
    re.compile(r"\.(pem|key|safetensors|bin|pt|pth|gguf)$"),
    re.compile(r"hidden_states", re.IGNORECASE),
    re.compile(r"route-runs", re.IGNORECASE),
    re.compile(r"counterfactual-evidence", re.IGNORECASE),
    re.compile(r"codex-replay", re.IGNORECASE),
)

SECRET_PATTERNS = (
    re.compile(r"OPENAI_API_KEY\s*="),
    re.compile(r"ANTHROPIC_API_KEY\s*="),
    re.compile(r"GROK_API_KEY\s*="),
    re.compile(r"XAI_API_KEY\s*="),
    re.compile(r"(?i)\b(api[_-]?key|access_token|refresh_token|client_secret)\b\s*[:=]"),
    re.compile(r"sk-[A-Za-z0-9_-]{10,}"),
    re.compile(r"ghp_[A-Za-z0-9_]{10,}"),
    re.compile(r"hf_[A-Za-z0-9_]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


@dataclass(frozen=True)
class PublicSafetyIssue:
    kind: str
    path: str
    detail: str


def scan_public_safety(root: Path, *, max_file_bytes: int = 1_000_000) -> list[PublicSafetyIssue]:
    root = root.resolve()
    issues: list[PublicSafetyIssue] = []
    for path in sorted(_iter_files(root)):
        rel = path.relative_to(root).as_posix()
        issues.extend(_path_issues(rel))

        size = path.stat().st_size
        if size > max_file_bytes:
            issues.append(
                PublicSafetyIssue("large_file", rel, f"{size} bytes exceeds {max_file_bytes}")
            )

        issues.extend(_content_issues(path, rel))
    return issues


def _iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in path.relative_to(root).parts):
            continue
        yield path


def _path_issues(rel: str) -> list[PublicSafetyIssue]:
    for pattern in FORBIDDEN_PATH_PATTERNS:
        if pattern.search(rel):
            return [PublicSafetyIssue("forbidden_path", rel, "forbidden public filename")]
    return []


def _content_issues(path: Path, rel: str) -> list[PublicSafetyIssue]:
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return []
    issues: list[PublicSafetyIssue] = []
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            issues.append(
                PublicSafetyIssue("secret_pattern", rel, f"matched {pattern.pattern}")
            )
    return issues
