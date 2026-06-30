from pathlib import Path

from baby_fugu.public_safety import PublicSafetyIssue, scan_public_safety


def test_scan_public_safety_accepts_tiny_safe_repo(tmp_path: Path) -> None:
    (tmp_path / "README.md").write_text("Baby Fugu\n", encoding="utf-8")
    (tmp_path / "fixtures").mkdir()
    (tmp_path / "fixtures" / "tiny.jsonl").write_text('{"ok": true}\n', encoding="utf-8")

    issues = scan_public_safety(tmp_path, max_file_bytes=1024)

    assert issues == []


def test_scan_public_safety_rejects_env_files(tmp_path: Path) -> None:
    fake_key = "OPENAI" + "_API_KEY=" + "sk-" + "not-real-but-forbidden"
    (tmp_path / ".env").write_text(fake_key + "\n", encoding="utf-8")

    issues = scan_public_safety(tmp_path, max_file_bytes=1024)

    assert PublicSafetyIssue("forbidden_path", ".env", "forbidden public filename") in issues


def test_scan_public_safety_rejects_secret_patterns(tmp_path: Path) -> None:
    fake_key = "OPENAI" + "_API_KEY=" + "sk-" + "testvalue1234567890"
    (tmp_path / "notes.md").write_text(fake_key + "\n", encoding="utf-8")

    issues = scan_public_safety(tmp_path, max_file_bytes=1024)

    assert any(issue.kind == "secret_pattern" and issue.path == "notes.md" for issue in issues)


def test_scan_public_safety_rejects_large_files(tmp_path: Path) -> None:
    (tmp_path / "large.jsonl").write_bytes(b"x" * 2048)

    issues = scan_public_safety(tmp_path, max_file_bytes=1024)

    assert PublicSafetyIssue("large_file", "large.jsonl", "2048 bytes exceeds 1024") in issues


def test_scan_public_safety_ignores_git_and_cache_dirs(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    ignored_key = "token = " + "sk-" + "ignored1234567890"
    (tmp_path / ".git" / "config").write_text(ignored_key + "\n", encoding="utf-8")
    (tmp_path / "__pycache__").mkdir()
    (tmp_path / "__pycache__" / "module.pyc").write_bytes(b"x" * 2048)

    issues = scan_public_safety(tmp_path, max_file_bytes=1024)

    assert issues == []
