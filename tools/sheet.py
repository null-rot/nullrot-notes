"""Shared building blocks for the A4/A5 cheat-sheet booklets (every device).

Device content files do `from sheet import *` and get chips(), card(), tbl(), H/P/T and CSS.
"""
import re
from panel import panel

def chips(s):
    return re.sub(r'\[\[(.+?)\]\]', lambda m: f'<b class="k">{m.group(1)}</b>', s)

CROPW = {"lower": 92, "buttons": 92, "pads": 92, "knobs": 92, "auto": 92, "top": 92}

def card(title, hl, crops, body, span=1):
    if isinstance(crops, str): crops = [crops]
    svgs = "".join(f'<div class="pn">{panel(hl, c, width_mm=CROPW[c], bigfs=1.0, aria=title)}</div>' for c in crops)
    return f'<section class="card s{span}"><h3>{title}</h3>{svgs}<div class="cb">{chips(body)}</div></section>'

def tbl(head, rows, cls=""):
    h = "".join(f"<th>{x}</th>" for x in head)
    r = "".join("<tr>" + "".join(f"<td>{chips(c)}</td>" for c in row) + "</tr>" for row in rows)
    return f'<table class="{cls}"><thead><tr>{h}</tr></thead><tbody>{r}</tbody></table>'

H, P, T = "hold", "press", "turn"

CSS = '''
/* self-hosted Barlow (SIL OFL 1.1), shared with the web app */
@font-face { font-family:'Barlow'; font-style:normal; font-weight:400; src:url(../docs/fonts/barlow-400.woff2) format('woff2') }
@font-face { font-family:'Barlow'; font-style:italic; font-weight:400; src:url(../docs/fonts/barlow-400-italic.woff2) format('woff2') }
@font-face { font-family:'Barlow'; font-style:normal; font-weight:500; src:url(../docs/fonts/barlow-500.woff2) format('woff2') }
@font-face { font-family:'Barlow'; font-style:normal; font-weight:600; src:url(../docs/fonts/barlow-600.woff2) format('woff2') }
@font-face { font-family:'Barlow'; font-style:normal; font-weight:700; src:url(../docs/fonts/barlow-700.woff2) format('woff2') }
@font-face { font-family:'Barlow'; font-style:normal; font-weight:800; src:url(../docs/fonts/barlow-800.woff2) format('woff2') }
@font-face { font-family:'Barlow Condensed'; font-style:normal; font-weight:500; src:url(../docs/fonts/barlow-condensed-500.woff2) format('woff2') }
@font-face { font-family:'Barlow Condensed'; font-style:normal; font-weight:600; src:url(../docs/fonts/barlow-condensed-600.woff2) format('woff2') }
@font-face { font-family:'Barlow Condensed'; font-style:normal; font-weight:700; src:url(../docs/fonts/barlow-condensed-700.woff2) format('woff2') }
@page { size: A4; margin: 0 }
* { box-sizing: border-box }
html,body { margin:0; font-family: Barlow, Inter, Helvetica, Arial, sans-serif; color:#161617; font-size: 8.6pt; line-height: 1.32 }
.page { width: 210mm; height: 297mm; padding: 9mm 10mm 12mm; position: relative; overflow: hidden; page-break-after: always; break-after: page; background:#fff }
header { display:flex; justify-content: space-between; align-items:flex-end; border-bottom: 2.2pt solid #111; padding-bottom: 2mm; margin-bottom: 3mm }
header h1 { margin:0; font: 700 23pt/1 'Barlow Condensed', Barlow, sans-serif; letter-spacing:.2pt }
header p { margin: 1.2mm 0 0; font-size: 9pt; color:#333 }
.pg { text-align:right; font-size: 7.5pt; color:#333; line-height:1.3 }
.pg b { font-size: 10pt; color:#111 }
footer { position:absolute; left:10mm; right:10mm; bottom:5mm; font-size: 6.6pt; color:#444; border-top: .6pt solid #999; padding-top:1.2mm; line-height:1.25 }
h2 { font: 700 10pt 'Barlow Condensed', Barlow, sans-serif; margin: 0 0 1.5mm; text-transform: uppercase; letter-spacing:1.2pt }
h2.sec { margin-top: 3mm; border-bottom: 1pt solid #111; padding-bottom: .8mm }
h3 { font: 700 10.4pt/1.2 'Barlow Condensed', Barlow, sans-serif; margin: 0 0 1mm; letter-spacing:.1pt }
.k { display:inline-block; border:.9pt solid #111; border-bottom-width:1.8pt; border-radius: 2pt; padding: 0 2.2pt; font: 700 7.9pt/1.25 'Barlow Condensed', Barlow, sans-serif; letter-spacing:.2pt; background:#fff; white-space:nowrap; line-height: 1.25; margin: 0 .3pt }
.grid { column-count:2; column-gap: 4mm }
.card { border: 1pt solid #111; border-radius: 3pt; padding: 1.6mm 2mm 1.8mm; break-inside: avoid; background:#fff; margin-bottom: 2.4mm; display:block }
.pn { line-height:0; margin: 0 0 1mm; border:.5pt solid #bbb }
.pn svg { width:100%; height:auto; display:block }
.cb { font-size: 8.2pt; line-height:1.34 }
.hero { text-align:center; margin: 1mm 0 2mm }
.hero svg { width: 172mm; height:auto }
.legend { display:flex; flex-wrap:wrap; gap: 1.5mm 5mm; font-size: 7.8pt; margin-bottom: 3mm; align-items:center }
.legend span { display:inline-flex; align-items:center; gap:1.5mm }
.sw { display:inline-flex; width: 5mm; height: 3.4mm; border: 1pt solid #111; border-radius:1.5pt; align-items:center; justify-content:center; font-style:normal; font-size:6pt; font-weight:800 }
.sw.hold { background:#FFB8D9; box-shadow: inset 0 0 0 .8pt #FFB8D9, inset 0 0 0 1.4pt #161617 }
.sw.press { background:#B5EBFF } .sw.turn { background:#B8F5CD } .sw.num { background:#111; color:#fff; border-radius:50%; width:3.6mm } .sw.sh { background:#F26A1B }
.cols2 { display:grid; grid-template-columns:1fr 1fr; gap: 4mm }
.tight { margin-top:2.4mm }
.box { border:1pt solid #111; border-radius:3pt; padding:2mm 2.6mm }
.box ul { margin:0; padding-left: 4mm } .box li { margin-bottom: 1mm }
.box p { margin:0 }
.small { font-size: 8pt }
.warn { border:1pt solid #111; background:#f3f3f3; padding: 1.5mm 2.5mm; margin-top: 3mm; border-radius:3pt }
.map { display:grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; font-size: 8pt }
table { width:100%; border-collapse: collapse; font-size: 7.9pt; margin-top: 3mm }
th { text-align:left; background:#161617; color:#ECE8DF; padding: 1mm 1.6mm; font-size: 7.6pt; letter-spacing:.3pt }
td { padding: .85mm 1.5mm; border-bottom: .7pt solid #888; vertical-align: top }
.cols2 table { margin-top: 0 }
.padref td { padding: .9mm 1.2mm; font-size: 7.4pt }
.pg4 { display:grid; grid-template-columns: repeat(4,1fr); gap: 1mm }
.pc { border: .8pt solid #111; border-radius: 2pt; padding: .6mm 1mm; font-size: 6.6pt; line-height:1.15; min-height: 8.2mm }
.pc b { display:block; font-size: 9pt }
.pc.u { background:#EFECE4; border-width: 1.4pt }
.pc.u b { text-decoration: underline 1.3pt; text-underline-offset: 1.4pt }
.cap { font-size: 7pt; color:#444; margin: 1mm 0 0 }
'''
