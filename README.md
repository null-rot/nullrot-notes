# Nullrot Notes

Printable, foldable, dark-mode and searchable web cheat sheets for my gear. Each device lives in `devices/`
and gets its own panel diagram, guides and PDFs; the web app switches between them.

| Device | Guides |
|---|---|
| Roland SP-404MKII | **stock OS (v4.00)** and **DOOM OS 0.7** (Klangfeld Labs) |
| Yamaha SEQTRAK | **OS V2.00** |

| Output | Where |
|---|---|
| Web app (GitHub Pages, installable, offline) | `docs/` |
| A4 booklets (light, print) | `pdf/*-cheat-sheet.pdf` |
| A4 booklets (dark hardware palette, on-screen) | `pdf/*-cheat-sheet-dark.pdf` |
| Foldable A4-landscape booklets (print duplex, fold in half) | `pdf/*-foldable-booklet.pdf` |

## Publish the web app
Settings > Pages > Deploy from branch > `main` / `/docs`.

## Rebuild
```
pip install -r requirements.txt
./build.sh              # every device; or ./build.sh sp404mk2
```
The build finds Chrome or Edge on Windows, macOS or Linux (or set `CHROME_PATH`); without one it falls back to
Playwright's Chromium (`playwright install chromium`). It stops if any A4 page runs into its footer.

## Layout
```
devices/<id>/device.py   names, guides, output file names, footers
devices/<id>/layout.py   panel geometry: every control's position, size and label; named crops
devices/<id>/<guide>.py  booklet content (cards, tables, pages)
tools/                   shared: panel renderer, booklet CSS/helpers, PDF + web-data build
docs/                    the web app (data.js is generated)
```
To add a device, copy `devices/sp404mk2/` as a starting point, redraw `layout.py` for the new panel,
write the guide content, and run `./build.sh <id>`.

## Credits and licence notes
Unofficial; not affiliated with Roland or Klangfeld Labs. Sources: Roland SP-404MK2 Reference Manual and v4.00 shortcut list
(static.roland.com), Klangfeld Labs DOOM OS 0.7 manual. Community extras on the stock guide are from vultilion's sheet
(https://vultilion.github.io/sp404mk2-cheatsheet/, CC BY-NC 4.0).
The SEQTRAK guide is written from Yamaha's SEQTRAK User Guide (OS V2.00) and checked against it; the community
sheets by devopscmac (https://github.com/devopscmac/synth-cheat-sheets) and TAKEUCHI Hitoshi
(https://cheatsheets.namaraii.com/seqtrak.html) were used as checklists. Not affiliated with Yamaha.
