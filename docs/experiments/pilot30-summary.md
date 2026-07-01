# Pilot30 Summary

Date: 2026-07-01

This is a summary only. Raw OAuth replay logs, provider responses, hidden-state
dumps, and full local experiment artifacts are intentionally excluded from this
public repository.

## Setup

- Slice: Korean long-context route signal
- Model shape: frozen Qwen hidden state + one four-class head
- Classes:
  - `mini_ok`
  - `strong_profile_required`
  - `inconclusive`
  - `neither_profile_sufficient`

## Observed Pilot30 Labels

```json
{
  "inconclusive": 1,
  "mini_ok": 10,
  "neither_profile_sufficient": 9,
  "strong_profile_required": 10
}
```

## Result

| Router | Correct | Accuracy |
| --- | ---: | ---: |
| deterministic / cheap baseline | 6 / 30 | 20.0% |
| `baby_fugu` v6 one-head | 17 / 30 | 56.7% |
| observed80 one-head | 18 / 30 | 60.0% |

## Interpretation

The one-head router showed real signal over deterministic routing on this narrow
slice. The binary boundary between `mini_ok` and `strong_profile_required` was
useful.

The failure mode is also clear: `neither_profile_sufficient` was not learned.
Rows where no route had enough information were usually over-routed as
`strong_profile_required`.

Observed80 per-label accuracy:

| Label | Correct |
| --- | ---: |
| `mini_ok` | 9 / 10 |
| `strong_profile_required` | 9 / 10 |
| `inconclusive` | 0 / 1 |
| `neither_profile_sufficient` | 0 / 9 |

The current head is learning the cheap-vs-strong boundary, not the abstention
boundary.

## Decision

Do not promote. Keep collecting targeted examples for:

- missing artifacts
- unresolved prior decisions
- external-state gaps
- true inconclusive cases
