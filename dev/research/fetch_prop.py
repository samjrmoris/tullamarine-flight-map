#!/usr/bin/env python3
"""Fetch missing house figures from yourinvestmentpropertymag (CoreLogic) and append them to fill_<id>.jsonl.
One request every 8 s. Usage: python fetch_prop.py act nt wa"""
import html, json, os, re, sys, time, urllib.request, urllib.error

S = os.path.dirname(os.path.abspath(__file__))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36'
NUM = r'(-?[\d,]+(?:\.\d+)?)'

def slug(n):
    return re.sub(r'\s+', '-', n.lower().replace("'", '-')).strip('-')

def text(url):
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        t = r.read().decode('utf-8', 'ignore')
    t = re.sub(r'<script.*?</script>|<style.*?</style>', '', t, flags=re.S)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', t)))

def grab(pat, t):
    m = re.search(pat, t)
    return float(m.group(1).replace(',', '')) if m else None

def parse(t):
    # Only the house sentence, never the unit one
    i = t.find('median property price for a house')
    if i < 0:
        return None
    h = t[i:i + 700]
    med = grab(r'house is currently \$ ?' + NUM, h)
    gr = grab(r'annual capital growth of ' + NUM + r' ?%', h)
    yl = grab(r'rental yields for houses are currently ' + NUM + r' ?%', h)
    rent = grab(r'median rent of \$ ?' + NUM, h)
    if med is None and rent is None:
        return None
    return [int(med) if med else None, gr, yl, int(rent) if rent else None]

for st in sys.argv[1:]:
    data = json.load(open(os.path.join(S, f'{st}.json'), encoding='utf-8'))
    todo = [s for s in data['suburbs'] if not s.get('prop')]
    print(f'{st}: {len(todo)} to fetch', flush=True)
    out = open(os.path.join(S, f'fill_{st}.jsonl'), 'a', encoding='utf-8')
    for s in todo:
        url = f"https://www.yourinvestmentpropertymag.com.au/top-suburbs/{st}/{s['postcode']}-{slug(s['name'])}"
        try:
            p = parse(text(url))
            print(f"  {s['name']}: {p}", flush=True)
            if p:
                out.write(json.dumps({'n': s['name'], 'prop': p}, ensure_ascii=False) + '\n')
                out.flush()
        except urllib.error.HTTPError as e:
            print(f"  {s['name']}: HTTP {e.code} {url}", flush=True)
            if e.code == 429:
                time.sleep(300)
        except Exception as e:
            print(f"  {s['name']}: ERROR {e}", flush=True)
        time.sleep(8)
