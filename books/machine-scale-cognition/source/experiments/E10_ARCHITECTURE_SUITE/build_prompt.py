# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import json
import pathlib
import sys

root = pathlib.Path(__file__).parent
key = sys.argv[1]
architectures = json.loads((root / "architectures.json").read_text())
tasks = json.loads((root / "tasks.json").read_text())
print(f"Apply operating architecture {key} exactly: {architectures[key]}")
print("For each task, produce a compact operating decision. Do not research or invent facts. Return only a JSON array with one object per task and exactly these string fields: id, binding_constraint, first_action, machine_work, selector, human_object, stop_authority, durable_learning. Make operations task-specific; allow the architecture to fail rather than silently importing another architecture. Tasks:")
print(json.dumps(tasks))
