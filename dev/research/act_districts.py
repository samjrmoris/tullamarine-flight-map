#!/usr/bin/env python3
"""Append ACT Policing district crime (12 months Jul 2025 - Jun 2026) to fill_act.jsonl; merge_fills.py applies it.
Source: src/act_police_jun26.xlsx (police.act.gov.au, June26-Website-Stats-Monthy-Download.xlsx), Tables 2-9.
Populations: ABS 2021 Census QuickStats, SA3 areas matching each police district."""
import json, os
import openpyxl

S = os.path.dirname(os.path.abspath(__file__))
ACT_POP = 454499
DISTRICTS = {  # police district: (ABS SA3 name, population, suburbs on the map)
    'Inner North': ('North Canberra', 61188, ['Campbell', 'Reid', 'Braddon', 'Turner', 'Ainslie', 'Hackett', 'Watson', 'Downer', 'Dickson', 'Lyneham', "O'Connor"]),
    'Inner South': ('South Canberra', 31592, ['Kingston', 'Griffith', 'Narrabundah', 'Red Hill']),
    'Tuggeranong': ('Tuggeranong', 89461, ['Gordon', 'Conder', 'Banks', 'Calwell', 'Theodore', 'Isabella Plains', 'Chisholm', 'Gowrie', 'Fadden', 'Macarthur', 'Wanniassa', 'Kambah']),
    'Gungahlin': ('Gungahlin', 87682, ['Gungahlin', 'Franklin', 'Harrison', 'Crace', 'Forde', 'Bonner', 'Casey', 'Ngunnawal', 'Amaroo', 'Throsby', 'Taylor']),
    'Belconnen': ('Belconnen', 106061, ['Belconnen', 'Bruce', 'Macquarie', 'Page', 'Kaleen', 'Giralang', 'Evatt', 'Florey', 'Holt', 'Dunlop']),
    'Molonglo District': ('Molonglo', 11435, ['Coombs', 'Wright', 'Denman Prospect']),
    'Woden': ('Woden Valley', 39279, ['Phillip', 'Mawson', 'Curtin', 'Farrer']),
}
PERSON = {'Assault', 'Homicide', 'Offences against a person', 'Robbery', 'Sexual Assault'}
PROPERTY = {'Burglary', 'Motor vehicle theft', 'Property damage', 'Theft (excluding motor vehicles)'}
NOT_CRIME = {'Road Collision with injury', 'Road Fatality', 'Traffic infringement notices', 'Total'}

rows = list(openpyxl.load_workbook(os.path.join(S, 'src', 'act_police_jun26.xlsx'), read_only=True, data_only=True)['Offence Statistics'].iter_rows(values_only=True))
tabs, cur = {}, None
for r in rows:
    if r[0] and str(r[0]).startswith('Table'):
        cur = str(r[0]).split(':', 1)[1].split(' - ')[0].strip()
        tabs[cur] = {}
    elif cur and r[0] and isinstance(r[1], (int, float)):
        tabs[cur][r[0].strip()] = sum(v or 0 for v in r[1:13])   # JUN26 back to JUL25

def split(t):
    return (sum(v for k, v in t.items() if k not in NOT_CRIME),
            sum(v for k, v in t.items() if k in PERSON),
            sum(v for k, v in t.items() if k in PROPERTY))

out = []
for d, (sa3, pop, subs) in DISTRICTS.items():
    off, per, prop = split(tabs[d])
    for n in subs:
        out.append({'n': n, 'crime': [off, pop, per, prop, f'{d.replace(" District", "")} police district']})
out.append({'n': 'Pialligo', 'crime': None})   # in ACT Policing's catch-all "Other Areas", which has no matching population
act_total = split(tabs['ACT'])[0]
rate = round(act_total / ACT_POP * 1000, 2)
out.append({'n': '_meta', 'name': 'ACT Policing offence statistics by police district (June 2026 monthly download)',
            'url': 'https://police.act.gov.au/__data/assets/excel_doc/0006/336174/June26-Website-Stats-Monthy-Download.xlsx',
            'period': '12 months, July 2025 to June 2026', 'level': 'district', 'stateRatePer1000': rate,
            'stateRateSource': f'{act_total:,} offences ACT-wide (traffic infringements and road collisions excluded) / {ACT_POP:,} residents (ABS 2021 Census) = {rate} per 1,000',
            'notes': 'ACT Policing publishes offences by police district, not by suburb. Every suburb carries its whole district figures; district populations are the matching ABS 2021 Census SA3 areas (Inner North = North Canberra, Inner South = South Canberra, Woden = Woden Valley). Pialligo sits in ACT Policing\'s "Other Areas" group, so it has no figure. Suburb figures compiled by a third party (northremovals.com.au) were dropped because they did not reconcile with the official district totals.'})
with open(os.path.join(S, 'fill_act.jsonl'), 'a', encoding='utf-8') as f:
    for r in out:
        f.write(json.dumps(r, ensure_ascii=False) + '\n')
print(f'ACT: {len(out) - 1} suburbs, ACT rate {rate}')
