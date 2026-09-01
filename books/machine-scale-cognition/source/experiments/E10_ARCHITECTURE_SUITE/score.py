# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import pathlib

root = pathlib.Path(__file__).parent
tasks = json.loads((root / "tasks.json").read_text())
fields = ["id","binding_constraint","first_action","machine_work","selector","human_object","stop_authority","durable_learning"]
for condition in json.loads((root / "architectures.json").read_text()):
    path = root / "output" / f"{condition}.md"
    try:
        rows = json.loads(path.read_text())
        by_id = {r.get("id"):r for r in rows}
        missing_tasks = [t["id"] for t in tasks if t["id"] not in by_id]
        missing_fields = sum(not isinstance(r.get(f),str) or not r.get(f).strip() for r in rows for f in fields)
        swe = sum(1 for t in tasks if t["domain"] == "swe")
        print(json.dumps({"condition":condition,"rows":len(rows),"missing_tasks":missing_tasks,"missing_fields":missing_fields,"swe_tasks":swe,"total_tasks":len(tasks)}))
    except Exception as exc:
        print(json.dumps({"condition":condition,"parse_error":str(exc)}))
