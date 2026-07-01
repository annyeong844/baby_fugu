# Architecture

Baby Fugu is the public-safe core of a small route-signal experiment.

```text
route envelope text
  -> frozen small-model hidden state
  -> one linear softmax head
  -> route-signal class
```

The public repository owns only the deterministic envelope, tiny datasets, the
one-head model format, and local train/evaluate scripts.

## Core Contract

The routing input is a label-free envelope:

```text
사용자 요청
현재 요청에 포함된 정보
이전 세션/프로젝트 맥락
첨부/파일/외부자료 상태
의도 명확성
부족한 핵심 입력
```

Label fields such as `semantic_label`, `semantic_confidence`, `why`, and reward
vectors must not affect the rendered envelope. This prevents answer leakage into
the hidden-state vector.

## Model Shape

Baby Fugu uses one four-class softmax head:

```text
mini_ok
strong_profile_required
inconclusive
neither_profile_sufficient
```

The base model remains frozen. Training updates only the small head.

## Non-Goals

- No provider replay.
- No paid batch submission.
- No credentials.
- No large hidden-state dumps.
- No raw provider transcripts.
- No production routing authority.

## Why One Head

The current research direction follows the small TRINITY-style shape: keep the
base model frozen and train a tiny selection head. This repository uses one
four-class head instead of a pile of special-case heads.

That constraint is intentional. The project should first prove that one small
head can separate the route signals before adding more moving parts.

## Public Safety

The renderer excludes label fields such as `semantic_label`, `why`, and reward
vectors from the route envelope. Tests cover that contract.

The public safety scanner rejects:

- secret-looking strings
- `.env` and key files
- large files
- raw replay/evidence/hidden-state filenames
- model weight filenames
