# Yamaha SEQTRAK (OS V2.00): booklet content. Shared helpers/CSS come from tools/sheet.py.
# Every combo here was checked against Yamaha's SEQTRAK User Guide for OS V2.00 (section numbers in comments).
# Chip names: Drum keys are [[key 1]]-[[key 16]] (top row 1-8, bottom row 9-16); Synth keys are [[S1]]-[[S7]].
from sheet import *

# diagrams print at the layout's fixed scale (see layout.MM_PER_UNIT) instead of stretching to the column
CSS = CSS + '''
.card .pn { display:inline-block; width:auto; max-width:100%; vertical-align:top }
.pn svg { width:auto; max-width:100% }
.hero svg { width:186mm }
'''

TOTAL = 5
def page(n, title, sub, inner):
    return f'''<div class="page"><header><div><h1>{title}</h1><p>{sub}</p></div><div class="pg">SEQTRAK · OS V2.00<br><b>{n} / {TOTAL}</b></div></header>{inner}
<footer>Unofficial cheat sheet compiled from Yamaha’s SEQTRAK User Guide (OS V2.00), cross-checked with community sheets by devopscmac (GitHub) and TAKEUCHI Hitoshi (namaraii.com). Not affiliated with Yamaha. Diagrams are schematic, not to scale.</footer></div>'''

# ---------------- PAGE 1 : panel map ----------------
legend = '''<div class="legend"><span><i class="sw hold"></i>HOLD this control</span><span><i class="sw press"></i>PRESS / TAP it</span><span><i class="sw turn"></i>TURN this knob</span><span><i class="sw num">1</i>order of steps</span><span><b>key 1–16</b> = Drum keys (top row 1–8) · <b>S1–S7</b> = Synth keys</span></div>'''
p1 = f'''
<div class="hero">{panel(None, "all", width_mm=186, aria="SEQTRAK panel map")}</div>
{legend}
<div class="cols2 tight">
<div class="box"><h2>Where things live</h2>
<ul>
<li><b>Left edge</b> – [[VOL+]] / [[VOL−]], [[DELETE]], [[MUTE]], [[SOLO]], [[PAGE]] and [[PLAY]] (hold 2 s = power).</li>
<li><b>Track knobs</b> – [[ALL]] plus the 7 drum tracks (KICK … PERC 2) and SYNTH 1, SYNTH 2, DX, SAMPLER. <b>Turn</b> = change pattern, <b>press</b> = select the track (when stopped it also plays the sound).</li>
<li><b>Drum keys 1–16</b> – the steps; also numbered choices (projects 1–8, patterns 1–6, sound categories, scenes).</li>
<li><b>Record key + Synth keys S1–S7</b> – play notes or samples. Above them on the top edge: BAR LENGTH, OCTAVE, SCALE, KEY, REC SAMPLE.</li>
<li><b>Right</b> – SOUND 1–4 knobs with SD PAGE and UNDO/REDO; FX knob, MASTER/SINGLE, CLEAR FX, touch sliders FX LEVEL · HIGH PASS · REPEATER with FX PAGE. <b>Right edge</b>: BPM+ / BPM−, SWING, PROJECT↑.</li>
</ul></div>
<div class="box"><h2>Golden rules</h2>
<ul>
<li><b>Hold [[ALL]] is the shift key</b> – it opens the modes: Mixer, Mute, Song, keyboard input, metronome, chord edit.</li>
<li><b>[[ALL]] is also the dial</b>: hold BPM±, SWING, OCTAVE, SCALE, KEY, VOL± or PAGE and turn [[ALL]] to scroll the value.</li>
<li><b>Press and turn</b> any knob for bigger jumps (a whole bar at a time for lengths).</li>
<li><b>Saving is automatic</b> when you switch projects or power off.</li>
<li>[[UNDO/REDO]] covers sound and effect tweaks only – not notes or sound choices.</li>
<li>Combos are written <b>hold + press</b>: keep the first control held, tap the second.</li>
</ul></div>
</div>
<div class="box"><h2>Booklet map</h2>
<div class="map"><div><b>p2 Projects &amp; patterns</b><br>power · projects · tempo · swing · patterns · length · copy</div><div><b>p3 Drums &amp; synths</b><br>steps · micro timing · substeps · probability · chords · step input</div><div><b>p4 Sampler &amp; sound</b><br>sampling · sounds · pages · parameter lock · motion rec</div><div><b>p5 FX, mixer &amp; modes</b><br>effects · mixer · mute · song · every shortcut</div></div></div>
'''

# ---------------- PAGE 2 ----------------
# 3.2, 4.1-4.6, 5.1-5.5, 5.8
c2 = [
 card("Power · play / stop", {"play": (P, 1)}, "auto",
      "Hold [[PLAY]] for 2 s to switch on or off (the project saves). Press [[PLAY]] to start / stop the project."),
 card("Switch project", {"project": (H, 1), "k3": (P, 2)}, "auto",
      "Hold [[PROJECT↑]] + [[key 1]]–[[key 8]] for projects 1–8 (the current one is lit yellow). Delete: hold [[PROJECT↑]] + [[DELETE]] + that key."),
 card("Tempo · metronome", {"bpm_up": (H, 1), "all": (T, 2)}, "auto",
      "[[BPM+]] / [[BPM−]] (hold to scroll), or hold one and turn [[ALL]]: 5–300 BPM. Both together = back to the project’s starting tempo. Metronome: hold [[ALL]] + [[BPM+]]."),
 card("Swing", {"swing": (H, 1), "all": (T, 2)}, "auto",
      "[[SWING]], or hold [[SWING]] and turn [[ALL]]: −58 to +58 ticks on even steps. Reset: hold [[DELETE]] + [[SWING]]."),
 card("Switch patterns", {"kick": (H, 1), "k2": (P, 2)}, "auto",
      "Turn a Track knob = switch now. Press and turn = switch at the next Launch Quantize. Or hold the knob + [[key 1]]–[[key 6]] (double-tap = now). [[ALL]] does the same for all 11 tracks."),
 card("Pattern length", {"bar_length": (H, 1), "synth1": (T, 2)}, "auto",
      "[[BAR LENGTH]] steps through 1 · 2 · 4 · 8 bars. Hold [[BAR LENGTH]] and turn a Track knob for 1–128 steps. Drum tracks also: hold [[PAGE]] + turn the drum knob."),
 card("Copy · paste · delete a pattern", {"snare": (H, 1), "page": (H, 2), "k4": (P, 3)}, "auto",
      "Copy: hold a Track knob + any Drum key for 2 s (meter flashes). Paste: hold the Track knob + [[PAGE]] + a Drum key. Delete: hold [[DELETE]] + press the Track knob ([[ALL]] = all tracks)."),
 card("Mute · solo a track", {"mute": (H, 1), "clap": (P, 2)}, "auto",
      "Hold [[MUTE]] + press a Track knob (lit green); hold [[SOLO]] + press a Track knob (lit cyan). Press again to undo. Hold [[MUTE]] + [[ALL]] unmutes everything."),
]
more2 = tbl(["Do this", "Input", "Result"], [
 ["<b>Launch Quantize</b>", "hold [[PROJECT↑]] + turn [[ALL]]", "When reserved pattern switches land (default 16 steps); press and turn = per bar"],
 ["<b>Temporary save / restore</b>", "hold [[PROJECT↑]] + the yellow key / the cyan key", "One slot; cleared when you switch project or power off"],
 ["<b>3 ↔ 6 patterns</b>", "hold a Track knob + [[key 4]]–[[key 6]]", "Press the blue keys 4–6 for six patterns; press all three together to go back to three"],
 ["<b>Long patterns</b>", "[[PAGE]] · hold [[PAGE]] + turn [[ALL]]", "Shows the next 16 steps (page flashes cyan on the meter)"],
 ["<b>Battery level</b>", "hold [[ALL]] + [[PLAY]]", "Meter: cyan = charging, white = on battery"],
 ["<b>Force power off</b>", "hold [[PLAY]] + [[PROJECT↑]]", "Only if it hangs – changes since power-on are lost"],
 ["<b>Auto power off</b>", "power on while holding [[key 9]]", "Toggles the 30-minute auto power off"],
 ["<b>Factory reset</b>", "power on while holding [[SAMPLER]] + [[UNDO/REDO]]", "Restores demo projects and settings (meter lights red)"],
])
p2 = '<div class="grid">' + "".join(c2) + '</div>' + more2

# ---------------- PAGE 3 ----------------
# 6.1-6.7, 7.1-7.9
c3 = [
 card("Enter drum steps", {"kick": (P, 1), "k1": (P, 2), "k5": (P, 2), "k9": (P, 2), "k13": (P, 2)}, "drums",
      "Press a drum Track knob, then press Drum keys to toggle steps. Patterns longer than 16 steps: [[PAGE]] for the next page."),
 card("Micro timing", {"k5": (H, 1), "snare": (T, 2)}, "auto",
      "Hold a lit Drum key (or several) and turn a Track knob: −60 to +59 ticks (one step = 120)."),
 card("Substeps (ratchets)", {"k6": (H, 1), "k14": (P, 2)}, "auto",
      "Hold a lit Drum key for 2 s; five keys light on the other row: none · ×2 · ×3 (8th triplet) · ×3 (16th triplet) · ×4."),
 card("Step probability", {"k7": (H, 1), "mute": (P, 2)}, "auto",
      "Hold a lit Drum key + press [[MUTE]]: each press lowers the chance one of 8 levels (meter shows it); from the lowest it wraps to 100%."),
 card("Drum track type (OS 2.00)", {"perc1": (H, 1), "k10": (H, 2)}, "auto",
      "Stopped only. Hold the drum Track knob, then hold [[key 9]] Drum · [[key 10]] DrumKit (sounds on S1–S7) · [[key 11]] Synth for 5 s until it lights purple. Erases that track’s notes."),
 card("Play drums live", {"hat1": (H, 1), "s1": (P, 2)}, "auto",
      "Hold a drum Track knob + press a Synth key to toggle real-time input; then play the Synth keys and press [[REC]] to record."),
 card("Play &amp; record synths", {"synth1": (P, 1), "rec": (P, 2), "s3": (P, 3)}, "synth",
      "Press [[SYNTH 1]], [[SYNTH 2]] or [[DX]], play S1–S7, press [[REC]] to record (overdubs keep earlier notes). Quantize on/off: hold [[ALL]] + [[REC]]."),
 card("Octave · scale · key", {"octave": (P, None), "scale": (P, None), "key": (H, 1), "all": (T, 2)}, "auto",
      "Press [[OCTAVE]] / [[SCALE]] / [[KEY]], or hold one and turn [[ALL]]. Octave −3 to +2; 8 scales per project; key in semitones. Recorded notes don’t change."),
 card("Chords", {"all": (H, 1), "s2": (P, 2)}, "auto",
      "[[SOUND 2]] on page 1 picks MONO · POLY · CHORD (7 chords on S1–S7). Edit one: hold [[ALL]] + its Synth key, then toggle up to 4 notes on the Drum keys."),
 card("Keyboard input · step input", {"page": (H, 1), "dx": (P, 2)}, "auto",
      "Hold [[ALL]] + [[KEY]]: the Drum keys become a keyboard. Step input: hold [[PAGE]] + press a synth-section knob; keys enter the last note played. Hold a lit key + turn [[ALL]] = note length."),
]
scales = '<p class="cap">Default scales, in [[SCALE]] order: Minor · Major · Minor pentatonic · Major pentatonic · Lydian · Dorian · Mixolydian · Phrygian (edit them in the app).</p>'
p3 = '<div class="grid">' + "".join(c3) + '</div>' + scales

# ---------------- PAGE 4 ----------------
# 8.1-8.11, 5.7, 9.1-9.5
c4 = [
 card("Sample a sound", {"sampler": (P, 1), "s4": (P, 2), "rec_sample": (P, 3)}, "synth",
      "Press [[SAMPLER]], press the Synth key to fill (flashes red), then [[REC SAMPLE]] to start and again to stop (16 s max). A cable in AUDIO IN is sampled instead of the mic."),
 card("Sampling source · cancel", {"rec_sample": (H, 1), "k1": (P, 2)}, "auto",
      "Hold [[REC SAMPLE]] 2 s + the white Drum key: mic / AUDIO IN · USB audio · resample. Cancel a take: hold [[DELETE]] + [[REC SAMPLE]]."),
 card("Count-in · input level", {"rec_sample": (H, 1), "vol_up": (P, 2)}, "auto",
      "Count-in on/off: hold [[ALL]] + [[REC SAMPLE]]. Input meter (monitoring): hold [[REC SAMPLE]] + [[VOL+]], same again to leave."),
 card("Per-sample mute · clear", {"mute": (H, 1), "s5": (P, 2)}, "auto",
      "With SAMPLER selected: hold [[MUTE]] + a Synth key mutes that sample (lit green); hold [[DELETE]] + a Synth key clears that sample’s pattern."),
 card("Choose a sound", {"sd1": (T, 1)}, "auto",
      "Select a track, turn [[SOUND 1]] on page 1 (SAMPLER: press the Synth key first). Category jump: hold [[SOUND 1]] + a Drum key ([[key 16]] = your favourites)."),
 card("Sound Design pages", {"sd_page": (P, 1), "sd2": (T, 2)}, "auto",
      "[[SOUND 1]]–[[SOUND 4]] edit four parameters; [[SD PAGE]] moves to the next page. Hold [[SD PAGE]] 2 s for the advanced pages. Press and turn = bigger moves."),
 card("Parameter lock", {"k5": (H, 1), "sd3": (T, 2)}, "auto",
      "Hold a lit Drum key (or several) and turn [[SOUND 1]]–[[SOUND 4]] or slide [[FX LEVEL]]: the step turns purple. Clear: hold [[DELETE]] + press that knob (add the Drum key for one step)."),
 card("Motion recording · save", {"rec": (H, 1), "sd4": (T, 2)}, "auto",
      "Hold [[REC]] and turn SOUND knobs or slide the touch sliders to record moves. Clear: hold [[DELETE]] + press the knob. Save a sound: hold [[ALL]] + press [[SOUND 1]] (added as “_editNN” and to favourites)."),
]
pages_tbl = tbl(["Track", "Pages 1 · 2", "Advanced pages (hold SD PAGE 2 s)"], [
 ["<b>Drum / DrumKit</b>", "SOUND · PITCH · PAN · VOLUME · ATTACK · DECAY · FILTER · RESONANCE", "3: REVERB · DELAY · EQ HIGH · EQ LOW"],
 ["<b>SYNTH 1 / 2</b> (and Synth-type drums)", "SOUND · MONO/POLY/CHORD · PAN · VOLUME · ATTACK · DECAY/RELEASE · FILTER · RESONANCE", "3: REVERB · DELAY · EQ HIGH · EQ LOW · 4: PORTAMENTO · ARP TYPE · ARP GATE · ARP SPEED"],
 ["<b>DX</b>", "as SYNTH (DECAY instead of DECAY/RELEASE)", "3 and 4 as SYNTH · 5: FM ALGORITHM · MOD AMOUNT · MOD FREQUENCY · MOD FEEDBACK"],
 ["<b>SAMPLER</b>", "SOUND · PITCH · PAN · VOLUME · ATTACK · DECAY · FILTER · RESONANCE", "3: REVERB · DELAY · EQ HIGH · EQ LOW · 4: START · END · LOOP ON/OFF · LOOP LENGTH · 5: pitch EG attack/decay level and time"],
])
p4 = '<div class="grid">' + "".join(c4) + '</div><h2 class="sec">Sound Design pages (knobs 1–4, top to bottom)</h2>' + pages_tbl

# ---------------- PAGE 5 ----------------
# 10, 11, 12, 13, 15.1.2, 16.4
c5 = [
 card("Effects", {"master_single": (P, 1), "fx": (T, 2), "fx_level": (P, 3)}, "auto",
      "[[MASTER/SINGLE]]: MASTER = whole mix, SINGLE = selected track. Turn [[FX]] for the type (8 categories × 8). The sliders set its parameters; [[FX PAGE]] swaps slider pages. [[CLEAR FX]] drops the current parameter to minimum."),
 card("HIGH PASS · REPEATER", {"high_pass": (P, None), "repeater": (P, None)}, "auto",
      "Performance sliders: on page 1 they always act on every track, and stop when you lift your finger."),
 card("Mixer mode", {"all": (H, 1), "vol_up": (P, 2)}, "auto",
      "Hold [[ALL]] + [[VOL+]] (same to leave). Press [[SOUND 1]]–[[SOUND 4]] for PAN · VOLUME · REVERB · DELAY, then turn Track knobs per track; [[ALL]] sets the project / return level. Reverb or delay picked: [[FX]] chooses the preset."),
 card("Mute mode", {"all": (H, 1), "mute": (P, 2)}, "auto",
      "Hold [[ALL]] + [[MUTE]]: now a press on any Track knob mutes it; [[ALL]] unmutes all; [[MUTE]] leaves."),
 card("Song · scene mode", {"all": (H, 1), "project": (P, 2)}, "auto",
      "Hold [[ALL]] + [[PROJECT↑]] = Song mode (again = Scene mode, which loops one scene). Drum keys are scenes (up to 16): an empty key adds a copy; turn Track knobs to set its patterns; [[DELETE]] + red key removes. [[PLAY]] plays; double-tap a scene to loop it; hold [[PAGE]] + turn [[ALL]] sets its length."),
 card("Bluetooth · volume", {"all": (H, 1), "swing": (P, 2)}, "auto",
      "Pair with the app: hold [[ALL]] + [[SWING]] (waits 30 s; also shows the link status). Master volume: [[VOL+]] / [[VOL−]], or hold one and turn [[ALL]]."),
]
master = tbl(["Function", "Input", "Function", "Input"], [
 ["Power on / off", "hold [[PLAY]] 2 s", "Metronome", "hold [[ALL]] + [[BPM+]]"],
 ["Switch project", "hold [[PROJECT↑]] + [[key 1]]–[[key 8]]", "Launch Quantize", "hold [[PROJECT↑]] + turn [[ALL]]"],
 ["Delete project", "hold [[PROJECT↑]] + [[DELETE]] + key", "Swing reset", "hold [[DELETE]] + [[SWING]]"],
 ["Copy pattern", "hold Track knob + Drum key 2 s", "Paste pattern", "hold Track knob + [[PAGE]] + Drum key"],
 ["Delete pattern", "hold [[DELETE]] + Track knob", "Copy / paste steps", "hold Drum key 2 s · hold [[PAGE]] + Drum key"],
 ["Mute / solo track", "hold [[MUTE]] / [[SOLO]] + Track knob", "Unmute all", "hold [[MUTE]] + [[ALL]]"],
 ["Quantize on/off", "hold [[ALL]] + [[REC]]", "Keyboard input", "hold [[ALL]] + [[KEY]]"],
 ["Step input (synth)", "hold [[PAGE]] + synth knob", "Note length", "hold lit Drum key + turn [[ALL]]"],
 ["Count-in", "hold [[ALL]] + [[REC SAMPLE]]", "Cancel sampling", "hold [[DELETE]] + [[REC SAMPLE]]"],
 ["Save sound", "hold [[ALL]] + press [[SOUND 1]]", "Undo / redo sound", "[[UNDO/REDO]]"],
 ["Mixer mode", "hold [[ALL]] + [[VOL+]]", "Mute mode", "hold [[ALL]] + [[MUTE]]"],
 ["Song mode", "hold [[ALL]] + [[PROJECT↑]]", "Bluetooth pairing", "hold [[ALL]] + [[SWING]]"],
])
p5 = '<div class="grid">' + "".join(c5) + '</div><h2 class="sec">Master shortcut table</h2>' + master

pages = [
 page(1, "SEQTRAK", "Pocket cheat sheet &amp; panel map for the Yamaha SEQTRAK (OS V2.00)", p1),
 page(2, "Projects &amp; patterns", "Power · projects · tempo · swing · patterns · length · copy · mute", p2),
 page(3, "Drums &amp; synths", "Steps · micro timing · substeps · probability · track types · synth input · chords", p3),
 page(4, "Sampler &amp; sound design", "Sampling · sounds · Sound Design pages · parameter lock · motion recording", p4),
 page(5, "FX, mixer &amp; modes", "Effects · mixer · mute · song and scenes · every shortcut on one page", p5),
]
