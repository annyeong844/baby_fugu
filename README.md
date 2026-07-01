# Baby Fugu

[![CI](https://github.com/annyeong844/baby_fugu/actions/workflows/ci.yml/badge.svg)](https://github.com/annyeong844/baby_fugu/actions/workflows/ci.yml)

Baby Fugu is a tiny, public-safe route-signal router.

It keeps the base model frozen, reads a hidden-state vector, and trains one
linear softmax head to choose one of four routing outcomes.

```text
route envelope
  -> frozen small-model hidden state
  -> one four-class head
  -> route signal
```

This repository is intentionally not the full experiment lab. Raw OAuth replay
logs, provider responses, large hidden-state dumps, credentials, and model
weights stay out of this repo.

## What It Does

Baby Fugu answers a narrow routing question:

> Is the current request enough for a cheap route, does it need stronger context,
> is it ambiguous, or is neither route sufficient?

The public version contains only:

- deterministic route-envelope rendering
- one-head train/evaluate code
- tiny synthetic fixtures
- public safety checks
- summarized experiment notes

## Route Signals

```text
mini_ok
strong_profile_required
inconclusive
neither_profile_sufficient
```

| Signal | Meaning |
| --- | --- |
| `mini_ok` | The current request has enough information for the cheap route. |
| `strong_profile_required` | The request depends on prior session or project context. |
| `inconclusive` | The available evidence does not cleanly identify the route. |
| `neither_profile_sufficient` | The task is missing artifacts, final decisions, or external state. |

## Quick Start

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .[dev]
.\.venv\Scripts\python.exe -m pytest
```

Run the public safety guard:

```powershell
.\.venv\Scripts\python.exe scripts\check_public_safety.py .
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

Expected tiny-fixture result:

```json
{"accuracy": 1.0, "correct": 4, "record_count": 4}
```

## Repository Map

```text
baby_fugu/
  route_envelope.py     label-free routing envelope renderer
  one_head.py           one linear softmax head
  dataset.py            JSONL and vector helpers
  public_safety.py      public repo safety scanner
scripts/
  train_one_head.py
  evaluate_one_head.py
  check_public_safety.py
fixtures/
  ko_route_signal_tiny.eval-ready.jsonl
docs/
  architecture.md
  experiments/pilot30-summary.md
```

## Public Safety Boundary

Allowed in this public repo:

- minimal source code
- unit tests
- synthetic tiny fixtures
- architecture notes
- summarized experiment reports

Not allowed in this public repo:

- OAuth replay raw logs
- provider response transcripts
- large datasets or hidden-state dumps
- credentials, tokens, SSH keys
- model weights
- adult/Grok slice source text

The CI runs `scripts/check_public_safety.py .` before tests. If a forbidden file
or secret-looking pattern lands in the repo, CI fails.

## Current Status

Baby Fugu has shown signal on a narrow Korean long-context route-signal slice, but it
is not production-ready. In the pilot30 summary, the one-head router beat the
deterministic baseline while still failing to learn `neither_profile_sufficient`.

See [docs/experiments/pilot30-summary.md](docs/experiments/pilot30-summary.md).
