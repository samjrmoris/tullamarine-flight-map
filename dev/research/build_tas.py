import json
DIV = {
 "Clarence": {"offences":3434,"person":559,"property":2699},
 "East Coast": {"offences":845,"person":185,"property":615},
 "Hobart": {"offences":5159,"person":833,"property":4086},
 "Glenorchy": {"offences":3669,"person":642,"property":2819},
 "Bridgewater": {"offences":2607,"person":541,"property":1949},
 "Kingston": {"offences":1615,"person":242,"property":1307},
}
S=[
# name, pc, division, prop(median,growth,yield,rent), schools, mall, growth, flags
("Cambridge","7170","Clarence",(911250,5.16,None,None),[["Cambridge Primary School","p","g",59]],"Cambridge Park retail precinct",False,["Hobart Airport sits in/next to this locality; Cambridge aerodrome also here"]),
("Seven Mile Beach","7170","Clarence",(1305000,18.64,None,None),[],None,False,["Adjoins Hobart Airport runway"]),
("Lauderdale","7021","Clarence",(800000,7.38,4.14,690),[["Lauderdale Primary School","p","g",45]],None,False,[]),
("Rokeby","7019","Clarence",(615000,12.43,4.90,568),[["Emmanuel Christian School","c","i",38],["Bayview Secondary College","s","g",29],["Rokeby Primary School","p","g",22]],None,False,[]),
("Howrah","7018","Clarence",(821000,9.91,4.19,670),[["Howrah Primary School","p","g",52]],"Shoreline Plaza",False,[]),
("Tranmere","7018","Clarence",(1175000,6.82,3.56,740),[],None,False,[]),
("Bellerive","7018","Clarence",(905000,2.67,3.79,670),[["The Cottage School","p","i",71],["Corpus Christi Catholic School","p","c",56],["Bellerive Primary School","p","g",56],["Clarence High School","s","g",51]],None,False,["Blundstone Arena (major events) and Bellerive police divisional HQ"]),
("Rosny","7018","Clarence",(1000000,6.38,3.69,720),[],None,False,["Next to Rosny Park / Eastlands shopping centre"]),
("Lindisfarne","7015","Clarence",(791325,1.65,4.06,650),[["Lindisfarne Primary School","p","g",60],["St Cuthbert's Catholic School","p","c",57]],None,False,[]),
("Geilston Bay","7015","Clarence",(782500,7.93,4.32,675),[["Australian Christian College - Hobart","c","i",55],["Lindisfarne North Primary School","p","g",45]],None,False,[]),
("Rose Bay","7015","Clarence",(945000,-0.87,3.81,650),[["Rose Bay High School","s","g",44]],None,False,[]),
("Montagu Bay","7018","Clarence",(741500,8.66,3.93,610),[["Montagu Bay Primary School","p","g",58]],None,False,[]),
("Mornington","7018","Clarence",(672000,13.13,4.88,580),[["MacKillop Catholic College","s","c",55]],None,False,[]),
("Warrane","7018","Clarence",(610000,10.91,4.94,570),[["Eastside Lutheran College","c","i",51],["Warrane Primary School","p","g",42]],None,False,[]),
("Clarendon Vale","7019","Clarence",(510000,9.68,5.22,540),[["John Paul II Catholic School","p","c",51]],None,False,[]),
("Oakdowns","7019","Clarence",(764500,8.75,4.94,625),[],None,False,[]),
("Risdon Vale","7016","Clarence",(529000,15.75,5.48,550),[["Risdon Vale Primary School","p","g",35]],None,False,["Risdon Prison Complex is in this locality"]),
("Richmond","7025","Clarence",(975000,-4.41,3.70,650),[["Richmond Primary School","p","g",57],["St John's Catholic School","p","c",52]],None,False,["Tourist village"]),
("Acton Park","7170","Clarence",(1330000,11.76,None,None),[],None,False,[]),
("Sorell","7172","East Coast",(730000,8.96,4.54,630),[["Sorell School","c","g",35]],None,True,["Division assignment (East Coast) assumed from Sorell police station/LGA"]),
("Midway Point","7171","East Coast",(709000,15.28,4.65,610),[],None,True,["Population grew 2,859 (2016) to 3,384 (2021) per YIP page","Division assignment (East Coast) assumed from LGA"]),
("Penna","7171","East Coast",(None,None,3.81,None),[],None,False,["Only 3 house sales in 12 months; no median published","Division assignment (East Coast) assumed from LGA"]),
("Hobart","7000","Hobart",(903250,-17.51,3.91,690),[["St Michael's Collegiate School","c","i",61],["St Mary's College","c","c",55]],"Hobart CBD retail (Cat & Fiddle, Centrepoint)",False,["CBD and Salamanca/waterfront nightlife","House median based on few sales (22)"]),
("Sandy Bay","7005","Hobart",(1300000,1.96,3.19,800),[["Princes Street Primary School","p","g",67],["Waimea Heights Primary School","p","g",66],["The Hutchins School","c","i",63],["Fahan School","c","i",61],["Mount Carmel College","c","c",56]],None,False,["University of Tasmania campus and Wrest Point casino"]),
("Battery Point","7004","Hobart",(2070000,47.86,2.97,780),[["Albuera Street Primary School","p","g",74]],None,False,["Adjoins Salamanca nightlife strip","House median based on few sales (18); growth figure volatile"]),
("South Hobart","7004","Hobart",(874000,0.69,3.89,640),[["South Hobart Primary School","p","g",66]],None,False,[]),
("North Hobart","7000","Hobart",(905000,3.72,3.80,620),[["The Friends' School","c","i",60],["Campbell Street Primary School","p","g",55]],None,False,["Elizabeth Street restaurant/bar strip"]),
("West Hobart","7000","Hobart",(1020000,7.37,3.60,678),[["Lansdowne Crescent Primary School","p","g",62],["Goulburn Street Primary School","p","g",59]],None,False,[]),
("New Town","7008","Hobart",(885000,0.00,4.01,675),[["New Town Primary School","p","g",58],["Hobart City High School","s","g",55],["Sacred Heart College","c","c",50]],None,False,[]),
("Lenah Valley","7008","Hobart",(850000,12.96,4.35,675),[["Lenah Valley Primary School","p","g",73],["Immaculate Heart of Mary Catholic School","p","c",57]],None,False,[]),
("Mount Stuart","7000","Hobart",(958500,0.37,4.10,688),[["Mount Stuart Primary School","p","g",65]],None,False,[]),
("Moonah","7009","Glenorchy",(695000,8.26,4.66,622),[["St Therese's Catholic School","p","c",56],["Bowen Road Primary School","p","g",49]],None,False,["Main Road Moonah shopping strip"]),
("West Moonah","7009","Glenorchy",(690000,6.98,4.44,620),[["Hilliard Christian School","c","i",54],["Springfield Gardens Primary School","p","g",40]],None,False,[]),
("Glenorchy","7010","Glenorchy",(647500,11.64,4.84,580),[["Dominic College","c","c",52],["Glenorchy Primary School","p","g",30],["Indie School - Glenorchy","c","i",30],["Cosgrove High School","s","g",24]],"Northgate Shopping Centre",False,["Glenorchy CBD / Elwick racecourse / MONA nearby"]),
("Claremont","7011","Glenorchy",(613500,11.55,4.76,570),[["OneSchool Global Tas","c","i",69],["Holy Rosary Catholic School","p","c",42],["Windermere Primary School","p","g",36],["Austins Ferry Primary School","p","g",33]],"Claremont Plaza",False,[]),
("Berriedale","7011","Glenorchy",(650000,11.49,4.73,558),[],None,False,["MONA (Museum of Old and New Art) is here"]),
("Montrose","7010","Glenorchy",(686500,12.54,4.45,630),[],None,False,[]),
("Rosetta","7010","Glenorchy",(720000,13.83,4.41,620),[["Rosetta Primary School","p","g",52],["Montrose Bay High School","s","g",29]],None,False,[]),
("Bridgewater","7030","Bridgewater",(520000,23.81,5.47,500),[["Northern Christian School","p","i",49],["St Paul's Catholic School","p","c",35],["JRLF - Senior School","s","g",18],["JRLF - East Derwent Primary School","p","g",5]],"Cove Hill Fair",False,[]),
("Brighton","7030","Bridgewater",(658222,9.70,4.57,575),[["Brighton High School","s","g",41],["Brighton Primary School","p","g",41]],None,True,["New residential estates; 2021 census may undercount"]),
("Old Beach","7017","Bridgewater",(710000,-5.27,4.14,645),[],None,True,["New residential estates; 2021 census may undercount"]),
("Gagebrook","7030","Bridgewater",(457000,20.11,5.66,470),[["JRLF - Gagebrook Primary School","p","g",12]],None,False,[]),
("Kingston","7050","Kingston",(820000,9.33,4.28,650),[["Southern Christian College","c","i",63],["Calvin Christian School","c","i",62],["Kingston Primary School","p","g",54],["Kingston High School","s","g",43]],"Channel Court Shopping Centre",True,[]),
("Blackmans Bay","7052","Kingston",(850000,3.34,3.84,650),[["Illawarra Primary School","p","g",64],["Blackmans Bay Primary School","p","g",52]],None,False,[]),
("Taroona","7053","Kingston",(950000,1.09,3.65,765),[["Taroona Primary School","p","g",65],["Taroona High School","s","g",55]],None,False,[]),
]
out={"region":"tas","crimeSource":{
 "name":"Tasmania Police (DPFEM) Corporate Performance Report, June 2026 - offences by police division",
 "url":"https://www.police.tas.gov.au/uploads/Corporate-Performance-Report-June-2026.pdf",
 "period":"financial year to 30 June 2026",
 "level":"district",
 "stateRatePer1000":59.7,
 "stateRateSource":"33,296 total offences statewide (same report, year to 30 June 2026) / 557,571 Tasmanian residents (ABS 2021 Census). Using a current ERP (~575k) would give ~58.",
 "notes":"Tasmania Police publishes no suburb-level offence counts. Finest level is the police DIVISION (13 statewide; Southern District = Hobart, Glenorchy, Kingston, Bridgewater, Clarence, East Coast). Every suburb carries its whole division's totals; 'area' names the division. Suburbs were assigned to divisions by their council (Hobart City->Hobart, Glenorchy City->Glenorchy, Clarence City->Clarence, Brighton->Bridgewater, Kingborough->Kingston, Sorell->East Coast); Tasmania Police does not publish division boundaries, so the Sorell->East Coast mapping in particular is an assumption. Division populations are not published, so population is null (no per-capita rate at suburb level). person = 'Offences Against the Person' table; property = 'Offences Against Property' table; offences = 'Total Offences' table (includes fraud and other categories). Division sums reconcile with district totals within ~15 offences. Figures read from the PDF via an automated extractor; worth a spot-check."},
 "suburbs":[]}
for n,pc,div,p,sch,mall,g,fl in S:
    c=dict(DIV[div]); c={"offences":c["offences"],"population":None,"person":c["person"],"property":c["property"],"area":div+" police division"}
    out["suburbs"].append({"name":n,"postcode":pc,"crime":c,
     "prop":{"median":p[0],"growth":p[1],"yield":p[2],"rent":p[3]},
     "schools":sch,"mall":mall,"growthArea":g,"flags":fl})
json.dump(out,open("/tmp/claude-0/-home-claude-tullamarine-flight-map/a94e428b-9c1e-5182-90c8-c6aeb42cd856/scratchpad/regions/tas.json","w"),indent=1)
s=out["suburbs"]
print(len(s),sum(1 for x in s if x["prop"]["median"]),sum(1 for x in s if x["schools"]))
