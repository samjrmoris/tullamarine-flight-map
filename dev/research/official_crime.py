#!/usr/bin/env python3
"""Append official crime figures to fill_sa.jsonl and fill_nt.jsonl (merge_fills.py applies them).
SA: SAPOL suburb CSV 2025-26 (data.sa.gov.au), downloaded to src/sa_crime_2025_26.csv.
NT: region populations and NT rate from ABS 2021 Census QuickStats."""
import collections, csv, json, os

S = os.path.dirname(os.path.abspath(__file__))
SA_POP, NT_POP = 1781516, 232605           # ABS 2021 Census QuickStats, People
NT_REGION_POP = {'Darwin police reporting region': 80530,       # City of Darwin LGA71000
                 'Palmerston police reporting region': 37247}   # City of Palmerston LGA72800

def append(st, rows):
    with open(os.path.join(S, f'fill_{st}.jsonl'), 'a', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')

# SA
per, prop = collections.Counter(), collections.Counter()
for r in csv.DictReader(open(os.path.join(S, 'src', 'sa_crime_2025_26.csv'), encoding='utf-8-sig')):
    sub = r['Suburb - Incident'].strip().upper()
    if not sub or sub == 'NOT DISCLOSED':
        continue   # sexual offences published without location; excluded from suburb and state totals alike
    k = (sub, r['Postcode - Incident'].strip())
    (per if 'PERSON' in r['Offence Level 1 Description'] else prop)[k] += int(r['Offence count'] or 0)
state_total = sum(per.values()) + sum(prop.values())
rows = []
for s in json.load(open(os.path.join(S, 'sa.json'), encoding='utf-8'))['suburbs']:
    k = (s['name'].upper(), s['postcode'])
    pop = (s.get('crime') or {}).get('population')
    rows.append({'n': s['name'], 'crime': [per[k] + prop[k], pop, per[k], prop[k]]})
rate = round(state_total / SA_POP * 1000, 2)
rows.append({'n': '_meta', 'name': 'SA Police suburb crime statistics 2025-26 (data.sa.gov.au)',
             'url': 'https://data.sa.gov.au/data/dataset/860126f7-eeb5-4fbc-be44-069aa0467d11',
             'period': 'financial year to 30 June 2026', 'level': 'suburb', 'stateRatePer1000': rate,
             'stateRateSource': f'{state_total:,} offences against the person and property with a suburb recorded, 2025-26 / {SA_POP:,} residents (ABS 2021 Census) = {rate} per 1,000',
             'notes': 'Offences = against the person + against property, the only two groups SA Police publish by suburb. Sexual offences are published without a location, so they are left out of both suburb and state figures. Suburb populations are ABS 2021 Census (via AU Crime Tracker).'})
append('sa', rows)
print(f'SA: {len(rows) - 1} suburbs, state rate {rate}')

# NT
d = json.load(open(os.path.join(S, 'nt.json'), encoding='utf-8'))
rows = []
for s in d['suburbs']:
    c = s.get('crime')
    if c and c.get('area') in NT_REGION_POP:
        rows.append({'n': s['name'], 'crime': [c['offences'], NT_REGION_POP[c['area']], c['person'], c['property'], c['area']]})
rate = round(31441 / NT_POP * 1000, 2)
rows.append({'n': '_meta', 'stateRatePer1000': rate,
             'stateRateSource': f'NT total 31,441 offences (12,595 against the person + 18,846 property), 12 months to January 2026 (PFES Table 3) / {NT_POP:,} residents (ABS 2021 Census) = {rate} per 1,000. Region populations: City of Darwin 80,530 and City of Palmerston 37,247 (ABS 2021 Census, council areas used as the closest match to the police regions).'})
append('nt', rows)
print(f'NT: {len(rows) - 1} suburbs given region populations, NT rate {rate}')
