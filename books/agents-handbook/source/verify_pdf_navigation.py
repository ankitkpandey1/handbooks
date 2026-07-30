#!/usr/bin/env python3
from __future__ import annotations
import argparse,re
from pathlib import Path
import fitz
ap=argparse.ArgumentParser(); ap.add_argument('pdf',type=Path); a=ap.parse_args()
doc=fitz.open(a.pdf); toc=doc.get_toc(simple=True)
if len(toc)<350: raise SystemExit(f'bookmark count unexpectedly low: {len(toc)}')
errors=[]
for level,title,page in toc:
    if page<1 or page>doc.page_count: errors.append(f'invalid bookmark page {page}: {title}'); continue
    page_text=doc[page-1].get_text().lower().replace('-\n','')
    key=re.sub(r'[^a-z0-9]+',' ',title.lower()).strip()
    # Match a distinctive prefix, tolerant of line wrapping and punctuation.
    probe=' '.join(key.split()[:8])
    hay=' '.join(re.sub(r'[^a-z0-9]+',' ',page_text).split())
    if probe and probe not in hay:
        errors.append(f'bookmark destination does not contain title: p{page} {title}')
        if len(errors)>=12: break
# Verify internal GoTo links exist and destinations are in range.
internal=0
for p in doc:
    for link in p.get_links():
        if link.get('kind')==fitz.LINK_GOTO:
            internal+=1
            dest=link.get('page',-1)
            if dest<0 or dest>=doc.page_count: errors.append(f'invalid internal link destination {dest}')
if internal<350: errors.append(f'internal link count unexpectedly low: {internal}')
if errors: raise SystemExit('\n'.join(errors))
print(f'OK: {len(toc)} bookmarks and {internal} internal links resolve to valid rendered destinations')
