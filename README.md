# Flight Path Australia

Interactive 3D house-hunting map for every Australian capital city. It shows airport land, runways and flight paths with an estimated peak-loudness (LAmax) map in plain words, plus trains and roads (existing and planned), data centres, crime, house prices, schools, a suburb shortlist and an address check.

Live: https://samjrmoris.github.io/tullamarine-flight-map/

Cities: Melbourne, Sydney, Brisbane, Perth, Adelaide, Hobart, Canberra and Darwin (capital city metro areas). Pick one on first visit, switch from the side panel, or link straight to one with `?state=`: `vic`, `nsw`, `qld`, `wa`, `sa`, `tas`, `act`, `nt`. For example https://samjrmoris.github.io/tullamarine-flight-map/?state=nsw

Noise model: NATS representative Lmax tables, SAE AIR 1751 lateral attenuation, wide-bodies calibrated to Melbourne Airport third runway fact sheet. Screening tool only; check exact addresses with each airport's own flight path and noise tool.

Data: house figures from CoreLogic via Your Investment Property (12 months to June 2026), market notes from Cotality's Home Value Index (August 2026), school scores from SchoolRank, crime from each state's police figures (Hobart, Canberra and Darwin police publish only area-wide figures, so those cards cover the whole police area). Where a figure is missing the map says "No data". Sources for each city are listed at the bottom of its side panel.

How it is built: `index.html` is the map engine; each city is a file in `regions/` (see `regions/_schema.md`), generated from the research in `dev/research/` by `build_regions.py`.
