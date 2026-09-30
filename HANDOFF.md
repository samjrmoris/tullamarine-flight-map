# HANDOFF: Flight Path Map, multi-state expansion

Written 30 Sep 2026 so work can continue in Claude Code. Read this whole file first.

## 1. What this project is

Sam (Melbourne, buying a family home with his wife, currently lives in Avondale Heights) built an interactive 3D house-hunting map. It started as a Melbourne-only map and is being expanded to every Australian capital city.

- **Live site (still the Melbourne-only version):** https://samjrmoris.github.io/tullamarine-flight-map/
- **Repo:** https://github.com/samjrmoris/tullamarine-flight-map (GitHub Pages serves `main`, repo root)
- **Work-in-progress branch:** `multi-state`. It holds everything in this file. `main` has NOT been touched by the multi-state work.

### What the map does (Melbourne, all live on main)

- **Flight paths and planes:**
  - A 3D map (MapLibre GL 4.7.1 plus deck.gl 9.0.38, loaded from unpkg).
  - Melbourne Airport land is outlined in red, with runways, today's flight paths and the third runway (2031).
  - 3D planes are animated, and there is a "Fly a landing" follow camera.
  - Essendon Fields, Avalon and RAAF Point Cook are shown, and each airport's paths have their own toggle.
- **Plane noise:**
  - The model uses NATS Lmax curves and SAE AIR 1751 lateral attenuation.
  - Wide-body jets are calibrated to Melbourne Airport's fact sheet.
  - Results are shown in plain English only: Very loud / Loud / Noticeable / Faint / Quiet. No dB or feet.
  - Everything is compared with a reference home (default Avondale Heights), which the user can change.
- **Other layers:**
  - Trains and highways, existing and planned.
  - Data centres, existing and planned, as 3D blocks.
  - Crime by suburb, per 1,000 residents.
  - Property: median price, 12-month growth, $ change, rent yield.
  - Schools (kinder to uni) with a minimum-score slider.
  - Suburb labels show the numbers when a layer is on.
- **Suburb ranking list:** family, quietest, lowest crime, schools, growth, value and biggest drops.
- **"Houses I've checked":** Sam pastes a Domain or realestate.com.au link to Claude, Claude researches it (the `house-check` skill), and adds an entry to `listings.json`. The map then shows a coloured pin (below / fair / above) and a card with an asking vs fair range bar.
- **Controls:** rotate and spin buttons, a clean-map toggle, and everything can be switched on or off.
- **Default load state:**
  - Street map, Today view, plane size "All jets".
  - On: flight paths, planes, airport land, trains, highways, data centres, 3D buildings, hills (terrain).
  - Off: noise shading, planned trains, planned roads, crime, property, schools, suburb names.

### Sam's standing preferences

- Avoid em dashes in all text, both UI copy and messages.
- Use plain language, not jargon, and keep the look real-map, not childish.
- Base feedback on evidence, stay neutral, and say what is and isn't supported by data.
- Never invent numbers. If data is missing, show "No data" and say why.
- Commit with author `Sam <samjrmoris@users.noreply.github.com>`.
- Don't scrape realestate.com.au (blocked, and against its terms). Use Domain instead.
- Never put API keys in the public page. The Google 3D key stays in the viewer's browser localStorage (`tfpm:gkey`).
- Sam's latest instruction: release all states **at once**, not one by one. Cover the **capital city metro area** of each state, not whole states.

## 2. Where things are up to

### Done (on branch `multi-state`, not yet on main)

1. **The engine is refactored and tested.**
   - `index.html` is now region-agnostic.
   - All Melbourne data moved to `regions/vic.js`, which sets `window.REGION`.
   - Loading order: `?state=<id>` in the URL, then localStorage `tfpm:region`, then existing Melbourne users (who have `tfpm:ref`) default to vic, otherwise a full-screen "Which state are you buying in?" picker appears.
   - There is a state switcher in the panel header.
   - Cache keys are namespaced per region; vic keys are unchanged, so existing users keep their cache. When storage is full, other regions' caches are purged.
   - Flight-path toggles and wind buttons are generated from the region config.
   - `future:null` hides the Today / After-2031 switch.
   - `listings.json` entries are filtered by state (optional `state` field, or the address ending, e.g. " VIC 3037").
   - A test comparing old against new Victoria output matched line for line: noise at 330 points, the grid, every list sort, and the cards.
2. **`regions/_schema.md`** documents every REGION field. Read it before editing any region file.
3. **Region files are generated for all 7 other states:** `regions/nsw.js qld.js wa.js sa.js tas.js act.js nt.js`, built by `dev/research/build_regions.py` from the research JSON. Each runs to completion in the node harness (outputs in `dev/tests/out_*.txt`).
4. **Research status by state:**

| State | Suburbs | Crime | Property | Schools | Airports/infra | Status |
|---|---|---|---|---|---|---|
| NSW (Sydney) | 115 (`nsw_a.json` 55 airport side, `nsw_b.json` 60 west incl. Western Sydney Airport) | suburb level, aucrimetracker, yr to Mar 2026, NSW rate 77.7 / 1,000 | 111 | 106 | `nsw_infra.json`: YSSY 3 runways, YSWS Western Sydney Intl (passengers from 25 Oct 2026, used as the "future" toggle), Bankstown, Camden, Richmond; 10 transport plans; 69 data centres | **Complete** |
| QLD (Brisbane) | 73 | suburb level, aucrimetracker (QPS), yr to Aug 2026, state rate 110 / 1,000 (FY24-25) | 73 | 64 | `qld_infra.json`: YBBN parallel runways, Archerfield, Amberley; future = parallel ops late 2027 | **Complete** |
| TAS (Hobart) | 45 | police **division** level only (Tas Police has no suburb data), state rate 59.7 | 44 | 35 | in `small_infra.json` (key `tas`) | **Complete** (crime shown as area-wide) |
| WA (Perth) | 65 | suburb level, RedSuburbs (WA Police), calendar 2025, rate 107.85 | 3 in `wa.json` **+ 62 in `fill_wa.jsonl`** | 1 in `wa.json` **+ 64 in `fill_wa.jsonl`** | `wa_infra.json`: YPPH + new runway 03R/21L (2028, approx placement), Jandakot, Pearce | **Data complete, fill not merged** |
| SA (Adelaide) | 65 | 65 in `fill_sa.jsonl` (some totals only) | 63 in `fill_sa.jsonl` | **1 only, 64 to do** | `sa_infra.json`: market figure **missing** | **Partial** |
| ACT (Canberra) | 56 | 49 in `fill_act.jsonl` (+7 in act.json); no source/meta line yet | **2 only, ~53 to do** | **1 only, 55 to do** | in `small_infra.json` (key `act`) | **Partial** |
| NT (Darwin) | 47 | district level (NT PFES), rate needs NT population | 46 in `fill_nt.jsonl` | 44 in `fill_nt.jsonl` (2 to do: see `todo_nt.txt`) | in `small_infra.json` (key `nt`) | **Nearly complete, fill not merged** |

The `fill_*.jsonl` files are the gap-fill results. They are **not yet merged** into the `<state>.json` files, and `build_regions.py` does not read them. The last background researchers may still have been writing to them when the session ended, so re-tally before trusting the counts above.

## 3. Repo layout (branch `multi-state`)

```
index.html               region-agnostic engine (single inline script; startApp() runs after regions/<id>.js loads)
listings.json            "Houses I've checked" entries (global; filtered by state)
regions/_schema.md       REGION field documentation
regions/vic.js           Melbourne (hand-migrated from the old single file; the reference implementation)
regions/{nsw,qld,wa,sa,tas,act,nt}.js   generated by dev/research/build_regions.py; DO NOT hand-edit, regenerate
HANDOFF.md               this file
dev/research/            all research data + scripts
  SUBURB_BRIEF.md        brief given to suburb-data researchers (schema of <state>.json)
  INFRA_BRIEF.md         brief for airports/transport/data-centre researchers (schema of *_infra.json)
  FILL_BRIEF.md          brief for gap-filling (pacing rules; fill_*.jsonl line format)
  REFACTOR_SPEC.md       the spec the engine refactor was built to
  nsw_a.json nsw_b.json qld.json wa.json sa.json tas.json act.json nt.json    suburb data
  nsw_infra.json qld_infra.json wa_infra.json sa_infra.json small_infra.json (tas/act/nt)
  fill_{wa,sa,act,nt}.jsonl   gap-fill results, one JSON object per line: {"n":suburb,"prop":[median,growth,yield,rent]} | {"n":..,"schools":[[name,p|s|c,g|c|i,score]]} | {"n":..,"crime":[offences,population,person,property,(optional area name)]} | {"n":"_meta"/"_market",...}
  todo_{wa,sa,act,nt}.txt     what was still missing when the gap-fill started
  build_regions.py       builds regions/<id>.js from research JSON (per-state CONF: bbox, airports config, future toggle, price thresholds, colour ramps)
  build_wa.py build_tas.py sa_build.py small_infra_build.py nsw_b_data.py add_sa.py   helper/builder scripts used by researchers
dev/tests/               node mock harnesses + outputs, Playwright scripts
dev/screens/             Playwright screenshots of picker/panel (map itself can't render in the sandbox: CDN blocked)
dev/index.single-file-vic-backup.html   the pre-refactor single-file Melbourne app (same as main's index.html)
```

**Paths inside scripts are absolute to the old cloud sandbox** (`/tmp/claude-0/.../scratchpad/regions/` and `/home/claude/tullamarine-flight-map/regions`). Before running anything, change them to repo-relative paths: in `build_regions.py`, set `S` = `dev/research` and `OUT` = `regions`. Do the same in the harnesses.

## 4. Next steps to finish (in order)

1. **Check out the branch:** `git fetch && git checkout multi-state`.
2. **Write `dev/research/merge_fills.py`:**
   - For each of wa, sa, act, nt, read `fill_<id>.jsonl` and patch `<id>.json` by suburb name (exact match). Set `prop` to `{median,growth,yield,rent}`, set `schools`, and set `crime` to `{offences,population,person,property,area}`.
   - Apply `_meta` lines to `crimeSource` (stateRatePer1000, source, level) and `_market` lines to the matching infra file's `market.text`/`url`.
   - Later lines win.
   - Print counts per state afterwards.
3. **Fill the remaining gaps.** Recompute from the merged data; roughly:
   - SA: schools for about 64 suburbs, the Adelaide Cotality market sentence (August 2026 results), and the SA state crime rate per 1,000.
   - ACT: property for about 53 suburbs and schools for 55. Record the crime source used for the 49 ACT crime lines (check how they were sourced: ACT Policing suburb data?) and the ACT rate.
   - NT: 2 school pages, plus the NT population (ABS ERP) to compute the rate from 31,441 offences.
   - Follow `FILL_BRIEF.md`. Pages used: `https://www.yourinvestmentpropertymag.com.au/top-suburbs/<state>/<postcode>-<slug>` for property and `https://schoolrank.com.au/suburb/<slug>-<state>` for schools.
   - **Pace requests:** one fetch at a time with an ~8s gap. Running 14 parallel researchers caused HTTP 429 blocks last time. At most 3 to 4 workers in parallel.
   - If Claude Code's WebFetch is used, results are summarised by a small model, so ask for exact numbers.
4. **Rebuild the region files:** `python3 dev/research/build_regions.py` (all states) or `... build_regions.py wa sa`. Read its warnings.
5. **Test:**
   - Extract the inline script from index.html (the last `<script>` block, starting `(function(){` or `function startApp`), then run `node --check` on it and on each regions/*.js.
   - Run the mock harness for every state (`dev/tests/harness_region.js`, fix paths first; it evals regions/<id>.js and then the app script, then calls startApp()). All 8 must complete without errors.
   - Open the site locally (`python3 -m http.server`) in a real browser: check the picker, each state loads, planes fly, runways line up with the base map, and crime, property and school layers colour suburbs. Real network is needed for tiles, Overpass and Nominatim.
6. **Verify data quality before release.** Spot-check about 5 random numbers per state against the source pages. Known issues to review:
   - **Approximate runway ends:**
     - Western Sydney runway 05/23 was calculated from the aerodrome reference point and could be up to 200 m out.
     - Perth's new runway 03R/21L could be up to 500 m out along its length.
     - Cambridge (Hobart) is approximate.
     - Essendon and Avalon ends in vic.js are approximate.
     - OSM runways override config at runtime when they match by number, bearing and midpoint, so this mostly self-corrects.
   - **Weak route data:** planned transport polylines for QLD, WA, SA, TAS, ACT and NT are mostly approximate (hand placed). They are marked `cert:"approx"` or `"concept"` and are off by default.
   - **Suspect figures:**
     - Matraville rent $1,690 at 2.58% yield.
     - Kenwick's yield doesn't match its price and rent.
     - Some parent-page crime totals are inflated by transport and justice offences (flagged per suburb).
   - **Area-level crime:** TAS and NT (and possibly ACT) use division or district figures. The engine handles this via `meta.crimeLevel` and the 5th crime element: the cards say "whole area" and the crime layer doesn't colour suburbs. Check that it reads well.
   - **Price thresholds** for tags like Rising, Premium and Entry are set per state in `build_regions.py` CONF (`thresholds`, `ramps`). Sanity-check them against each city's median.
   - **The Darwin data centre** "D1, 2 Harvey St" address is unverified.
7. **Release (Sam asked for all states at once):**
   - Update README.md: it is multi-state now, list the states, and say the live URL `?state=nsw` works.
   - Merge `multi-state` into `main`, then push.
   - Hard refresh (Ctrl+Shift+R) at https://samjrmoris.github.io/tullamarine-flight-map/ and check vic still looks identical for an existing user, and that a fresh browser shows the picker.
   - Consider renaming the page title and repo (e.g. "Flight Path Map Australia"). **Ask Sam first**: a repo rename changes the URL.
8. **Update the `house-check` skill** (saved in Sam's Claude skills). It currently assumes Victoria and Melbourne market context. Make it:
   - set `"state"` in listings.json entries,
   - use the right city's Cotality figures,
   - use the Domain URL patterns for other states, which are the same.

## 5. Key technical facts

- **Geometry:** local km coordinates relative to `REGION.origin` (`toL` / `toLL`). The noise grid is 0.35 km cells over `REGION.grid`.
- **Noise model:**
  - `curveL(ac, kind, ft)` uses NATS narrow, wide and turbo curves.
  - Wide-bodies get −5 dB on arrival and −6 dB on departure, tapering to 0 by 4,000 ft. Below 1,000 ft the level is capped at +2 dB.
  - Plain-language levels: Very loud ≥76, Loud ≥70, Noticeable ≥63, Faint ≥56, otherwise Quiet.
  - Approaches are 3°. Departures climb at 10% with ±40° fans at the main airport only.
- **Data sources:**
  - Overpass: suburbs are admin_level=10 boundaries inside `REGION.bbox`, plus aerodromes and runways.
  - Nominatim geocoding (1.1 s between requests).
  - OpenFreeMap positron style, Esri satellite, AWS terrarium terrain.
  - Google Photorealistic 3D is optional and uses the viewer's own key.
- **Melbourne data sources:**
  - Crime: CSA via aucrimetracker, year to June 2026, VIC rate 86.8.
  - Property: CoreLogic via yourinvestmentpropertymag, 12 months to June 2026.
  - Schools: SchoolRank NAPLAN score out of 100.
  - Market: Cotality. Melbourne was −1.1% in Aug 2026, −3.9% over 3 months and −4.7% over the year, and 6.8% below the March 2022 peak.
- **Domain pages are fetchable; realestate.com.au is blocked.** House checks use:
  - the Domain listing,
  - `/property-profile/<slug>` for the value estimate and sale history,
  - `/sold-listings/<suburb>-<state>-<postcode>/house/<n>-bedrooms/` for comparable sales.
- **Testing without a browser:** node mock harness (stubs maplibregl, deck, fetch and document). Playwright with `executablePath:'/opt/pw-browsers/chromium'` was used in the old sandbox; locally, use your own Chromium.
- **Commit format** (Sam as author):
  `git -c user.name="Sam" -c user.email="samjrmoris@users.noreply.github.com" commit -m "<msg>"`

## 6. Not done / offered but not confirmed

- A monthly scheduled refresh of suburb prices and Cotality figures (offered earlier, Sam hasn't said yes).
- The Domain Developer API backend was considered and deferred. It would need a server to keep the key secret.

## 7. Progress in Claude Code (30 Sep 2026)

Local copy: `C:\Users\caris\Projects\tullamarine-flight-map` (branch `multi-state`). Local preview: launch config `flight-path-australia` (port 5650).

Done:
- Paths fixed: `build_regions.py` writes to repo `regions/` and now reads/writes UTF-8 (Windows default encoding had corrupted en dashes). `dev/tests/run_all.sh` extracts the app script and runs `node --check` + the harness for all 8 regions (all pass).
- `merge_fills.py` written and run. It is idempotent: re-run after appending lines to any `fill_<id>.jsonl`.
- Property gaps fetched by script (`fetch_prop.py`, exact figures, 8 s pacing). Still no house data: Pialligo (ACT); Brinkin, The Gardens, Palmerston City, Mitchell (NT); 3 in SA.
- Market sentences (Cotality HVI, August 2026 results) added for Sydney, Brisbane, Perth and Adelaide (`set_market.py`). These were empty, not only SA.
- SA crime switched to the official SA Police 2025-26 suburb CSV (data.sa.gov.au) with person/property split; SA rate 65.25 per 1,000 (`official_crime.py`).
- NT: rate 135.17 per 1,000; Darwin/Palmerston region populations from ABS 2021 council areas.
- ACT crime switched to official ACT Policing district figures (June 2026 spreadsheet, 12 months to June 2026), Caris's decision. The removal-company suburb figures were dropped: Gungahlin's 11 suburbs summed to 3,183 vs the official district total of 3,202. ACT rate 57.89. `act_districts.py`.
- Site name changed to "Flight Path Australia" (page title, header, picker). Repo name and URL kept.
- BUG FIXED (affects live Melbourne too): OpenStreetMap now tags Australian suburbs admin_level 9, not 10, so the suburb query returned nothing and an empty result was cached forever. Query now accepts 9 or 10, never caches an empty list, cache key bumped to `v3:subs`, old `v2:subs` removed.

Still open:
- Schools: SchoolRank blocks this machine (Vercel bot check / HTTP 429). SA (64 suburbs) and ACT (55) have no school scores; the request was handed to the claude.ai chat (`request_for_other_chat_schools.md`). Returned lines go into `fill_sa.jsonl` / `fill_act.jsonl`, then `merge_fills.py`, then `build_regions.py`.
- If schools stay missing: the suburb card says "No rated schools listed" for a suburb with no data; the wording should say the scores are missing instead.
- Spot-check suspicious house medians: Kingston ACT $615k, Phillip ACT $432k (mostly-unit suburbs), plus the existing list in section 4.6.
- README, merge to main, house-check skill (section 4, steps 7 and 8).
