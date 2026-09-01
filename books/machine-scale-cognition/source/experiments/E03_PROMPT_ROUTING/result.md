# E03 Result

**Claim level:** `REPRODUCIBLE_INTERNAL` for this batch only
**Result:** null prompt effect; task batch saturated

`python experiments/E03_PROMPT_ROUTING/score.py` returns 8/8 and valid JSON for all three conditions. Final outputs are byte-identical. Raw events show that every condition used or attempted external computation despite prompt wording. Reported usage was:

| Condition | Output tokens | Reasoning tokens |
|---|---:|---:|
| Direct | 465 | 333 |
| Decompose | 592 | 354 |
| CoT | 386 | 202 |

This does not establish equivalence of prompting methods. Eight authored items, one model, one run per condition, and tool-capable agent behavior make the batch underpowered and confounded. It rejects only the claim that these prompt instructions improved accuracy on this batch. It supports routing computation to an external checker and evaluating the whole inference system rather than interpreting prompt labels as mechanisms.
