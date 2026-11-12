import sys, re
sys.path.insert(0, '.')
import panel as _pm
import devices
dev, gid = sys.argv[1], sys.argv[2]
g = devices.guide(dev, gid); out = g['dark_html']
devices.use(dev, gid)
_pm.set_theme('hardware')
src = devices.source(dev, gid)
ns = {}
exec(src[:src.index("pages = [")], ns)
calls = re.findall(r'page\((\d), "(.*?)", "(.*?)", (p\d)\)', src[src.index("pages = ["):])
pages = [ns['page'](int(n), t, s, ns[v]) for n, t, s, v in calls]
DARK = '''
/* hardware palette, matching the web app: charcoal body, ivory print, orange only for SHIFT, LED roles */
html,body { background:#161617; color:#ece8df }
.page { background:#161617 }
header { border-bottom-color:#ece8df }
header h1 { color:#ece8df }
header p { color:#aaa59b }
.pg { color:#aaa59b } .pg b { color:#ece8df }
footer { color:#aaa59b; border-top-color:#323237 }
h2 { color:#aaa59b } h2.sec { border-bottom-color:#323237 }
h3 { color:#ece8df }
.k { background:#303035; color:#ece8df; border-color:#4a4a51; border-bottom-color:#0e0e10 }
th .k { background:#161617 }
.card, .box { background:#1e1e20; border-color:#323237 }
.pn { border-color:#323237 }
.warn { background:#1e1e20; border-color:#4a4a51 }
th { background:#303035; color:#ece8df }
td { border-bottom-color:#323237 }
.cap { color:#aaa59b }
.pc { background:#1e1e20; border-color:#4a4a51 }
.pc span { color:#f26a1b }
.pc.u { background:#27272b; border-color:#ece8df }
.sw { border-color:#ece8df }
.sw.hold { background:#ff4fa3; box-shadow: inset 0 0 0 .8pt #ff4fa3, inset 0 0 0 1.4pt #161617 }
.sw.press { background:#38d1ff } .sw.turn { background:#4cf28a }
.sw.num { background:#ece8df; color:#161617 } .sw.sh { background:#f26a1b }
.cb b:not(.k), li b:not(.k), td b:not(.k), p b:not(.k), .map b { color:#ece8df; font-weight:700 }
'''
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{out} (dark)</title><style>{ns["CSS"]}{DARK}</style></head><body>{ns["chips"]("".join(pages))}</body></html>'
open(f'../build/{out}.html', 'w', encoding='utf-8').write(html); print('ok')
