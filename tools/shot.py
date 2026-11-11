import sys
from playwright.sync_api import sync_playwright
import browser
src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
with sync_playwright() as p:
    b = browser.launch(p)
    pg = b.new_page(viewport={'width': w, 'height': h})
    pg.goto(browser.file_url(src)); pg.screenshot(path=out, full_page=True); b.close()
