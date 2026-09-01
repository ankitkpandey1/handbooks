# E01 Preregistration — Architecture Failure Search

**Result:** `ABORTED_PROCESS_FAILURE`. The run was stopped after thread creation and before any model output because the hypotheses had not first been derived from deep research. It counts as experiment 1 of 10. Raw transport events are retained under `output/`.

**Frozen before execution:** 2026-08-31
**Model:** `gpt-5.6-luna` through Codex CLI
**Conditions:** A0–A5 as defined in `docs/12_ARCHITECTURE_CANDIDATES.md`
**Tasks:** T1–T3 in `tasks.md`

## Purpose

Test whether the six candidate logics yield materially different, executable operating plans and expose disqualifying failures. This is an assessed model probe, not outcome validation.

## Measures

For each architecture/task pair score 0–4 on: executable next action, scalable workload, external selection, bounded human review, and stop/authority boundary. Also record architecture-specific failure and whether its plan is distinguishable from A0 after removing labels.

## Failure criteria

- Any architecture with a zero on external selection or bounded review is disqualified.
- If plans are operationally indistinguishable, the ontology has no demonstrated value.
- Model scores are suggestions only; final scoring must cite raw plan text.

## Researcher degrees of freedom

One combined call is used to avoid selective reruns. No prompt repair after output. A failed harness call counts; only a transport failure may be rerun and must remain logged.
