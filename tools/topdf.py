import sys
from playwright.sync_api import sync_playwright
src, out = sys.argv[1], sys.argv[2]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    pg = b.new_page(); import os; pg.goto('file://' + os.path.abspath(src)); pg.wait_for_timeout(500)
    pg.pdf(path=out, format='A4', print_background=True, margin={'top':'0','bottom':'0','left':'0','right':'0'})
    # overflow report per page
    res = pg.evaluate("""() => [...document.querySelectorAll('.page')].map(p => { const f = p.querySelector('footer').getBoundingClientRect().top; let m=0; for (const c of p.children) { if (c.tagName==='FOOTER') continue; m=Math.max(m, c.getBoundingClientRect().bottom) } return [Math.round(m), Math.round(f)] })""")
    print(res); b.close()
