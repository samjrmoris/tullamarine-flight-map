"""Apply fact-check results (dev/research/audit/<file>.json) to a state's infra JSON.

Rules (evidence only, nothing guessed):
- data centres: verdict remove / status cancelled or 'not a data centre' -> dropped; status live/plan taken
  from the audit; exact [lon,lat] taken when the audit found one (stored as element 5, so the map skips
  geocoding); a corrected street address is taken when the audit verdict is fix and the address is a
  single, confirmed address. MANUAL may rename, skip or add entries.
- missing data centres: added unless listed in MANUAL[id]['skipMissing'].
- plans: fix_points replace the drawn line; cert taken from the audit; status from MANUAL only.
- rail hubs: corrected [lon,lat] when verdict is fix.
Usage: python dev/research/apply_audit.py <id> <audit file> [more audit files]
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
R = os.path.join(ROOT, 'dev', 'research')
INFRA = {'nsw': 'nsw_infra.json', 'qld': 'qld_infra.json', 'wa': 'wa_infra.json', 'sa': 'sa_infra.json',
         'tas': 'small_infra.json', 'act': 'small_infra.json', 'nt': 'small_infra.json'}

# Judgement calls, each from the audit text (see the audit json for sources).
MANUAL = json.load(open(os.path.join(R, 'audit', 'manual_fixes.json'), encoding='utf8'))


def shaky(addr):
    return not addr or re.search(r'unconfirmed|per a search|not published|no street|lot not|;|several|\bor\b', addr, re.I)


def main(rid, files):
    path = os.path.join(R, INFRA[rid])
    whole = json.load(open(path, encoding='utf8'))
    inf = whole[rid] if rid in whole and isinstance(whole[rid], dict) else whole
    man = MANUAL.get(rid, {})
    audit = {}
    for f in files:
        for k, v in json.load(open(os.path.join(R, 'audit', f), encoding='utf8')).items():
            if isinstance(v, list):
                audit.setdefault(k, []).extend(v)
    log = []
    # ---- data centres: audit entries are in the same order as ours, matched by index (checked by name)
    dcs = inf['dataCentres']
    keep = []
    byname = {a['name']: a for a in audit.get('dataCentres', [])}
    for i, d in enumerate(dcs):
        a = man.get('dcMatch', {}).get(d[0])
        a = byname.get(a) if a else byname.get(d[0])
        if a is None:
            cands = [x for x in audit.get('dataCentres', []) if x['name'].split(' (')[0].lower() in d[0].lower() or d[0].split(' (')[0].lower() in x['name'].lower()]
            a = cands[0] if len(cands) == 1 else None
        if a is None:
            if audit.get('dataCentres'):
                log.append('dc NOT IN AUDIT (kept): ' + d[0])
            keep.append(d); continue
        st = (a.get('status') or '').lower()
        if a.get('verdict') == 'remove' or st in ('cancelled', 'not a data centre') or d[0] in man.get('removeDcs', []):
            log.append('dc REMOVED: %s (%s)' % (d[0], st or a.get('verdict'))); continue
        d = list(d) + [''] * (5 - len(d))
        if st in ('live', 'plan') and st != d[3]:
            log.append('dc status %s -> %s: %s' % (d[3], st, d[0])); d[3] = st
        if a.get('verdict') == 'fix' and not shaky(a.get('address')) and a['address'] != d[2] and d[0] not in man.get('keepAddress', []):
            log.append('dc address: %s: "%s" -> "%s"' % (d[0], d[2], a['address'])); d[2] = a['address']
        if d[0] in man.get('status', {}):
            log.append('dc status (manual) -> %s: %s' % (man['status'][d[0]], d[0])); d[3] = man['status'][d[0]]
        if d[0] in man.get('renameDcs', {}):
            log.append('dc renamed: %s -> %s' % (d[0], man['renameDcs'][d[0]])); d[0] = man['renameDcs'][d[0]]
        if d[0] in man.get('operators', {}):
            d[1] = man['operators'][d[0]]
        if d[0] in man.get('dcNotes', {}):
            d[4] = man['dcNotes'][d[0]]
        ll = None if d[0] in man.get('noCoords', []) else a.get('lnglat')
        if ll and not re.search(r'suburb|centroid of suburb|street only', a.get('coord_method') or '', re.I):
            d = d[:5] + [[round(ll[0], 5), round(ll[1], 5)]]
        keep.append(d)
    for m in audit.get('dataCentresMissing', []):
        if m['name'] in man.get('skipMissing', []):
            continue
        ll = m.get('lnglat') if not re.search(r'street only|street centre|suburb', m.get('coord_method') or '', re.I) else None
        if not ll and shaky(m.get('address')):
            log.append('missing dc SKIPPED (no confirmed address): ' + m['name']); continue
        row = [man.get('renameMissing', {}).get(m['name'], m['name']), m.get('operator', ''), m.get('address', ''),
               'plan' if m.get('status') == 'plan' else 'live', man.get('dcNotes', {}).get(m['name'], '')]
        if ll:
            row.append([round(ll[0], 5), round(ll[1], 5)])
        keep.append(row); log.append('dc ADDED: ' + row[0])
    for row in man.get('addDcs', []):
        keep.append(row); log.append('dc ADDED (manual): ' + row[0])
    inf['dataCentres'] = keep
    # ---- plans
    pl = {p['name']: p for p in inf['plans']}
    for a in audit.get('plans', []):
        p = pl.get(man.get('planMatch', {}).get(a['name'], a['name']))
        if p is None:
            cands = [p for n, p in pl.items() if n.split(' (')[0].lower() in a['name'].lower() or a['name'].split(' (')[0].lower() in n.lower()]
            p = cands[0] if len(cands) == 1 else None
        if p is None:
            log.append('plan NOT MATCHED: ' + a['name']); continue
        if a.get('fix_points') and len(a['fix_points']) >= 2:
            p.pop('coords', None); p['line'] = [[round(x, 5), round(y, 5)] for x, y in a['fix_points']]
            log.append('plan line replaced (%d pts): %s' % (len(p['line']), p['name']))
        if a.get('cert') in ('route', 'approx', 'concept') and a['cert'] != p.get('cert'):
            log.append('plan cert %s -> %s: %s' % (p.get('cert'), a['cert'], p['name'])); p['cert'] = a['cert']
    for name, st in man.get('planStatus', {}).items():
        pl[name]['status'] = st; log.append('plan status: %s -> %s' % (name, st))
    for name, u in man.get('planUrl', {}).items():
        pl[name]['url'] = u; log.append('plan url: ' + name)
    for name, ab in man.get('planAbout', {}).items():
        pl[name]['about'] = ab; log.append('plan about: ' + name)
    # ---- rail hubs
    hubs = inf.get('railHubs', [])
    for a in audit.get('railHubs', []):
        if a.get('verdict') != 'fix' or not a.get('lnglat'):
            continue
        h = [h for h in hubs if h[2].split(' (')[0].lower() == a['name'].split(' (')[0].lower()]
        if len(h) != 1:
            log.append('hub NOT MATCHED: ' + a['name']); continue
        h[0][0], h[0][1] = round(a['lnglat'][0], 5), round(a['lnglat'][1], 5); log.append('hub moved: ' + a['name'])
    for k, v in man.get('set', {}).items():
        inf[k] = v; log.append('set %s = %s' % (k, str(v)[:80]))
    json.dump(whole, open(path, 'w', encoding='utf8'), ensure_ascii=False, indent=1)
    print('\n'.join(log))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2:])
