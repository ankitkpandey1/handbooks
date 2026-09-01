# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import ast
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).parent
for condition in ("b1", "s"):
    repo = root / "output" / f"{condition}_repo"
    run = subprocess.run(["python", "-m", "pytest", "-q"], cwd=repo, text=True, capture_output=True)
    calls = 0
    for path in repo.glob("*.py"):
        if path.name.startswith("test_"): continue
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node, ast.Attribute) and node.attr in {"lower", "casefold", "strip", "replace"}: calls += 1
    print(json.dumps({"condition":condition,"exit":run.returncode,"pytest":run.stdout.strip(),"normalization_calls":calls}))
