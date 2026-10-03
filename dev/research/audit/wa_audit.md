# Perth (wa) fact-check, 1 October 2026

Full detail with sources: wa_audit.json. Reliable parts first.

RUNWAYS: all 9 runways are right (within 30 m of OpenStreetMap; ends[0] is correct on each).
- New parallel runway 03R/21L: nobody publishes threshold coordinates. Perth Airport's Major Development Plan wording (3,000 m long, 2 km from the main runway, moved 1,030 m south of the existing northern threshold) gives ends within about 10 m of ours. So the "up to 500 m out" worry looks unfounded, but the true accuracy is only that of the published round numbers (about 100-200 m). Perth Airport PDFs are blocked to us (403), so the wording came via search snippets.
- Opening 2028 is confirmed (construction began March 2026). Airservices has not designed the new flight paths yet (draft in early 2027), so future paths are placeholders.

FLIGHT PATHS: the map's plus/minus 40 degree fans are wrong for the main airport. Airservices says about 60% of departures use runway 21; two thirds turn LEFT to the east and about 40% turn RIGHT to the west, and the published SID legs are about 85-90 degrees (track 107 or 280 magnetic after 196), starting at 1,000 ft. Runway 03 departures go north to the Pearce military airspace and then turn left (west) or right (east). Suggested fans: 21 = [-90, 0, 85]; 03 = [-90, 0, 70]; 06 = [-45, 0, 25]; 24 = [-45, 0]. Jets align on a straight final about 10 km out (we draw 26 km). No curfew; voluntary preferred runways only (21/03 departures, 21/24 arrivals).

AIRPORT LAND: boundaries exist in OSM for all three airports with correct ICAO tags. The Perth one stops short of the new-runway site, so the new runway will draw outside the airport land.

DATA CENTRES (most wrong):
- OK: NEXTDC P1 (4 Millrose Dr, Malaga) and P2 (11 Newcastle St / Lord St, East Perth). Exact building points found for both.
- REMOVE: GreenSquareDC Hazelmere. Withdrawn May 2026 after 1,829 objections.
- WRONG: DCA PIER is in Canning Vale (1 Martin Place), not Perth CBD. Equinix PE1 is 3 Tully Rd, East Perth; PE3 is at 37 Lemnos St with PE2 (Shenton Park); our "Perth" geocodes land in the CBD. "DC Two Osborne Park" is now Zettagrid and "Zettagrid Bibra Lake" is probably the same listing (duplicate). "Telstra Malaga" and "Vocus Perth" are unverified or only telco rooms in office buildings.
- MISSING: CDC Maddington (582 Bickley Rd, 200 MW, under construction, first stage early 2027) is the biggest in Perth. CDC Hazelmere (178-196 Bushmead Rd) is lodged, not approved. GreenSquareDC WAi1 (37-39 Abernethy Rd, Belmont, 96 MW, approved 2022) has conflicting status, unresolved.
- No exact building points could be found for PE1, DC Two, Fujitsu (16 Mulgul Rd), CDC sites.

RAIL AND ROADS: all five rail lines are open and correctly dated, but 4 of 5 polylines are off by up to 6 km (Ellenbrook line the worst; also says "Malaga" station, should be Ballajura). Corrected points taken from the real OSM track are in the json. Every station hub is 0.5-2.2 km off (High Wycombe 1.8 km, Ellenbrook 2.2 km, Morley 1.1 km). Corrected coordinates are in the json. Midland new station opened 22 Feb 2026 (matches). Tonkin Highway Extension is under construction, completion late 2028 (ours says unconfirmed). EastLink WA is in planning and unfunded; its alignment cannot be checked.

OTHER: Central Park is 226 m to the roof and about 262 m with its antenna (ours says about 250 m). schoolZoneUrl works (HTTP 200); other links work or are bot-blocked (403).

COULD NOT VERIFY: exact new-runway coordinates; turn distances (SID waypoint positions); official airport boundaries; datacentermap.com (rate-limited, so the missing list may be incomplete); Telstra Malaga; Jandakot movements and Pearce aircraft claims.
