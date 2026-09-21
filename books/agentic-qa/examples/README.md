# Example repository for *Agentic QA*

The listings and outputs in the book were produced here. Python 3.14.3 was used;
the pinned dependencies are in `requirements.txt`.

```bash
python3 -m venv venv && . venv/bin/activate
pip install -r requirements.txt
python -m pytest -q tests_agent      # the agent-style suite: 11 tests, all green
python -m pytest -q tests_real       # the recommended suite: 12 tests, all green
bash scripts/prove_it_fails.sh tests_real/test_pricing.py orders/pricing.py
bash scripts/mock_density.sh tests_agent/*.py
mutmut run                           # test selection is set in setup.cfg
```

To reproduce the bug table in Chapter 1, plant each bug by hand in `orders/`
(the exact lines are shown in Chapter 3) and run both suites.

`tests_agent/` is a composite written to match what coding agents typically
produce. It was written by hand for the comparison, not captured from an agent
session. Code here is licensed under Apache-2.0.
