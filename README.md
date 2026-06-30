# Baby Fugu

Baby Fugu is a small, public-safe router experiment:

- frozen small-model hidden states
- one linear head
- four route-signal classes
- deterministic, local train/evaluate tooling

This repository is intentionally not the full experiment lab. Raw OAuth replay logs,
provider responses, large hidden-state dumps, credentials, and model weights stay out
of this repo.

## Route Classes

```text
mini_ok
strong_profile_required
inconclusive
neither_profile_sufficient
```

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe -m pytest
```

Train on the tiny public fixture:

```powershell
.\.venv\Scripts\python.exe scripts\train_one_head.py `
  fixtures\ko_route_signal_tiny.eval-ready.jsonl `
  outputs\tiny-one-head.json
```

Evaluate:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate_one_head.py `
  outputs\tiny-one-head.json `
  fixtures\ko_route_signal_tiny.eval-ready.jsonl
```

## Public Safety Boundary

Allowed here:

- minimal source code
- unit tests
- synthetic tiny fixtures
- architecture notes
- summarized experiment reports

Not allowed here:

- OAuth replay raw logs
- provider response transcripts
- large datasets or hidden-state dumps
- credentials, tokens, SSH keys
- model weights
- adult/Grok slice source text

## Current Status

Baby Fugu has shown signal on a narrow Korean long-context route-signal slice, but it
is not production-ready. In the pilot30 summary, the one-head router beat the
deterministic baseline while still failing to learn `neither_profile_sufficient`.

See [docs/experiments/pilot30-summary.md](docs/experiments/pilot30-summary.md).
