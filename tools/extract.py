import sys, re, json
sys.path.insert(0, '.')
import panel as _pm

def strip_tags(h):
    h = re.sub(r'<br\s*/?>', ' ', h)
    h = re.sub(r'<[^>]+>', '', h)
    h = h.replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
    return re.sub(r'\s+', ' ', h).strip()

def chips_of(*hs):
    out = []
    for h in hs:
        out += re.findall(r'\[\[(.+?)\]\]', h or '')
    return out

def run(kind):
    srcfile = 'book.py' if kind == 'doom' else 'book_stock.py'
    book = open('book.py').read()
    src = open(srcfile).read()
    ns = {}
    first = re.search(r'^# -+ PAGE 1', src, re.M).start()
    exec(src[:first], ns)          # helpers (card/tbl/panel/H/P/T)
    _pm.DISP_SUB = '' if kind == 'stock' else 'DOOM OS grid'
    records = []
    cur = {'page': 0}
    ocard, otbl = ns['card'], ns['tbl']
    def card(title, hl, crops, body, span=1):
        records.append(dict(page=cur['page'], kind='card', title=title,
                            hl={k: [v[0], v[1]] for k, v in hl.items()}, crops=[crops] if isinstance(crops, str) else list(crops), body=body))
        return ocard(title, hl, crops, body, span)
    def tbl(head, rows, cls=""):
        records.append(dict(page=cur['page'], kind='table', head=head, rows=rows))
        return otbl(head, rows, cls)
    ns['card'], ns['tbl'] = card, tbl
    # run page blocks in order
    pat = r'(?m)^# -+ PAGE (\d)[^\n]*'
    marks = [(m.start(), m.end(), int(m.group(1))) for m in re.finditer(pat, src)]
    endpos = src.index('pages = [') if kind == 'doom' else src.index('pages = [')
    if kind == 'stock':
        ns['page'] = lambda *a, **k: ''   # not needed
        ns['chips'] = ns['chips']
    for i, (s, e, n) in enumerate(marks):
        block = src[e: (marks[i+1][0] if i + 1 < len(marks) else endpos)]
        cur['page'] = n
        exec(block, ns)
    calls = re.findall(r'page\((\d), "(.*?)", "(.*?)", (p\d)\)', src[src.index('pages = ['):])
    sections = []
    for n, title, sub, var in calls:
        n = int(n); inner = ns[var]
        sec = dict(n=n, title=title, sub=sub, entries=[])
        # cards and tables in order of creation
        for rec in [r for r in records if r['page'] == n]:
            if rec['kind'] == 'card':
                sec['entries'].append(dict(type='card', title=rec['title'], hl=rec['hl'], crops=rec['crops'],
                                           body=rec['body'], chips=chips_of(rec['body'])))
            else:
                head = rec['head']; rows = rec['rows']; ncol = len(head)
                title = strip_tags(head[0]).rstrip(' +') if ncol != 4 else 'Shortcuts'
                grp = dict(type='group', title=None, rows=[])
                if ncol == 2:
                    grp['title'] = strip_tags(head[0]); labels = (head[0], head[1])
                    for r in rows: grp['rows'].append(dict(name=r[0], input=r[1], result='' , chips=chips_of(r[1])) if False else dict(name=r[0], input='', result=r[1], chips=chips_of(r[0], r[1])))
                elif ncol == 3:
                    grp['title'] = strip_tags(head[0])
                    for r in rows: grp['rows'].append(dict(name=r[0], input=r[1], result=r[2], chips=chips_of(r[0], r[1], r[2])))
                elif ncol == 4:
                    shiftmode = strip_tags(head[0]).startswith('SHIFT')
                    grp['title'] = 'SHIFT + button' if shiftmode else 'Master shortcut table'
                    for r in rows:
                        for a, b in ((0, 1), (2, 3)):
                            if shiftmode: nm, inp = r[b], '[[SHIFT]] + ' + r[a]; res = ''
                            else: nm, inp, res = r[a], r[b], ''
                            grp['rows'].append(dict(name=nm, input=inp, result=res, chips=chips_of(nm, inp, res)))
                sec['entries'].append(grp)
        for m in re.finditer(r'<div class="box(?: small)?"><h2>(.*?)</h2>(.*?)</div>', inner, re.S):
            t = m.group(1)
            if t == 'Booklet map': continue
            body = m.group(2).strip()
            sec['entries'].append(dict(type='note', title=t, body=body, chips=chips_of(body)))
        if 'class="pg4"' in inner:
            used = sorted(ns.get('USED', []))
            sec['entries'].append(dict(type='pads', title='Pad SHIFT functions', labels=ns['PADSH'], used=used, chips=[f'pad {i+1}' for i in range(16)]))
        sections.append(sec)
    return dict(id=kind, sections=sections)

out = []
for k, name, sub in (('doom', 'DOOM OS', 'Klangfeld Labs DOOM OS 0.7 on the SP-404MKII'), ('stock', 'Stock OS', 'Roland SP-404MKII firmware v4.00')):
    g = run(k); g['name'] = name; g['sub'] = sub
    n = sum(len(s['entries']) for s in g['sections'])
    print(k, [(s['n'], s['title'], len(s['entries'])) for s in g['sections']])
    out.append(g)
elems = [dict(id=e[0], kind=e[1], cx=e[2], cy=e[3], w=e[4], h=e[5], label=e[6], sub=e[7]) for e in _pm.ELEMS]
json.dump(dict(guides=out, elems=elems, crops=_pm.CROPS), open('../build/data.json', 'w'), ensure_ascii=False)
print('json bytes', len(json.dumps(out, ensure_ascii=False)))
payload = json.load(open('../build/data.json'))
open('../docs/data.js', 'w').write('window.DATA = ' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + ';\n')
print('wrote ../docs/data.js')
