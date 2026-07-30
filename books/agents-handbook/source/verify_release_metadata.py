#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
checks={
 'README.md':[r'Edition 1\.8\.0',r'bash run_publication_checks\.sh'],
 'BUILD_ENVIRONMENT.txt':[r'Edition: 1\.8\.0'],
 'canonical_source_manifest.json':[r'"edition": "1\.8\.0"',r'edition_1_8\.md'],
 'framework_source_contract_manifest.json':[r'"edition": "1\.8\.0"'],
 'reproduce_qa_evaluation.py':[r'evaluation in Edition 1\.8'],
}
errors=[]
for name,patterns in checks.items():
    p=ROOT/name
    if not p.exists(): errors.append(f'missing {name}'); continue
    text=p.read_text()
    for pattern in patterns:
        if not re.search(pattern,text): errors.append(f'{name}: missing {pattern}')
for name in ['BUILD_ENVIRONMENT.txt','README.md','requirements.txt','reproduce_qa_evaluation.py','run_publication_checks.sh']:
    p=ROOT/name
    if p.exists() and re.search(r'Edition 1\.[457](?!\d)',p.read_text()):
        errors.append(f'{name}: stale release metadata')
if errors: raise SystemExit('\n'.join(errors))
print('OK: authoritative package metadata consistently identifies Edition 1.8.0')
