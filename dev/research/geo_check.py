"""Mechanical fact-check for every region, no agents needed.

For each regions/<id>.js: runway threshold ends vs OpenStreetMap and OurAirports,
aerodrome boundary present in OSM with the right ICAO tag, and our data centres
vs OSM data-centre features (nearest distance). Downloads are cached in
dev/research/src/geo/ so re-runs cost nothing.

Usage: python dev/research/geo_check.py [ids...]   -> dev/research/audit/geo_check.json
"""
import csv, json, math, os, subprocess, sys, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, 'dev', 'research', 'src', 'geo')
OUT = os.path.join(ROOT, 'dev', 'research', 'audit', 'geo_check.json')
IDS = sys.argv[1:] or ['vic', 'nsw', 'qld', 'wa', 'sa', 'tas', 'act', 'nt']
UA = 'FlightPathAustralia-audit/1.0 (github.com/samjrmoris/tullamarine-flight-map)'
OVERPASS = ['https://overpass-api.de/api/interpreter', 'https://maps.mail.ru/osm/tools/overpass/api/interpreter']
os.makedirs(SRC, exist_ok=True)


def dist(a, b):  # [lon,lat] -> metres
    R = 6371000
    p1, p2 = math.radians(a[1]), math.radians(b[1])
    dp, dl = p2 - p1, math.radians(b[0] - a[0])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def get(url, path, data=None):
    if os.path.exists(path):
        return open(path, encoding='utf8').read()
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, data=data, headers={'User-Agent': UA})
            body = urllib.request.urlopen(req, timeout=180).read().decode('utf8')
            open(path, 'w', encoding='utf8').write(body)
            time.sleep(8)
            return body
        except Exception as e:
            print('  fetch failed', url[:60], e)
            time.sleep(30)
    raise SystemExit('giving up on ' + url)


def overpass(q, path):
    if os.path.exists(path):
        return json.load(open(path, encoding='utf8'))
    for ep in OVERPASS:
        try:
            return json.loads(get(ep, path, urllib.parse.urlencode({'data': q}).encode()))
        except SystemExit:
            continue
    raise SystemExit('overpass down')


def region(i):
    js = ("global.window={};require('./regions/%s.js');const R=window.REGION;"
          "console.log(JSON.stringify({airports:R.airports,dcs:R.dcs,bbox:R.bbox,dcBbox:R.dcBbox||R.bbox}))") % i
    return json.loads(subprocess.check_output(['node', '-e', js], cwd=ROOT, text=True))


def norm(r):
    return r.upper().lstrip('0')


# OurAirports runway table (thresholds incl. displaced)
oa = {}
for row in csv.DictReader(get('https://davidmegginson.github.io/ourairports-data/runways.csv',
                              os.path.join(SRC, 'ourairports_runways.csv')).splitlines()):
    for e in ('le', 'he'):
        try:
            oa[(row['airport_ident'], norm(row[e + '_ident']))] = [float(row[e + '_longitude_deg']), float(row[e + '_latitude_deg'])]
        except ValueError:
            pass

report = {}
for i in IDS:
    R = region(i)
    s, w, n, e = R['dcBbox']
    q = '[out:json][timeout:120];('
    for a in R['airports']:
        q += 'way["aeroway"="runway"](around:4500,%s,%s);' % (a['lat'], a['lng'])
        q += 'nwr["aeroway"="aerodrome"]["icao"="%s"];' % a['icao']
    q += 'nwr["telecom"="data_center"](%s,%s,%s,%s);nwr["building"="data_center"](%s,%s,%s,%s););out tags center geom;' % (s, w, n, e, s, w, n, e)
    osm = overpass(q, os.path.join(SRC, 'overpass_%s.json' % i))['elements']
    ways = [x for x in osm if x.get('tags', {}).get('aeroway') == 'runway' and x.get('geometry')]
    # join pieces with the same ref that touch end to end (same rule as index.html applyAirportData)
    joined = True
    while joined:
        joined = False
        for a_ in range(len(ways)):
            for b_ in range(a_ + 1, len(ways)):
                s_, t_ = ways[a_], ways[b_]
                ref = s_['tags'].get('ref')
                if not ref or ref != t_['tags'].get('ref'):
                    continue
                ps = [[p['lon'], p['lat']] for p in (s_['geometry'][0], s_['geometry'][-1], t_['geometry'][0], t_['geometry'][-1])]
                if min(dist(p, q) for p in ps[:2] for q in ps[2:]) >= 50:
                    continue
                far = max(((p, q) for p in ps for q in ps), key=lambda pq: dist(*pq))
                ways[a_] = {'tags': s_['tags'], 'geometry': [{'lon': far[0][0], 'lat': far[0][1]}, {'lon': far[1][0], 'lat': far[1][1]}]}
                del ways[b_]
                joined = True
                break
            if joined:
                break
    out = {'runways': [], 'airportLand': [], 'dcs': [], 'osmDcsNotOurs': []}
    for a in R['airports']:
        land = [x for x in osm if x.get('tags', {}).get('aeroway') == 'aerodrome' and x['tags'].get('icao') == a['icao']]
        out['airportLand'].append({'airport': a['icao'], 'osm': ['%s %s' % (x['type'], x['id']) for x in land] or 'MISSING'})
        for rw in a.get('runways', []):
            ends = rw['ends']
            refs = [norm(r) for r in rw['refs']]
            alt = [norm(r) for r in rw.get('futureRefs', [])]
            best = None
            for x in ways:
                g = [[p['lon'], p['lat']] for p in x['geometry']]
                ref = [norm(r) for r in x['tags'].get('ref', '').replace('-', '/').split('/')]
                d0 = min(dist(ends[0], g[0]) + dist(ends[1], g[-1]), dist(ends[0], g[-1]) + dist(ends[1], g[0]))
                if set(ref) in (set(refs), set(alt)) or d0 < 3000:
                    if best is None or d0 < best[0]:
                        best = (d0, x, g)
            row = {'airport': a['icao'], 'refs': rw['refs'], 'era': rw.get('era', 'both'), 'ours': ends}
            if best:
                g = best[2]
                if dist(ends[0], g[0]) > dist(ends[0], g[-1]):
                    g = g[::-1]
                row['osm'] = [g[0], g[-1]]
                row['osm_ref'] = best[1]['tags'].get('ref')
                row['diff_osm_m'] = [round(dist(ends[0], g[0])), round(dist(ends[1], g[-1]))]
            o = [oa.get((a['icao'], r)) for r in refs]
            if all(o):
                row['ourairports'] = o
                row['diff_oa_m'] = [round(dist(ends[k], o[k])) for k in (0, 1)]
            worst = max(row.get('diff_osm_m', [0]) + ([] if 'osm' in row else row.get('diff_oa_m', [9999])))
            row['verdict'] = 'ok' if worst <= 150 else ('future/no OSM' if rw.get('era') == 'future' and 'osm' not in row else 'fix')
            out['runways'].append(row)
    osm_dc = []
    for x in osm:
        t = x.get('tags', {})
        if t.get('telecom') == 'data_center' or t.get('building') == 'data_center':
            c = x.get('center') or {'lon': x.get('lon'), 'lat': x.get('lat')}
            if c.get('lon') is not None:
                osm_dc.append({'osm': '%s %s' % (x['type'], x['id']), 'name': t.get('name') or t.get('operator') or '',
                               'operator': t.get('operator', ''), 'addr': ' '.join(filter(None, [t.get('addr:housenumber'), t.get('addr:street'), t.get('addr:suburb')])),
                               'lnglat': [round(c['lon'], 5), round(c['lat'], 5)]})
    used = set()
    for d in R['dcs']:
        row = {'name': d[0], 'operator': d[1], 'address': d[2], 'status': d[3], 'verified_lnglat': d[5] if len(d) > 5 else None}
        if row['verified_lnglat']:
            near = sorted(osm_dc, key=lambda o: dist(row['verified_lnglat'], o['lnglat']))[:1]
            if near:
                row['nearest_osm'] = near[0]
                row['nearest_osm_m'] = round(dist(row['verified_lnglat'], near[0]['lnglat']))
                if row['nearest_osm_m'] < 300:
                    used.add(near[0]['osm'])
        out['dcs'].append(row)
    out['osmDcsNotOurs'] = [o for o in osm_dc if o['osm'] not in used]
    report[i] = out
    rw = out['runways']
    print('%s: runways %d ok / %d fix / %d future; land missing %s; dcs %d (%d with coords); OSM data centres %d' % (
        i, sum(r['verdict'] == 'ok' for r in rw), sum(r['verdict'] == 'fix' for r in rw), sum(r['verdict'].startswith('future') for r in rw),
        [l['airport'] for l in out['airportLand'] if l['osm'] == 'MISSING'] or 'none', len(R['dcs']),
        sum(1 for d in out['dcs'] if d['verified_lnglat']), len(osm_dc)))
    for r in rw:
        if r['verdict'] == 'fix':
            print('   FIX', r['airport'], r['refs'], 'osm', r.get('diff_osm_m'), 'oa', r.get('diff_oa_m'))

old = json.load(open(OUT, encoding='utf8')) if os.path.exists(OUT) else {}
old.update(report)
json.dump(old, open(OUT, 'w', encoding='utf8'), indent=1)
