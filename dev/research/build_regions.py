#!/usr/bin/env python3
"""Build regions/<id>.js for the flight path map from the research JSON files."""
import json, math, os, sys, statistics, html

S = os.path.dirname(os.path.abspath(__file__))
OUT = '/home/claude/tullamarine-flight-map/regions'
esc = lambda t: html.escape(str(t), quote=False)

def load(f):
    return json.load(open(os.path.join(S, f)))

CONF = {
 'nsw': dict(sub=['nsw_a.json', 'nsw_b.json'], infra=('nsw_infra.json', 'nsw'), bbox=[-34.12, 150.62, -33.62, 151.28],
   stateAdj='NSW', suffix=', New South Wales', slug='nsw',
   title='Sydney Flight Path Map', lede="See how much plane noise any street in Sydney gets, today and once Western Sydney International Airport starts passenger flights. You can also see train lines, motorways and data centres, existing and planned.",
   airports={'YSSY': dict(chip='Sydney (Mascot)'),
             'YSWS': dict(model='jets', chip='Western Sydney (Badgerys Creek)', short='Western Sydney Airport', label='Western Sydney International', era='future', dropRefs=['05R'], depKm=22),
             'YSBK': dict(model='none', near=(4, "About {d} km from Bankstown Airport, a busy training and light-aircraft airport. Small planes and helicopters circle here most days, and they aren't in this estimate.")),
             'YSCN': dict(model='none', near=(4, "About {d} km from Camden Airport, used by light aircraft and gliders. They aren't in this estimate.")),
             'YSRI': dict(model='none', near=(6, "About {d} km from RAAF Base Richmond. Air Force C-130J transport planes train here, sometimes at night, and aren't in this estimate."))},
   future=dict(label='After Western Sydney Airport opens (Oct 2026)', short='After WSI opens', mode='After Western Sydney Airport opens', legend='Western Sydney Airport paths (from Oct 2026)'),
   railPlanSub='Airport metro, Metro West, Bankstown line', roadPlanSub='M6, Western Harbour Tunnel, Outer Sydney Orbital',
   listTitle='Best suburbs to consider', thresholds=dict(rising=1.5e6, premium=2.0e6, entry=900000, budget=1.1e6),
   ramps=dict(price=dict(cuts=[900000,1200000,1600000,2200000], words=['Under $900k','$900k–1.2m','$1.2m–1.6m','$1.6m–2.2m','Over $2.2m']),
              dollar=dict(cuts=[-100000,0,75000,150000], words=['Down $100k+','Down','Up to $75k','Up $75k–150k','Up $150k+']))),
 'qld': dict(sub=['qld.json'], infra=('qld_infra.json', 'qld'), bbox=[-27.72, 152.85, -27.05, 153.3],
   stateAdj='Queensland', suffix=', Queensland', slug='qld',
   title='Brisbane Flight Path Map', lede="See how much plane noise any street in Brisbane gets from both of Brisbane Airport's parallel runways. You can also see train lines, motorways and data centres, existing and planned.",
   airports={'YBBN': dict(chip='Brisbane Airport'),
             'YBAF': dict(model='none', near=(4, "About {d} km from Archerfield Airport, a busy training and light-aircraft airport. Small planes and helicopters circle here most days, and they aren't in this estimate.")),
             'YAMB': dict(model='none', near=(12, "About {d} km from RAAF Base Amberley. Super Hornet and Growler fighter jets fly from here and are much louder than airliners when they pass. They aren't in this estimate."))},
   future=None, railPlanSub='Cross River Rail, faster rail to the Gold and Sunshine Coasts', roadPlanSub='Coomera Connector, Bruce Highway upgrade',
   listTitle='Best suburbs to consider', thresholds=dict(rising=1.1e6, premium=1.5e6, entry=750000, budget=850000),
   ramps=dict(price=dict(cuts=[750000,950000,1200000,1600000], words=['Under $750k','$750k–950k','$950k–1.2m','$1.2m–1.6m','Over $1.6m']))),
 'wa': dict(sub=['wa.json'], infra=('wa_infra.json', 'wa'), bbox=[-32.36, 115.72, -31.6, 116.12],
   stateAdj='WA', suffix=', Western Australia', slug='wa',
   title='Perth Flight Path Map', lede="See how much plane noise any street in Perth gets, today and once Perth Airport's new parallel runway opens. You can also see train lines, highways and data centres, existing and planned.",
   airports={'YPPH': dict(chip='Perth Airport', futureRefs={'03': ['03L', '21R']}),
             'YPJT': dict(model='none', near=(5, "About {d} km from Jandakot Airport, one of Australia's busiest pilot-training airports. Small planes circle overhead most of the day, and they aren't in this estimate.")),
             'YPEA': dict(model='none', near=(10, "About {d} km from RAAF Base Pearce, where Air Force pilots train in PC-21 and Hawk jets. They aren't in this estimate."))},
   future=dict(label="After the new runway opens (2028)", short='After 2028', mode='After 2028, new parallel runway', legend='New runway paths (2028)'),
   railPlanSub='METRONET lines (most now open)', roadPlanSub='Tonkin Highway extension, EastLink WA',
   listTitle='Best suburbs to consider', thresholds=dict(rising=900000, premium=1.3e6, entry=650000, budget=750000)),
 'sa': dict(sub=['sa.json'], infra=('sa_infra.json', 'sa'), bbox=[-35.3, 138.45, -34.58, 138.9],
   stateAdj='SA', suffix=', South Australia', slug='sa',
   title='Adelaide Flight Path Map', lede="See how much plane noise any street in Adelaide gets from Adelaide Airport. You can also see train lines, motorways and data centres, existing and planned.",
   airports={'YPAD': dict(chip='Adelaide Airport'),
             'YPPF': dict(model='none', near=(4, "About {d} km from Parafield Airport, a busy pilot-training airport. Small planes circle overhead most of the day, and they aren't in this estimate.")),
             'YPED': dict(model='none', near=(6, "About {d} km from RAAF Base Edinburgh, home of the Air Force's P-8 maritime patrol jets. They aren't in this estimate."))},
   future=None, railPlanSub='Aldinga rail extension (corridor only)', roadPlanSub='North–South Corridor tunnels (T2D), South Eastern Freeway',
   listTitle='Best suburbs to consider', thresholds=dict(rising=900000, premium=1.3e6, entry=650000, budget=750000)),
 'tas': dict(sub=['tas.json'], infra=('small_infra.json', 'tas'), bbox=[-43.02, 147.2, -42.68, 147.6],
   stateAdj='Tasmanian', suffix=', Tasmania', slug='tas',
   title='Hobart Flight Path Map', lede="See how much plane noise any street in Hobart gets from Hobart Airport. You can also see roads, transport plans and data centres.",
   airports={'YMHB': dict(chip='Hobart Airport'),
             'YCBG': dict(model='none', near=(3, "About {d} km from Cambridge Aerodrome, used by light aircraft, flying schools and scenic flights. They aren't in this estimate."))},
   future=None, railPlanSub='Northern Suburbs rapid bus corridor', roadPlanSub='Southern Outlet, Tasman Highway causeways',
   listTitle='Best suburbs to consider', thresholds=dict(rising=800000, premium=1.1e6, entry=600000, budget=700000)),
 'act': dict(sub=['act.json'], infra=('small_infra.json', 'act'), bbox=[-35.5, 148.98, -35.15, 149.22],
   stateAdj='ACT', suffix=', Australian Capital Territory', slug='act',
   title='Canberra Flight Path Map', lede="See how much plane noise any street in Canberra gets from Canberra Airport. You can also see light rail, roads and data centres, existing and planned.",
   airports={'YSCB': dict(chip='Canberra Airport')},
   future=None, railPlanSub='Light rail to Woden, later Belconnen', roadPlanSub='Monaro Highway, Athllon Drive, William Hovell Drive',
   listTitle='Best suburbs to consider', thresholds=dict(rising=1.0e6, premium=1.3e6, entry=750000, budget=850000)),
 'nt': dict(sub=['nt.json'], infra=('small_infra.json', 'nt'), bbox=[-12.6, 130.8, -12.33, 131.15],
   stateAdj='NT', suffix=', Northern Territory', slug='nt',
   title='Darwin Flight Path Map', lede="See how much plane noise any street in Darwin and Palmerston gets from Darwin Airport, which is shared with RAAF Base Darwin. You can also see roads, projects and data centres.",
   airports={'YPDN': dict(chip='Darwin Airport', near=(6, "Darwin Airport is shared with RAAF Base Darwin. Fighter jets (F-35s and visiting aircraft during exercises) are far louder than airliners and aren't in this estimate, which covers airline jets only. Check Defence's noise forecast (ANEF) for this address."))},
   future=None, railPlanSub='', roadPlanSub='Roystonea Avenue, Tiger Brennan Drive',
   listTitle='Best suburbs to consider', thresholds=dict(rising=700000, premium=1.0e6, entry=500000, budget=600000)),
}

D2R = math.pi / 180
def mk_local(lon0, lat0):
    KX = 111.320 * math.cos(lat0 * D2R); KY = 110.574
    return (lambda lon, lat: ((lon - lon0) * KX, (lat - lat0) * KY))

def brg(a, b, toL):
    ax, an = toL(*a); bx, bn = toL(*b)
    return (math.degrees(math.atan2(bx - ax, bn - an)) + 360) % 360

def angdiff(a, b):
    return abs(((a - b) + 540) % 360 - 180)

def refnum(r):
    return int(''.join(c for c in r if c.isdigit()) or 0)

def fix_runway(rw, toL, warn):
    """Make ends[0] the threshold of refs[0] (planes landing on refs[0] travel towards ends[1])."""
    b = brg(rw['ends'][0], rw['ends'][1], toL)
    want = refnum(rw['refs'][0]) * 10
    if angdiff(b, want) > 40 and angdiff((b + 180) % 360, want) <= 40:
        rw['ends'] = [rw['ends'][1], rw['ends'][0]]; warn.append(f"swapped ends of {rw['refs']}")
    elif angdiff(b, want) > 40:
        warn.append(f"runway {rw['refs']} bearing {b:.0f} vs {want} ?")
    return rw

def js(v):
    return json.dumps(v, ensure_ascii=False)

def build(rid):
    c = CONF[rid]; warn = []
    inf = load(c['infra'][0])[c['infra'][1]]
    ma = inf['mainAirport']
    lon0, lat0 = ma['lng'], ma['lat']
    toL = mk_local(lon0, lat0)
    # ---------- airports ----------
    airports = []; model_pts = []
    def add_rw(ap_conf, rws, era_all, keyp, futureRefs=None):
        out = []
        for i, r in enumerate(rws):
            if ap_conf.get('dropRefs') and r['refs'][0] in ap_conf['dropRefs']:
                continue
            r = fix_runway({'refs': r['refs'], 'ends': r['ends']}, toL, warn) | {k: r[k] for k in ('plain', 'era') if k in r}
            o = {'key': f"{keyp}-{i}", 'refs': r['refs'], 'ends': [[round(x, 6) for x in e] for e in r['ends']],
                 'era': 'future' if era_all == 'future' else (r.get('era') or 'both'), 'plain': r.get('plain') or f"runway {r['refs'][0]}/{r['refs'][1]}"}
            if futureRefs and r['refs'][0] in futureRefs:
                o['futureRefs'] = futureRefs[r['refs'][0]]
            out.append(o)
        return out
    mc = c['airports'][ma['icao']]
    mrw = add_rw(mc, ma['runways'], 'both', ma['icao'].lower(), mc.get('futureRefs'))
    for r in mrw:
        # shorten the plain names: keep the first clause
        r['plain'] = r['plain'].split(' (')[0].split(';')[0].strip()
        r['plain'] = r['plain'].replace('main (only) runway, north-west to south-east', 'runway')
        model_pts += r['ends']
    main = {'icao': ma['icao'], 'name': ma['name'].split(' / ')[0], 'label': ma['short'], 'short': ma['short'], 'chip': mc.get('chip', ma['short']),
            'lng': lon0, 'lat': lat0, 'main': True, 'toggle': True, 'ac': None, 'arrKm': 26, 'depKm': None, 'fans': [-40, 0, 40], 'era': 'both',
            'fallbackRing': [[round(2.2 * math.cos(a / 12 * 2 * math.pi), 2), round(2.2 * math.sin(a / 12 * 2 * math.pi), 2)] for a in range(12)],
            'runways': mrw}
    if mc.get('near'):
        main['nearNote'] = {'km': mc['near'][0], 'text': mc['near'][1]}
    airports.append(main)
    for o in inf['otherAirports']:
        oc = c['airports'].get(o['icao'])
        if not oc:
            warn.append('skip airport ' + o['icao']); continue
        if oc.get('model') == 'jets':
            rws = add_rw(oc, o.get('runways', []), oc.get('era', 'both'), o['icao'].lower())
            for r in rws:
                model_pts += r['ends']
            a = {'icao': o['icao'], 'name': o['name'].split(' (')[0], 'label': oc.get('label', o['name'].split(' (')[0]), 'short': oc.get('short', o['name']),
                 'chip': oc.get('chip', o['name']), 'lng': o['lng'], 'lat': o['lat'], 'main': False, 'toggle': True, 'ac': None,
                 'arrKm': 26, 'depKm': oc.get('depKm', 22), 'era': oc.get('era', 'both'), 'runways': rws}
        else:
            a = {'icao': o['icao'], 'name': o['name'], 'label': o['name'], 'short': o['name'], 'lng': o['lng'], 'lat': o['lat'],
                 'main': False, 'toggle': False, 'noModel': True, 'era': 'both', 'runways': []}
        if oc.get('near'):
            a['nearNote'] = {'km': oc['near'][0], 'text': oc['near'][1]}
        airports.append(a)
    # ---------- grid covering all modelled paths ----------
    xs, ns = [], []
    for (lon, lat) in model_pts:
        x, n = toL(lon, lat); xs += [x - 30, x + 30]; ns += [n - 30, n + 30]
    x0, x1, n0, n1 = min(xs), max(xs), min(ns), max(ns)
    step = 0.35
    while ((x1 - x0) / step) * ((n1 - n0) / step) > 42000:
        step += 0.05
    grid = {'x0': round(x0, 2), 'n1': round(n1, 2), 'cols': int((x1 - x0) / step) + 1, 'rows': int((n1 - n0) / step) + 1, 'step': round(step, 2)}
    # ---------- suburbs ----------
    subs = []; csrc = None
    for f in c['sub']:
        d = load(f); csrc = csrc or d['crimeSource']; subs += d['suburbs']
    CR, PR, SC, MALLS, GROW, FLAGS = {}, {}, [], {}, [], {}
    seen = set()
    for s in subs:
        k = s['name'].lower().strip()
        if k in seen:
            continue
        seen.add(k)
        cr = s.get('crime')
        if cr and cr.get('offences') is not None:
            row = [cr['offences'], cr.get('population'), cr.get('person'), cr.get('property')]
            if cr.get('area'):
                row.append(cr['area'])
            CR[k] = row
        p = s.get('prop')
        if p and p.get('median') and p.get('growth') is not None:
            PR[k] = [p['median'], p['growth'], p.get('yield'), p.get('rent')]
        for sc in (s.get('schools') or []):
            if len(sc) >= 4 and isinstance(sc[3], (int, float)):
                SC.append([sc[0], s['name'], sc[1] if sc[1] in 'psc' else 's', sc[2] if sc[2] in 'gci' else 'g', sc[3]])
        if s.get('mall'):
            MALLS[k] = s['mall']
        if s.get('growthArea'):
            GROW.append(k)
    # typical crimes against people
    pr_rates = [r[2] / r[1] * 1000 for r in CR.values() if r[1] and r[1] >= 3000 and r[2] is not None]
    typical = round(statistics.median(pr_rates), 1) if pr_rates else None
    # ---------- infra ----------
    plans = []
    for p in inf['plans']:
        coords = p.get('coords') or p.get('line') or []
        if p['kind'] not in ('rail', 'road') or len(coords) < 2:
            continue
        plans.append({'kind': p['kind'], 'cert': p['cert'], 'name': p['name'], 'status': p['status'], 'about': p['about'], 'url': p.get('url', ''), 'coords': coords})
    hubs = [h[:4] for h in inf.get('railHubs', [])]
    import re
    dcs = []
    for d in inf['dataCentres']:
        addr = re.sub(r'\s+(NSW|QLD|WA|SA|TAS|ACT|NT|VIC)(\s+\d{4})?$', '', d[2].strip())
        row = [d[0], d[1], addr, 'plan' if d[3] == 'plan' else 'live']
        if len(d) > 4 and d[4]:
            row.append(d[4])
        dcs.append(row)
    city = inf['city']
    mk = inf['market']
    market = None
    if mk.get('month'):
        t = mk['text']
        market = {'html': f"<b>Market right now:</b> {esc(t)} The suburb figures on this map cover the 12 months to June 2026, so today's prices may differ.",
                  'cardFlag': f"Since June: {t}"}
    v = inf['view']
    view = {'center': v['center'], 'zoom': round(v['zoom'] + 0.7, 1), 'pitch': 58, 'bearing': -20}
    top = {'center': v['center'], 'zoom': v['zoom']}
    dh = inf['defaultHome']
    tb = inf['tallBuilding'].split(' (')[0].replace(' tall', '')
    bb = c['bbox']
    geobox = f"{bb[1]-0.3},{bb[2]+0.3},{bb[3]+0.3},{bb[0]-0.3}"
    # ---------- notes ----------
    other_txt = []
    for a in airports[1:]:
        if a.get('noModel'):
            other_txt.append(f"{a['name']} is outlined only. Its aircraft aren't in the noise estimate, so a note appears on nearby spots instead.")
        else:
            other_txt.append(f"{a['name']} uses the same jet figures as {main['short']}.")
    if rid == 'nt':
        other_txt.append("Darwin Airport is shared with RAAF Base Darwin. This map models airline jets only. Military fighter jets are much louder and fly less predictable patterns, so check Defence's ANEF noise forecast for any address.")
    if rid == 'nsw':
        other_txt.append("Western Sydney International's paths are drawn as simple straight-in approaches and departures on its runway. The official design sends most daytime landings in from the north-east and, at night, both landings and take-offs over the less-populated south-west. Check the official flight path tool for the exact tracks.")
    lvl = csrc.get('level')
    crime_note = f"Crime: {esc(csrc['name'])}, {esc(csrc['period'])}."
    if lvl == 'suburb':
        crime_note += " Offences are divided by each suburb's 2021 census population."
        if csrc.get('stateRatePer1000'):
            crime_note += f" \"All crime\" is compared with the {esc(c['stateAdj'])} average of about {round(csrc['stateRatePer1000'])} offences per 1,000 people."
        if typical:
            crime_note += f" \"Crimes against people\" is compared with the typical suburb on this map, about {round(typical)} per 1,000."
        crime_note += " Big shopping centres, nightlife strips, fast-growing estates and suburbs with very few residents can make the figures look worse than the streets are, and the map flags these cases."
    else:
        crime_note += f" Police here only publish figures for large areas ({esc(lvl)} level), not suburb by suburb, so the cards show the whole area's figures and the crime layer doesn't colour suburbs."
    if csrc.get('notes') and lvl != 'suburb':
        pass
    links = ''.join(f'<li><a href="{esc(u)}" target="_blank" rel="noopener">{esc(t)}</a></li>' for t, u in inf.get('links', [])[:14])
    links += f'<li><a href="{esc(ma.get("noiseUrl",""))}" target="_blank" rel="noopener">{esc(main["short"])} noise and flight path information</a></li>'
    links += f'<li><a href="{esc(csrc["url"])}" target="_blank" rel="noopener">Crime figures: {esc(csrc["name"].split(" (")[0])}</a></li>'
    links += f'<li><a href="https://www.yourinvestmentpropertymag.com.au/top-suburbs/{c["slug"]}" target="_blank" rel="noopener">Your Investment Property: suburb data (CoreLogic)</a></li>'
    links += '<li><a href="https://schoolrank.com.au/" target="_blank" rel="noopener">SchoolRank (NAPLAN-based scores)</a></li>'
    links += f'<li><a href="{esc(inf["schoolZoneUrl"])}" target="_blank" rel="noopener">School zones and local intake areas</a></li>'
    if mk.get('url'):
        links += f'<li><a href="{esc(mk["url"])}" target="_blank" rel="noopener">Cotality Home Value Index</a></li>'
    notes = f"""
        <p class="note">Plane noise: for every spot, the map works out how close each flight path passes and how high the plane is there. It then looks up how loud that plane sounds on the ground, using published measurements from NATS, the UK air traffic service. The loudness words match common measures. "Loud" starts where a plane interrupts a conversation indoors with the windows open, the level airports track as N70. Ten points louder sounds about twice as loud.</p>
        <p class="note">{esc(main['short'])}: {esc(ma.get('curfew',''))}. {esc(' '.join(other_txt))}</p>
        <p class="note">Switching an airport off hides its flight paths, planes and noise shading. Suburb rankings and spot checks always include every airport, because you'll hear them all.</p>
        <p class="note">It shows the loudest single plane, not how many fly over each day, which changes with the wind. Flight paths are simplified to straight-in approaches and fanned departures, so treat the results as a guide and check the airport's own flight path tool for the exact address.</p>
        <p class="note">Suburbs, airport boundaries, today's runways, train lines, stations and highways come from OpenStreetMap. Planned train lines and roads are drawn from public announcements. Where the exact route isn't public, the line is marked as approximate. Data centres come from OpenStreetMap, Data Center Map and 2026 news, with locations found from their street addresses.</p>
        <p class="note">{crime_note}</p>
        <p class="note">Property: median house price, price change over the 12 months to June 2026, and gross rental yield (a year's rent as a share of the price). The figures are from CoreLogic, as published suburb by suburb on Your Investment Property. Suburbs with few house sales can swing a lot. Past growth doesn't guarantee future growth. This isn't financial advice.</p>
        <p class="note">Schools: scores out of 100 from SchoolRank, which compares each school's NAPLAN results with the national average for the same year level. About 50 is average. Kindergartens, TAFEs and universities are shown from OpenStreetMap without ratings. Scores reflect test results, which are shaped partly by the families a school serves, so visit and check the school's zone or intake area.</p>
        <p class="note">Check the exact address before buying:</p>
        <ul class="links">{links}</ul>
"""
    R = {
        'id': rid, 'abbr': inf['abbr'], 'stateName': inf['stateName'], 'stateAdj': c['stateAdj'], 'city': city, 'cachePrefix': rid + ':',
        'title': c['title'], 'lede': esc(c['lede']),
        'origin': [lon0, lat0], 'view': view, 'focusView': None, 'topView': top,
        'bbox': bb, 'grid': grid, 'geocode': {'viewbox': geobox, 'suffix': c['suffix']},
        'airports': airports, 'future': c['future'],
        'tallBuilding': tb, 'defaultRef': {'lng': dh['lng'], 'lat': dh['lat'], 'title': dh['title'].split(' (')[0]},
        'listTitle': c['listTitle'], 'listNoun': 'suburbs',
        'crime': {'data': CR, 'stateRate': csrc.get('stateRatePer1000') or 0, 'typicalPerson': typical or 0, 'typicalPersonWord': 'a typical suburb on this map',
                  'period': csrc['period'], 'flags': FLAGS, 'malls': MALLS, 'growth': GROW},
        'prop': {'data': PR, 'period': '12 months to June 2026', 'thresholds': c.get('thresholds', {}), **({'ramps': c['ramps']} if c.get('ramps') else {})},
        'market': market,
        'schools': {'data': SC, 'zoneSite': inf['schoolZoneUrl'].split('//')[-1].split('/')[0]},
        'plans': plans, 'railHubs': hubs, 'railHubNote': 'a station on a new or upgraded line',
        'dcs': dcs, 'dcSource': 'Data Center Map', 'dcPlanSource': '2025–2026 planning news / Data Center Map',
        'fallbackSubs': [],
        'text': {'aptLandSub': ', '.join(a['short'] if a.get('main') else a['name'] for a in airports),
                 'railPlanSub': c['railPlanSub'], 'roadPlanSub': c['roadPlanSub'], 'addrPlaceholder': 'e.g. 12 Smith St, ' + (dh['title'].split(' (')[0]), 'notes': notes},
        'meta': {'crimeLevel': lvl, 'counts': {'suburbs': len(seen), 'crime': len(CR), 'prop': len(PR), 'schools': len(SC)}}
    }
    if not R['crime']['stateRate'] and lvl == 'suburb':
        warn.append('no state crime rate')
    src = f"// {inf['stateName']} ({city}) region for the flight path map engine in ../index.html.\n// Generated from research files; field docs: regions/_schema.md\nwindow.REGION={js(R)};\n"
    open(os.path.join(OUT, rid + '.js'), 'w').write(src)
    print(rid, R['meta']['counts'], 'grid', grid, 'typicalPerson', typical, 'plans', len(plans), 'dcs', len(dcs), 'airports', [(a['icao'], len(a['runways'])) for a in airports], 'warn', warn)

for rid in (sys.argv[1:] or CONF.keys()):
    build(rid)
