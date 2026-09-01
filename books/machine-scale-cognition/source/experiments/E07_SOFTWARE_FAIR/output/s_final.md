Fixed the recurring tier-normalization issue by centralizing trimming and case-folding in `Tier.normalize()` / `Tier.from_raw()`, then applying it across all sibling flows.

Verification:

- `pytest -q`: 2 passed
- Cross-flow whitespace checks passed for export, quote, refund, renewal, and support
- `git diff --check` passed