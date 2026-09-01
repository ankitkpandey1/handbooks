# E03 Preregistration — Direct vs Decomposition vs CoT

**Frozen before execution:** 2026-08-31
**Budget position:** experiment 3 of 10
**Model:** `gpt-5.6-luna`; three fresh ephemeral calls; identical tasks
**Purpose:** test H4 on exact-answer tasks, not choose a universally best prompt

Conditions: C0 answer directly; C1 decompose into typed subproblems and compute; C2 reason step by step before answering. All return the same JSON answer schema. Primary score is exact match across eight items. Secondary measures are output tokens and invalid format. One batch is too small for a general model claim.

Prediction: decomposition or CoT may help multi-step items but will not strictly dominate direct output; all variants should be externally scored rather than self-judged.

**Pre-run key correction:** deterministic checking found q6 was mistyped as 13 instead of 20 and q7 as 18 instead of 16. Corrected before any model call; q8 was independently enumerated. This does not consume a run.
