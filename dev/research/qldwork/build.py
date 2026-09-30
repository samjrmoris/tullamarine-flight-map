import json
malls={"Chermside":"Westfield Chermside","Carindale":"Westfield Carindale","North Lakes":"Westfield North Lakes","Indooroopilly":"Westfield Indooroopilly","Strathpine":"Westfield Strathpine","Capalaba":"Capalaba Park Shopping Centre","Sunnybank":"Sunnybank Plaza / Market Square","Mitchelton":"Brookside Shopping Centre","Cleveland":"Stockland Cleveland"}
growth={"North Lakes","Mango Hill","Springfield Lakes"}
flags={
"Ascot":["Eagle Farm and Doomben racecourses"],
"Hamilton":["Racecourse Rd dining strip and Portside Wharf / cruise terminal"],
"Boondall":["Brisbane Entertainment Centre (events inflate crime counts)"],
"Virginia":["Large industrial area with small resident population inflates the per-capita rate"],
"Tingalpa":["Includes industrial land"],
"Hemmant":["Mostly industrial / port-side land"],
"New Farm":["Adjoins Fortitude Valley nightlife precinct"],
"Newstead":["Adjoins Fortitude Valley nightlife precinct","Apartment-dominated: no house rent/yield data"],
"Teneriffe":["Adjoins Fortitude Valley nightlife precinct"],
"Kangaroo Point":["Inner-city, adjoins CBD"],
"Albion":["Small population with commercial/industrial land inflates the per-capita rate"],
"Acacia Ridge":["Large industrial and rail freight area inflates the per-capita rate","Near Archerfield Airport"],
"Coopers Plains":["Includes industrial land","Near Archerfield Airport"],
"Salisbury":["Includes industrial land","Near Archerfield Airport"],
"Springwood":["Logan City Council (not Brisbane City)"],
"Redcliffe":["Moreton Bay Council; foreshore/entertainment strip"],
"Chermside":["Major regional shopping centre and Prince Charles Hospital precinct inflate crime counts"],
"Nudgee":["No rated schools listed on schoolrank for this suburb (Nudgee College is listed under Boondall)"],
"Northgate":["No rated schools listed on schoolrank for this suburb (Northgate State School is listed under Nundah)"],
}
out=[]
for line in open("data.txt"):
    if line.startswith("#") or not line.strip(): continue
    parts=line.strip().split("|")
    name,pc,cr,pr=parts[:4]
    sch=parts[4:]
    o,pe,prp,rate=[int(x) for x in cr.split(",")]
    pop=round(o/rate*100000)
    m,g,y,r=pr.split(",")
    f=lambda v,t:None if v=="null" else t(v)
    schools=[]
    for s in sch:
        if s in("SCHOOLS404","NOSCHOOLS"): continue
        n,l,se,sc=s.split(";")
        schools.append([n,l,se,int(sc)])
    out.append({"name":name,"postcode":pc,
      "crime":{"offences":o,"population":pop,"person":pe,"property":prp,"area":None},
      "prop":{"median":f(m,int),"growth":f(g,float),"yield":f(y,float),"rent":f(r,int)},
      "schools":schools,"mall":malls.get(name),"growthArea":name in growth,"flags":flags.get(name,[])})
doc={"region":"qld",
 "crimeSource":{"name":"AU Crime Tracker (aucrimetracker.com), republishing Queensland Police Service suburb-level reported offences",
  "url":"https://www.aucrimetracker.com/qld/<suburb-slug>/",
  "period":"12 months to August 2026 (site label '2025 - 2026 (Aug)')",
  "level":"suburb",
  "stateRatePer1000":110.0,
  "stateRateSource":"Queensland Government Statistician's Office, Crime report, Queensland, 2024-25 (620,898 recorded offences, 10,998.1 per 100,000 persons; FY 2024-25): https://www.qgso.qld.gov.au/issues/7856/crime-report-qld-2024-25.pdf",
  "notes":"QLD pages on aucrimetracker do not render the population number; population here is back-calculated as offences / published rate per 100,000 (2021 census basis) and rounded, so may be off by 1-2 people (checked: Ascot gives 6,531, matching the 2021 census). Duplicate QLD place names use a '-brisbane' slug (ascot-brisbane, albion-brisbane, red-hill-brisbane, the-gap-brisbane). 'person' = site's 'offences against persons' (homicide, assault, sexual offences, robbery, other); 'property' = site's 'property crime' (arson, theft, damage, etc.). The QLD 'person' share looks low next to the official state split (about 6-10% of offences vs 14% statewide), so person counts may exclude some categories. The state rate is for a different period (FY 2024-25) because the site's own implied QLD total (1,107,708) is far above the official 620,898 and was not used. All 73 suburbs are in Brisbane City except North Lakes, Mango Hill, Redcliffe, Kallangur, Strathpine and Albany Creek (Moreton Bay), Springfield Lakes (Ipswich), Springwood (Logan), and Capalaba and Cleveland (Redland)."},
 "suburbs":out}
json.dump(doc,open("../qld.json","w"),indent=1,ensure_ascii=False)
print(len(out),sum(1 for s in out if s["prop"]["median"]),sum(1 for s in out if s["schools"]))
