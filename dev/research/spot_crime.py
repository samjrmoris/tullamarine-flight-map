#!/usr/bin/env python3
"""Spot-check stored offence totals: NSW/QLD on aucrimetracker, WA on RedSuburbs. 4 random suburbs each."""
import json, os, random, re, sys, time
sys.argv = ['x']
from fetch_prop import S, slug, text
random.seed(30)
CASES = [('nsw', ['nsw_a.json', 'nsw_b.json'], 'https://www.aucrimetracker.com/nsw/{s}/'),
         ('qld', ['qld.json'], 'https://www.aucrimetracker.com/qld/{s}/'),
         ('wa', ['wa.json'], 'https://redsuburbs.com.au/suburbs/{s}/')]
for st, fs, url in CASES:
    subs = [s for f in fs for s in json.load(open(os.path.join(S, f), encoding='utf-8'))['suburbs'] if s.get('crime')]
    for s in random.sample(subs, 4):
        n = s['crime']['offences']
        try:
            t = text(url.format(s=slug(s['name'])))
            m = re.search(r'calculated from ([\d,]+) reported', t)
            found = m.group(1) if m else ('number present' if re.search(r'\b' + f'{n:,}'.replace(',', ',?') + r'\b', t) else 'number NOT on page')
        except Exception as e:
            found = f'ERR {e}'
        print(f"{st} {s['name']:20} stored {n}  page: {found}", flush=True)
        time.sleep(8)
