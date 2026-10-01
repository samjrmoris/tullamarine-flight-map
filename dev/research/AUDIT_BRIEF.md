# Fact-check brief (read fully)

You are auditing one city of "Flight Path Australia", a public house-hunting map. The owner wants every fact on the map checked against primary sources. Your job is to CHECK and REPORT corrections with sources. Do not edit any file except your two output files. Today is 1 October 2026.

Repo: `C:\Users\caris\Projects\tullamarine-flight-map`. Your inputs:
- The research file for your city in `dev/research/` (named in your task) and the generated `regions/<id>.js` (what the map actually shows; `window.REGION`, fields documented in `regions/_schema.md`).

## Rules
- Never invent or estimate a fact. Every value you report needs a source URL. If you cannot verify something, say "UNVERIFIED" and why.
- Pace web requests: at most one request per website every 8 seconds (use `sleep 8` in Bash between fetches to the same site). On HTTP 429 or "rate limited", wait 5 minutes (`sleep 300`) and move on to other items, then come back. Other agents share this connection.
- Do NOT use schoolrank.com.au (it blocks us). Do NOT use realestate.com.au.
- WebFetch summarises pages with a small model: always ask it for exact numbers/addresses/coordinates verbatim.
- Overpass (OpenStreetMap) queries are allowed from Bash with curl: POST to https://overpass-api.de/api/interpreter (fallback https://maps.mail.ru/osm/tools/overpass/api/interpreter), one query at a time.

## What to check

### 1. Airports and runways
For the main airport and every other airfield in the file:
- ICAO, name, open/future status as of Oct 2026.
- Every runway: designators and BOTH threshold coordinates. Compare with ourairports.com (`https://ourairports.com/airports/<ICAO>/runways.html`) and, where possible, OpenStreetMap runway ways (Overpass `way["aeroway"="runway"](around:4000,lat,lng);out geom;`). Report the distance in metres between our ends and the source. Flag anything over 150 m. `ends[0]` must be the threshold of `refs[0]`.
- Future runways: status, opening year and placement from the official master plan / major development plan. Say how precise the placement can be.

### 2. Flight paths (how the map draws them)
The map draws, for each runway end: a straight-in arrival along the extended centreline for 26 km on a 3 degree slope, and departures that go straight for about 6 km then turn by `fans` degrees (default -40, 0, +40; negative = left) or go straight for `depKm` km. For the MAIN airport (and any jet airport), find from official sources (Airservices Australia flight path / noise pages, the airport's master plan noise chapter or N70/N60 maps, noise-sharing / runway mode pages, published departure procedure descriptions) for EACH runway end:
- which way departing jets actually turn (left/right, roughly how many degrees, or straight ahead) and roughly where;
- whether arrivals fly a straight final for the last ~15-25 km or use curved/offset approaches;
- any noise rules that change usage (curfew, preferred runways, over-water ops).
Recommend replacement `fans` per runway end where the evidence supports it, with sources. If the published information is too vague, say so.

### 3. Airport land
The map draws airport land from OpenStreetMap at runtime (aerodrome way/relation with the ICAO tag). Check with Overpass that an aerodrome boundary with the right `icao` tag exists for each airport, roughly what area it covers, and whether it plausibly matches the official airport boundary (master plan / airport lease plan). Flag missing or clearly wrong boundaries.

### 4. Data centres (most important; the owner noticed problems here)
For EVERY data centre entry `[name, operator, address, status, note]`:
- Does it exist? Correct operator and name? Exact street address?
- Status as of Oct 2026: operating, under construction, approved/planned, or cancelled. Map "live" = operating, "plan" = under construction or approved/planned. Cancelled = remove.
- EXACT coordinates of the building/site: from the OSM building or data-centre polygon (Overpass `nwr["telecom"="data_center"]` or `building="data_center"` near the address), the operator's own site, or a precisely geocoded street number. Report `[lon, lat]` with 5 decimals and the method used. Suburb-centre coordinates are NOT acceptable; if the exact site is not public, say so.
- Duplicates (same building listed twice) and entries that are not data centres.
Then list notable data centres in the metro area MISSING from the file (operating or publicly planned/approved), with the same fields and sources (datacentermap.com city page, operator sites, state planning portals, recent news).

### 5. Planned transport and rail hubs
For each plan: correct name, current status and opening year (Oct 2026), official URL. Check the polyline against official station locations / alignment maps: report points that are clearly off (> 500 m from the official alignment) and give corrected points where official station coordinates exist. Check that `cert` ("route", "approx", "concept") is honest. Same for each rail hub (location, name, note).

### 6. Other facts shown
`tallBuilding` (name and height), the "future" toggle wording and date, `schoolZoneUrl` (does it load?), each URL in `links`, airport notes (curfew, wide-body jets, military types). Report anything wrong.

## Output (two files)
1. `dev/research/audit/<id>_audit.json`:
```
{"id": "<id>", "checked": "2026-10-01",
 "runways": [{"airport":"YSSY","refs":["16R","34L"],"ours":[[lon,lat],[lon,lat]],"source":[[lon,lat],[lon,lat]],"diff_m":[12,30],"source_url":"...","verdict":"ok|fix","note":""}],
 "flightPaths": [{"airport":"YSSY","runwayEnd":"16R","departs":"...","arrives":"...","fans_now":[-40,0,40],"fans_recommended":[...]|null,"sources":["..."],"confidence":"high|medium|low"}],
 "airportLand": [{"airport":"YSSY","osm":"relation 123 / way 456 / MISSING","verdict":"ok|fix","note":""}],
 "dataCentres": [{"name":"...","operator":"...","address":"...","status":"live|plan|cancelled|not a data centre","lnglat":[lon,lat]|null,"coord_method":"...","sources":["..."],"verdict":"ok|fix|remove","changes":"what differs from ours"}],
 "dataCentresMissing": [{"name":"...","operator":"...","address":"...","status":"live|plan","lnglat":[lon,lat]|null,"coord_method":"...","sources":["..."],"note":""}],
 "plans": [{"name":"...","verdict":"ok|fix","status_now":"...","fix_points":[[lon,lat],...]|null,"cert":"route|approx|concept","sources":["..."],"note":""}],
 "railHubs": [{"name":"...","verdict":"ok|fix","lnglat":[lon,lat],"sources":["..."],"note":""}],
 "other": [{"field":"tallBuilding","verdict":"ok|fix","correct":"...","sources":["..."]}],
 "unverified": ["anything you could not check and why"]}
```
Validate it with `python -m json.tool`.
2. `dev/research/audit/<id>_audit.md`: a plain-English summary (under 40 lines) of what was wrong, what is right, and what could not be verified.

Final reply: 5 lines max: counts of ok / fix / remove per section, and the biggest problems.
