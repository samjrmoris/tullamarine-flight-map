#!/usr/bin/env python3
"""Merge fill_<id>.jsonl gap-fill results into <id>.json (and _market lines into the infra file).
Later lines win. Usage: python merge_fills.py [wa sa act nt]"""
import json, os, sys

S = os.path.dirname(os.path.abspath(__file__))
INFRA = {'wa': ('wa_infra.json', None), 'sa': ('sa_infra.json', None), 'act': ('small_infra.json', 'act'), 'nt': ('small_infra.json', 'nt')}

def load(f):
    return json.load(open(os.path.join(S, f), encoding='utf-8'))

def save(f, d):
    with open(os.path.join(S, f), 'w', encoding='utf-8') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False)
        fh.write('\n')

def merge(st):
    data = load(f'{st}.json')
    subs = {s['name']: s for s in data['suburbs']}
    done = {'prop': 0, 'schools': 0, 'crime': 0}
    missing = set()
    path = os.path.join(S, f'fill_{st}.jsonl')
    for line in open(path, encoding='utf-8'):
        line = line.strip()
        if not line:
            continue
        o = json.loads(line)
        n = o['n']
        if n == '_meta':
            data['crimeSource'].update({k: v for k, v in o.items() if k != 'n'})
            continue
        if n == '_market':
            f, key = INFRA[st]
            inf = load(f)
            tgt = inf[key] if key else inf
            tgt.setdefault('market', {}).update({k: v for k, v in o.items() if k in ('text', 'url')})
            save(f, inf)
            continue
        s = subs.get(n)
        if s is None:
            missing.add(n)
            continue
        if 'prop' in o:
            p = o['prop']
            s['prop'] = None if p is None else dict(zip(('median', 'growth', 'yield', 'rent'), p))
            done['prop'] += 1
        if 'schools' in o:
            s['schools'] = o['schools']
            done['schools'] += 1
        if 'crime' in o:
            c = o['crime']
            s['crime'] = None if c is None else dict(zip(('offences', 'population', 'person', 'property', 'area'), list(c) + [None] * (5 - len(c))))
            done['crime'] += 1
    save(f'{st}.json', data)
    ss = data['suburbs']
    have = {'prop': sum(1 for s in ss if s.get('prop')),
            'schools': sum(1 for s in ss if s.get('schools') is not None),
            'crime': sum(1 for s in ss if s.get('crime'))}
    print(f"{st}: {len(ss)} suburbs | merged lines {done} | now have {have}"
          + (f" | NOT FOUND: {sorted(missing)}" if missing else ''))

for st in sys.argv[1:] or ['wa', 'sa', 'act', 'nt']:
    merge(st)
