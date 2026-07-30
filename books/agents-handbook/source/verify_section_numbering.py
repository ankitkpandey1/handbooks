#!/usr/bin/env python3
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parent
cm=json.loads((ROOT/"canonical_source_manifest.json").read_text())
s=(ROOT/cm["source_filename"]).read_text()
nums=[int(x) for x in re.findall(r"^### 18B\.(\d+)\b",s,re.M)]
if nums!=list(range(1,18)): raise SystemExit(f"Part 18B numbering invalid: {nums}")
print("OK: Part 18B numbering is continuous 18B.1 through 18B.17")
