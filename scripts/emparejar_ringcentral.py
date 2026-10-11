import json
from collections import Counter
from datetime import datetime,timedelta
D=json.load(open('/home/user/minibus/all.json'))
R=json.load(open('/home/user/minibus/rc_today.json'))
P=lambda s: datetime.fromisoformat(s.replace('Z','+00:00'))
used=set();un=[];res=[]
for d in D:
  for t in d['transfers']:
    ts=P(t['ts']);best=None
    for r in R:
      if r['id'] in used or r['to_ext']!=t['ext']: continue
      dt=(P(r['start'])-ts).total_seconds()
      if abs(dt)<=15 and (best is None or abs(dt)<abs(best[1])): best=(r,dt)
    if best: used.add(best[0]['id']); res.append((d,t,best[0],best[1]))
    else: un.append((d,t))
print('matched',len(res),'unmatched',len(un))
print('dt dist',Counter(round(b) for _,_,_,b in res))
for d,t in un: print('UNM',d['pais'],d['run_id'],t['ext'],t.get('error'),t['ts'])
for d,t,r,dt in res:
  if (t.get('error') or '') not in ('',) : print('ERR',d['run_id'][:8],t['ext'],t.get('error'),r['duration'],r['result'])
# matched connected short durations
print('dur of ok', sorted(r['duration'] for d,t,r,_ in res if not t.get('error'))[:15])
mini={'18056','18059','18069','18073','18063','18066'}
print('RC minibus legs total',Counter(r['to_ext'] for r in R if r['to_ext'] in mini|{'2114','2115','2119'}))
print('RC minibus legs unmatched',[(r['to_ext'],r['start'],r['duration']) for r in R if r['to_ext'] in mini|{'2114','2115','2119'} and r['id'] not in used])
json.dump({'used':list(used)},open('/home/user/minibus/rc_used.json','w'))
