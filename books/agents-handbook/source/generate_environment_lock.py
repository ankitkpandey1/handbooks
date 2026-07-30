#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,platform,subprocess,sys
from importlib import metadata
from pathlib import Path
from packaging.requirements import Requirement
ROOTS=['numpy','pandas','scipy','PyMuPDF','pypdf','packaging']

def canon(n): return n.lower().replace('_','-')
seen={}; queue=list(ROOTS)
while queue:
    name=queue.pop(0); key=canon(name)
    if key in seen: continue
    try: dist=metadata.distribution(name)
    except metadata.PackageNotFoundError: continue
    files=[]
    for f in dist.files or []:
        p=Path(dist.locate_file(f))
        if p.is_file():
            try: h=hashlib.sha256(p.read_bytes()).hexdigest(); size=p.stat().st_size
            except OSError: continue
            files.append({'path':str(f),'sha256':h,'size':size})
    files.sort(key=lambda x:x['path'])
    tree=hashlib.sha256('\n'.join(f"{x['sha256']}  {x['path']}" for x in files).encode()).hexdigest()
    reqs=[]
    for raw in dist.requires or []:
        try:
            r=Requirement(raw)
            if r.marker and not r.marker.evaluate(): continue
            reqs.append(str(r)); queue.append(r.name)
        except Exception: reqs.append(raw)
    seen[key]={'name':dist.metadata['Name'] or name,'version':dist.version,'requires':sorted(reqs),'installed_tree_sha256':tree,'file_count':len(files)}
binaries={}
for cmd in ['python','pandoc','xelatex','pdftotext','gs']:
    path=subprocess.run(['bash','-lc',f'command -v {cmd}'],capture_output=True,text=True).stdout.strip()
    if path and Path(path).is_file():
        version=subprocess.run([path,'--version'],capture_output=True,text=True).stdout.splitlines()[:2]
        if cmd=='pdftotext': version=subprocess.run([path,'-v'],capture_output=True,text=True).stderr.splitlines()[:2]
        binaries[cmd]={'path':path,'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'version_lines':version}
out={'schema_version':'production-agent-engineering/environment-lock/v1','edition':'1.8.0','platform':platform.platform(),'python':sys.version,'packages':sorted(seen.values(),key=lambda x:x['name'].lower()),'binaries':binaries}
Path(__file__).with_name('environment_attestation.json').write_text(json.dumps(out,indent=2)+'\n')
Path(__file__).with_name('requirements.txt').write_text('\n'.join(f"{x['name']}=={x['version']}" for x in out['packages'])+'\n')
print(f"wrote {len(out['packages'])} package records and {len(binaries)} binary hashes")
