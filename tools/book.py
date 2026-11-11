import sys, re
sys.path.insert(0, '.')
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

def page(n, title, sub, inner):
    return f'''<div class="page"><header><div><h1>{title}</h1><p>{sub}</p></div><div class="pg">DOOM OS 0.7 · SP-404MKII<br><b>{n} / 5</b></div></header>{inner}
<footer>Unofficial cheat sheet compiled from the DOOM OS 0.7 manual (Klangfeld Labs) with panel layout taken from Roland’s SP-404MK2 Reference Manual. Not affiliated with Roland. Diagrams are schematic, not to scale.</footer></div>'''

H, P, T = "hold", "press", "turn"

# ---------------- PAGE 1 : panel map ----------------
legend = '''<div class="legend"><span><i class="sw hold"></i>HOLD this key</span><span><i class="sw press"></i>PRESS / TAP this key</span><span><i class="sw turn"></i>TURN this knob</span><span><i class="sw num">1</i>order of steps</span><span><i class="sw sh"></i>orange bar = Roland’s printed SHIFT function for that pad</span></div>'''
p1 = f'''
<div class="hero">{panel(None, "all", width_mm=172, aria="SP-404MKII panel map")}</div>
{legend}
<div class="cols2 tight">
<div class="box"><h2>Where things live</h2>
<ul>
<li><b>Display + FX row</b> – DOOM OS draws its grid on the display. FX buttons (FILTER+DRIVE, RESONATOR, DELAY, ISOLATOR, DJFX LOOPER, MFX) flank it.</li>
<li><b>Knobs</b> – CTRL 1 / 2 / 3 edit whatever the screen shows; VALUE scrolls (turn) and confirms (press).</li>
<li><b>Left block</b> – PATTERN SELECT, PATTERN EDIT, RECORD SETTING / DEL, REC, RESAMPLE / EXIT, COPY, REMAIN.</li>
<li><b>Right block</b> – START/END, PITCH/SPEED, MARK / BPM SYNC, GATE, LOOP, REVERSE, ROLL / bank buttons A/F–E/J and SHIFT.</li>
<li><b>Pads</b> – 16 pads in a 4×4 grid, numbered left→right, top→bottom. In DOOM OS they are the <b>16 steps</b>. BUS FX, HOLD, EXT SOURCE and SUB PAD sit in the column on the right.</li>
</ul></div>
<div class="box"><h2>Golden rules</h2>
<ul>
<li><b>Open</b>: hold [[REMAIN]] + press [[SUB PAD]]. <b>Close</b>: [[EXIT]] (saves).</li>
<li><b>Lost?</b> Hold [[SHIFT]] for 3 s, then press any control to see what it does. [[EXIT]] leaves help.</li>
<li><b>[[EXIT]]</b> always backs out one level: closes menus, cancels pattern tools, bounces and parameter-lock edits.</li>
<li><b>Undo / redo</b>: [[SHIFT]] + [[PATTERN SELECT]] / [[REMAIN]] + [[PATTERN SELECT]].</li>
<li><b>Saving is automatic</b> after edits, on pattern change and on exit.</li>
<li>Combos are written <b>hold + press</b>: the first key is held down, the second is tapped.</li>
</ul></div>
</div>
<div class="box"><h2>Booklet map</h2>
<div class="map"><div><b>p2 Getting around</b><br>open · play · patterns · tempo · tracks · steps · menus · grid · piano roll</div><div><b>p3 Record &amp; edit</b><br>rec modes · quantize · bounce · pattern tools · parameter locks</div><div><b>p4 Sound &amp; mix</b><br>instruments · kits · arp · mixer · EQ · side chain</div><div><b>p5 FX &amp; reference</b><br>FX · automation · settings · master shortcut table</div></div></div>
'''

# ---------------- PAGE 2 ----------------
c2 = [
 card("Open / close DOOM OS", {"remain": (H,1), "sub_pad": (P,2)}, "auto",
      "Open: hold [[REMAIN]] + press [[SUB PAD]].<br>Close: press [[EXIT]] – saves changes. A <i>Hold to Exit</i> setting can require holding it."),
 card("Play / stop · undo · redo", {"pattern_select": (P,1), "shift": (H,None), "remain": (H,None)}, "buttons",
      "Play / stop: [[PATTERN SELECT]]<br>Undo: hold [[SHIFT]] + [[PATTERN SELECT]]<br>Redo: hold [[REMAIN]] + [[PATTERN SELECT]]"),
 card("New / switch pattern", {"pattern_select": (H,1), "p5": (P,2), "sub_pad": (P,3)}, "auto",
      "New: hold [[PATTERN SELECT]] + an <b>empty</b> pad.<br>Switch: hold [[PATTERN SELECT]] + a pad – starts when the playing pattern ends. <b>Add [[SUB PAD]]</b> to switch immediately."),
 card("Tempo", {"shift": (H,1), "p11": (P,2)}, "auto",
      "[[SHIFT]] + [[pad 11]] (TAP TEMPO), or press [[RECORD SETTING]] twice &gt; BPM."),
 card("Add a track", {"sub_pad": (H,1), "p3": (P,2), "p7": (P,2)}, "pads",
      "Sample track: hold [[SUB PAD]], tap sample pads, release.<br>Instrument track: hold [[SUB PAD]] + tap an <b>empty</b> pad (opens the instrument browser, p4)."),
 card("Steps &amp; notes (CTRL 1 / 2 / 3)", {"c1": (T,None), "c2": (T,None), "c3": (T,None), "p6": (H,1)}, ["knobs", "pads"],
      "The 16 pads are the 16 <b>steps</b>: tap to toggle, hold a pad to select that note.<br>[[CTRL 1]] velocity · [[CTRL 2]] length · [[CTRL 3]] nudge. Turn with <b>no pad held</b> = whole track; hold a pad = that one note."),
]
menus = tbl(["Do this", "Input", "Result"], [
 ["<b>Fine edits</b>", "[[SHIFT]] + [[CTRL 2]] · [[SHIFT]] + [[CTRL 1]]", "Length in 1/128 steps · pitch up to ±12 semitones. Keep a selection: hold pad + [[REMAIN]]"],
 ["<b>Mute / solo track</b>", "[[SHIFT]] + press [[VALUE]] · [[SHIFT]] + [[ROLL]]", ""],
 ["<b>Copy / paste / delete</b>", "[[COPY]], then [[RECORD SETTING]] &gt; EDIT &gt; PASTE · [[DEL]]", "DEL asks first; CLEAR… asks YES/NO; PASTE does <u>not</u> ask"],
 ["<b>TRACK page</b>", "[[RECORD SETTING]] once", "EDIT (SWAP PAD, PASTE, CLEAR…, BOUNCE…) · PATTERN (CLEAR…, BOUNCE…) · GENERATE (PRINT ARP…, CLEAR…) · VIEWS (MIXER, AUTOMATION, ARP, SIDECHAIN)"],
 ["<b>PATTERN panel</b>", "[[RECORD SETTING]] twice (3rd closes)", "BPM · LENGTH (bars) · REC mode"],
])
note2 = '<p class="cap">Patterns over 512 notes, and effect movements, can’t be undone.</p>'
p2 = '<div class="grid">' + "".join(c2) + '</div>' + menus + note2

# ---------------- PAGE 3 ----------------
c3 = [
 card("Record (REC)", {"rec": (P,1)}, "buttons",
      "1st press = <b>rehearsal</b> (nothing recorded). 2nd press = <b>records</b>. [[EXIT]] stops recording (pattern keeps playing). [[HOLD]] is ignored while REC is on."),
 card("Record mode", {"shift": (H,1), "rec": (P,2)}, "buttons",
      "[[SHIFT]] + [[REC]] cycles <b>SINGLE</b> · <b>MULTI</b> · <b>CHROMATIC</b> (pad 5 = original pitch) · <b>16 VEL</b> (pad 4 = 127, pad 13 = 1). Also set in the PATTERN panel."),
 card("Metronome", {"shift": (H,1), "p9": (P,2)}, "auto",
      "[[SHIFT]] + [[pad 9]] cycles ON · RECPLAY · OFF."),
 card("Input quantize (new notes)", {"shift": (H,1), "pattern_edit": (P,2)}, "buttons",
      "[[SHIFT]] + [[PATTERN EDIT]] sets <b>QNT</b> · <b>SWG</b> · <b>VEL</b> · <b>LEN</b> for newly recorded notes."),
 card("Bounce in place", {"resample": (P,1), "shift": (H,None)}, "buttons",
      "[[RESAMPLE]] = bounce the <b>track</b>; [[SHIFT]] + [[RESAMPLE]] = <b>everything you hear</b>. Pick type with [[VALUE]], tap an <b>empty pad</b>, then press [[RESAMPLE]] or [[VALUE]]. A track bounce swaps the track’s notes for one note on the new pad – [[SHIFT]] + [[PATTERN SELECT]] undoes it; [[EXIT]] cancels."),
 card("Pattern tools", {"pattern_edit": (P,1), "value": (T,2)}, "buttons",
      "[[PATTERN EDIT]] &gt; turn [[VALUE]] to a tool &gt; press [[VALUE]] &gt; set amount &gt; press [[VALUE]] to apply. Tap a track pad to limit to that track; tap again for ALL."),
 card("Parameter locks", {"mark": (P,1), "c1": (T,3), "c2": (T,3), "c3": (T,3)}, ["knobs", "buttons"],
      "[[MARK]] (grid or editor) &gt; tap a step &gt; edit with [[CTRL 1–3]] &gt; [[MARK]] saves, [[EXIT]] discards. Locked pads show <b>blue</b>; [[DEL]] resets a step."),
]
tools = tbl(["Pattern tool", "Range / note"], [
 ["<b>QUANT</b>", "1/4 to 1/32, incl. triplets"],
 ["<b>SWING</b>", "50–75; [[SHIFT]] switches 8th / 16th"],
 ["<b>SHIFT</b>", "±16 steps, wraps around"],
 ["<b>DOUBLE</b> · <b>HALVE</b>", "DOUBLE max 64 bars / 512 notes; HALVE not on a 1-bar pattern"],
 ["<b>REVERSE</b>", "–"],
 ["<b>HUMAN</b> · <b>TRANSP</b>", "HUMAN 1–30 · TRANSP ±12 semitones"],
])
bounce = tbl(["Bounce type", "What it captures"], [
 ["<b>CUT</b>", "Pattern length"], ["<b>TAIL</b>", "Includes effect decay, up to 30 s"], ["<b>LOOP</b>", "Loops from the second pass"],
])
plocks = '<div class="box small"><h2>Parameter-lock facts</h2><ul><li>Per-step instrument parameters, instrument tracks only.</li><li>Locks follow notes when moved (SHIFT tool, QUANTIZE, DUPLICATE, CROP, SWAP PAD, COPY, PASTE).</li><li>Limits: 4096 locks per project · 64 steps per session · 126 locks per track in a pattern.</li></ul></div>'
views = tbl(["View", "Input", "Result"], [
 ["<b>Grid views</b>", "[[SHIFT]] + [[RECORD SETTING]]", "Cycles GRID (8 tracks) · LABELS · BEATS · BOTH · ZOOM (4 larger tracks)"],
 ["<b>Zoom · move · follow</b>", "[[REMAIN]]+turn [[VALUE]] · [[SHIFT]]+turn [[VALUE]] · [[SHIFT]]+[[HOLD]]", "Zoom in ZOOM view · move by bar (beat at 1-beat zoom) · toggle Follow (playhead)"],
])
p3 = '<div class="grid">' + "".join(c3) + '</div><div class="cols2 tight"><div>' + tools + '</div><div>' + bounce + '<div style="height:3mm"></div>' + plocks + '</div></div>' + views

# ---------------- PAGE 4 ----------------
c4 = [
 card("Instrument browser", {"sub_pad": (H,1), "p8": (P,2)}, "pads",
      "Hold [[SUB PAD]] + tap an <b>empty</b> pad, release. Turn [[VALUE]] to choose; hold [[SUB PAD]] to preview; [[VALUE]] loads. 20 instruments and 11 drum kits are built in."),
 card("Instrument editor", {"start_end": (P,1), "value": (T,2), "c1": (T,3), "c2": (T,3), "c3": (T,3)}, ["knobs", "buttons"],
      "On an instrument track press [[START/END]]. Turn [[VALUE]] to pick a section (TONE, MOD, AMP, OUT…); [[CTRL 1–3]] edit; [[SHIFT]] = finer steps; [[EXIT]] saves."),
 card("Chromatic keys &amp; octave", {"shift": (H,1), "p4": (P,2), "bank_AF": (P,3), "bank_BG": (P,3), "bank_CH": (P,3), "bank_DI": (P,3), "bank_EJ": (P,3)}, "auto",
      "In the editor: [[SHIFT]] + [[pad 4]]. Octave via the BANK buttons: <b>C/H</b> default · <b>B/G</b>, <b>A/F</b> down · <b>D/I</b>, <b>E/J</b> up."),
 card("Drum kits", {"shift": (H,1), "value": (T,1), "bank_AF": (P,3), "bank_EJ": (P,3)}, "buttons",
      "[[SHIFT]] + turn [[VALUE]] to KITS, choose, press [[VALUE]], pick a bank with a BANK button, press [[VALUE]]. A non-empty bank asks to overwrite (can’t undo); protected banks are refused."),
 card("Mixer", {"record_setting": (H,1), "value": (T,2), "c1": (T,3), "c2": (T,3), "c3": (T,3)}, ["knobs", "buttons"],
      "Hold [[RECORD SETTING]] 0.6 s. [[VALUE]] selects a track; [[CTRL 1]] pan · [[CTRL 2]] bus (B1 · B2 · DRY) · [[CTRL 3]] level. Tap a pad = mute; [[REMAIN]] + pad = solo. [[VALUE]] cycles pan / bus / level for fine adjust; [[EXIT]] deselects."),
]
more = tbl(["Tool", "How", "Details"], [
 ["<b>Arpeggiator</b>", "[[RECORD SETTING]] &gt; ARP, or the grid while playing", "Hold pads to arp. [[VALUE]] toggles arp and swaps PLAY / PITCH pages; [[HOLD]] keeps it running. Persists until power-off. <b>PLAY</b>: [[CTRL 1]] TYPE (UP, DOWN, U/D, RND, ORD, CHRD, CONV, DIV, PNKY, THMB, U/D+) · [[CTRL 2]] RATE 1/4–1/32 + triplets · [[CTRL 3]] GATE 1–100%. <b>PITCH</b>: KEY (C–B) · SCALE (40) · OCT (±3). Print: [[RECORD SETTING]] &gt; GENERATE &gt; PRINT ARP… (replaces all notes on the track)"],
 ["<b>Track EQ</b>", "in mixer, [[PITCH/SPEED]]", "[[CTRL 1]] gain ±12 dB · [[CTRL 2]] freq 20 Hz–20 kHz · [[CTRL 3]] Q 0.3–10. [[VALUE]] opens the screen; again = ADV band select. Up to 16 pads; EQ belongs to the pad"],
 ["<b>Side chain</b>", "[[RECORD SETTING]] &gt; SIDECHAIN", "[[VALUE]] on a <b>source</b> bus, then a <b>target</b> bus; [[VALUE]] twice on one bus = compress it. [[CTRL 1]] THR · [[CTRL 2]] RAT · [[CTRL 3]] REL; GAIN via [[VALUE]]. Off: hold [[DEL]] + [[VALUE]] on the bus. Shared with the unit’s own side chain, all projects"],
 ["<b>Piano roll</b>", "press [[VALUE]] on the grid", "Hold a step’s pad + press another pad to set pitch (pad 5 = original; +1 semitone per pad across, and up the rows). Turn [[VALUE]] scrolls; [[SHIFT]]+turn changes track"],
 ["<b>Waveform display</b>", "[[SHIFT]] + [[START/END]]", "1× output · 2× selected track · 3× hide. Shows the last two seconds"],
 ["<b>Replace instrument</b>", "in editor: [[REMAIN]], choose, YES", "Notes stay, parameters reset"],
 ["<b>Remove instrument</b>", "outside DOOM OS: hold [[DEL]] + pad, then [[VALUE]]", "<u>Cannot be undone</u>"],
 ["<b>Mixer display</b>", "[[SHIFT]] + [[RECORD SETTING]]", "ARROWS / DITHER, with or without NAMES"],
])
p4 = '<div class="grid">' + "".join(c4) + '</div>' + more

# ---------------- PAGE 5 ----------------
c5 = [
 card("Effects", {"fx_fd": (P,1), "fx_res": (P,1), "fx_delay": (P,1), "fx_iso": (P,1), "fx_djfx": (P,1), "fx_mfx": (P,1), "c1": (T,2), "c2": (T,2), "c3": (T,2)}, "top",
      "Each FX button turns its effect <b>on</b> and opens its page (stays open until [[EXIT]]; the effect stays on). Press again to turn <b>off</b>. [[CTRL 1–3]] set parameters; hold [[VALUE]] for page 2. [[REMAIN]] + FX button reopens a page without toggling."),
 card("Bus FX settings · record movements", {"shift": (H,1), "p16": (P,2), "rec": (P,3)}, "auto",
      "[[SHIFT]] + [[pad 16]] opens bus effects settings. Record movements: open an FX page, press [[REC]] twice, turn knobs. [[BUS FX]] switches buses."),
 card("FX automation", {"shift": (H,1), "mark": (P,2), "start_end": (P,3), "value": (T,None)}, "buttons",
      "[[SHIFT]] + [[MARK]] opens it. Turn [[VALUE]] for a parameter; [[SHIFT]] + turn = next effect. Press [[VALUE]] for per-step view, tap a pad, turn [[VALUE]]. [[START/END]] toggles <b>EFX MOTION PLAY</b> – movements only play while it is on."),
]
master = tbl(["Function", "Input", "Function", "Input"], [
 ["Open DOOM OS", "[[REMAIN]]+[[SUB PAD]]", "Bounce track / mix", "[[RESAMPLE]] / [[SHIFT]]+[[RESAMPLE]]"],
 ["Undo / Redo", "[[SHIFT]]+[[PATTERN SELECT]] / [[REMAIN]]+[[PATTERN SELECT]]", "Instrument editor", "[[START/END]]"],
 ["Mixer", "hold [[RECORD SETTING]] 0.6 s", "Parameter locks", "[[MARK]]"],
 ["Help mode", "hold [[SHIFT]] 3 s", "FX automation", "[[SHIFT]]+[[MARK]]"],
 ["Metronome", "[[SHIFT]]+[[pad 9]]", "Waveform display", "[[SHIFT]]+[[START/END]]"],
 ["Record mode", "[[SHIFT]]+[[REC]]", "Bus FX settings", "[[SHIFT]]+[[pad 16]]"],
 ["Tempo", "[[SHIFT]]+[[pad 11]]", "UTILITY menu", "[[REMAIN]]+[[PATTERN EDIT]]"],
 ["MFX effect select", "hold [[MFX]] + pad (17–32 via [[DJFX LOOPER]]; 33–48 via [[ISOLATOR]])", "Piano roll", "press [[VALUE]] on the grid"],
 ["Input quantize", "[[SHIFT]]+[[PATTERN EDIT]]", "DOOM OS settings", "[[EXIT]], then [[SHIFT]]+[[pad 13]] &gt; SYSTEM &gt; DOOM OS"],
])
settings = '<div class="box small"><h2>DOOM OS settings</h2><p>Path: [[EXIT]], then [[SHIFT]] + [[pad 13]] &gt; SYSTEM &gt; <b>DOOM OS</b> tab ([[CTRL 3]] navigates). Options: Mixer Level (ARROWS / DITHER) · Mixer Names · Boot Anim (GRAFFITI, VHS, HELLO, BUBBLE, SKETCH, HYPERSPACE, RANDOM) · Pattern View · Grid Lines · Pattern Follow · Motion Rec (OVERWRITE / OVERDUB) · Hold to Exit (0.1–1.0 s or OFF) · Boot to DOOM (YES / NO). The SHORTCUT tab holds up to 8 custom shortcuts.</p></div>'
PADSH = ["FIXED VELOCITY","16 VELOCITY","CUE","CHROMATIC","EXCHANGE","INIT PARAM","PAD LINK","MUTE GROUPS","METRONOME","COUNT-IN","TAP TEMPO","GAIN","UTILITY","IMPORT/EXPORT","PAD SETTING","EFX SETTING"]
USED = {4, 9, 11, 13, 16}
padref = '<div class="pg4">' + "".join(f'<div class="pc{" u" if i+1 in USED else ""}"><b>{i+1}</b><span>{t}</span></div>' for i, t in enumerate(PADSH)) + '</div>'
padnote = '<p class="cap">Underlined = pad shortcuts DOOM OS refers to. Labels are Roland’s printed SHIFT functions.</p>'
p5 = '<div class="grid">' + "".join(c5) + '</div><h2 class="sec">Master shortcut table</h2>' + master + '<div class="cols2 tight"><div><h2 class="sec">Pad SHIFT functions</h2>' + padref + padnote + '</div><div>' + settings + '</div></div>'

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
pages = [
 page(1, "DOOM OS · SP-404MKII", "Pocket cheat sheet &amp; panel map – a graphical sequencer layer for the Roland SP-404MKII", p1),
 page(2, "Getting around", "Open · play · patterns · tempo · tracks · steps · menus · grid · piano roll", p2),
 page(3, "Record &amp; edit", "Recording modes · quantize · bounce in place · pattern tools · parameter locks", p3),
 page(4, "Sound &amp; mix", "Instruments · drum kits · arpeggiator · mixer · EQ · side chain · waveform", p4),
 page(5, "FX &amp; quick reference", "Effects · automation · settings · every shortcut on one page", p5),
]
body_html = chips("".join(pages))
html = f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>DOOM OS for SP-404MKII – cheat sheet</title><style>{CSS}</style></head><body>{body_html}</body></html>'
open('../build/doom-os-cheat-sheet.html', 'w').write(html)
print(len(html))
