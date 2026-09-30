# Refactor spec: make the Melbourne map a multi-state engine

Repo: /home/claude/tullamarine-flight-map (static GitHub Pages site). Main file: index.html (~157 KB, one inline <script> wrapped in an IIFE). Do NOT commit or push. Do not change look or behaviour for Victoria: after the refactor, loading ?state=vic must behave exactly as today.

Goal: all Melbourne/Victoria-specific data and wording move out of index.html into regions/vic.js. index.html becomes a generic engine driven by a global REGION object. Other states (nsw, qld, wa, sa, tas, act, nt) will later get their own regions/<id>.js with the SAME schema; write regions/_schema.md documenting every field (type, meaning, example) so someone can author those files without reading the engine.

## Loading
- Region id: URL ?state=<id> (lowercase), else localStorage 'tfpm:region', else: if localStorage has 'tfpm:ref' (existing Melbourne user) use 'vic', else show a full-screen, clean "Which state are you buying in?" picker (8 buttons: VIC Melbourne, NSW Sydney, QLD Brisbane, WA Perth, SA Adelaide, TAS Hobart, ACT Canberra, NT Darwin). Match the app's existing visual style (fonts, colours, radius).
- Load regions/<id>.js by injecting a <script> tag; that file sets window.REGION = {...}. When loaded, start the app (turn the current IIFE into a function startApp() called after REGION is ready, after the map libraries check). Remember the choice in localStorage 'tfpm:region'.
- A list of available regions lives in index.html: const REGIONS=[{id:'vic',abbr:'VIC',city:'Melbourne'},...]. If a region file fails to load, show a toast and the picker.
- In the panel header, add a compact state switcher (a <select> or segmented chip showing e.g. "VIC · Melbourne ▾"). Changing it sets localStorage and reloads with ?state=<id>. Also update history URL to include ?state=<id>.

## Caches
All localStorage keys that hold region-specific data (subs, apt, dc geo, dc osm, schools osm, school geo, ref, watch, chkgeo) must be namespaced by region: key = 'tfpm:' + REGION.cachePrefix + rest. For vic, cachePrefix is '' so existing keys ('tfpm:v2:subs', 'tfpm:v3:apt', 'tfpm:ref', ...) are unchanged. Others use e.g. 'nsw:'. Make cacheSet resilient: on quota error, delete big cache keys belonging to OTHER regions (keys matching tfpm:<otherprefix>: and the vic ones if current isn't vic, excluding tfpm:region, tfpm:gkey) and retry once.
listings.json (Houses I've checked) stays global; entries have an address; only show pins/list entries whose "state" field (optional, default "vic") equals REGION.id, or whose address ends with the state's abbr + postcode (e.g. " VIC 3037").

## REGION schema (implement exactly these names; vic.js must fill all of them from what's in index.html today)
id, abbr, stateName ('Victoria'), stateAdj ('Victorian'), city ('Melbourne'), cachePrefix
title (page <title> and h1), lede (HTML)
origin: [lon, lat]  -> replaces LAT0/LON0 (vic: [144.8433,-37.6733])
view: {center, zoom, pitch, bearing} (initial + "tilt" button); focusView: {label:'West side', center, zoom, pitch, bearing} (the vWest button; hide the button if null); topView: {center, zoom}
bbox: [south, west, north, east] used for all Overpass queries (suburbs, schools, data centres). vic: suburbs used (-37.96,144.55,-37.52,145.0); data centres used a slightly bigger box, keep a separate optional dcBbox.
grid: {x0, n1, cols, rows} for the noise grid in km relative to origin (vic: -40, 15, 178, 172; step stays 0.35).
geocode: {viewbox:'144.3,-37.3,145.3,-38.2', suffix:', Victoria'}
airports: array. Each: {icao, name, label (map label, upper-case applied by engine), short (plain name used in sentences e.g. 'Tullamarine'), lng, lat, main:true|false, toggle:true|false (gets its own flight-path checkbox; generate the checkboxes from this list instead of the hard-coded aML/aEN/aAV), ac: null|'narrow'|'wide'|'turbo' (null = follow the plane-size selector), arrKm, depKm (null for main = the fan model), fans (main airport: 3 departure tracks at -40/0/+40), noModel:true (draw the red boundary only, no flight paths), era:'both'|'future' (whole airport opens in future), runways:[{key, refs:['16','34'], futureRefs:['16L','34R'] optional, ends:[[lon,lat],[lon,lat]] (ends[0] is the threshold of refs[0]), era:'both'|'future', plain:'main runway'}], nearNote: {km:5, text:'About {d} km from Essendon Fields Airport. ...'} optional (replaces the hard-coded Point Cook / Essendon notes in the spot card)}.
  - Runway geometry: use ends from config. After the Overpass airport fetch, for each config runway find an OSM aeroway=runway way whose midpoint is within 1.5 km of the config midpoint and whose bearing is within 12 degrees (either direction); if found use the OSM end points (oriented to match ends[0]/ends[1]). The Overpass query must fetch aerodromes by the configured ICAO codes and runways within ~4 km of each airport (around:), generically.
  - Melbourne's third runway: compute its coordinates from today's defaultRunways()+deriveNew() math and hardcode them in vic.js as a runway with era:'future', refs ['16R','34L'] (key 'new'). The magenta 'rw3' fill layer should draw every runway with era 'future' (all airports), not just key 'new'.
  - P.apt for main airport paths = its icao (was hard-coded 'YMML'); state.apts built from airports with toggle.
  - RWNAME is replaced by runway.plain. P.plain() wording stays the same for vic.
flows: derive automatically from main-airport runways: for each runway direction (travel bearing of planes = runway bearing when using refs[0] i.e. from ends[0] toward ends[1], and the reverse), map to the nearest of N/E/S/W (or NE etc. if needed to keep them distinct), producing the 'flow' radio buttons and FLOWB and the mode text (' · north wind'). For vic this must reproduce the current buttons: All, North(34), South(16), West(27), East(09).
future: null or {label:'After 2031 (3 runways)', short:'After 2031', mode:'After 2031, three runways', legend:'New runway paths (2031)'}. If null: hide the era radio group and the future legend item, and in the cards show only the "Today" verdict (no second row); list sorting/wording that says 'after 2031' uses today instead and wording drops the 'after 2031'.
tallBuilding: 'a Eureka Tower is about 300 m' (used in heightWords)
defaultRef: {lng, lat, title}
focusFilter: optional {maxLon: 144.905} (replaces s.west). If absent, every suburb that has crime or property data is 'in focus'. listTitle: 'Best suburbs in the west'; wording '<n> western suburbs' -> use REGION.listNoun ('western suburbs' for vic; e.g. 'suburbs' elsewhere).
crime: {data: CRIME object (name-> [offences, population, person, property] plus optional 5th element: area name when the figure is council/district-wide rather than suburb), stateRate: 86.8, typicalPerson: 10.5, typicalPersonWord:'a typical western suburb', period:'year to June 2026', flags:{ravenhall:'Ravenhall has several prisons...'}, malls:{...}, growth:[...]} ; when a 5th element (area) exists, add flag 'These figures cover the whole <area>, not just this suburb.'
prop: {data: PROP object, period:'12 months to June 2026'}
market: {html: the 'Market right now' panel text, cardFlag: 'Since June, Melbourne values overall fell about 3.9%...'}
schools: {data: SCH array, zoneSite:'findmyschool.vic.gov.au'}
plans: PLANS array (unchanged format), railHubs: RAIL_HUBS (4th element optional note), railHubNote: 'part of the Airport Rail upgrade (stage 1 due 2030)'
dcs: DCS array (unchanged format), dcSource: 'Data Center Map'
fallbackSubs: FALLBACK_SUBS
text: {aptLandSub:'Melbourne, Essendon Fields, Avalon and Point Cook airfields', railPlanSub:'Airport Rail, Suburban Rail Loop West', roadPlanSub (if the markup has one), notes: HTML of the "About / sources" notes block (all the <p class=note> paragraphs and the sources <ul>) moved verbatim from index.html}
Anything else Melbourne-specific you find (search for Melbourne, Victoria, Tullamarine, Essendon, Avalon, Avondale, Eureka, 2031, west, 144., -37.) must move into REGION too. After the refactor, `grep -n -i "melbourne\|tullamarine\|victoria\|essendon\|avalon\|2031\|144\.\|-37\." index.html` should only hit the REGIONS list / picker.

## Testing (required)
- Extract the script and run `node --check`.
- There is a node mock harness at /tmp/claude-0/-home-claude/a94e428b-9c1e-5182-90c8-c6aeb42cd856/scratchpad/harness2.js (it evals m.js = the extracted inline script). Adapt a copy (harness3.js in the same folder) so it first evals regions/vic.js (set global.window = global so window.REGION works) and then calls startApp(); it must run to completion printing layers, subs, apt ring, mesh, etc. with no errors, like the original.
- Also make a quick fake region (e.g. a tiny test region with one main airport with 2 runways, future:null, no focusFilter, empty data) and run the harness with it to prove the engine is region-agnostic and the future:null path works.
- Playwright + Chromium is available (executablePath '/opt/pw-browsers/chromium'; require playwright via NODE_PATH=$(npm root -g)). The CDN is blocked in this sandbox so the map itself won't render; still screenshot the picker overlay and the panel to check the layout (block CDN requests or stub maplibregl/deck if needed).
Report: what you changed, the schema file path, test results, and anything you were unsure about.
