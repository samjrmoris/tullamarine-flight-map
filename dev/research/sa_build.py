import json
def dm(deg, minutes, neg):  # degrees + decimal minutes
    v = deg + minutes/60.0
    return round(-v if neg else v, 5)
def pt(latd, latm, lond, lonm):
    return [dm(lond, lonm, False), dm(latd, latm, True)]

sa = {
 "city": "Adelaide", "stateName": "South Australia", "abbr": "SA",
 "mainAirport": {
  "icao": "YPAD", "name": "Adelaide Airport", "short": "Adelaide Airport",
  "lng": 138.533393, "lat": -34.947512,
  "runways": [
   {"refs": ["05","23"], "ends": [pt(34,57.46,138,31.11), pt(34,56.44,138,32.60)],
    "plain": "main runway (south-west to north-east, 3,100 m)", "era": "both", "opens": None},
   {"refs": ["12","30"], "ends": [pt(34,56.47,138,31.32), pt(34,56.96,138,32.22)],
    "plain": "cross runway (north-west to south-east, 1,652 m)", "era": "both", "opens": None}
  ],
  "wideBodies": True,
  "curfew": "11pm-6am (federal curfew; limited exceptions for emergency, some small jets, propeller aircraft and freight)",
  "noiseUrl": "https://www.airservicesaustralia.com/community/environment/aircraft-noise/webtrak/",
  "notes": "Runway end coordinates from SkyVector (0.01-minute precision, ~20 m); runway 05 has a displaced threshold so the 05 touchdown point is a little north-east of the listed end. No new runway is planned; the 2019 Master Plan (approved 2020) is the current official plan. Main runway 05/23 approaches pass over the CBD/inner north-east (Thebarton, Walkerville side) and Gulf St Vincent/Glenelg North; runway 12/30 approaches pass over Plympton, Glandore, Black Forest, Unley Park towards Mitcham."
 },
 "otherAirports": [
  {"icao": "YPPF", "name": "Parafield Airport", "lng": dm(138,37.98,False), "lat": dm(34,47.60,True),
   "kind": "light", "status": "open", "opens": None,
   "runways": [
    {"refs": ["03L","21R"], "ends": [pt(34,48.23,138,37.84), pt(34,47.58,138,38.26)], "plain": "main training runway (1,350 m)", "era": "both", "opens": None},
    {"refs": ["03R","21L"], "ends": [pt(34,48.13,138,38.06), pt(34,47.52,138,38.46)], "plain": "parallel training runway (1,279 m)", "era": "both", "opens": None}
   ],
   "note": "One of Australia's busiest pilot-training airports: small single- and twin-engine planes doing repeated circuits all day, over Parafield Gardens, Mawson Lakes, Salisbury and Para Hills. Not loud like jets, but very frequent; also has shorter 08/26 runways."},
  {"icao": "YPED", "name": "RAAF Base Edinburgh", "lng": dm(138,37.25,False), "lat": dm(34,42.15,True),
   "kind": "military", "status": "open", "opens": None,
   "runways": [
    {"refs": ["18","36"], "ends": [pt(34,41.67,138,37.05), pt(34,43.04,138,36.81)], "plain": "main north-south runway (2,966 m)", "era": "both", "opens": None}
   ],
   "note": "Home of the P-8A Poseidon maritime patrol jets (a Boeing 737 derivative) plus other military aircraft; movements are far fewer than a civil airport but jet noise affects Elizabeth, Edinburgh, Burton and Penfield. Coordinates from SkyVector; listed ends may be thresholds rather than pavement ends (spacing is shorter than the published 2,966 m)."}
 ],
 "future": None,
 "plans": [
  {"kind": "road", "name": "North-South Corridor: River Torrens to Darlington (T2D)",
   "status": "Under construction; whole project opens to traffic by 2031",
   "about": "10.5 km non-stop motorway under/along South Road: 2.2 km northern tunnels (James Congdon Drive to south of Grange Road), 2.7 km open motorway, and 4.5 km southern tunnels (just south of Anzac Highway, Glandore, to Darlington). $15.4 billion, completing the non-stop North-South Corridor from Gawler to Old Noarlunga.",
   "url": "https://dit.sa.gov.au/infrastructure/projects/river-torrens-to-darlington",
   "cert": "approx",
   "line": [[138.5700,-34.9045],[138.5712,-34.9160],[138.5720,-34.9230],[138.5728,-34.9300],[138.5725,-34.9365],[138.5710,-34.9495],[138.5710,-34.9665],[138.5712,-34.9905],[138.5745,-35.0185]]},
  {"kind": "road", "name": "South Eastern Freeway upgrades (Glen Osmond to Mount Barker)",
   "status": "Mount Barker and Verdun interchange upgrades under construction; Crafers-Glen Osmond managed motorway in planning (2026)",
   "about": "A program of interchange upgrades and smart-motorway works on the freeway linking Adelaide with the fast-growing Mount Barker area in the Adelaide Hills.",
   "url": "https://dit.sa.gov.au/infrastructure/projects/south-eastern-freeway-projects",
   "cert": "approx",
   "line": [[138.6480,-34.9610],[138.6755,-34.9785],[138.7050,-34.9990],[138.7240,-35.0035],[138.7700,-35.0080],[138.8050,-35.0290],[138.8500,-35.0610]]},
  {"kind": "rail", "name": "Aldinga rail extension (Seaford line)",
   "status": "Corridor preserved; preliminary planning done, unfunded, 'to be pursued in the 2030s'",
   "about": "Would extend the electrified Seaford line south about 10 km through Seaford Rise to Aldinga, with a station at Quinliven Road and an interchange station with park 'n' ride near Aldinga Beach Road.",
   "url": "https://dit.sa.gov.au/infrastructure/projects/aldinga-rail-extension",
   "cert": "concept",
   "line": [[138.4797,-35.1886],[138.4830,-35.2150],[138.4850,-35.2530],[138.4865,-35.2725]]}
 ],
 "railHubs": [
  [138.5960,-34.9210,"Adelaide Railway Station","City terminus of all suburban lines (approx. location)"],
  [138.4797,-35.1886,"Seaford","Current southern terminus; start of the planned Aldinga extension (approx. location)"],
  [138.5680,-35.0095,"Tonsley","Rail extension opened 2020, next to the southern end of T2D (approx. location)"],
  [138.5870,-34.9510,"Goodwood","Station upgrade in planning (approx. location)"],
  [138.6420,-34.7585,"Salisbury","Gawler line interchange; electrified 2022 (approx. location)"],
  [138.7455,-34.5985,"Gawler Central","Northern terminus of the Gawler line, electrified 2022 (approx. location)"]
 ],
 "dataCentres": [
  ["NEXTDC A1 Adelaide","NEXTDC","125 Frome Street, Adelaide SA","live","Tier IV, ~6 MW"],
  ["NEXTDC A2 Adelaide","NEXTDC","Adelaide SA","plan","Second Adelaide site; exact address not confirmed (suburb-level only)"],
  ["Equinix AE1 (ex-Metronode)","Equinix","274 Hindley Street, Adelaide SA","live",""],
  ["EscapeNet Adelaide","EscapeNet","90 King William Street, Adelaide SA","live",""],
  ["Colocity DC1","Colocity","247 Pulteney Street, Adelaide SA","live",""],
  ["Colocity DC3","Colocity","172 Morphett Street, Adelaide SA","live",""],
  ["DigiCo ADL1 (ex-YourDC Edinburgh)","DigiCo","23 Woomera Avenue, Edinburgh SA","live","~15 MW"],
  ["DigiCo ADL2 (ex-YourDC Hawthorn)","DigiCo","60 Belair Road, Hawthorn SA","live","~1.5 MW"],
  ["Adelaide Data Centre","5G Networks","340 Findon Road, Kidman Park SA","live","~1 MW"],
  ["DCI Adelaide 01 (ADL01)","DCI Data Centers","Kidman Park SA","live","Suburb-level only; street address not confirmed"],
  ["DCI Adelaide 02 (ADL02)","DCI Data Centers","Adelaide SA","live","$70m high-security facility opened 2024 in the western suburbs; exact site not confirmed"],
  ["DCI Adelaide 03 (ADL03)","DCI Data Centers","Adelaide SA","plan","Listed by Baxtel; status and site not confirmed"],
  ["Vocus Adelaide","Vocus","Adelaide SA","live","Address not confirmed (suburb-level only)"]
 ],
 "market": {"text": "Adelaide Cotality home value figures for August/September 2026 could not be retrieved in this pass; see the Cotality Home Value Index report.",
            "url": "https://discover.cotality.com/hubfs/Article-Reports/COTALITY%20HVI%20SEP%202026%20FINAL%20(1).pdf",
            "month": None},
 "tallBuilding": "Westpac House, one of Adelaide's tallest office towers, is about 130 m (approximate)",
 "defaultHome": {"title": "Burnside", "lng": 138.6470, "lat": -34.9405},
 "schoolZoneUrl": "https://www.education.sa.gov.au/parents-and-families/enrol-school-or-preschool/school-zones",
 "view": {"center": [138.600, -34.880], "zoom": 10.3, "bearing": 0},
 "links": [
  ["SkyVector - YPAD Adelaide Airport","https://skyvector.com/airport/YPAD/Adelaide-Airport"],
  ["SkyVector - YPPF Parafield","https://skyvector.com/airport/YPPF/Adelaide-Parafield-Airport"],
  ["SkyVector - YPED Edinburgh","https://skyvector.com/airport/YPED/Edinburgh-Airport"],
  ["OurAirports - YPAD","https://ourairports.com/airports/YPAD/runways.html"],
  ["Adelaide Airport - Aircraft noise & curfew","https://corporate.adelaideairport.com.au/community/aircraft-noise-curfew/"],
  ["Airservices WebTrak","https://www.airservicesaustralia.com/community/environment/aircraft-noise/webtrak/"],
  ["Adelaide Airport Master Plan","https://corporate.adelaideairport.com.au/planning-building/airport-master-plan/"],
  ["DIT - River Torrens to Darlington","https://dit.sa.gov.au/infrastructure/projects/river-torrens-to-darlington"],
  ["T2D project timeline","https://www.t2d.sa.gov.au/project-timeline"],
  ["DIT - Active projects list","https://dit.sa.gov.au/infrastructure/projects"],
  ["DIT - Aldinga rail extension","https://dit.sa.gov.au/infrastructure/projects/aldinga-rail-extension"],
  ["Datacentermap - Adelaide","https://www.datacentermap.com/australia/adelaide/"]
 ]
}
out = "/tmp/claude-0/-home-claude-tullamarine-flight-map/a94e428b-9c1e-5182-90c8-c6aeb42cd856/scratchpad/regions/sa_infra.json"
json.dump({"sa": sa}, open(out, "w"), indent=1)
print(json.dumps(sa["mainAirport"]["runways"]), json.dumps(sa["otherAirports"][0]["runways"][0]["ends"]))
