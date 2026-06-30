# Architecture

Baby Fugu is the public-safe core of the route-signal experiment.

```text
route envelope text
  -> frozen small-model hidden state
  -> one linear softmax head
  -> route-signal class
```

The public repository owns only the deterministic envelope, tiny datasets, the
one-head model format, and local train/evaluate scripts.

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

## Public Safety

The renderer excludes label fields such as `semantic_label`, `why`, and reward
vectors from the route envelope. Tests cover that contract.
