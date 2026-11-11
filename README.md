# SP-404MKII cheat sheets

Printable, foldable, dark-mode and searchable web cheat sheets for the Roland SP-404MKII, covering the
**stock OS (v4.00)** and **DOOM OS 0.7** (Klangfeld Labs).

| Output | Where |
|---|---|
| Web app (GitHub Pages, installable, offline) | `docs/` |
| A4 booklets (light, print) | `pdf/*-cheat-sheet.pdf` |
| A4 booklets (Dracula dark, on-screen) | `pdf/*-cheat-sheet-dark.pdf` |
| Foldable A4-landscape booklets (print duplex, fold in half) | `pdf/*-foldable-booklet.pdf` |

## Publish the web app
Settings > Pages > Deploy from branch > `main` / `/docs`.

## Rebuild
```
pip install -r requirements.txt && playwright install chromium   # or have google-chrome at /usr/bin/google-chrome
./build.sh
```
See `handoff.md` for how it all works and what to watch for.

## Credits and licence notes
Unofficial; not affiliated with Roland or Klangfeld Labs. Sources: Roland SP-404MK2 Reference Manual and v4.00 shortcut list
(static.roland.com), Klangfeld Labs DOOM OS 0.7 manual. Community extras on the stock guide are from vultilion's sheet
(https://vultilion.github.io/sp404mk2-cheatsheet/, CC BY-NC 4.0).
