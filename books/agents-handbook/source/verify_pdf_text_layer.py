#!/usr/bin/env python3
from __future__ import annotations
import argparse,re,shutil,subprocess,tempfile
from pathlib import Path
import fitz
WORDS=['field','workflow','verification','official','different','sufficient','first','files','effect','information-flow']; BROKEN=[r'work\s+ow',r'veri\s+cation',r'o\s+cial',r'di\s+erent',r'su\s+cient',r'\beld\b',r'\brst\b']
def check(name,text):
    e=[]; low=text.lower()
    if '\ufffd' in text or '□' in text: e.append(f'{name}: replacement/square characters present')
    for w in WORDS:
        if w not in low: e.append(f'{name}: missing searchable token {w!r}')
    for p in BROKEN:
        if re.search(p,low): e.append(f'{name}: broken ligature pattern {p!r}')
    return e
a=argparse.ArgumentParser(); a.add_argument('pdf'); x=a.parse_args(); pdf=Path(x.pdf)
if not pdf.exists(): raise SystemExit(f'PDF not found: {pdf}')
if not shutil.which('pdftotext'): raise SystemExit('pdftotext is required')
with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'p.txt'; subprocess.run(['pdftotext',str(pdf),str(out)],check=True); pop=out.read_text(errors='replace')
doc=fitz.open(pdf); pym='\n'.join(p.get_text() for p in doc); errors=check('Poppler',pop)+check('PyMuPDF',pym)
if errors: raise SystemExit('\n'.join(errors))
print('OK: Poppler and PyMuPDF text extraction passed ligature/search token checks')
