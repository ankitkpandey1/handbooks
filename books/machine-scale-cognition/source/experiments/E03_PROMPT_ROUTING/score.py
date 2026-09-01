# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import pathlib
import sys

root = pathlib.Path(__file__).parent
gold = json.loads((root / "answers.json").read_text())
rows = []
for name in ("c0_direct", "c1_decompose", "c2_cot"):
    path = root / "output" / f"{name}.md"
    try:
        got = json.loads(path.read_text())
        exact = sum(got.get(k) == v for k, v in gold.items())
        valid = set(got) == set(gold) and all(isinstance(v, int) for v in got.values())
    except Exception as exc:
        got, exact, valid = {"error": str(exc)}, 0, False
    rows.append({"condition": name, "exact": exact, "total": len(gold), "valid_schema": valid, "answers": got})
print(json.dumps(rows, indent=2, sort_keys=True))
sys.exit(0 if all(r["valid_schema"] for r in rows) else 1)
