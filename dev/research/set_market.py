#!/usr/bin/env python3
"""Set the Cotality market sentence (August 2026 results, published September 2026) in each infra file."""
import json, os

S = os.path.dirname(os.path.abspath(__file__))
URL = 'https://discover.cotality.com/hubfs/Article-Reports/COTALITY%20HVI%20SEP%202026%20FINAL%20(1).pdf'
TEXT = {
    'nsw_infra.json': "Sydney home values fell 1.4% in August 2026, 4.7% over three months and 4.6% over the year, and sit 7.1% below the February 2026 peak (Cotality).",
    'qld_infra.json': "Brisbane home values fell 1.0% in August 2026 and 2.7% over three months, but are up 10.8% over the year and sit 2.7% below the May 2026 peak (Cotality).",
    'sa_infra.json': "Adelaide home values fell 0.8% in August 2026 and 1.6% over three months, but are up 8.6% over the year and sit 1.6% below the May 2026 peak (Cotality).",
    'wa_infra.json': "Perth home values fell 0.8% in August 2026 and 3.2% over three months, but are up 15.6% over the year and sit 3.2% below the April 2026 peak (Cotality).",
}
for f, t in TEXT.items():
    p = os.path.join(S, f)
    d = json.load(open(p, encoding='utf-8'))
    d['market'] = {'text': t, 'url': URL, 'month': '2026-08'}
    with open(p, 'w', encoding='utf-8') as fh:
        json.dump(d, fh, indent=1, ensure_ascii=False)
        fh.write('\n')
    print(f, 'set')
