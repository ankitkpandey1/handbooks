#!/usr/bin/env python3
"""Application-level deterministic checks only; not a provider SDK integration test."""
import hashlib,json,time

def canon(name,args): return json.dumps({'name':name,'arguments':args},sort_keys=True,separators=(',',':'))
def action_hash(name,args): return hashlib.sha256(canon(name,args).encode()).hexdigest()
record={'name':'WriteTicket','args':{'ticket':'QA-17','body':'verified'},'policy':'p7','authority':'a3','expires':time.time()+60,'executed':False}
record['hash']=action_hash(record['name'],record['args'])
assert action_hash(record['name'],record['args'])==record['hash']
assert action_hash(record['name'],{'ticket':'QA-17','body':'changed'})!=record['hash']
assert record['expires']>time.time()
def commit(r,name,args,policy,authority):
    assert not r['executed']; assert time.time()<r['expires']; assert policy==r['policy']; assert authority==r['authority']; assert action_hash(name,args)==r['hash']; r['executed']=True
commit(record,record['name'],record['args'],'p7','a3')
try: commit(record,record['name'],record['args'],'p7','a3')
except AssertionError: pass
else: raise SystemExit('duplicate execution was not suppressed')
print('OK: application approval hash, mutation rejection, expiry, policy/authority binding and duplicate suppression tested; provider defer/resume NOT tested')
