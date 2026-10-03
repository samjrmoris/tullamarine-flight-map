# Fact-check brief, round 2 (read fully, it is short)

You are fact-checking part of "Flight Path Australia", a public house-hunting map. CHECK and REPORT with sources; do not edit any file except your own output file. Today is 3 October 2026.

Repo: `C:\Users\caris\Projects\tullamarine-flight-map`. Your task message names your city id, the sections to do and your output file.

## Token budget (most important rule)
Every tool call re-reads your whole conversation, so the number of calls and the size of results are what cost money.
- Aim for under 50 tool calls in total; hard stop at 70. If you run out, save what you have and list the rest under `unverified`.
- Never read whole data files. Extract only the fields you need with one `node -e` or `python -c` command, e.g. `node -e "global.window={};require('./regions/nsw.js');console.log(JSON.stringify(window.REGION.dcs))"`.
- Prefer WebSearch (snippets usually hold the fact) over WebFetch. Use WebFetch only when you need an exact figure, and ask it for exact numbers/addresses verbatim in one short answer.
- Do NOT make a tool call just to `sleep`. When you need several pages or API calls from one site (curl, Overpass, Nominatim), put them in ONE script that loops with `time.sleep(8)` between requests and prints a compact summary.
- Do not use schoolrank.com.au, realestate.com.au or datacentermap.com (they block us).
- Runway ends and airport boundaries are ALREADY checked by script (`dev/research/audit/geo_check.json`). Do not redo them.
- Exact coordinates: for a street address, geocode with Nominatim in a batch script (`https://nominatim.openstreetmap.org/search?format=json&q=<address>`, User-Agent header `FlightPathAustralia-audit/1.0`, 1.5 s between requests). Report `[lon,lat]` with 5 decimals and say whether it was a building/house-number match or only a street. Suburb-centre coordinates are not acceptable.

## Rules
- Never invent or estimate a fact. Every value needs a source URL. If you cannot verify something, say "UNVERIFIED" and why.
- Save as you go: write your output file after each section, so nothing is lost if you are stopped. If it already exists, read it and continue.

## Sections (do only the ones named in your task)
**F. Flight paths** (main airport and any jet airport). From official sources (Airservices Australia flight path / noise pages, airport master plan noise chapter, N70 maps, runway mode / noise-sharing pages), for EACH runway end: which way departing jets turn (left/right, about how many degrees, straight), whether arrivals fly a straight final and for about how many km, and noise rules (curfew, preferred runways). The map draws a straight arrival of `arrKm` km (default 26) on a 3 degree slope and departures that go straight about 6 km then turn by each value in `fans` (negative = left). Recommend `fans` per runway end and `arrKm` per airport where evidence supports it.
**D. Data centres.** For every `dcs` entry `[name, operator, address, status, note]`: exists? right operator/name? exact street address? status Oct 2026 (live = operating; plan = under construction/approved/planned; cancelled = remove; not a data centre = remove)? exact `[lon,lat]`? duplicates? Then notable data centres MISSING from the file (operating or publicly planned), with the same fields.
**P. Planned transport and rail hubs.** For each `plans` entry: name, status and opening year (Oct 2026), official URL, whether `cert` is honest, points clearly off (> 500 m) with corrected points where official station coordinates exist. Same for each `railHubs` entry.
**O. Other.** `tallBuilding` (name, height), the `future` wording/date, `schools.zoneSite` / links (do they load?), airport `nearNote` texts (curfew, wide-body, military claims). For a future runway: status, opening year and placement versus the official plan.

## Output
One JSON file at the path in your task, validated with `python -m json.tool`:
```
{"id":"<id>","checked":"2026-10-03","sections":"F,D,P,O",
 "flightPaths":[{"airport":"YSSY","runwayEnd":"16R","departs":"...","arrives":"...","fans_now":[-40,0,40],"fans_recommended":[...]|null,"arrKm_recommended":null,"sources":["..."],"confidence":"high|medium|low"}],
 "dataCentres":[{"name":"...","operator":"...","address":"...","status":"live|plan|cancelled|not a data centre","lnglat":[lon,lat]|null,"coord_method":"...","sources":["..."],"verdict":"ok|fix|remove","changes":"what differs from ours"}],
 "dataCentresMissing":[{"name":"...","operator":"...","address":"...","status":"live|plan","lnglat":[lon,lat]|null,"coord_method":"...","sources":["..."],"note":""}],
 "plans":[{"name":"...","verdict":"ok|fix","status_now":"...","fix_points":[[lon,lat],...]|null,"cert":"route|approx|concept","sources":["..."],"note":""}],
 "railHubs":[{"name":"...","verdict":"ok|fix","lnglat":[lon,lat],"sources":["..."],"note":""}],
 "other":[{"field":"...","verdict":"ok|fix","correct":"...","sources":["..."]}],
 "unverified":["..."]}
```
Final reply: 5 lines max: counts of ok / fix / remove per section, and the biggest problems.
