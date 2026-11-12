# Roland SP-404MKII: what to build and how it is named.
# Content lives in one file per guide (doom.py, stock.py); panel geometry in layout.py.

DEVICE = dict(
    id="sp404mk2",
    name="SP-404MKII",
    order=1,                              # menu position; the first device is the default
    maker="Roland",
    # web app wording for this device
    both_label="Both OS",                 # toggle that searches every guide of this device
    pads_note="Orange labels are Roland’s printed SHIFT functions. Tap a pad to filter.",
    credits=('Unofficial. Compiled from Roland’s SP-404MK2 Reference Manual &amp; v4.00 shortcut list, and the Klangfeld Labs DOOM OS 0.7 manual. '
             'Community extras credit <a href="https://vultilion.github.io/sp404mk2-cheatsheet/">vultilion</a> (CC BY-NC 4.0). '
             'Not affiliated with Roland or Klangfeld Labs. Diagrams are schematic.'),
    guides=[
        dict(
            id="doom",
            name="DOOM OS",
            sub="Klangfeld Labs DOOM OS 0.7 on the SP-404MKII",
            content="doom.py",
            disp_sub="DOOM OS grid",          # small text under DISPLAY in the panel drawing
            pads_used_note="Underlined numbers = pads DOOM OS refers to.",
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
            pads_used_note="",
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
