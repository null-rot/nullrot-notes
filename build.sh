#!/usr/bin/env bash
# Rebuilds every PDF and the web app data. Run from the repo root.
set -euo pipefail
cd "$(dirname "$0")/tools"
mkdir -p ../build ../pdf
DOOM_FOOT="DOOM OS 0.7 · SP-404MKII · unofficial cheat sheet, not affiliated with Roland · diagrams schematic"
STOCK_FOOT="SP-404MKII stock OS v4.00 · unofficial cheat sheet from Roland’s manuals, not affiliated with Roland · diagrams schematic"

# 1. light A4 booklets (5 / 6 pages). topdf.py prints [content_bottom, footer_top] per page: bottom must be < footer.
python3 book.py
python3 book_stock.py
python3 topdf.py ../build/doom-os-cheat-sheet.html ../pdf/doom-os-sp-404mk2-cheat-sheet.pdf
python3 topdf.py ../build/sp404mk2-stock-cheat-sheet.html ../pdf/sp-404mk2-stock-os-cheat-sheet.pdf

# 2. dark (hardware palette, matches the web app) A4 for screens
python3 make_dark.py doom doom-os-dark
python3 make_dark.py stock stock-os-dark
python3 topdf.py ../build/doom-os-dark.html ../pdf/doom-os-sp-404mk2-cheat-sheet-dark.pdf
python3 topdf.py ../build/stock-os-dark.html ../pdf/sp-404mk2-stock-os-cheat-sheet-dark.pdf

# 3. foldable A5 booklets: flow layout -> pad to multiple of 4 -> impose onto A4 landscape
python3 make_a5.py doom doom-os "$DOOM_FOOT"
python3 make_a5.py stock stock-os "$STOCK_FOOT"
python3 impose.py ../build/doom-os-a5.pdf ../pdf/doom-os-sp-404mk2-foldable-booklet.pdf
python3 impose.py ../build/stock-os-a5.pdf ../pdf/sp-404mk2-stock-os-foldable-booklet.pdf

# 4. web app data (docs/data.js) from the same booklet source
python3 extract.py
echo "done: pdf/ and docs/data.js updated"
