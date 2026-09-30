# Suburb data brief (read fully)

You are gathering per-suburb data for a house-hunting map (plane noise, crime, property, schools). A Melbourne version already exists; we are now adding other Australian capitals with the SAME data. Accuracy matters more than speed: never invent or estimate a number. If a figure can't be found, use null.

Tools: use WebFetch for every page (the shell has no internet). WebSearch is allowed for discovering sources. realestate.com.au is blocked; don't use it.

## 1. Choose the suburbs
Pick the suburb list described in your task. Use official locality names exactly as the ABS / Australia Post / OpenStreetMap spell them (e.g. "St Marys", "Mount Druitt"). Include the 4-digit postcode.

## 2. Property (every suburb)
URL pattern: https://www.yourinvestmentpropertymag.com.au/top-suburbs/<state lowercase>/<postcode>-<suburb-slug>
e.g. https://www.yourinvestmentpropertymag.com.au/top-suburbs/nsw/2170-liverpool
Get, for HOUSES: median price ($), 12-month capital growth (%), gross rental yield (%), median weekly rent ($). Data is CoreLogic, "12 months to June 2026". If the page shows no house data, null.

## 3. Schools (every suburb)
URL: https://schoolrank.com.au/suburb/<suburb-slug>-<state lowercase>   e.g. https://schoolrank.com.au/suburb/liverpool-nsw
For each school WITH a numeric score: [name, level, sector, score]
 level: "p" primary, "s" secondary, "c" combined (P/K-12, K-9 etc.)
 sector: "g" government, "c" Catholic, "i" independent
Skip unrated schools. If the slug 404s, try with a hyphenated qualifier (e.g. "st-marys-nsw") or search the site.

## 4. Crime
Goal per suburb: total recorded offences in the latest 12 months, the suburb population (2021 census is fine), offences against the person (assault, robbery, sexual offences, homicide, threats), and property offences (theft, burglary/break-in, vehicle theft, damage, arson).
- NSW: https://www.aucrimetracker.com/nsw/<suburb-slug>/ (year ending Mar 2026). Worked example: Mascot gave offences 1364, population 21591, person 287, property 716.
- Other states: find the best official or reputable republisher source with suburb-level counts (e.g. Queensland Police Service online crime map / data.qld.gov.au, WA Police "crime statistics" by locality, SAPOL / data.sa.gov.au suburb crime CSV, ACT Policing suburb statistics, Tasmania Police, NT Police/PFES). Try aucrimetracker first for your state too. If only council/district-level figures exist, give those for the council/district each suburb sits in and set "area" to that council/district name (population then = that area's population). Say exactly what you found.
Also give the state-wide rate of recorded offences per 1,000 residents for the same period and definition, with source.

## 5. Flags (short plain-English notes, optional)
Things that distort a suburb's crime figures: a big shopping centre ("mall": "Westfield Liverpool"), prisons, the airport itself, a CBD/nightlife strip, or a fast-growing new estate where 2021 population undercounts residents ("growthArea": true).

## Output
Write ONE JSON file (valid JSON, no comments) to the path given in your task, with this shape:
{
 "region": "<id>",
 "crimeSource": {"name": "...", "url": "...", "period": "year to March 2026", "level": "suburb" | "council" | "district", "stateRatePer1000": 72.1, "stateRateSource": "...", "notes": "anything the reader must know"},
 "suburbs": [
  {"name": "Mascot", "postcode": "2020",
   "crime": {"offences": 1364, "population": 21591, "person": 287, "property": 716, "area": null} ,
   "prop": {"median": 1500000, "growth": 3.2, "yield": 3.1, "rent": 850},
   "schools": [["Mascot Public School","p","g",58]],
   "mall": null, "growthArea": false, "flags": []}
 ]
}
Validate the file with python3 -m json.tool before finishing. Your final reply: counts (suburbs, with crime, with property, with schools), the crime source/level, and any problems. Keep the reply short; the data is in the file.
