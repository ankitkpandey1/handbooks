# E06 Preregistration — Fair-Access Systemic Software Case

**Result:** `FAILED_HARNESS`. Relative prompt paths were resolved from the wrong working directory; both calls received empty instructions and returned “How can I help?”. No treatment occurred. Counts as experiment 6/10. The frozen fixture remains eligible for one corrected run under E07.

**Frozen before model calls:** 2026-08-31
**Budget position:** experiment 6 of 10
**Fixture:** `fixture_base/`, preserved unchanged
**Model:** Luna; fresh copies; same repository and tool access; one agent turn each

## Ordinary issue

“Quote creation rejects tier values with surrounding whitespace, such as ` Pro `. Fix it.”

## Conditions

- B1 receives only the issue, may inspect/edit the full copied repo, and may run public tests.
- S receives the same issue plus the constraint-crossing field instruction to inspect siblings, infer the class/mechanism, centralize prevention when justified, run tests, and stop when marginal value turns negative.

Neither condition receives `hidden_test_behavior.py` until after its turn. It is then copied unchanged into each result repo.

## Measures

- public reported-instance tests;
- hidden cross-flow behavior across case/whitespace/aliases;
- rejection of unknown values;
- number of independent normalization implementations remaining;
- scope and complexity of change;
- raw tool/actions and reported rationale.

No replacement fixture may be selected after results. A baseline systemic win is retained.
