# Roland SP-404MKII: what to build and how it is named.
# Content lives in one file per guide (doom.py, stock.py); panel geometry in layout.py.

DEVICE = dict(
    id="sp404mk2",
    name="SP-404MKII",
    guides=[
        dict(
            id="doom",
            name="DOOM OS",
            sub="Klangfeld Labs DOOM OS 0.7 on the SP-404MKII",
            content="doom.py",
            disp_sub="DOOM OS grid",          # small text under DISPLAY in the panel drawing
            title="DOOM OS for SP-404MKII – cheat sheet",
            html="doom-os-cheat-sheet",       # build/<html>.html
            dark_html="doom-os-dark",
            a5_name="doom-os",
            pdf="doom-os-sp-404mk2-cheat-sheet",            # pdf/<pdf>.pdf and pdf/<pdf>-dark.pdf
            foldable="doom-os-sp-404mk2-foldable-booklet",  # pdf/<foldable>.pdf
            foot="DOOM OS 0.7 · SP-404MKII · unofficial cheat sheet, not affiliated with Roland · diagrams schematic",
        ),
        dict(
            id="stock",
            name="Stock OS",
            sub="Roland SP-404MKII firmware v4.00",
            content="stock.py",
            disp_sub="",
            title="SP-404MKII stock OS – cheat sheet",
            html="sp404mk2-stock-cheat-sheet",
            dark_html="stock-os-dark",
            a5_name="stock-os",
            pdf="sp-404mk2-stock-os-cheat-sheet",
            foldable="sp-404mk2-stock-os-foldable-booklet",
            foot="SP-404MKII stock OS v4.00 · unofficial cheat sheet from Roland’s manuals, not affiliated with Roland · diagrams schematic",
        ),
    ],
)
