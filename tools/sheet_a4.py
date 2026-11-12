# Light A4 booklet HTML for one guide: python3 sheet_a4.py <device> <guide>
import sys
sys.path.insert(0, '.')
import devices

dev, gid = sys.argv[1], sys.argv[2]
g = devices.guide(dev, gid)
devices.use(dev, gid)
ns = {}
exec(devices.source(dev, gid), ns)
body_html = ns['chips']("".join(ns['pages']))
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{g["title"]}</title><style>{ns["CSS"]}</style></head><body>{body_html}</body></html>'
open(f'../build/{g["html"]}.html', 'w', encoding='utf-8').write(html)
print(len(html))
