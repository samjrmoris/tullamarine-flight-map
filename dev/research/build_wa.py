import json,csv,os
D=os.path.dirname(os.path.abspath(__file__))
def rd(f):
    p=os.path.join(D,f)
    if not os.path.exists(p): return {}
    return {r[0]:r[1:] for r in csv.reader(open(p),delimiter='\t') if r}
crime=rd('wa_crime.tsv'); prop=rd('wa_prop.tsv'); meta=rd('wa_meta.tsv')
schools={}
sp=os.path.join(D,'wa_schools.json')
if os.path.exists(sp): schools=json.load(open(sp))
flags={
 'Welshpool':['Mostly industrial; 2021 population only 16, so per-capita rate is meaningless'],
 'Kewdale':['Large industrial/freight area (Kewdale freight terminal) inflates property offences per resident'],
 'Hazelmere':['Largely industrial/semi-rural; small resident population'],
 'Midland':['Regional centre: Midland Gate, hospital and train station inflate offences per resident'],
 'Cannington':['Westfield Carousel drives high theft counts relative to small population'],
 'Victoria Park':['Albany Highway dining/nightlife strip'],
 'East Victoria Park':['Albany Highway strip'],
 'Mount Lawley':['Beaufort Street dining/nightlife strip'],
 'Scarborough':['Beachfront nightlife/tourist precinct'],
 'Joondalup':['City centre: Lakeside Joondalup, ECU campus, hospital; small resident population'],
 'Morley':['Galleria regional shopping centre'],
 'Belmont':['Directly beside Perth Airport; Perth Airport itself is a separate locality so airport crime is not counted here'],
 'Redcliffe':['Adjoins Perth Airport (airport is a separate locality); METRONET Redcliffe station area redeveloping'],
 'Jandakot':['Contains Jandakot Airport; small population'],
 'Bibra Lake':['Large industrial area'],
 'Success':['Cockburn Gateway shopping centre'],
}
out=[]
for n,m in meta.items():
    c=crime.get(n); p=prop.get(n)
    f=lambda x: None if x in ('','NA',None) else x
    out.append({"name":n,"postcode":m[0],
     "crime":({"offences":int(c[0]),"population":int(c[1]),"person":int(c[2]),"property":int(c[3]),"area":None} if c else None),
     "prop":({"median":int(p[0]) if f(p[0]) else None,"growth":float(p[1]) if f(p[1]) else None,"yield":float(p[2]) if f(p[2]) else None,"rent":int(p[3]) if f(p[3]) else None} if p else {"median":None,"growth":None,"yield":None,"rent":None}),
     "schools":schools.get(n,[]),
     "mall":None if m[1]=='-' else m[1],"growthArea":m[2]=='1',"flags":flags.get(n,[])})
doc={"region":"wa",
 "crimeSource":{"name":"RedSuburbs (republishes WA Police Force locality crime statistics; population = ABS 2021 Census)",
  "url":"https://redsuburbs.com.au/states/wa/","period":"calendar year 2025","level":"suburb",
  "stateRatePer1000":107.85,"stateRateSource":"RedSuburbs WA page: 285,969 offences in 2025 / 2,651,542 residents (ABS 2021) = 107.85 per 1,000",
  "notes":"Suburb pages at redsuburbs.com.au/suburbs/<slug>/. 'person' = RedSuburbs 'violent crimes'; 'property' = RedSuburbs 'property crimes'; total also includes drug, deception and other offences. Period is calendar 2025, not year to March 2026 (WA Police locality data is only available via a Power BI dashboard, not fetchable; aucrimetracker WA pages load no data). Perth Airport is its own locality, so airport offences are not in Belmont/Redcliffe etc. Rates for fast-growing estates use 2021 population and overstate per-capita crime."},
 "suburbs":out}
json.dump(doc,open(os.path.join(D,'wa.json'),'w'),indent=1)
print(len(out), sum(1 for s in out if s['crime']), sum(1 for s in out if s['prop']['median']), sum(1 for s in out if s['schools']))
