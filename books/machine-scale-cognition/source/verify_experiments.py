#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
"""Check the retained experiment facts cited by the handbook.

This checks source artifacts, not PDF/source identity or real-world outcomes. It is an
additional Tier-B content check, not a Tier-A release verifier.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent
EXP = ROOT / "experiments"
errors: list[str] = []
passed: list[str] = []


def check(ok: bool, message: str) -> None:
    (passed if ok else errors).append(message)


dirs = sorted(p.name for p in EXP.iterdir() if p.is_dir())
check(len(dirs) == 10, f"ten experiment directories (found {len(dirs)})")
check([d[:3] for d in dirs] == [f"E{i:02d}" for i in range(1, 11)], "IDs are E01–E10")

# E03: exact-answer prompt batch.
p = subprocess.run([sys.executable, str(EXP / "E03_PROMPT_ROUTING/score.py")], text=True, capture_output=True)
check(p.returncode == 0, "E03 scorer exits zero")
if p.returncode == 0:
    rows = json.loads(p.stdout)
    check(len(rows) == 3 and all(r["exact"] == 8 and r["valid_schema"] for r in rows), "E03 records the 8/8 ceiling effect in all conditions")

# E04: frozen literature corpus and cited-paper membership.
e04 = EXP / "E04_RESEARCH_SEARCH"
corpus = json.loads((e04 / "output/corpus.json").read_text())
records = corpus.get("records", corpus) if isinstance(corpus, dict) else corpus
dois = {str(r.get("doi", "")).lower() for r in records}
check(len(dois) == 164, f"E04 has 164 unique DOI records (found {len(dois)})")
check(sum(bool(r.get("abstract")) for r in records) == 130, "E04 has 130 abstracts")
p = subprocess.run([sys.executable, str(e04 / "score.py")], text=True, capture_output=True)
check(p.returncode == 0, "E04 scorer exits zero")

# E05: retained simulation dimensions and adverse boundary cases.
sim = json.loads((EXP / "E05_EVOLUTIONARY_SIM/output/simulation.json").read_text())
check(sim.get("worlds") == 100000, "E05 records 100,000 authored worlds")
check(sim.get("numerically_verified_worlds") == 500, "E05 records 500 verification worlds")
mismatch_count = sim.get("analytic_numeric_mismatches_over_003", -1)
check(mismatch_count == 6, f"E05 retains six finite-horizon mismatches (found {mismatch_count})")

# E07: fair-access software fixture.
p = subprocess.run([sys.executable, str(EXP / "E07_SOFTWARE_FAIR/score.py")], text=True, capture_output=True)
check(p.returncode == 0, "E07 scorer exits zero")
check('"passed": 23' in p.stdout or '23 passed' in p.stdout, "E07 reports 23 passing tests")
check('"normalization_calls": 11' in p.stdout and '"normalization_calls": 3' in p.stdout, "E07 structural count is 11 versus 3")

# E09: deterministic held-out selection from a bundled frozen input.
e09 = EXP / "E09_HELDOUT"
p = subprocess.run([sys.executable, str(e09 / "select.py")], text=True, capture_output=True)
check(p.returncode == 0, "E09 selector exits zero")
if p.returncode == 0:
    got = json.loads(p.stdout)
    expected = json.loads((e09 / "output/selection.json").read_text())
    check(got == expected, "E09 held-out selection reproduces exactly")

# E10: 20 tasks, seven architectures, 35% software allocation, complete schema.
e10 = EXP / "E10_ARCHITECTURE_SUITE"
tasks = json.loads((e10 / "tasks.json").read_text())
architectures = json.loads((e10 / "architectures.json").read_text())
fields = ["id", "binding_constraint", "first_action", "machine_work", "selector", "human_object", "stop_authority", "durable_learning"]
check(len(tasks) == 20, "E10 contains 20 tasks")
check(sum(t.get("domain") == "swe" for t in tasks) == 7, "E10 software allocation is 7/20")
complete = True
for name in architectures:
    rows = json.loads((e10 / "output" / f"{name}.md").read_text())
    complete &= len(rows) == 20 and all(all(isinstance(row.get(f), str) and row[f].strip() for f in fields) for row in rows)
check(len(architectures) == 7 and complete, "E10 has seven complete 20-task outputs")

for message in passed:
    print(f"PASS: {message}")
for message in errors:
    print(f"FAIL: {message}", file=sys.stderr)
print(f"{len(passed)} passed, {len(errors)} failed")
raise SystemExit(bool(errors))
