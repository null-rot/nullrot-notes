# Handoff

## What this is
Cheat sheets for the Roland SP-404MKII in four forms, built from one content source:
1. A4 printable booklets (DOOM OS 5 pages, stock OS 6 pages) with vector panel diagrams highlighting hold/press/turn controls and step order.
2. Dark (Dracula) A4 versions for screens.
3. Foldable booklets: A5 flow layout, padded to a multiple of 4 pages, imposed onto A4 landscape for duplex print and fold.
4. Searchable responsive web app (static, offline PWA) for tablet/phone.

## Layout
```
build.sh                 one-command rebuild
tools/panel.py           SVG panel generator: ELEMS (every control with x/y/size/label), CROPS, themes LIGHT/DRACULA, panel()
tools/book.py            DOOM OS content + A4 page assembly + CSS (also holds the shared helpers card/tbl/chips and CSS)
tools/book_stock.py      stock OS content; reuses helpers/CSS from book.py via exec
tools/make_dark.py       same booklets with Dracula theme + dark CSS
tools/topdf.py           HTML -> A4 PDF via headless Chrome; prints per-page overflow check
tools/make_a5.py         A5 flow booklet (@page margin boxes), pads with notes pages to multiple of 4
tools/impose.py          pypdf imposition into A4 landscape sheets, e.g. 12 pages -> (12,1),(2,11),(10,3),(4,9),(8,5),(6,7)
tools/extract.py         runs the booklet code, captures cards/tables/notes, writes build/data.json + docs/data.js
tools/test_webapp.py     Playwright smoke test (needs `python3 -m http.server 8765` running in docs/)
tools/smoke.py, shot.py  panel smoke render / screenshot helpers
docs/                    the web app (index.html, styles.css, app.js, data.js, sw.js, manifest, icons)
pdf/                     generated PDFs (committed so you can print without building)
build/                   generated HTML/intermediates (gitignored)
```

## Key design decisions and gotchas
- **Panel layout** was verified against Roland's reference-manual photos: round display centre, FX buttons either side, knob row VOLUME/CTRL1-3, left 3x3 block, right block with VALUE knob, bank buttons A/F-E/J + SHIFT, 4x4 pads numbered left-right/top-bottom, right column BUS FX/HOLD/EXT SOURCE/SUB PAD. Coordinates live in `panel.build_elems()`.
- **Highlight roles:** hold = amber + double ring, press = blue, turn = green, numbered badge = order. Crop `"auto"` fits the highlighted controls' bounding box.
- **Display sublabel:** `panel.DISP_SUB` is "DOOM OS grid" for DOOM, empty for stock.
- **Overflow:** A4 pages are fixed height. `topdf.py` prints `[content_bottom, footer_top]` per page in px; if bottom > footer, content overflows. Fix by moving rows/cards between pages, not by shrinking fonts.
- **`book_stock.py` execs `book.py`'s head and CSS slice** by string index (`'# ---------------- PAGE 1'`, `CSS = '''`, `'''\npages`). Don't rename those markers without updating `book_stock.py`, `make_a5.py`, `make_dark.py` and `extract.py` (all slice source by marker/regex, `page\((\d), "(.*?)", "(.*?)", (p\d)\)`). A sensible refactor is to move content into data files (YAML/JSON) and generate everything from that.
- **Web app data** is derived by `extract.py` by monkeypatching `card()`/`tbl()` while executing page blocks. Pages' `<div class="box">` notes are regex-captured. The 4-column master/SHIFT tables are flattened into rows.
- **Web panel renderer** (`panelSVG` in app.js) is a hand port of `panel.panel()`; colours come from CSS variables (`--pbtn`, `--hold`, ...) so theming is pure CSS.
- **Tap-to-filter** matches an entry if its highlight set contains the control id or any `[[chip]]` normalises (uppercase, no spaces) to the control label.
- **Service worker** is network-first, falls back to cache; bump `V` in `sw.js` on releases if you want a hard refresh.
- Rendering needs Chrome at `/usr/bin/google-chrome` (hardcoded `executable_path` in topdf/make_a5/shot/test). Change it or drop the argument to use Playwright's own Chromium.

## Sources
- Roland SP-404MK2 Reference Manual and "List of Shortcut Keys" v4.00 (static.roland.com).
- Klangfeld Labs DOOM OS 0.7 manual: https://klangfeldlabs.com/doom-os/manual/
- Community extras (stock guide, marked "not in Roland's list"): https://vultilion.github.io/sp404mk2-cheatsheet/ (CC BY-NC 4.0).

## Known gaps / ideas
- Content is unverified against hardware; community items are labelled as such. Worth a proof-read on the unit.
- Stock panel diagram shows no per-mode LED states; DJ-mode pads aren't diagrammed.
- Possible next steps: move content to JSON/YAML as the source of truth, add a CI action that runs `build.sh` and publishes `docs/`, pad-level "what does pad N do in this mode" view, firmware-version badge per entry, print stylesheet for the web app cards.
- Roland firmware and DOOM OS will change: re-check the shortcut list when v4.x/DOOM updates ship.
