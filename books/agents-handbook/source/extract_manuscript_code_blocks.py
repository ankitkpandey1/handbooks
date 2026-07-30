#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,re
from pathlib import Path
LABEL_TOKENS=("Tested example", "Tested companion example", "Generated from", "Source-contract checked", "Illustrative API mapping", "Framework-neutral pseudocode", "data contract", "protocol sketch", "authority profile")
def extract(src:Path):
    lines=src.read_text().splitlines()
    blocks=[]; i=0; idx=0
    while i<len(lines):
        m=re.match(r'^```\s*([^ ]*)\s*$',lines[i])
        if not m: i+=1; continue
        lang=m.group(1).strip().lower(); start=i+1; j=i+1
        while j<len(lines) and not re.match(r'^```\s*$',lines[j]): j+=1
        if j>=len(lines): raise SystemExit(f'unclosed fence at line {i+1}')
        content='\n'.join(lines[start:j])+'\n'
        label=None
        for k in range(i-1,max(-1,i-12),-1):
            x=lines[k].strip().strip('*')
            if not x: continue
            if any(tok.lower() in x.lower() for tok in LABEL_TOKENS): label=x; break
        idx+=1
        blocks.append({'index':idx,'start_line':start+1,'language':lang,'nonblank_lines':sum(bool(x.strip()) for x in content.splitlines()),'authenticity_label':label,'sha256':hashlib.sha256(content.encode()).hexdigest(),'content':content})
        i=j+1
    return {'schema_version':'production-agent-engineering/manuscript-code-blocks/v2','edition':'1.7.0','source_filename':src.name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'blocks':blocks}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('source',type=Path); ap.add_argument('output',type=Path); a=ap.parse_args()
    a.output.write_text(json.dumps(extract(a.source),indent=2,ensure_ascii=False)+'\n')
if __name__=='__main__': main()
