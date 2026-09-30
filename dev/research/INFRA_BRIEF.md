# Airports & infrastructure brief (read fully)

You are gathering data for a house-hunting map that shows plane flight paths and noise, train lines and highways (existing and planned), and data centres. A Melbourne version exists. Accuracy matters: never invent coordinates or figures; mark anything approximate as approximate. Tools: WebFetch/WebSearch (the shell has no internet). Today is 29 Sep 2026.

For EACH city in your task, produce the following.

## A. Main airport
- ICAO, full name, short name, lat/lng of the airport reference point.
- Every runway: its two designators and the lat/lng of BOTH ends (thresholds). ourairports.com runway pages give these, e.g. https://ourairports.com/airports/YSSY/runways.html (or /airports/YSSY/). Give ends as [lon, lat] (longitude first!) with 4+ decimals. "ends[0]" must be the threshold of "refs[0]" (i.e. where planes landing on refs[0] touch down).
- A short plain name per runway ("main north-south runway", "parallel runway", "cross runway").
- Planned/under-construction runways (e.g. Perth's new parallel runway): designators if known, approximate end coordinates (from official master plan / major development plan; describe how you placed it), status and expected opening year. era = "future".
- Main aircraft mix: does it get regular wide-body jets (A330/787/777/A380)? Night curfew? Link to the airport's official noise / flight path tool.

## B. Other airfields in or near the metro area
Secondary airports, general-aviation fields and RAAF bases within ~50 km that affect homes (e.g. Sydney: Western Sydney International (Nancy-Bird Walton), Bankstown, Camden, RAAF Richmond; Brisbane: Archerfield, RAAF Amberley; Perth: Jandakot, RAAF Pearce; Adelaide: Parafield, RAAF Edinburgh; Hobart: Cambridge; Canberra: none major; Darwin: note Darwin Airport is shared with RAAF Base Darwin (fighter jets)).
For each: ICAO, name, lat/lng, runways as above (only the main 1–2 runways), what flies there ("jets" like A320/737, "turboprop", "light" training aircraft/helicopters, "military" fighters), whether it is open now or opening later (exact status as of Sep 2026: e.g. is Western Sydney International open yet? when do passenger flights start?), and a 1–2 sentence plain-English note for home buyers.

## C. "Future" scenario
What single change in the next ~10 years most changes plane noise for this city (new airport/runway opening, flight path changes)? Give a short label for a toggle, e.g. "After Western Sydney Airport opens (late 2026)", a 3-word short form, and a 2-sentence explanation. If nothing significant, say null.

## D. Planned transport (big, relevant, official)
Planned/under-construction train/metro lines and major motorways in the metro area. For each: kind "rail" or "road", name, status (plain words with year), 1–2 sentence "about", official URL, and a polyline of [lon,lat] points (5–15 points) along the route. cert = "route" if the alignment is public and you traced it from official maps/station locations, "approx" if only the general corridor is known, "concept" if just end points. Station coordinates are the best anchors. Up to ~8 per city, focus on the biggest ones. Also list up to 8 key existing or new rail stations that are part of these upgrades as railHubs [lon, lat, "Name", "short note"].

## E. Data centres
Operating and planned data centres in the metro area (datacentermap.com city page, operator sites, 2025–2026 planning news). Each: [name, operator, street address with suburb, "live" or "plan", note or ""]. Aim for the full list (Sydney will have 40+). Addresses must be geocodable; if the exact site isn't public, give the suburb and say so in the note.

## F. Market right now
Latest Cotality (formerly CoreLogic) home value index results for this capital city: monthly change for the latest month (Aug or Sep 2026), 3-month and 12-month change, and position vs previous peak if reported. Source URL. Write one plain sentence like: "Sydney home values rose 0.4% in August 2026, 1.1% over three months and 3.2% over the year (Cotality)."

## G. Misc
- A well-known tall building in that city and its height, for plain-language height comparisons (e.g. "Sydney Tower Eye is about 300 m").
- A sensible default "home" to compare against: a middle-ring family suburb near but not under the main flight paths, with lat/lng.
- The state's school zone finder URL.
- Suggested map overview view: center [lon,lat], zoom, bearing so both the main airport and the western/family suburbs show.

## Output
Write valid JSON to the path in your task: an object keyed by region id, e.g. {"nsw": {...}}, with keys: city, stateName, abbr, mainAirport{icao,name,short,lng,lat,runways:[{refs:["16R","34L"],ends:[[lon,lat],[lon,lat]],plain,era:"both"|"future",opens:null}],wideBodies:true,curfew,noiseUrl,notes}, otherAirports[{icao,name,lng,lat,kind,status:"open"|"future",opens,runways[...],note}], future{label,short,explain}|null, plans[...], railHubs[...], dataCentres[...], market{text,url,month}, tallBuilding, defaultHome{title,lng,lat}, schoolZoneUrl, view{center,zoom,bearing}, links[[title,url]] (the key official sources you used). Validate with python3 -m json.tool. Final reply: a short summary and any uncertainties; the data is in the file.
