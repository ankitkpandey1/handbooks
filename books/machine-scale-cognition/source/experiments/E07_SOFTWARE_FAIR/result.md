# E07 Result

**Claim level:** `REPRODUCIBLE_INTERNAL` for fixture behavior and static structure
**Outcome boundary:** no maintenance outcome observed

After both calls ended, the identical hidden test was copied into each result repo. `python experiments/E07_SOFTWARE_FAIR/score.py` produced:

| Condition | Tests | Independent normalization operations |
|---|---:|---:|
| B1 | 23 passed | 11 |
| S | 23 passed | 3 |

B1 inspected all sibling files but changed only `quote.py`. It fixed the reported instance and passed every frozen hidden behavior, because the fixture's other flows already handled the tested common inputs.

S centralized common normalization in `Tier.normalize`/`Tier.from_raw` and changed all five flows while preserving alias handling. It also ran an explicit sibling check.

The only measured advantage is structural: fewer distributed normalization operations. The experiment does not show fewer future bugs, lower maintenance time, or superior product outcomes. It also shows that a hidden behavior suite can fail to discriminate local repair from systemic prevention when existing siblings already pass; prevention requires a structural or mutation-based selector, not only current examples.
