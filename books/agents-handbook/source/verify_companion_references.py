#!/usr/bin/env python3
from pathlib import Path
import json,re
R=Path(__file__).resolve().parent
cm=json.loads((R/'canonical_source_manifest.json').read_text())
s=(R/cm['source_filename']).read_text()
# Resolve companion filenames explicitly mentioned in code-font spans. Ignore URLs, schema names and illustrative paths.
refs=set(re.findall(r'`([^`\n]+\.(?:py|json|csv|txt|yaml|yml|sh|zip|md))`',s))
ignore={'CLAUDE.md','AGENTS.md','README.md'}
missing=[]
for ref in sorted(refs-ignore):
    name=Path(ref.split()[-1]).name
    if name.startswith('Production_Agent_Engineering_Edition_1.8'):
        continue
    if not (R/name).exists(): missing.append(ref)
if missing: raise SystemExit(f'missing referenced companion artefacts: {missing}')
print(f'OK: resolved {len(refs-ignore)-len(missing)} manuscript companion-file references')
