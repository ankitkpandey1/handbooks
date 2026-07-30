#!/usr/bin/env python3
import argparse,hashlib,json,re,datetime
from pathlib import Path
import fitz
R=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
ap=argparse.ArgumentParser(); ap.add_argument('pdf',type=Path); ap.add_argument('archive',type=Path); ap.add_argument('receipt',type=Path); a=ap.parse_args(); r=json.loads(a.receipt.read_text())
required={'schema_version','edition','generated_at','canonical_source','reproducibility_archive','final_pdf','build_inputs','build_command','tool_versions','attestation','circularity_boundary'}
if set(r)!=required: raise SystemExit(f'receipt fields mismatch: {set(r)^required}')
if r['schema_version']!='production-agent-engineering/publication-build-receipt/v2' or r['edition']!='1.8.0': raise SystemExit('receipt schema/edition mismatch')
datetime.datetime.fromisoformat(r['generated_at'])
cm=json.loads((R/'canonical_source_manifest.json').read_text()); src=R/cm['source_filename']; d=fitz.open(a.pdf)
checks=[(r['canonical_source'],src),(r['reproducibility_archive'],a.archive),(r['final_pdf'],a.pdf)]
for rec,p in checks:
    if rec['filename']!=Path(p).name or rec['sha256']!=sha(p): raise SystemExit(f'receipt file binding mismatch: {p}')
actual={'pages':d.page_count,'bookmarks':len(d.get_toc(simple=True)),'links':sum(len(p.get_links()) for p in d),'linearized':bool(d.is_fast_webaccess)}
for k,v in actual.items():
    if r['final_pdf'][k]!=v: raise SystemExit(f'receipt PDF field mismatch: {k}')
for n,h in r['build_inputs'].items():
    if not (R/n).is_file() or sha(R/n)!=h: raise SystemExit(f'build-input mismatch: {n}')
expected=f'bash build_pdf.sh {src.name} {a.archive.name} {a.pdf.name}'
if r['build_command']!=expected: raise SystemExit('build command mismatch')
if r['attestation'].get('signed') is not False: raise SystemExit('unsupported signing claim')
print('OK: complete unsigned build receipt validated')
