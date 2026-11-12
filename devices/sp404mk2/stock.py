# SP-404MKII stock OS v4.00: booklet content. Shared helpers/CSS come from tools/sheet.py.
from sheet import *

TOTAL = 6
def page(n, title, sub, inner):
    return f'''<div class="page"><header><div><h1>{title}</h1><p>{sub}</p></div><div class="pg">SP-404MKII · stock OS (v4.00)<br><b>{n} / {TOTAL}</b></div></header>{inner}
<footer>Unofficial cheat sheet compiled from Roland’s SP-404MK2 Reference Manual and v4.00 List of Shortcut Keys (static.roland.com). Not affiliated with Roland. Diagrams are schematic, not to scale. Check the Roland documents for anything safety- or data-critical.</footer></div>'''

# ---------- PAGE 1 ----------
legend = '<div class="legend"><span><i class="sw hold"></i>HOLD this key</span><span><i class="sw press"></i>PRESS / TAP this key</span><span><i class="sw turn"></i>TURN this knob</span><span><i class="sw num">1</i>order of steps</span><span><i class="sw sh"></i>orange bar = printed SHIFT function for that pad</span></div>'
p1 = f'''
<div class="hero">{panel(None, "all", width_mm=172, disp_sub="", aria="SP-404MKII panel map")}</div>
{legend}
<div class="cols2 tight">
<div class="box"><h2>Where things live</h2><ul>
<li><b>Display + FX row</b> – effect buttons FILTER+DRIVE, RESONATOR, DELAY (left) and ISOLATOR, DJFX LOOPER, MFX (right) flank the display.</li>
<li><b>Knobs</b> – VOLUME, CTRL 1–3 (effect / edit parameters) and VALUE (turn to select, press to confirm).</li>
<li><b>Left block</b> – PATTERN SELECT, PATTERN EDIT, RECORD SETTING / DEL, REC, RESAMPLE / EXIT, COPY, REMAIN.</li>
<li><b>Right block</b> – START/END, PITCH/SPEED, MARK / BPM SYNC, GATE, LOOP, REVERSE, ROLL / banks A/F–E/J and SHIFT.</li>
<li><b>Pads</b> – 16 pads numbered left→right, top→bottom. The column on their right: BUS FX, HOLD, EXT SOURCE, SUB PAD.</li></ul></div>
<div class="box"><h2>Golden rules</h2><ul>
<li><b>[[SHIFT]]</b> gives a pad or button its alternate function while held (orange labels).</li>
<li><b>[[EXIT]]</b> backs out or cancels. Stop everything: [[SHIFT]] + [[EXIT]].</li>
<li><b>Banks</b>: 10 banks via [[A/F]]–[[E/J]]; press [[A/F]] to toggle A and F. For banks F–J press the bank button twice so it blinks.</li>
<li><b>Buses</b>: [[BUS FX]] switches the selected bus – solid orange = BUS 1, blinking orange = BUS 2.</li>
<li><b>Live safety</b>: hold [[SHIFT]] + hold [[REMAIN]] for 3 s = LIVE MODE (locks edit buttons).</li>
<li>Combos read <b>hold + press</b>: the first key is held, the second tapped.</li></ul></div>
</div>
<div class="box"><h2>Booklet map</h2>
<div class="map" style="grid-template-columns:repeat(5,1fr)"><div><b>p2 Sampling</b><br>REC · skip-back · resample · merge · copy · delete</div><div><b>p3 Play &amp; edit</b><br>gate · loop · roll · velocity · mute · chop · live mode</div><div><b>p4 Patterns</b><br>record · TR-REC · chain · edit · tempo</div><div><b>p5 FX &amp; system</b><br>buses · MFX · projects · utility</div><div><b>p6 DJ &amp; SHIFT</b><br>DJ mode · SHIFT table · pad grid</div></div></div>
'''

# ---------- PAGE 2 ----------
c2 = [
 card("Sample (REC)", {"rec": (P,1), "p5": (P,2)}, "auto",
      "Press [[REC]] – empty pads blink red. Press a blinking pad (destination). Press [[REC]] to start; press the pad or [[REC]] again to stop. [[CTRL 2]] sets length; [[EXIT]] cancels."),
 card("Skip-back sampling (MARK)", {"mark": (P,1), "rec": (P,2), "p9": (P,3)}, "auto",
      "Play a sample or pattern (or use [[EXT SOURCE]]); [[MARK]] blinks while audio is buffered. Press [[MARK]] (waveform shown), press [[REC]] (“Select Pad To Save”), then a pad. [[EXIT]] discards. [[SHIFT]] + press [[VALUE]] switches [[MARK]] between skip-back and Looper."),
 card("Resample", {"resample": (P,1), "rec": (P,3)}, "buttons",
      "Press [[RESAMPLE]]; [[CTRL 2]] sets length; [[RECORD SETTING]] &gt; ROUTING = Mix; press [[EXIT]] or [[RESAMPLE]]. Press a blinking pad, then a pad to begin (starts when the pattern plays). Press the pad or [[REC]] to stop."),
 card("Sample merge", {"shift": (H,1), "resample": (P,2), "value": (T,3), "c1": (T,3), "c3": (T,3)}, ["knobs", "buttons"],
      "[[SHIFT]] + [[RESAMPLE]]. Press up to four pads. [[CTRL 1]] picks SUM or MUL; [[CTRL 3]] sets levels; press [[VALUE]] to run. Press the destination pad, then [[VALUE]]."),
 card("Copy · swap a sample", {"copy": (P,1), "p2": (P,2), "p10": (P,3), "shift": (H,None)}, "auto",
      "Copy: [[COPY]], source pad, destination pad, then [[VALUE]] or [[COPY]] to confirm (overwrites). Swap: [[SHIFT]] + [[pad 5]], press two pads, then [[VALUE]] or [[COPY]]."),
 card("Delete a sample", {"del": (P,1), "p6": (P,2)}, "auto",
      "One pad: [[DEL]], the pad, then [[VALUE]] or [[DEL]]. Whole bank: hold [[DEL]] + [[EXIT]], press the bank button, then [[VALUE]] or [[DEL]]."),
]
bankops = tbl(["Do this", "Input", "Notes"], [
 ["<b>Copy a bank</b>", "hold [[COPY]] + [[EXIT]]", "Select the source bank, turn [[VALUE]] to move the cursor, then select the destination bank"],
 ["<b>Protect a bank</b>", "bank button(s), then [[SHIFT]] + [[COPY]]", "Choose OK with [[VALUE]] and press it. Repeat to remove protection. Stops samples/patterns being copied over, edited over or deleted"],
 ["<b>Bank volume</b>", "[[SHIFT]] + bank button [[A/F]]–[[E/J]]", "Overall volume of that bank"],
 ["<b>Count-in · metronome</b>", "[[SHIFT]] + [[pad 10]] · [[SHIFT]] + [[pad 9]]", "Count-in cycles 1MEAS, 2MEAS, WAIT, OFF"],
 ["<b>Sound generator</b>", "[[SHIFT]] + [[RECORD SETTING]]", "Switches to sound generator mode"],
 ["<b>Input settings</b>", "[[SHIFT]] + [[EXT SOURCE]]", "Opens the input settings screen"],
])
p2 = '<div class="grid">' + "".join(c2) + '</div>' + bankops

# ---------- PAGE 3 ----------
c3 = [
 card("GATE · LOOP · REVERSE · ROLL · HOLD", {"gate": (P,1), "loop": (P,1), "reverse": (P,1), "roll": (P,1), "hold": (P,2)}, "lower",
      "[[GATE]] toggles (with [[SHIFT]] = whole bank). [[LOOP]] on; add [[REVERSE]] for reverse looping; [[SHIFT]] + [[LOOP]] = ping-pong. [[ROLL]]: hold + pad, or press during playback; [[SHIFT]] + [[ROLL]] cycles the interval. [[HOLD]]: with GATE on, hold pads then press [[HOLD]]."),
 card("Velocity &amp; chromatic", {"shift": (H,1), "p1": (P,2), "p2": (P,2), "p4": (P,2)}, "auto",
      "[[SHIFT]] + [[pad 1]] FIXED VELOCITY (always 127) · [[SHIFT]] + [[pad 2]] 16 VELOCITY · [[SHIFT]] + [[pad 4]] CHROMATIC (pads play pitches as a scale)."),
 card("Pad mute", {"shift": (H,1), "reverse": (H,2), "p6": (P,3)}, "auto",
      "Hold [[SHIFT]] + [[REVERSE]], then press pads 1–16 to mute/unmute. Add [[REMAIN]] to latch SHIFT and REVERSE so you can let go."),
 card("Select silently · timing", {"value": (H,1), "p8": (P,2), "sub_pad": (P,3)}, "lower",
      "Hold [[VALUE]] + pad selects a sample with no sound (a pattern if PATTERN SELECT is lit). Hold [[VALUE]] + [[SUB PAD]] minimises timing differences when playing several samples together."),
 card("Live mode", {"shift": (H,1), "remain": (H,2)}, "buttons",
      "Hold [[SHIFT]] and hold [[REMAIN]] for 3 s. While on, [[DEL]], [[REC]], [[RESAMPLE]], [[COPY]] and [[MARK]] are disabled. Repeat to turn off."),
]
edit = tbl(["Edit / marker tool", "Input", "Notes"], [
 ["<b>CHOP</b>", "[[SHIFT]] + [[START/END]]", "Or: add markers with [[MARK]], press [[VALUE]], choose ASSIGN TO PAD, press target pads, set marker with [[CTRL 2]], order pads with [[VALUE]], [[MARK]] confirms, [[VALUE]] assigns"],
 ["<b>ENVELOPE</b>", "[[SHIFT]] + [[PITCH/SPEED]]", "Fade-in / fade-out (ATTACK, HOLD, RELEASE)"],
 ["<b>Edit a whole bank</b>", "hold [[REMAIN]] + knob on the PITCH/SPEED or ENVELOPE screen", "Applies SPEED, PITCH, VOLUME, PAN, BPM, BPM SYNC, GATE, LOOP, REVERSE (and ATTACK/HOLD/RELEASE) to every sample in the bank"],
 ["<b>Edit a mute group</b>", "hold [[COPY]] + same knobs", "Same parameters, but only samples in the same mute group"],
 ["<b>Switch-all</b>", "[[SHIFT]] + [[GATE]] · [[SHIFT]] + [[BPM SYNC]]", "GATE ALL / SYNC ALL on or off for the selected bank"],
 ["<b>One-shot mode</b>", "hold [[VALUE]] + [[GATE]]", "Toggles one-shot playback"],
 ["<b>Sample tempo</b>", "[[PITCH/SPEED]], pick pad, [[VALUE]]", "BPM SET = AUTO or MANU"],
 ["<b>Stop all · pause</b>", "[[SHIFT]] + [[EXIT]] · [[SHIFT]] + [[HOLD]]", "Stops all playing samples · pauses everything playing"],
])
p3 = '<div class="grid">' + "".join(c3) + '</div>' + edit

# ---------- PAGE 4 ----------
c4 = [
 card("Record a pattern (real-time)", {"pattern_select": (P,1), "rec": (P,2), "remain": (P,3)}, "buttons",
      "[[PATTERN SELECT]], then [[REC]] (empty pads blink red). Press a blinking pad. Press [[REMAIN]] for Real-Time. [[CTRL 1]] BPM · [[CTRL 2]] LENGTH · [[CTRL 3]] STRENGTH · [[VALUE]] QTZ. Press [[REC]] to start. [[EXIT]] once = finish &amp; save; again = stop playback. While recording, [[REC]] toggles rehearsal ↔ recording."),
 card("Tempo · count-in · metronome", {"shift": (H,1), "p9": (P,2), "p10": (P,2), "p11": (P,2)}, "auto",
      "[[SHIFT]] + [[pad 9]] metronome · [[SHIFT]] + [[pad 10]] count-in · [[SHIFT]] + [[pad 11]] opens TEMPO SEL: [[CTRL 1]] picks PROJECT or BANK A–J, [[VALUE]] sets, [[EXIT]]. Tap tempo: tap [[SUB PAD]] in time, then [[EXIT]]."),
 card("TR-REC (step sequencer)", {"pattern_select": (P,1), "rec": (P,2), "remain": (P,3), "sub_pad": (H,4)}, "lower",
      "[[PATTERN SELECT]], [[REC]], blinking pad, [[REMAIN]] for TR-REC. [[CTRL 1]] BPM · [[CTRL 2]] LENGTH · [[CTRL 3]] SHUFFLE. [[REC]] begins. Hold [[SUB PAD]] + a pad to pick the sample; pads 1–16 place steps; [[VALUE]] moves to the next measure; [[EXIT]] twice to finish. Also [[SHIFT]] + [[REC]] while a pattern plays."),
 card("Pattern chain", {"pattern_select": (P,1), "hold": (H,2), "p3": (P,3), "sub_pad": (P,4)}, "lower",
      "Create: [[PATTERN SELECT]], hold [[HOLD]] + a pad (chain number), press pads to add patterns, [[EXIT]] saves. Repeat: [[REMAIN]] toggles; [[START/END]] cycles REPEAT All / Current / Off. Play: hold [[HOLD]] + chain pad; [[SUB PAD]] start/stop; [[EXIT]] leaves."),
 card("Pattern edit &amp; quantize", {"pattern_select": (P,1), "pattern_edit": (P,2), "record_setting": (P,3)}, "buttons",
      "[[PATTERN SELECT]], [[PATTERN EDIT]], the pattern pad. [[CTRL 1]] BPM · [[CTRL 2]] LOOP START · [[CTRL 3]] LENGTH; [[VALUE]] menu: DUPLICATE (doubles) or CROP (keeps loop range). Quantize: [[RECORD SETTING]], press sample pads, [[CTRL 2]] QTZ · [[CTRL 3]] STR · [[SHIFT]]+[[CTRL 2]] QS · [[SHIFT]]+[[CTRL 3]] QE, [[VALUE]] &gt; OK (<u>can’t be undone</u>)."),
]
patt = tbl(["Do this", "Input", "Notes"], [
 ["<b>Undo last input</b>", "[[SHIFT]] + [[PATTERN SELECT]]", "Only while recording a pattern"],
 ["<b>Pattern bank</b>", "bank [[A/F]]–[[E/J]] while PATTERN SELECT is lit", "[[A/F]] toggles A/F; double-press for F–J"],
 ["<b>Delete notes (TR-REC)</b>", "[[DEL]] + [[A/F]] · [[DEL]] + [[B/G]]", "One measure for the selected pad · for all pads"],
 ["<b>Record knob motion (TR-REC)</b>", "[[ROLL]] + [[CTRL 1]] / [[CTRL 2]] / [[CTRL 3]]", "Needs MODE = TRIG"],
 ["<b>Delete EFX motion · pad mutes</b>", "[[DEL]] + [[MARK]] · [[DEL]] + [[REVERSE]]", "On the pattern edit screen"],
 ["<b>Select pattern silently</b>", "hold [[VALUE]] + pad", "While PATTERN SELECT is lit (pattern does not play)"],
])
p4 = '<div class="grid">' + "".join(c4) + '</div>' + patt

# ---------- PAGE 5 ----------
c5 = [
 card("Effects &amp; buses", {"fx_fd": (P,1), "fx_res": (P,1), "fx_delay": (P,1), "fx_iso": (P,1), "fx_djfx": (P,1), "fx_mfx": (P,1), "c1": (T,2), "c2": (T,2), "c3": (T,2)}, "top",
      "Press [[BUS FX]] to pick the bus (solid orange BUS 1 · blinking BUS 2). With a bus selected, press an effect button (FILTER+DRIVE … MFX) to assign it. Play a pad and edit with [[CTRL 1–3]]."),
 card("Route a sample to a bus", {"remain": (H,1), "p3": (P,2), "bank_BG": (P,2)}, "auto",
      "Select BUS 2 with [[BUS FX]], hold [[REMAIN]], press a pad: orange = BUS 1, green = BUS 2, white = dry. Hold [[REMAIN]] + a bank button sets the send for every sample in that bank."),
 card("MFX list", {"fx_mfx": (H,1), "c3": (T,2), "value": (T,2)}, ["knobs", "buttons"],
      "Hold [[MFX]] and turn [[VALUE]] or [[CTRL 3]]; release [[MFX]] to switch on. Hold [[MFX]] + [[DJFX LOOPER]] for the list from #17, [[MFX]] + [[ISOLATOR]] from #33."),
]
fx = tbl(["Effects &amp; routing", "Input", "Result"], [
 ["<b>Effect grab</b>", "hold [[VALUE]] + effect button", "Effect applies only while the button is held"],
 ["<b>Mute bus</b>", "[[SHIFT]] + [[BUS FX]]", "Silences the bus send, so only the effect is heard"],
 ["<b>Swap BUS 1 / BUS 2</b>", "hold [[REMAIN]] + [[BUS FX]]", "Swaps the two buses’ effects (parameters kept)"],
 ["<b>Bypass BUS 3 &amp; 4</b>", "hold [[VALUE]] + [[BUS FX]]", "Temporary bypass"],
 ["<b>Keep MFX screen open</b>", "hold [[REMAIN]] + [[MFX]]", "Effect edit screen stays displayed"],
 ["<b>Save EFX parameters</b>", "[[SHIFT]] + hold [[MARK]] 3 s", "Saves main parameters of BUS 1 / BUS 2 effects"],
 ["<b>EFX settings (BUS 3/4)</b>", "[[SHIFT]] + [[pad 16]]", "UTILITY &gt; EFX SET"],
])
sysx = tbl(["System &amp; projects", "Input", "Result"], [
 ["<b>Select project</b>", "[[SHIFT]] + [[SUB PAD]], then pad 1–16", "SELECT PROJECT screen"],
 ["<b>Copy · delete project</b>", "[[SHIFT]] + [[SUB PAD]], then [[COPY]] (source pad, destination pad) or [[DEL]] (pad), then [[VALUE]]", "Copy overwrites the destination"],
 ["<b>Utility menu</b>", "[[SHIFT]] + [[pad 13]]", "Also: [[pad 12]] GAIN · [[pad 15]] PAD SET"],
 ["<b>Import / export</b>", "[[SHIFT]] + [[pad 14]]", "Samples or projects, to / from SD card"],
 ["<b>Headphone CUE</b>", "[[SHIFT]] + [[pad 3]]", "[[CTRL 3]] balances C (cue) ↔ M (main); [[EXIT]] leaves"],
 ["<b>Input settings</b>", "[[SHIFT]] + [[EXT SOURCE]]", "Also toggles external input on/off with [[EXT SOURCE]]"],
])
p5 = '<div class="grid">' + "".join(c5) + '</div>' + fx + sysx

# ---------- PAGE 6 ----------
dj = tbl(["DJ mode (enter: banks D/I + E/J together)", "Input"], [
 ["Mute CH1 / CH2", "[[SHIFT]] + [[REVERSE]] + [[pad 13]] / [[pad 15]]"],
 ["Play from marker", "[[SHIFT]] + pads 1–16 (latch SHIFT with [[SHIFT]] + [[REMAIN]]; [[EXIT]] cancels)"],
 ["Add · edit · delete markers", "[[SHIFT]] + [[MARK]] · [[SHIFT]] + [[START/END]] · [[SHIFT]] + [[DEL]] + pad"],
 ["Roll size · roll", "[[SHIFT]] + [[ROLL]] (1/4, 1/2, 1, 2 bars) · [[ROLL]] + [[pad 13]] / [[pad 15]]"],
 ["Change roll while rolling", "[[ROLL]] + pads 1–4 (¼ · ½ · 1 · 2 bars)"],
 ["Bus per channel", "hold [[REMAIN]] + [[pad 14]] (CH1) / [[pad 16]] (CH2): BUS-1 → BUS-2 → DRY"],
 ["CTRL 3 function", "[[START/END]] switches CUE MIX ↔ X-FADE"],
 ["Mixer ↔ EFX view", "[[MARK]]"],
 ["Fader curve", "hold [[RESAMPLE]] + press [[VALUE]]: FAST CUT → LINEAR → SQUARE → CUBIC"],
 ["Reset BPM", "[[DEL]] + pads [[2]] + [[6]] (CH1) / [[4]] + [[8]] (CH2)"],
 ["BPM digits · reverse channel", "[[PITCH/SPEED]] · [[BPM SYNC]] (picks CH for [[REVERSE]])"],
])
shiftbtn = tbl(["SHIFT +", "Function", "SHIFT +", "Function"], [
 ["bank [[A/F]]–[[E/J]]", "BANK VOLUME", "[[GATE]]", "GATE ALL ON/OFF"],
 ["[[COPY]]", "BANK PROTECT", "[[BPM SYNC]]", "SYNC ALL ON/OFF"],
 ["[[LOOP]]", "PING-PONG LOOP", "[[REC]]", "TR-REC (pattern playing)"],
 ["[[ROLL]]", "ROLL SET", "[[RESAMPLE]]", "SAMPLE MERGE"],
 ["[[START/END]]", "CHOP", "[[RECORD SETTING]]", "SOUND GENERATOR"],
 ["[[PITCH/SPEED]]", "ENVELOPE", "[[EXIT]]", "STOP all samples"],
 ["[[PATTERN SELECT]]", "UNDO (recording)", "[[HOLD]]", "PAUSE"],
 ["[[REMAIN]] 3 s", "LIVE MODE", "[[BUS FX]]", "MUTE BUS"],
 ["[[MARK]] 3 s", "SAVE EFX PARAMETER", "[[EXT SOURCE]]", "INPUT SETTING"],
 ["[[VALUE]] (press)", "MARK = skip-back ↔ Looper", "[[SUB PAD]]", "PROJECT"],
])
PADSH = ["FIXED VELOCITY","16 VELOCITY","CUE","CHROMATIC","EXCHANGE","INIT PARAM","PAD LINK","MUTE GROUPS","METRONOME","COUNT-IN","TAP TEMPO","GAIN","UTILITY","IMPORT/EXPORT","PAD SETTING","EFX SETTING"]
padgrid = '<div class="pg4">' + "".join(f'<div class="pc"><b>{i+1}</b><span>{t}</span></div>' for i, t in enumerate(PADSH)) + '</div>'
extras = '<div class="box small"><h2>Community extras – not in Roland’s list</h2><p>From the SP-404MK2 Workflow Cheat Sheet v5.50 by vultilion (CC BY-NC 4.0); <b>not verified against Roland’s documents</b>: rename sample – hold [[REMAIN]] + click [[VALUE]] · numerical start/end edit – [[SHIFT]] + [[VALUE]] · preview loop end – [[ROLL]] · waveform zoom – turn / hold [[VALUE]] · Koala: [[PATTERN EDIT]] opens piano roll / mixer · Serato: pads 1–8 play sampler slots, banks A–D pick Studio decks 1–4.</p></div>'
p6 = '<div class="cols2"><div>' + dj + '</div><div>' + shiftbtn + '</div></div><div class="cols2 tight"><div><h2 class="sec">Pad SHIFT functions</h2>' + padgrid + '</div>' + extras + '</div>'

pages = [
 page(1, "SP-404MKII · stock OS", "Pocket cheat sheet &amp; panel map for the Roland SP-404MKII (firmware v4.00 shortcuts)", p1),
 page(2, "Sampling", "Record · skip-back · resample · merge · copy · swap · delete · banks", p2),
 page(3, "Play &amp; edit", "Gate · loop · roll · velocity · mute · live mode · chop · bank-wide edits", p3),
 page(4, "Patterns", "Record · TR-REC · chain · edit · quantize · tempo", p4),
 page(5, "FX, routing &amp; system", "Buses · MFX · effect grab · projects · utility · import / export", p5),
 page(6, "DJ mode &amp; SHIFT table", "DJ shortcuts · every SHIFT + button · pad functions · community extras", p6),
]
