import sys, re
sys.path.insert(0, '.')
import panel as _pm
kind, out = sys.argv[1], sys.argv[2]
_pm.set_theme('dracula')
if kind == 'stock': _pm.DISP_SUB = ''
srcfile = 'book.py' if kind == 'doom' else 'book_stock.py'
src = open(srcfile).read()
ns = {}
code = src[:src.index("pages = [")]
if kind == 'stock':
    code = code.replace("import panel as _pm; _pm.DISP_SUB = ''\n", "")   # keep our theme-set module
exec(code, ns)
calls = re.findall(r'page\((\d), "(.*?)", "(.*?)", (p\d)\)', src[src.index("pages = ["):])
pages = [ns['page'](int(n), t, s, ns[v]) for n, t, s, v in calls]
DARK = '''
html,body { background:#282a36; color:#f8f8f2 }
.page { background:#282a36 }
header { border-bottom-color:#bd93f9 }
header h1 { color:#f8f8f2 }
header p { color:#bd93f9 }
.pg { color:#bfc3d9 } .pg b { color:#f8f8f2 }
footer { color:#a3abcf; border-top-color:#44475a }
h2 { color:#ff79c6 } h2.sec { border-bottom-color:#44475a }
h3 { color:#8be9fd }
.k { background:#44475a; color:#f8f8f2; border-color:#6272a4 }
th .k { background:#282a36 }
.card, .box { background:#21222c; border-color:#44475a }
.pn { border-color:#44475a }
.warn { background:#21222c; border-color:#44475a }
th { background:#44475a; color:#f8f8f2 }
td { border-bottom-color:#44475a }
.cap { color:#a3abcf }
.pc { background:#21222c; border-color:#6272a4 }
.pc.u { background:#44475a; border-color:#ffb86c }
.sw { border-color:#f8f8f2 }
.sw.hold { background:#ffb86c; box-shadow: inset 0 0 0 .8pt #ffb86c, inset 0 0 0 1.4pt #282a36 }
.sw.press { background:#8be9fd } .sw.turn { background:#50fa7b }
.sw.num { background:#ff79c6; color:#282a36 } .sw.sh { background:#ffb86c }
.cb b:not(.k), li b:not(.k), td b:not(.k), p b:not(.k), .map b { color:#f1fa8c }
'''
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{out} (dark)</title><style>{ns["CSS"]}{DARK}</style></head><body>{ns["chips"]("".join(pages))}</body></html>'
open(f'../build/{out}.html', 'w').write(html); print('ok')
