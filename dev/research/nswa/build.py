import json,re
subs=[];cur=None
for line in open('raw.txt'):
    line=line.rstrip('\n')
    if not line: continue
    if line.startswith('#'):
        n,p=line[1:].split('|'); cur={"name":n,"postcode":p,"crime":None,"prop":None,"schools":[],"mall":None,"growthArea":False,"flags":[]}; subs.append(cur)
    elif line.startswith('C '):
        d={k:int(v) for k,v in re.findall(r'(\w+)=(\d+)',line)}
        person=sum(d[k] for k in ['assault','robbery','sexual','homicide','intimidation','abduction','otherperson','blackmail'])
        prop=d['theft']+d['damage']+d['arson']
        cur['crime']={"offences":d['total'],"population":d['pop'],"person":person,"property":prop,"area":None}
    elif line.startswith('P '):
        d=dict(re.findall(r'(\w+)=([^;]+)',line[2:]))
        def num(v,f=float):
            v=v.strip().replace('$','').replace(',','').replace('%','')
            return None if v=='null' else f(v)
        cur['prop']={"median":num(d['median'],int),"growth":num(d['growth']),"yield":num(d['yield']),"rent":num(d['rent'],int)}
    elif line.startswith('S '):
        a=line[2:].split('|'); cur['schools'].append([a[0],a[1],a[2],int(a[3])])
m=next(s for s in subs if s['name']=='Mascot')
assert m['crime']=={"offences":1364,"population":21591,"person":287,"property":716,"area":None}
for s in subs: s['schools'].sort(key=lambda x:-x[3])
meta={
"Mascot":dict(flags=["Sydney Airport is inside the suburb; airport and station offences (e.g. 131 transport regulatory) count here"]),
"Marrickville":dict(mall="Marrickville Metro"),
"Newtown":dict(flags=["King Street / Enmore Road nightlife strip","493 against-justice-procedures offences (mostly bail breaches) inflate the total"]),
"Hurstville":dict(mall="Westfield Hurstville",flags=["1,785 transport regulatory offences (Hurstville station) inflate the total"]),
"Bankstown":dict(mall="Bankstown Central",flags=["1,726 against-justice-procedures offences (police/court hub) inflate the total"]),
"Miranda":dict(mall="Westfield Miranda"),
"Roselands":dict(mall="Roselands Shopping Centre"),
"Ashfield":dict(mall="Ashfield Mall"),
"Leichhardt":dict(mall="Leichhardt MarketPlace"),
"Campsie":dict(mall="Campsie Centre"),
"Hillsdale":dict(mall="Southpoint Shopping Centre"),
"Eastlakes":dict(mall="Eastlakes Shopping Centre"),
"Sutherland":dict(flags=["711 transport regulatory and 516 against-justice-procedures offences (station, police/court) make up most of the total"]),
"Kogarah":dict(flags=["422 against-justice-procedures and 233 transport regulatory offences inflate the total; St George Hospital"]),
"Riverwood":dict(flags=["397 transport regulatory and 357 against-justice-procedures offences inflate the total"]),
"Wolli Creek":dict(flags=["507 transport regulatory offences (Wolli Creek station) inflate the total","High-density apartment suburb: few house sales, no house price data"]),
"Sydenham":dict(flags=["Small residential population (1,100); 138 transport regulatory offences at Sydenham station inflate the rate"]),
"Cronulla":dict(flags=["Beach and nightlife strip"]),
"Kensington":dict(flags=["Next to UNSW; large student population"]),
"Kingsford":dict(flags=["Next to UNSW; large student population"]),
"Kyeemagh":dict(flags=["Very small population (935), so rates swing on a few incidents"]),
}
for s in subs:
    for k,v in meta.get(s['name'],{}).items(): s[k]=v
nosch={"Sydenham","Kingsford","Pagewood","Hillsdale","Wolli Creek","Kyeemagh","Monterey"}
for s in subs:
    if s['name'] in nosch: s['flags'].append("No schoolrank.com.au suburb page (404); nearby schools are listed under neighbouring suburbs")
out={"region":"nsw",
"crimeSource":{"name":"AU Crime Tracker (republishes NSW BOCSAR recorded criminal incidents)","url":"https://www.aucrimetracker.com/nsw/","period":"year to March 2026","level":"suburb","stateRatePer1000":77.7,
"stateRateSource":"AU Crime Tracker NSW page: 627,403 recorded incidents, year ending Mar 2026, NSW population 8,072,163 (2021 census) -> 77.7 per 1,000",
"notes":"Offences = all recorded incidents incl. transport regulatory, drug and against-justice-procedures offences. Person = assault + robbery + sexual + homicide + intimidation/stalking/harassment + abduction + blackmail/extortion + other offences against the person. Property = theft (incl. break-in and vehicle theft) + malicious damage + arson. Populations are 2021 census as shown by AU Crime Tracker. Punchbowl and Summer Hill use the qualified slugs punchbowl-canterbury-bankstown and summer-hill-inner-west. Property: CoreLogic via yourinvestmentpropertymag.com.au, houses only. Schools: schoolrank.com.au suburb pages, rated schools only."},
"suburbs":subs}
json.dump(out,open('/tmp/claude-0/-home-claude-tullamarine-flight-map/a94e428b-9c1e-5182-90c8-c6aeb42cd856/scratchpad/regions/nsw_a.json','w'),indent=1,ensure_ascii=False)
print(len(subs),sum(1 for s in subs if s['crime']),sum(1 for s in subs if s['prop'] and s['prop']['median']),sum(1 for s in subs if s['schools']))
print(round(627403/8072163*1000,2))
for s in subs:
    if not s['crime'] or not s['prop']: print('missing',s['name'])
