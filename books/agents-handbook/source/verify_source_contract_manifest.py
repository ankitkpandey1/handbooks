#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,re,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent
HEX40=re.compile(r'^[0-9a-f]{40}$'); HEX64=re.compile(r'^[0-9a-f]{64}$')
def git_blob(data:bytes)->str: return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def records(m):
    for g in [*m.get('examples',[]),*m.get('source_audits',[])]:
        repo,commit=g.get('repository'),g.get('commit')
        if not repo or not commit: continue
        if not HEX40.fullmatch(commit): raise SystemExit(f'invalid commit: {commit}')
        files=g.get('source_files',[])
        for s in files:
            b=s['git']['blob_sha1']; expected=s['content'].get('sha256'); v=s['verification']
            if not HEX40.fullmatch(b): raise SystemExit(f'invalid blob SHA-1: {repo}:{s["path"]}')
            if f'/blob/{commit}/' not in s['url']: raise SystemExit(f'non-immutable URL: {s["url"]}')
            if expected is not None and not HEX64.fullmatch(expected): raise SystemExit(f'invalid SHA-256: {repo}:{s["path"]}')
            if bool(expected) != bool(v.get('content_sha256_verified')):
                raise SystemExit(f'inconsistent content SHA-256 state: {repo}:{s["path"]}')
            yield repo,commit,s['path'],b,expected,v

def check_receipt(rs):
    receipt=json.loads((ROOT/'source_contract_verification_receipt.json').read_text())
    got={(x['repository'],x['commit'],x['path']):x for x in receipt['records']}
    if receipt['record_count']!=len(rs) or len(got)!=len(rs): raise SystemExit('source receipt record count mismatch')
    for repo,commit,path,b,expected,v in rs:
        r=got.get((repo,commit,path))
        if not r: raise SystemExit(f'missing receipt record: {repo}@{commit}:{path}')
        if r['expected_blob_sha1']!=b or r['fetched']!=v['fetched'] or r['git_blob_sha1_verified']!=v['blob_verified'] or r['expected_content_sha256']!=expected or r['content_sha256_verified']!=v['content_sha256_verified']:
            raise SystemExit(f'manifest/receipt state mismatch: {repo}@{commit}:{path}')

m=json.loads((ROOT/'framework_source_contract_manifest.json').read_text()); rs=list(records(m)); check_receipt(rs)
ap=argparse.ArgumentParser(); ap.add_argument('--manifest-only',action='store_true'); ap.add_argument('--require-content-sha256',action='store_true'); ap.add_argument('--timeout',type=float,default=30); a=ap.parse_args()
known=sum(x[4] is not None for x in rs)
if a.require_content_sha256 and known!=len(rs): raise SystemExit(f'strict raw SHA-256 verification unavailable: {known}/{len(rs)} records populated')
if a.manifest_only:
    print(f'OK: manifest and receipt structure agree for {len(rs)} immutable files; {known} carry expected raw SHA-256; contents NOT fetched in this run')
    raise SystemExit
verified256=0
for repo,commit,path,b1,s256,v in rs:
    req=urllib.request.Request(f'https://raw.githubusercontent.com/{repo}/{commit}/{path}',headers={'User-Agent':'production-agent-engineering-verifier/1.7'})
    with urllib.request.urlopen(req,timeout=a.timeout) as r: data=r.read()
    if git_blob(data)!=b1: raise SystemExit(f'Git blob mismatch: {repo}@{commit}:{path}')
    if s256 is not None:
        if hashlib.sha256(data).hexdigest()!=s256: raise SystemExit(f'raw SHA-256 mismatch: {repo}@{commit}:{path}')
        verified256+=1
print(f'OK: fetched and Git-blob-verified {len(rs)} files; raw SHA-256 verified for {verified256}; absent expected SHA-256 values were not claimed')
