import sys, json
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox'])
    # icons
    pg = b.new_page(viewport={'width':512,'height':512})
    pg.goto('http://localhost:8765/icon.svg'); pg.screenshot(path='../docs/icon-512.png')
    pg = b.new_page(viewport={'width':192,'height':192})
    pg.set_content('<body style="margin:0"><img src="http://localhost:8765/icon.svg" width=192 height=192>'); pg.wait_for_timeout(300)
    pg.screenshot(path='../docs/icon-192.png')
    errs=[]
    for name,(w,h) in {'phone':(390,844),'tablet':(820,1180),'desktop':(1366,800)}.items():
        pg = b.new_page(viewport={'width':w,'height':h}); pg.on('console', lambda m: errs.append(m.text) if m.type=='error' else None); pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500)
        pg.screenshot(path=f'../build/shot-{name}-home.png')
        pg.click('#tabs button[data-s="3"]'); pg.wait_for_timeout(200)
        pg.screenshot(path=f'../build/shot-{name}-s3.png')
        pg.fill('#q','resample'); pg.wait_for_timeout(400)
        n = pg.locator('#main .card, #main .grp .row, #main .box').count()
        print(name,'search resample hits',n, 'overflowX', pg.evaluate('document.documentElement.scrollWidth>innerWidth'))
        pg.screenshot(path=f'../build/shot-{name}-search.png')
        pg.fill('#q',''); pg.wait_for_timeout(300)
        pg.click('#tabs button[data-s="all"]'); pg.wait_for_timeout(200)
        pg.locator('#main g.el[data-id="shift"]').first.click(); pg.wait_for_timeout(400)
        print(name,'shift key hits', pg.locator('#main .card, #main .row, #main .box').count(), pg.inner_text('#pills'))
        pg.screenshot(path=f'../build/shot-{name}-key.png')
    print('errors',errs)
    b.close()
