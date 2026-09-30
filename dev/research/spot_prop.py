#!/usr/bin/env python3
"""Spot-check stored house figures against yourinvestmentpropertymag. 5 random suburbs per state + named suspects."""
import json, os, random, sys, time
sys.argv = ['x']
from fetch_prop import S, slug, text, parse
FILES = {'nsw': ['nsw_a.json', 'nsw_b.json'], 'qld': ['qld.json'], 'wa': ['wa.json'], 'sa': ['sa.json'], 'tas': ['tas.json'], 'act': ['act.json'], 'nt': ['nt.json']}
SUSPECT = {'Kingston', 'Phillip', 'Matraville', 'Kenwick'}
random.seed(30)
for st, fs in FILES.items():
    subs = [s for f in fs for s in json.load(open(os.path.join(S, f), encoding='utf-8'))['suburbs'] if s.get('prop')]
    pick = random.sample(subs, 5) + [s for s in subs if s['name'] in SUSPECT]
    for s in pick:
        p = s['prop']; mine = [p.get('median'), p.get('growth'), p.get('yield'), p.get('rent')]
        try:
            live = parse(text(f"https://www.yourinvestmentpropertymag.com.au/top-suburbs/{st}/{s['postcode']}-{slug(s['name'])}"))
        except Exception as e:
            live = f'ERR {e}'
        print(f"{st} {s['name']:20} {'MATCH' if live == mine else 'DIFF '} stored {mine} live {live}", flush=True)
        time.sleep(8)
