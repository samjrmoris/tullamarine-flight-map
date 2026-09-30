# Gap-fill brief (read fully)

A state's suburb file already exists; some suburbs are missing property, school or crime figures. Fill ONLY the gaps listed in your task. Never invent or estimate a number: if a page has no figure, record null / an empty list.

PACING MATTERS: several researchers share one web connection and yesterday it got blocked (HTTP 429) from too many requests. So:
- Do ONE WebFetch at a time, and run `sleep 8` in Bash between fetches.
- If you get a 429 or "rate limited", run `sleep 300` and try the NEXT page (not the refused one). If refused pages pile up, keep going through the list and come back to them at the end after another `sleep 300`. Do not give up early: work through the whole list.
- Save as you go (append each result immediately), so nothing is lost if you stop.

## Pages
Property (houses): https://www.yourinvestmentpropertymag.com.au/top-suburbs/<state>/<postcode>-<suburb-slug>  e.g. .../wa/6104-belmont
  -> median house price $, 12-month growth %, gross yield %, weekly rent $ (CoreLogic, 12 months to June 2026). Prompt WebFetch for exactly those four numbers for HOUSES.
Schools: https://schoolrank.com.au/suburb/<suburb-slug>-<state>  e.g. .../suburb/belmont-wa
  -> every school WITH a numeric score: [name, level p|s|c, sector g|c|i, score]. p primary, s secondary, c combined (K-12, P-12, K-10 etc), g government, c Catholic, i independent. Skip unrated. A 404 means none: record [].
Slugs: lowercase, spaces->hyphens, drop apostrophes ("o-connor"). Some names clash with other places in the same state and need a qualifier; if a page is clearly the wrong place (different postcode), search for the right one.

## Output
Append one JSON object per line to the file named in your task:
{"n":"Belmont","prop":[902000,18.37,4.03,750]}        (use null for any missing number; "prop":null if no house data)
{"n":"Belmont","schools":[["Belmont Primary School","p","g",59]]}
{"n":"Glenelg","crime":[590,3440,144,410]}            ([offences, population, person, property])
Use the suburb name exactly as given in your task. Final reply: counts done, anything refused or missing, and anything odd. Keep it short.
