# Region file schema

Each state lives in `regions/<id>.js`. The file sets one global, `window.REGION = {...}`, and `index.html` (the engine) reads everything region-specific from it. `regions/vic.js` is the complete worked example; copy it and change the values.

How a region is chosen and loaded:

1. `?state=<id>` in the URL (lowercase `id`), else the `tfpm:region` value saved in the browser, else the "Which state are you buying in?" picker. A returning user who only has the old `tfpm:ref` key goes straight to `vic`.
2. The engine adds `<script src="regions/<id>.js">`. After it loads, the engine checks that `window.REGION.id` equals the id it asked for, then starts. If the file is missing or the id doesn't match, the user sees a toast and the picker.
3. The list of states in the picker and in the panel switcher is `REGIONS` near the top of the script in `index.html`. Every `id` there should get a `regions/<id>.js`.

Conventions:

- Coordinates are `[lon, lat]` (GeoJSON order) unless a field says otherwise. `bbox` is the exception: it uses Overpass order.
- Local "km" coordinates are `x` km east and `n` km north of `origin`.
- Strings are plain text unless the field says HTML. HTML fields are inserted as-is, so escape `&` and `<` yourself.
- Keys in `crime.data`, `prop.data`, `crime.flags`, `crime.malls` and `crime.growth` are suburb names in lowercase, matching the OpenStreetMap suburb (admin_level 10) names.
- A section you have no data for can be an empty object or array. The engine shows "No data" instead.

---

## Identity

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `id` | string | Lowercase id. Must match the file name and the `REGIONS` entry. | `'vic'` |
| `abbr` | string | State abbreviation as it appears at the end of addresses (`" VIC 3037"`). It filters and strips addresses in "Houses I've checked". | `'VIC'` |
| `stateName` | string | Full state name. | `'Victoria'` |
| `stateAdj` | string | Adjective used in sentences ("The Victorian average is about 87"). | `'Victorian'` |
| `city` | string | Capital city name. | `'Melbourne'` |
| `cachePrefix` | string | Namespace for this region's browser caches: key = `'tfpm:' + cachePrefix + rest`. Must be `''` for vic, so existing caches keep working. Use `'<id>:'` for every other state (e.g. `'nsw:'`). If you leave it out, the engine uses `'<id>:'`. The quota clean-up relies on this pattern. | `''` |
| `title` | string | Page `<title>` and the panel `<h1>`. | `'Tullamarine Flight Path Map'` |
| `lede` | HTML string | Intro paragraph under the title. | `"See how much plane noise any street in Melbourne's west gets…"` |

## Map framing

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `origin` | `[lon, lat]` | Centre of the local km grid. Use the main airport. "km from the airport" distances are measured from here. | `[144.8433,-37.6733]` |
| `view` | `{center:[lon,lat], zoom, pitch, bearing}` | Starting camera. The "3D view" button returns here. | `{center:[144.815,-37.715],zoom:11.3,pitch:60,bearing:-25}` |
| `focusView` | `{label, center, zoom, pitch, bearing}` or `null` | Extra camera button. `label` is the button text. `null` hides the button. | `{label:'West side',center:[144.80,-37.72],zoom:11.9,pitch:64,bearing:60}` |
| `topView` | `{center, zoom}` | The "From above" button. Pitch and bearing are always 0. Defaults to `view`. | `{center:[144.80,-37.72],zoom:10.8}` |
| `bbox` | `[south, west, north, east]` | Area used for the Overpass suburb and school queries. | `[-37.96,144.55,-37.52,145.0]` |
| `dcBbox` | `[south, west, north, east]`, optional | Area used for the OpenStreetMap data-centre query. Defaults to `bbox`. | `[-37.98,144.5,-37.45,145.05]` |
| `grid` | `{x0, n1, cols, rows, step?}` | Noise-shading grid in km from `origin`: left edge `x0`, top edge `n1`, cell count, cell size `step` (default 0.35 km). It should cover every flight path. Cost grows with `cols × rows`. | `{x0:-40,n1:15,cols:178,rows:172}` |
| `geocode` | `{viewbox, suffix}` | Nominatim search settings. `viewbox` is `'west,north,east,south'` and results stay inside it. `suffix` is added to every query. | `{viewbox:'144.3,-37.3,145.3,-38.2',suffix:', Victoria'}` |

## Airports (`airports`: array)

List the main airport first. The order sets the airport-filter chips and the map labels.

| Field | Type | Meaning | vic example (Tullamarine) |
|---|---|---|---|
| `icao` | string | ICAO code. The Overpass query looks up the airport boundary (`aeroway=aerodrome`) by this code. | `'YMML'` |
| `name` | string | Full name, used in sentences ("planes landing at Essendon Fields Airport"). | `'Melbourne Airport'` |
| `label` | string | Map label. The engine makes it upper case. | `'Melbourne Airport'` |
| `short` | string | Everyday short name (e.g. "Tullamarine"). `{main}` in a `nearNote` becomes the main airport's `short`. | `'Tullamarine'` |
| `chip` | string, optional | Text on this airport's flight-path checkbox. Defaults to `name`. | `'Melbourne (Tullamarine)'` |
| `lng`, `lat` | numbers | Airport reference point. Used for the runway search radius, the label (until OpenStreetMap loads) and `nearNote` distances. | `144.8433`, `-37.6733` |
| `main` | boolean | Exactly one airport is `true`. The main airport gets the detailed model: departure fans, height markers, wind-direction buttons, "the main runway" wording. | `true` |
| `toggle` | boolean | `true` gives the airport its own checkbox under Flight paths. Airports without one are always included. | `true` |
| `ac` | `null`, `'narrow'`, `'wide'` or `'turbo'` | Noise curve. `null` follows the plane-size selector (All jets, Everyday jet or Big jet). Use `'turbo'` for turboprop and business traffic. | `null` (Essendon: `'turbo'`) |
| `arrKm` | number | Length of the straight-in approach drawn on a 3° slope, in km. Default 26. | `26` (Essendon: `14`) |
| `depKm` | number or `null` | Non-main airports: one straight departure this many km long. `null`: use the departure fan (`fans`). | `null` (Avalon: `22`) |
| `fans` | array of degrees | Main airport: departure tracks that turn this many degrees after takeoff. | `[-40,0,40]` |
| `noModel` | boolean, optional | `true`: draw the boundary and label only. No flight paths and no noise (for example a military or light-aircraft field). | Point Cook: `true` |
| `era` | `'both'` or `'future'` | `'future'`: the whole airport only exists in the future scenario (all its runways become future runways). | `'both'` |
| `fallbackRing` | array of `[x, n]` km, optional | Rough boundary drawn if OpenStreetMap has not loaded. Only used for the main airport. | `[[-2.9,3.4],[0.0,3.6],…]` |
| `runways` | array | See below. Can be `[]` for `noModel` airports. | |
| `nearNote` | `{km, text}`, optional | A spot within `km` of this airport gets `text` as a note on its card. `{d}` in the text becomes the distance, e.g. "4.2". | `{km:5,text:'About {d} km from Essendon Fields Airport. …'}` |

### Runways (`airports[].runways`)

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `key` | string | Unique id. | `'main'` |
| `refs` | `[string, string]` | Runway numbers. `refs[0]` is the runway you land on at `ends[0]`, travelling towards `ends[1]`. For 16/34 with `ends[0]` at the north end, that's `['16','34']`. | `['16','34']` |
| `futureRefs` | `[string, string]`, optional | Numbers after renaming, e.g. when a parallel runway opens. Only used to match OpenStreetMap. | `['16L','34R']` |
| `ends` | `[[lon,lat],[lon,lat]]` | Threshold positions. `ends[0]` is the threshold of `refs[0]`. | `[[144.829396,-37.652715],[144.836604,-37.685285]]` |
| `era` | `'both'` or `'future'` | `'future'`: the runway only exists in the future scenario. It is drawn in magenta, and its paths are purple. | `'both'` (third runway: `'future'`) |
| `plain` | string | Name in sentences: "planes landing on the **main runway**". Only the main airport uses it. Other airports use the airport `name`. | `'main runway'` |

**OpenStreetMap refinement.** After the airport query loads, the engine replaces a runway's configured `ends` with the OpenStreetMap geometry when a runway way (within about 4 km of the airport) matches. A way matches if its `ref` is the same pair as `refs` or `futureRefs` (e.g. `16/34`). Failing that, it matches if its midpoint is within 1.5 km of the configured midpoint and its heading is within 12°. Each way is used at most once, with the closest match first. The OpenStreetMap ends are re-ordered to match `ends[0]` and `ends[1]`. The configured `ends` are therefore the fallback when Overpass is down, so keep them reasonably accurate.

**Wind-direction buttons.** These are derived from the main airport's runways. Each runway direction gets a button, labelled with the compass point planes travel towards (North, South, East or West; eight points if four would clash). The button value is the runway number with any L/R/C removed (`'34'`). Its heading for the ±45° filter is that number × 10. The legend adds " · north wind" and so on. Parallel runways share a button.

## Future scenario

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `future` | object or `null` | `null`: no future scenario. The Today/Future switch and the purple legend line are hidden, cards show only "Today", and rankings use today's noise. | see below |
| `future.label` | string | Text on the era switch. | `'After 2031 (3 runways)'` |
| `future.short` | string | Card heading and sentence opener ("After 2031, 4 of 9 …"). It is also lower-cased mid-sentence ("Quiet skies after 2031"). | `'After 2031'` |
| `future.mode` | string | Legend title while the future era is on. | `'After 2031, three runways'` |
| `future.legend` | string | Legend entry for future flight paths. | `'New runway paths (2031)'` |

## Wording and the ranked list

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `tallBuilding` | string | Height comparison added to "low, about 450 m up (…)". Use `''` to leave it out. | `'a Eureka Tower is about 300 m'` |
| `defaultRef` | `{lng, lat, title}` | The spot everything is compared with until the user picks their own. | `{lng:144.862,lat:-37.761,title:'Avondale Heights'}` |
| `focusFilter` | `{maxLon}`, optional | Only suburbs whose label point is west of `maxLon` appear in the ranked list. If you leave it out, every suburb is listed (the list still needs crime or property data for most sorts). | `{maxLon:144.905}` |
| `listTitle` | string | Heading of the ranked list. | `'Best suburbs in the west'` |
| `listNoun` | string | Noun in the list summaries ("4 of 9 **western suburbs** …"). | `'western suburbs'` |

## Crime (`crime`)

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `data` | object: name → `[offences, population, crimesAgainstPeople, propertyCrimes, area?]` | Yearly counts and population. Rates are per 1,000 residents. A suburb under 3,000 people is flagged and left out of the crime-based rankings. Use the optional 5th element when the figure is council- or district-wide rather than for the suburb. The card then says "These figures cover the whole <area>, not just this suburb." | `"keilor":[275,5906,44,139]` or `"x":[900,20000,120,500,'City of Example']` |
| `stateRate` | number | State average offences per 1,000 people. "All crime" is compared with this. | `86.8` |
| `typicalPerson` | number | Typical crimes against people per 1,000 in the focus area. | `10.5` |
| `typicalPersonWord` | string | Words for that comparison: "where **a typical western suburb** has 11". | `'a typical western suburb'` |
| `period` | string | Period the data covers. For reference and for your notes text. | `'year to June 2026'` |
| `flags` | object: name → text | Extra notes for particular suburbs. | `{ravenhall:'Ravenhall has several prisons, …'}` |
| `malls` | object: name → shopping centre | Adds "Includes <centre>, where shoplifting … push the numbers up." | `{'taylors lakes':'Watergardens shopping centre'}` |
| `growth` | array of names | Fast-growing estates. Adds a note that the real rate is probably lower. | `['tarneit','truganina',…]` |

## Property, market and schools

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `prop.data` | object: name → `[medianHouse$, growth%, grossYield%, weeklyRent$]` | Suburb house figures over `prop.period`. | `"keilor":[1210000,11.01,3.35,650]` |
| `prop.period` | string | Used in "over the <period>". | `'12 months to June 2026'` |
| `prop.ramps` | object, optional | Overrides the colour cut-offs for the property layer, e.g. `{price:{cuts:[900000,1200000,1600000,2200000],words:['Under $900k','$900k–1.2m','$1.2m–1.6m','$1.6m–2.2m','Over $2.2m']}}`. Keys: `dollar`, `growth`, `price`, `yield`. Leave it out to keep the Melbourne defaults. | (not set) |
| `market` | `{html, cardFlag}` or `null` | `html`: the "Market right now" box under Houses I've checked (HTML, include the bold lead-in). `cardFlag`: a note on every suburb's property card. `null` hides both. | `{html:'<b>Market right now:</b> Melbourne home values fell …',cardFlag:'Since June, Melbourne values …'}` |
| `schools.data` | array of `[name, suburb, level, sector, score]` | `level`: `p` primary, `s` secondary, `c` combined P–9/12. `sector`: `g` government, `c` Catholic, `i` independent. `score` is out of 100 (about 50 is average). Schools are placed on the map by matching OpenStreetMap names, or by geocoding. | `["Keilor Primary School","Keilor","p","g",54]` |
| `schools.zoneSite` | string | Website named in school pop-ups ("Check zones at …"). `''` leaves out the line. | `'findmyschool.vic.gov.au'` |

## Transport, data centres and fallbacks

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `plans` | array of `{kind:'rail'|'road', cert:'route'|'approx'|'concept', name, status, about, url, coords:[[lon,lat],…]}` | Planned rail lines and roads. `cert` sets the line style: solid-dash for a known route, a shaded band for an approximate one, a sparse dotted line for a concept. | Airport Rail, SRL West, Outer Metropolitan Ring |
| `railHubs` | array of `[lon, lat, stationName, note?]` | Suburbs within 3 km get "About 1.2 km from <station> station, <note or railHubNote>." | `[144.8327,-37.7885,'Sunshine']` |
| `railHubNote` | string | Default note for `railHubs`. | `'part of the Airport Rail upgrade (stage 1 due 2030)'` |
| `dcs` | array of `[name, operator, streetAddress, 'live'|'plan', note?]` | Data centres, geocoded from the address (falling back to the suburb after the last comma). OpenStreetMap data centres in `dcBbox` are added too. | `['NEXTDC M2','NEXTDC','75 Sharps Road, Tullamarine','live']` |
| `dcSource` | string | Source line in operating data-centre pop-ups. | `'Data Center Map'` |
| `dcPlanSource` | string, optional | Source line for planned ones. Defaults to `dcSource`. | `'2026 planning news / Data Center Map'` |
| `fallbackSubs` | array of `[name, lat, lon]` | Suburb centres used as 1.1 km circles if the OpenStreetMap boundaries fail. **Note the `lat, lon` order** (kept from the original data). | `['Sunbury',-37.577,144.726]` |

## Panel text (`text`)

| Field | Type | Meaning | vic example |
|---|---|---|---|
| `text.aptLandSub` | string | Small print under "Airport land". | `'Melbourne, Essendon Fields, Avalon and Point Cook airfields'` |
| `text.railPlanSub` | string | Small print under "Planned train lines". | `'Airport Rail, Suburban Rail Loop West'` |
| `text.roadPlanSub` | string | Small print under "Planned roads". | `'Outer Ring Road land, roads being built'` |
| `text.addrPlaceholder` | string, optional | Placeholder in the "enter the details yourself" address box. | `'e.g. 12 Smith St, Taylors Hill'` |
| `text.notes` | HTML string | The whole "How this is worked out" block: `<p class="note">` paragraphs and the sources `<ul class="links">`. | see `vic.js` |

## Caches and shared data

- Region caches in the browser: `tfpm:<cachePrefix>v2:subs`, `v3:apt`, `v1:dcgeo`, `v1:dcosm`, `v1:schosm`, `v1:schgeo`, `v1:chkgeo`, plus the user's `ref` and `watch`. When storage is full, the engine deletes other regions' `…v<n>:…` caches (never `ref`, `watch`, `tfpm:region` or `tfpm:gkey`) and tries once more.
- `listings.json` (Houses I've checked) is shared by all states. An entry shows in a region when its optional `"state"` field equals the region `id`. When `"state"` is missing, it shows when the address ends in `" <ABBR> <postcode>"` for that state. Entries with neither count as `vic`.

## Checklist for a new state

1. Add or check the entry in `REGIONS` in `index.html`.
2. Copy `vic.js` to `<id>.js`. Set `id`, `abbr` and `cachePrefix: '<id>:'`.
3. Set `origin` and the three views. Size `grid` so it covers the flight paths.
4. Add the airports with runway `ends` and `refs` (check `ends[0]` is the threshold of `refs[0]`).
5. Fill in the data sections, or leave them empty (`{}` or `[]`).
6. Load `index.html?state=<id>` and check the wind buttons, a spot card and the ranked list.
