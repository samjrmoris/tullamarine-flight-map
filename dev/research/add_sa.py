import json,sys
f=open('/tmp/claude-0/-home-claude-tullamarine-flight-map/a94e428b-9c1e-5182-90c8-c6aeb42cd856/scratchpad/regions/fill_sa.jsonl','a')
kind=sys.argv[1]; n=sys.argv[2]
def num(x): 
  return None if x in('null','None','') else float(x) if '.' in x else int(x)
if kind=='c':
  o=num(sys.argv[3]); r=num(sys.argv[4])
  pop=round(o/r*1e5) if o and r else None
  d={'n':n,'crime':[o,pop,None,None]}
elif kind=='p':
  v=[num(x) for x in sys.argv[3:7]]
  d={'n':n,'prop':None if all(x is None for x in v) else v}
elif kind=='s':
  d={'n':n,'schools':json.loads(sys.argv[3])}
f.write(json.dumps(d)+'\n'); print(json.dumps(d))
