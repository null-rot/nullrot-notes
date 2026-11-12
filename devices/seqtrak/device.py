# Yamaha SEQTRAK: what to build and how it is named.
# Content lives in seqtrak.py; panel geometry in layout.py.

DEVICE = dict(
    id="seqtrak",
    name="SEQTRAK",
    order=2,
    maker="Yamaha",
    pad_word="key",                        # Drum keys 1-16 are written [[key 9]]; Synth keys are [[S1]]-[[S7]]
    both_label="All guides",
    pads_note="",
    credits=('Unofficial. Compiled from Yamaha’s SEQTRAK User Guide (OS V2.00) and checked against it; community sheets by '
             '<a href="https://github.com/devopscmac/synth-cheat-sheets">devopscmac</a> and '
             '<a href="https://cheatsheets.namaraii.com/seqtrak.html">TAKEUCHI Hitoshi</a> were used as checklists. '
             'Not affiliated with Yamaha. Diagrams are schematic.'),
    guides=[
        dict(
            id="os2",
            name="OS 2.00",
            sub="Yamaha SEQTRAK, OS V2.00",
            content="seqtrak.py",
            disp_sub="",
            pads_used_note="",
            title="Yamaha SEQTRAK – cheat sheet",
            html="seqtrak-cheat-sheet",
            dark_html="seqtrak-dark",
            a5_name="seqtrak",
            pdf="seqtrak-cheat-sheet",
            foldable="seqtrak-foldable-booklet",
            foot="SEQTRAK OS V2.00 · unofficial cheat sheet from Yamaha’s User Guide, not affiliated with Yamaha · diagrams schematic",
        ),
    ],
)
