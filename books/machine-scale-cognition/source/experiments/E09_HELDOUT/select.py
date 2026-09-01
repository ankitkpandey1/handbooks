# SPDX-FileCopyrightText: 2026 Ankit Kumar Pandey
# SPDX-License-Identifier: Apache-2.0
import hashlib
import json
import pathlib

requirements = pathlib.Path(__file__).parent / "frozen_requirements.md"
candidates = json.loads((pathlib.Path(__file__).parent / "candidates.json").read_text())
digest = hashlib.sha256(requirements.read_bytes()).hexdigest()
index = int(digest[:16], 16) % len(candidates)
print(json.dumps({"requirements_sha256":digest,"algorithm":"int(first_16_hex,16) mod N","candidate_count":len(candidates),"index":index,"selected":candidates[index]}, indent=2))
