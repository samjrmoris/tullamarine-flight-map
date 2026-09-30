D = []
def S(name, pc, crime, prop, schools, mall=None, growth=False, flags=None):
    c = None if crime is None else dict(zip(["offences","population","person","property","area"], list(crime)+[None]*(5-len(crime))))
    p = None if prop is None else dict(zip(["median","growth","yield","rent"], prop))
    D.append({"name":name,"postcode":pc,"crime":c,"prop":p,"schools":schools,"mall":mall,"growthArea":growth,"flags":flags or []})

S("Penrith","2750",(6612,17966,1069,2151),(1120000,15.46,3.12,630),
  [["Penrith High School","s","g",98],["St Nicholas of Myra Primary School","p","c",59],["Penrith Public School","p","g",48],["Penrith South Public School","p","g",47],["Wadangali Public School","p","g",31]],
  mall="Westfield Penrith", flags=["Regional CBD, Westfield Penrith and train station inflate counts relative to residents"])
S("Kingswood","2747",(1967,10633,548,662),(1125000,20.97,3.08,585),
  [["Kingswood Public School","p","g",64],["St Dominic's College","s","c",50],["St Joseph's Primary School","p","c",50],["Kingswood South Public School","p","g",45],["Kingswood High School","s","g",40]],
  flags=["Nepean Hospital and Western Sydney University Penrith campus nearby"])
S("Jamisontown","2750",(563,5321,126,328),(1140500,13.26,3.34,680),[])
S("Glenmore Park","2745",(604,25021,240,277),(1260000,5.88,3.31,790),
  [["Caroline Chisholm College","s","c",58],["Nangamay Public School","p","g",51],["Bethany Catholic Primary School","p","c",51],["Surveyors Creek Public School","p","g",51],["Glenmore Park Public School","p","g",43],["Glenmore Park High School","s","g",42]])
S("St Marys","2760",(3418,13256,559,1059),(1200000,16.67,2.88,575),
  [["Our Lady of The Rosary Primary School","p","c",53],["St Marys South Public School","p","g",34],["Oxley Park Public School","p","g",34],["St Marys Public School","p","g",32],["Colyton High School","s","g",31]],
  flags=["Town centre and train interchange; future Metro link to Western Sydney Airport starts here"])
S("Erskine Park","2759",(192,6486,75,88),(1328000,16.49,3.06,725),
  [["James Erskine Public School","p","g",45],["Erskine Park High School","s","g",42]])
S("St Clair","2759",(616,19942,225,292),(1210000,11.01,3.22,700),
  [["Holy Spirit Primary School","p","c",60],["St Clair Public School","p","g",54],["Clairgate Public School","p","g",51],["Blackwell Public School","p","g",48],["Banks Public School","p","g",46],["St Clair High School","s","g",42]])
S("Cambridge Park","2747",(395,7054,177,112),(1100000,17.65,3.33,610),
  [["Cambridge Gardens Public School","p","g",46],["Cambridge Park High School","s","g",37],["Cambridge Park Public School","p","g",34]])
S("Emu Plains","2750",(496,8126,136,251),(1180000,12.38,3.26,750),
  [["Leonay Public School","p","g",61],["Our Lady of The Way Primary School","p","c",55],["Penola Catholic College Emu Plains","s","c",51],["Emu Plains Public School","p","g",47],["Emu Heights Public School","p","g",47],["Nepean Creative and Performing Arts High School","s","g",46]],
  flags=["Contains Emu Plains Correctional Centre"])
S("Werrington","2747",(625,5328,187,267),(1125000,9.22,3.37,750),
  [["Wollemi College","c","i",71],["Werrington County Public School","p","g",41],["Werrington Public School","p","g",39]],
  flags=["Western Sydney University Werrington campus"])
S("Blacktown","2148",(7811,50961,1494,2066),(1171000,8.93,3.06,650),
  [["Blacktown West Public School","p","g",63],["Tyndale Christian School","c","i",63],["St Patrick's Primary School","p","c",60],["Nagle College","s","c",59],["Blacktown Boys High School","s","g",58],["Lynwood Park Public School","p","g",57],["Blacktown South Public School","p","g",57],["Blacktown Girls High School","s","g",56],["Blacktown North Public School","p","g",56],["Marayong South Public School","p","g",49],["Walters Road Public School","p","g",47],["Evans High School","s","g",47],["Patrician Brothers' College Blacktown","s","c",45],["Shelley Public School","p","g",43],["Mitchell High School","s","g",42],["Marayong Public School","p","g",37]],
  mall="Westfield Mount Druitt".replace("Mount Druitt","Blacktown"), flags=["Blacktown CBD, hospital and major rail interchange"])
S("Mount Druitt","2770",(5855,16986,736,1261),(1072500,7.25,3.03,628),
  [["Australian Islamic College of Sydney","c","i",65],["Colyton Public School","p","g",56],["Bethel Christian School","c","i",51],["St Bishoy Coptic Orthodox College","c","i",45],["Mount Druitt Public School","p","g",42],["Chifley College Mount Druitt Campus","s","g",30]],
  mall="Westfield Mount Druitt", flags=["Town centre, hospital and train interchange"])
S("Rooty Hill","2766",(827,16176,279,341),(1107500,10.75,3.22,650),
  [["St Aidan's Primary School","p","c",62],["St Agnes Catholic High School","s","c",57],["Rooty Hill Public School","p","g",44],["Rooty Hill High School","s","g",41]])
S("Plumpton","2761",(529,10070,140,327),(1075000,10.82,3.35,650),
  [["Western Grammar School","c","i",62],["Good Shepherd Primary School","p","c",58],["Plumpton High School","s","g",45],["Plumpton Public School","p","g",40]])
S("Marsden Park","2765",(612,14610,189,346),(1242000,6.70,3.51,850),
  [["St Luke's Catholic College (Secondary)","s","c",59],["St Luke's Catholic College (Primary)","p","c",57],["St Luke's Arrunga","c","c",57],["Marsden Park Anglican College","c","i",54],["Northbourne Public School","p","g",50],["Marsden Park Public School","p","g",48]],
  growth=True, flags=["Fast-growing new estates; 2021 population undercounts residents","Sydney Business Park / IKEA-Costco retail precinct"])
S("Schofields","2762",(608,15213,233,276),(1310000,4.38,3.19,830),
  [["St John Paul II Catholic College","s","c",62],["Galungara Public School","p","g",61],["St Joseph's Primary School","p","c",57],["Schofields Public School","p","g",54]],
  growth=True, flags=["Growth-area estates; 2021 population undercounts residents"])
S("Riverstone","2765",(1011,8627,244,220),(1250000,12.87,3.14,710),
  [["St John's Primary School","p","c",71],["South Creek School","c","g",64],["Norwest Christian College","c","i",60],["Australian Christian College - Marsden Park","c","i",59],["Ngarra Christian College","c","i",56],["Riverstone Public School","p","g",43],["Riverstone High School","s","g",37]],
  growth=True, flags=["Total inflated by 396 'against justice procedures' offences (breaches etc.)","Growth-area estates; 2021 population undercounts residents"])
S("Glenwood","2768",(324,15829,126,138),(1715000,2.54,2.69,870),
  [["Caddies Creek Public School","p","g",70],["Parklea Public School","p","g",64],["Holy Cross Primary School","p","c",62],["Glenwood High School","s","g",60]])
S("Kellyville Ridge","2155",(177,10890,72,83),(1632500,6.01,2.71,898),"RETRY")
S("Quakers Hill","2763",(853,27893,345,297),(1380000,9.52,2.98,700),
  [["Quakers Hill Public School","p","g",73],["Hambledon Public School","p","g",60],["Barnier Public School","p","g",60],["Mary Immaculate Primary School","p","c",59],["Quakers Hill High School","s","g",46]])
S("Stanhope Gardens","2768",(215,9349,66,111),(1605000,5.07,2.84,860),
  [["St John XXIII Catholic College (Secondary)","s","c",58],["St John XXIII Catholic College (Primary)","p","c",55]],
  flags=["Stanhope Village shopping centre"])
S("Doonside","2767",(1062,13614,390,317),(1120800,12.02,3.05,632),
  [["St John Vianney's Primary School","p","c",72],["Mountain View Adventist College","c","i",50],["Doonside High School","s","g",44],["Crawford Public School","p","g",40],["Doonside Public School","p","g",30]])
S("Liverpool","2170",(14840,31078,1171,2074),(1297500,15.59,3.02,650),
  [["All Saints Catholic College","c","c",55],["Marsden Road Public School","p","g",53],["Al Amanah College","c","i",53],["Liverpool Girls High School","s","g",39],["Liverpool Public School","p","g",39],["Liverpool Boys High School","s","g",37],["Gulyangarri Public School","p","g",36],["Liverpool West Public School","p","g",33]],
  mall="Westfield Liverpool", flags=["Regional CBD with courts, police station, Liverpool Hospital and rail interchange"])
S("Casula","2170",(962,16584,278,452),(1296500,12.74,3.25,790),
  [["Casula Public School","p","g",45],["Casula High School","s","g",33]])
S("Prestons","2170",(585,15694,187,290),(1220000,5.90,3.48,800),
  [["William Carey Christian School","c","i",66],["St Catherine of Siena Catholic Primary School","p","c",61],["Amity College","c","i",54],["Dalmeny Public School","p","g",50],["Prestons Public School","p","g",44]])
S("Edmondson Park","2174",(626,12080,150,333),(1339000,5.89,3.31,850),
  [["St Francis Catholic College","c","c",66],["Edmondson Park Public School","p","g",55]],
  growth=True, flags=["Fast-growing new estates; 2021 population undercounts residents","Ed.Square town centre at the station"])
S("Hoxton Park","2171",(149,4572,66,69),(1181000,19.81,3.43,720),
  [["Good Shepherd Catholic Primary School","p","c",61],["Hoxton Park Public School","p","g",44]])
S("Green Valley","2168",(684,12919,146,157),(1195500,3.87,3.29,700),
  [["Green Valley Public School","p","g",52],["Minarah College","c","i",50],["James Busby High School","s","g",38],["Busby West Public School","p","g",35]],
  flags=["Total inflated by 326 'against justice procedures' offences (breaches etc.)"])
S("Hinchinbrook","2168",(300,11521,134,100),(1163750,10.83,3.27,700),
  [["Good Samaritan Catholic College","s","c",56],["Hinchinbrook Public School","p","g",46],["Hoxton Park High School","s","g",41]])
S("Cecil Hills","2171",(145,6906,59,56),(1451000,-2.52,3.01,850),
  [["Cecil Hills Public School","p","g",56],["Cecil Hills High School","s","g",41]])
S("Bonnyrigg","2177",(454,9785,119,227),(1259000,11.42,3.26,700),
  [["Our Lady of Mt Carmel Catholic Primary School Mount Pritchard","p","c",72],["Bonnyrigg High School","s","g",56],["Bonnyrigg Public School","p","g",53]],
  flags=["Bonnyrigg Plaza shopping centre"])
S("Fairfield","2165",(2313,18596,440,511),(1370000,14.64,3.13,700),
  [["Our Lady of the Rosary Catholic Primary School","p","c",57],["Patrician Brothers' College Fairfield","s","c",55],["Fairvale Public School","p","g",42],["Fairfield Heights Public School","p","g",42],["Fairfield High School","s","g",38],["Fairfield Public School","p","g",30]],
  mall="Neeta City / Fairfield Forum", flags=["Town centre and rail interchange"])
S("Cabramatta","2166",(3128,21142,296,640),(1427000,4.35,2.82,650),
  [["Sacred Heart Catholic Primary School Cabramatta","p","c",67],["Cabramatta Public School","p","g",65],["Harrington Street Public School","p","g",64],["Lansvale East Public School","p","g",62],["Cabramatta High School","s","g",61],["Cabramatta West Public School","p","g",53]],
  flags=["Busy town centre and rail station; total far exceeds person+property counts"])
S("Horsley Park","2175",(115,1790,32,53),None,
  [["St Narsai Assyrian Christian College","s","i",63],["Marion Catholic Primary School","p","c",56],["Horsley Park Public School","p","g",39]],
  flags=["Semi-rural acreage; small population makes per-capita rates volatile"])
S("Kemps Creek","2178",(229,2121,57,141),(3950000,None,1.53,750),
  [["Trinity Catholic Primary School","p","c",59],["Christadelphian Heritage College Sydney","c","i",58],["Mamre Anglican School","c","i",54],["Emmaus Catholic College","s","c",51],["Kemps Creek Public School","p","g",35]],
  flags=["Semi-rural acreage next to Western Sydney Airport / Aerotropolis; small population makes per-capita rates volatile; house median from only ~18 sales"])
S("Austral","2179",(647,6847,250,301),(1110000,27.59,3.48,800),
  [["Arrahman College","p","i",71],["Al-Faisal College - Liverpool","c","i",67],["St Anthony of Padua Catholic College","c","c",50],["Unity Grammar College","c","i",50],["Austral Public School","p","g",49]],
  growth=True, flags=["Rezoned acreage turning into new estates; 2021 population undercounts residents"])
S("Leppington","2179",(652,9423,159,306),(1100000,6.49,3.18,820),
  [["Leppington Anglican College","c","i",58],["Leppington Public School","p","g",41]],
  growth=True, flags=["South West Growth Area estates; 2021 population undercounts residents"])
S("Middleton Grange","2171",(135,7043,69,49),(1252500,8.91,3.47,800),
  [["Thomas Hassall Anglican College","c","i",56],["Middleton Grange Public School","p","g",49]])
S("Bringelly","2556",(139,2433,45,67),(3600000,17.47,1.49,840),
  [["Bringelly Public School","p","g",35]],
  flags=["Semi-rural acreage bordering Western Sydney Airport / Aerotropolis; small population makes per-capita rates volatile"])
S("Rossmore","2557",(160,2241,73,71),None,
  [["Bellfield College","c","i",51],["Rossmore Public School","p","g",27]],
  flags=["Semi-rural acreage near Western Sydney Airport; small population makes per-capita rates volatile"])
S("Luddenham","2745",(125,1927,51,59),(2970000,26.92,2.25,750),
  [["Holy Family Primary School","p","c",53],["Luddenham Public School","p","g",42]],
  flags=["Semi-rural locality adjoining the Western Sydney International Airport site; small population makes per-capita rates volatile"])
S("Oran Park","2570",(615,17624,247,229),(1200000,10.60,3.27,780),
  [["Oran Park Anglican College","c","i",60],["St Benedict's Catholic College","s","c",56],["St Justin's Catholic Primary School","p","c",55],["Barramurra Public School","p","g",53],["Oran Park Public School","p","g",50],["Oran Park High School","s","g",46]],
  growth=True, flags=["Fast-growing new estates; 2021 population undercounts residents","Oran Park Podium town centre"])
S("Gregory Hills","2557",(440,9142,144,213),(1106250,8.99,3.45,750),
  [["St Gregory's College Campbelltown","c","c",51],["Gregory Hills Public School","p","g",46]],
  growth=True, flags=["Fast-growing new estates; 2021 population undercounts residents","Gregory Hills Town Centre and business park"])
S("Harrington Park","2567",(228,13332,79,109),(1565000,10.99,2.86,840),
  [["Harrington Park Public School","p","g",56]])
S("Narellan","2567",(738,3358,111,278),(1100000,10.00,3.26,680),
  [["Elizabeth Macarthur High School","s","g",51],["Narellan Public School","p","g",47]],
  mall="Narellan Town Centre", flags=["Small resident population vs a regional shopping centre inflates the per-capita rate"])
S("Camden","2570",(259,3378,93,92),(1200000,14.29,3.03,650),
  [["Mount Hunter Public School","p","g",54],["St Paul's Catholic Primary School","p","c",53],["Camden South Public School","p","g",52],["Camden Public School","p","g",51],["Mawarra Public School","p","g",45],["Camden High School","s","g",41],["Cawdor Public School","p","g",38]],
  flags=["Historic town centre; small resident population"])
S("Spring Farm","2570",(218,9868,73,99),(1140000,9.88,3.47,750),
  [["Spring Farm Public School","p","g",43]], growth=True, flags=["Newer estates; 2021 population may undercount residents"])
S("Mount Annan","2567",(345,11784,135,134),(1230000,13.89,3.44,750),
  [["Mount Annan Christian College","c","i",55],["Mount Annan Public School","p","g",46],["Mount Annan High School","s","g",44]],
  flags=["Mount Annan Marketplace shopping centre"])
S("Campbelltown","2560",(6610,16577,799,1459),None,
  [["St Peter's Anglican Grammar","p","i",69],["St Patrick's College Campbelltown","s","c",68],["St Thomas More Catholic Primary School","p","c",60],["St John The Evangelist Catholic Primary School","p","c",55],["Kentlyn Public School","p","g",53],["Briar Road Public School","p","g",52],["Campbelltown East Public School","p","g",47],["Campbelltown North Public School","p","g",43],["Campbelltown Public School","p","g",38],["Woodland Road Public School","p","g",37],["Campbelltown Performing Arts High School","s","g",36],["Airds High School","s","g",29]],
  mall="Macarthur Square", flags=["Regional CBD, hospital and rail interchange; total includes 2,745 transport regulatory and 1,012 justice-procedure offences"])
S("Ingleburn","2565",(1696,15264,350,582),(1102500,15.45,3.32,650),
  [["Holy Family Catholic Primary School","p","c",57],["Ingleburn High School","s","g",49],["Ingleburn Public School","p","g",43],["Sackville Street Public School","p","g",39]],
  flags=["Total includes 423 transport regulatory offences (fare evasion at the station)"])
S("Minto","2566",(1254,13940,311,494),(1055000,11.35,3.52,650),
  [["Al-Faisal College - Campbelltown","c","i",70],["Zahra Grammar School","p","i",53],["Sarah Redfern Public School","p","g",47],["Minto Public School","p","g",44],["Campbellfield Public School","p","g",42],["Sarah Redfern High School","s","g",40],["The Grange Public School","p","g",37]])
S("Leumeah","2560",(805,9992,224,237),(988500,9.83,3.42,620),
  [["Leumeah Public School","p","g",61],["Leumeah High School","s","g",44]])
S("Parramatta","2150",(9720,30211,1159,3193),(1610000,-14.72,2.40,750),
  [["Our Lady of Mercy College Parramatta","s","c",84],["Parramatta High School","s","g",72],["Parramatta East Public School","p","g",62],["St Patrick's Primary School","p","c",61],["Bayanami Public School","p","g",59],["Macarthur Girls High School","s","g",59],["Parramatta Public School","p","g",56],["Arthur Phillip High School","s","g",49],["Parramatta West Public School","p","g",45]],
  mall="Westfield Parramatta", flags=["Sydney's second CBD with nightlife, courts and major rail interchange; mostly apartments so house figures rest on few sales"])
S("Merrylands","2160",(3064,32472,605,1022),(1425000,5.56,2.90,750),
  [["Cerdon College","s","c",61],["St Margaret Mary's Primary School","p","c",60],["Merrylands East Public School","p","g",51],["Sherwood Grange Public School","p","g",48],["Merrylands Public School","p","g",40],["Hilltop Road Public School","p","g",39],["Merrylands High School","s","g",35]],
  mall="Stockland Merrylands")
S("Guildford","2161",(1539,24091,438,624),(1373500,11.67,3.00,750),
  [["St Patrick's Primary School","p","c",51],["Granville South Public School","p","g",44],["Guildford Public School","p","g",39],["Old Guildford Public School","p","g",27],["Granville South Creative and Performing Arts High School","s","g",21]])
S("Wentworthville","2145",(862,15098,213,431),(1527000,4.23,2.57,700),
  [["Darcy Road Public School","p","g",64],["Our Lady of Mount Carmel Primary School","p","c",57],["Wentworthville Public School","p","g",55],["Pendle Hill Public School","p","g",50],["Pendle Hill High School","s","g",39],["Toongabbie East Public School","p","g",15]])
S("Westmead","2145",(1169,16555,321,507),(2000000,12.68,2.30,710),
  [["Mother Teresa Primary School","p","c",70],["Catherine McAuley Westmead","s","c",63],["Parramatta Marist High School","s","c",62],["Westmead Public School","p","g",56],["Sacred Heart Primary School","p","c",51],["Westmead Christian Grammar School","p","i",45]],
  flags=["Westmead hospital precinct (Westmead and Children's hospitals); mostly apartments so house figures rest on few sales"])
S("Greystanes","2145",(637,23511,259,244),(1527500,14.63,2.76,800),
  [["Greystanes Public School","p","g",70],["Widemere Public School","p","g",60],["Our Lady Queen of Peace Primary School","p","c",59],["Beresford Road Public School","p","g",58],["St Paul's Catholic College","s","c",57],["Greystanes High School","s","g",52],["Ringrose Public School","p","g",39],["Holroyd High School","s","g",38]])
S("Pemulwuy","2145",(228,5532,74,111),(1357500,2.14,3.50,970),[])
S("Wetherill Park","2164",(645,6412,146,419),(1465000,12.91,2.89,750),
  [["Smithfield West Public School","p","g",47],["William Stimson Public School","p","g",45]],
  mall="Stockland Wetherill Park", flags=["Large industrial area adds business-premises property crime"])
