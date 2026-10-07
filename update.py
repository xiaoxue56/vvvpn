import os,json,pathlib,concurrent.futures,datetime
import vpngate as g
COUNTRIES=('JP','TW','SG')

def main():
 if not os.environ.get('DOMAIN','').startswith('https://') or not os.environ.get('CHECK_TOKEN'): raise RuntimeError('Required secrets unavailable')
 g.VPNGATE_API='https://www.vpngate.net/api/iphone/'
 rows,source=g.fetch_vpngate();nodes=g.dedupe(g.to_sstp_nodes(rows));picked=[]
 for country in COUNTRIES:picked.extend([n for n in nodes if n['country_code']==country][:20])
 def check(n):
  import requests
  x=g.check_one(n,requests.Session())
  # Checker strings cannot be trusted to be safe public output.
  x['error']=None if x.get('success') else 'check_failed';x['residential']='unverified'
  return x
 with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:results=list(pool.map(check,picked))
 data=g.build_outputs(results,len(rows),len(nodes),source)
 counts={c:sum(n['country_code']==c for n in data['available']) for c in COUNTRIES}
 data['target_source_counts']={c:sum(n['country_code']==c for n in nodes) for c in COUNTRIES}
 # Empty regions are published truthfully; they must not block healthy regions.
 p=pathlib.Path('public');p.mkdir(exist_ok=True)
 (p/'data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
 for c in COUNTRIES:
  available=[n for n in data['available'] if n['country_code']==c]
  (p/(c.lower()+'.json')).write_text(json.dumps({'generated_at':data['generated_at'],'country':c,'count':len(available),'nodes':available},ensure_ascii=False,indent=2))
  (p/(c.lower()+'.txt')).write_text(''.join(n['link']+'\n' for n in available))
 (p/'nodes.txt').write_text(''.join(n['link']+'\n' for n in data['available']))
 (p/'index.html').write_text('<!doctype html><meta charset="utf-8"><title>JP TW SG VPNGate</title><h1>JP / TW / SG VPNGate TCP candidate pools</h1><p>Empty pools mean no verified candidates. Not an SLA, residential proof, UDP or IPv6 support. Active sidecar refresh is separate and fail-closed.</p><a href="jp.json">JP JSON</a> <a href="tw.json">TW JSON</a> <a href="sg.json">SG JSON</a> <a href="nodes.txt">SSTP list</a><pre id="out"></pre><script>fetch("data.json").then(r=>r.json()).then(d=>out.textContent=JSON.stringify({generated_at:d.generated_at,stats:d.stats,target_source_counts:d.target_source_counts},null,2))</script>')
 for name in ('kr.json','kr.txt'):(p/name).unlink(missing_ok=True)
 for f in p.iterdir():
  if f.is_file():
   text=f.read_text()
   for secret in (os.environ['DOMAIN'],os.environ['CHECK_TOKEN']):assert secret not in text
 print('Generated checked candidate pools',counts)
if __name__=='__main__':
 try:main()
 except Exception as e:
  print('Pool build failed:',type(e).__name__);raise SystemExit(1)
