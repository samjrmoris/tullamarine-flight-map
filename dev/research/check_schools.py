#!/usr/bin/env python3
"""Check every school on the map against ACARA's official School Location 2025 list.
Reports: not found, wrong sector, wrong level, and where ACARA says the school is.
Usage: python check_schools.py <schools_all.json from the regions>  -> audit/schools_check.json"""
import json, os, re, sys, difflib
import openpyxl

S = os.path.dirname(os.path.abspath(__file__))
STATE = {'vic': 'VIC', 'nsw': 'NSW', 'qld': 'QLD', 'wa': 'WA', 'sa': 'SA', 'tas': 'TAS', 'act': 'ACT', 'nt': 'NT'}
SECTOR = {'g': 'Government', 'c': 'Catholic', 'i': 'Independent'}
LEVEL = {'p': {'Primary'}, 's': {'Secondary'}, 'c': {'Combined'}}

def norm(n):
    n = n.lower().replace('&', 'and').replace("'", '').replace('’', '')
    n = re.sub(r'\bst\.?\b', 'saint', n)
    n = re.sub(r'\b(the|school|college|campus|incorporated|inc|ltd)\b', ' ', n)
    return re.sub(r'[^a-z0-9]+', ' ', n).strip()

rows = list(openpyxl.load_workbook(os.path.join(S, 'src', 'acara_location_2025.xlsx'), read_only=True)['SchoolLocations 2025'].iter_rows(values_only=True))
head = rows[0]
ix = {h: i for i, h in enumerate(head)}
by_state = {}
for r in rows[1:]:
    by_state.setdefault(r[ix['State']], []).append({'name': r[ix['School Name']], 'suburb': r[ix['Suburb']], 'sector': r[ix['School Sector']],
                                                   'type': r[ix['School Type']], 'lat': r[ix['Latitude']], 'lng': r[ix['Longitude']], 'n': norm(r[ix['School Name']])})

ours = json.load(open(sys.argv[1], encoding='utf-8'))
report, summary = {}, {}
for rid, schools in ours.items():
    pool = by_state[STATE[rid]]
    names = [p['n'] for p in pool]
    res = []
    for name, sub, lvl, sec, score in schools:
        n = norm(name)
        cands = [p for p in pool if p['n'] == n]
        how = 'exact'
        if not cands:   # campus records: "Pembroke School - Kensington Park Campus"
            cands = [p for p in pool if p['n'].startswith(n + ' ')]
            how = 'campus'
        if not cands:
            close = difflib.get_close_matches(n, names, n=3, cutoff=0.86)
            cands = [p for p in pool if p['n'] in close]
            how = 'close' if cands else 'none'
        if lvl == 'c' and len(cands) > 1 and {p['type'] for p in cands} >= {'Primary', 'Secondary'}:
            cands = [dict(cands[0], type='Combined')]   # separate junior and senior campus records = combined school
        if len(cands) > 1:   # same name in several suburbs: prefer ours
            same = [p for p in cands if (p['suburb'] or '').lower() == sub.lower()]
            cands = same or cands
        m = cands[0] if cands else None
        issues = []
        if not m:
            issues.append('NOT FOUND in ACARA list')
        else:
            if how == 'close':
                issues.append(f'name differs: ACARA "{m["name"]}"')
            if m['sector'] != SECTOR[sec]:
                issues.append(f'sector: ours {SECTOR[sec]}, ACARA {m["sector"]}')
            if m['type'] not in LEVEL[lvl]:
                issues.append(f'level: ours {lvl}, ACARA {m["type"]}')
            if (m['suburb'] or '').lower() != sub.lower():
                issues.append(f'suburb: listed under {sub}, ACARA address suburb {m["suburb"]}')
            if len(cands) > 1:
                issues.append(f'{len(cands)} ACARA schools share this name')
        res.append({'name': name, 'suburb': sub, 'level': lvl, 'sector': sec, 'score': score,
                    'acara': {k: m[k] for k in ('name', 'suburb', 'sector', 'type', 'lat', 'lng')} if m else None, 'issues': issues})
    report[rid] = res
    cnt = lambda pat: sum(1 for x in res if any(pat in i for i in x['issues']))
    summary[rid] = {'schools': len(res), 'clean': sum(1 for x in res if not x['issues']), 'not_found': cnt('NOT FOUND'),
                    'sector': cnt('sector:'), 'level': cnt('level:'), 'name': cnt('name differs'), 'other_suburb': cnt('suburb:')}
os.makedirs(os.path.join(S, 'audit'), exist_ok=True)
json.dump({'source': 'ACARA School Location 2025 (acara.edu.au Data Access Program)', 'summary': summary, 'schools': report},
          open(os.path.join(S, 'audit', 'schools_check.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
for k, v in summary.items():
    print(k, v)
