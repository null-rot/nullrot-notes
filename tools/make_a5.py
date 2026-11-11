import sys, re, subprocess
sys.path.insert(0, '.')
from playwright.sync_api import sync_playwright
import browser

def load(kind):
    """exec the booklet source up to the page assembly; return (inner pages, css, chips, disp)"""
    ns = {}
    if kind == 'doom':
        src = open('book.py').read()
        code = src[:src.index("pages = [")]
        exec(code, ns)
        calls = re.findall(r'page\((\d), "(.*?)", "(.*?)", (p\d)\)', src[src.index("pages = ["):])
    else:
        import panel as _pm; _pm.DISP_SUB = ''
        src = open('book_stock.py').read()
        code = src[:src.index("pages = [")]
        exec(code, ns)
        calls = re.findall(r'page\((\d), "(.*?)", "(.*?)", (p\d)\)', src[src.index("pages = ["):])
    return ns, calls

A5CSS = '''
@page { size: 148mm 210mm; margin: 8mm 8mm 12mm;
  @bottom-left { content: "@@FOOT@@"; font: 5.8pt Inter, sans-serif; color:#444 }
  @bottom-right { content: counter(page); font: 700 8pt Inter, sans-serif; color:#111 } }
html,body { font-size: 8.4pt }
.sec { break-before: auto; margin-top: 4mm }
.sec:first-child { margin-top: 0 }
.pn { width: 78%; margin: 0 auto 1mm }
.sec.notes-sec { break-before: page }
header { margin-bottom: 2.5mm }
header h1 { font-size: 17pt }
header p { font-size: 8pt }
.pg { font-size: 6.6pt }
.grid { column-count: auto; display: block }
header { break-after: avoid }
.cb, h3 { orphans: 3; widows: 3 }
.card h3 { break-after: avoid }
.cols2 { grid-template-columns: 1fr; gap: 2.4mm }
.map { grid-template-columns: repeat(2,1fr) !important }
.hero svg { width: 100% }
.card, .box, tr, .pc { break-inside: avoid }
.cb { font-size: 8pt }
table { font-size: 7.6pt }
.notes { height: 168mm; border: 1pt solid #111; border-radius: 3pt;
  background-image: repeating-linear-gradient(to bottom, transparent 0, transparent 6.9mm, #bbb 6.9mm, #bbb 7.1mm) }
h2, h2.sec { break-after: avoid }
'''

def build(kind, out_html, foot, pad_to):
    ns, calls = load(kind)
    chips = ns['chips']; panel = ns['panel']; CSS = ns['CSS']
    secs = []
    for n, title, sub, var in calls:
        inner = ns[var]
        secs.append(f'<section class="sec"><header><div><h1>{title}</h1><p>{sub}</p></div></header>{inner}</section>')
    notes = lambda k: f'<section class="sec notes-sec"><header><div><h1>Notes</h1><p>Your own shortcuts, settings and tricks</p></div></header><div class="notes"></div></section>'
    body = "".join(secs) + "".join(notes(i) for i in range(pad_to))
    html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><style>{CSS}{A5CSS.replace("@@FOOT@@", foot)}</style></head><body>{chips(body)}</body></html>'
    open(out_html, 'w').write(html)

def render(html, pdf):
    with sync_playwright() as p:
        b = browser.launch(p)
        pg = b.new_page(); import os; pg.goto(browser.file_url(html)); pg.wait_for_timeout(500)
        pg.pdf(path=pdf, prefer_css_page_size=True, print_background=True)
        b.close()

def npages(pdf):
    from pypdf import PdfReader
    return len(PdfReader(pdf).pages)

if __name__ == '__main__':
    kind, name, foot = sys.argv[1], sys.argv[2], sys.argv[3]
    h = f'../build/{name}-a5.html'; pdf = f'../build/{name}-a5.pdf'
    build(kind, h, foot, 0); render(h, pdf); n = npages(pdf)
    pad = (-n) % 4
    print('pages before pad', n, 'pad', pad)
    if pad:
        build(kind, h, foot, pad); render(h, pdf); n = npages(pdf)
    print('final pages', n)
