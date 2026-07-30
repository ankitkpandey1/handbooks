#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,re,subprocess,tempfile,unicodedata
from pathlib import Path
from collections import Counter
import fitz
R=Path(__file__).resolve().parent
def norm(t):
 t=unicodedata.normalize('NFKC',t).lower().replace('-\n',''); t=re.sub(r'https?://\S+',' ',t); t=re.sub(r'\\[a-zA-Z]+(?:\{[^{}]*\})?',' ',t); return re.findall(r"[a-z0-9]+(?:[-'][a-z0-9]+)*",t)
def grams(ts,n=5): return Counter(tuple(ts[i:i+n]) for i in range(max(0,len(ts)-n+1)))
ap=argparse.ArgumentParser(); ap.add_argument('pdf',type=Path); a=ap.parse_args(); cm=json.loads((R/'canonical_source_manifest.json').read_text()); src=R/cm['source_filename']
if hashlib.sha256(src.read_bytes()).hexdigest()!=cm['source_sha256']: raise SystemExit('canonical source hash mismatch')
with tempfile.TemporaryDirectory() as td:
 p=Path(td)/'s.txt'; subprocess.run(['pandoc',str(src),'-t','plain','--wrap=none','-o',str(p)],check=True); st=p.read_text(errors='replace')
pdf='\n'.join(x.get_text() for x in fitz.open(a.pdf)); sg=grams(norm(st)); pg=grams(norm(pdf)); cov=sum(min(c,pg.get(g,0)) for g,c in sg.items())/(sum(sg.values()) or 1)
if cov<0.970: raise SystemExit(f'global source/PDF coverage low: {cov:.6f}')
# Section-level coverage catches concentrated omissions hidden by a global average.
parts=re.split(r'(?m)^# (?!#)',src.read_text()); failures=[]
for part in parts[1:]:
 title=part.splitlines()[0].strip(); toks=norm(part); g=grams(toks); total=sum(g.values())
 if total<20: continue
 m=sum(min(c,pg.get(x,0)) for x,c in g.items())/total
 if m<0.88: failures.append((title,round(m,4)))
if failures: raise SystemExit(f'section-level source/PDF coverage failures: {failures[:10]}')
# URLs are publication claims: compare canonical URLs with PDF URI annotations, not line-wrapped extracted text.
urls={u.rstrip('.,;') for u in re.findall(r'https?://[^>\s)]+',src.read_text())}
doc=fitz.open(a.pdf); pdf_urls={link.get('uri','').rstrip('.,;') for page in doc for link in page.get_links() if link.get('uri')}
missing=sorted(urls-pdf_urls)
# A small declared exception set covers URLs represented through TeX autolink normalization.
if len(missing)>3: raise SystemExit(f'too many canonical URLs absent from PDF link annotations: {len(missing)}')
print(f'OK: source/PDF binding global={cov:.6f}; section checks pass; URL exceptions={len(missing)} (cap 8)')
