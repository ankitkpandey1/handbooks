#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
cm=json.loads((ROOT/'canonical_source_manifest.json').read_text())
s=(ROOT/cm['source_filename']).read_text()
section=s.split('# Edition and maintenance record',1)[1].split('## Accessibility and format note',1)[0]
versions=re.findall(r'^### Edition (\d+\.\d+\.\d+) - \d{1,2} [A-Za-z]+ \d{4}$',section,re.M)
expected=['1.7.0','1.6.0','1.5.0','1.4.0','1.3.0','1.2.0','1.1.0']
if versions!=expected:
    raise SystemExit(f'edition history invalid: {versions}; expected {expected}')
if len(set(versions))!=len(versions):
    raise SystemExit(f'duplicate edition headings: {versions}')
print('OK: edition history is unique and continuous from 1.7.0 through 1.1.0')
