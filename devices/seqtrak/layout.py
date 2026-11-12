# Yamaha SEQTRAK top panel: element geometry for the schematic (not to scale).
# Arrangement follows the panel drawings in Yamaha's SEQTRAK User Guide (OS V2.00, section 2):
# side-face buttons are drawn beside the top panel (VOL+ ... PLAY on the left, BPM+ ... PROJECT↑ on the right),
# top-edge buttons above the section they sit on. The index column, Global Meter and speaker are not drawn.
# Each element: (id, kind, cx, cy, w, h, label, sublabel). See tools/panel.py for the kinds.

def build_elems():
    E = []
    # left side face
    for i, (id_, lab) in enumerate([("vol_up", "VOL+"), ("vol_dn", "VOL−"), ("delete", "DELETE"), ("mute", "MUTE"),
                                     ("solo", "SOLO"), ("page", "PAGE"), ("play", "PLAY")]):
        E.append((id_, "btn", 64, 40 + i * 52, 76, 42, lab, ""))
    # Drum section knobs (ALL + 7 drum tracks), 4 x 2
    for r, row in enumerate([[("all", "ALL"), ("kick", "KICK"), ("snare", "SNARE"), ("clap", "CLAP")],
                             [("hat1", "HAT 1"), ("hat2", "HAT 2"), ("perc1", "PERC 1"), ("perc2", "PERC 2")]]):
        for c, (id_, lab) in enumerate(row):
            E.append((id_, "knob", 178 + c * 150, 78 + r * 84, 44, 44, lab, ""))
    # Synth section knobs, 2 x 2
    for r, row in enumerate([[("synth1", "SYNTH 1"), ("synth2", "SYNTH 2")], [("dx", "DX"), ("sampler", "SAMPLER")]]):
        for c, (id_, lab) in enumerate(row):
            E.append((id_, "knob", 790 + c * 150, 78 + r * 84, 44, 44, lab, ""))
    # top-edge buttons above the Synth section
    for i, (id_, lab) in enumerate([("bar_length", "BAR\nLENGTH"), ("octave", "OCTAVE"), ("scale", "SCALE"),
                                     ("key", "KEY"), ("rec_sample", "REC\nSAMPLE")]):
        E.append((id_, "btn", 766 + i * 66, 24, 62, 36, lab, ""))
    # Drum keys 1-16: top row 1-8, bottom row 9-16
    for n in range(16):
        r, c = divmod(n, 8)
        E.append((f"k{n+1}", "pad", 170 + c * 74, 262 + r * 70, 66, 62, str(n + 1), ""))
    # Record key + Synth keys: top row REC, S1-S3; bottom row S4-S7
    E.append(("rec", "btn", 772, 262, 66, 62, "REC", ""))
    for i in range(7):
        r, c = divmod(i + 1, 4)
        E.append((f"s{i+1}", "pad2", 772 + c * 74, 262 + r * 70, 66, 62, f"S{i+1}", ""))
    # Sound Design: UNDO/REDO (top edge), knobs 1-4, Sound Design Page button (bottom edge)
    E.append(("undo", "btn", 1108, 24, 76, 36, "UNDO/\nREDO", ""))
    for i in range(4):
        E.append((f"sd{i+1}", "knob", 1092, 84 + i * 68, 40, 40, f"SOUND {i+1}", ""))
    E.append(("sd_page", "btn", 1108, 370, 76, 32, "SD PAGE", ""))
    # FX: CLEAR FX (top edge), FX knob, MASTER/SINGLE switch, touch sliders, FX Page button (bottom edge)
    E.append(("clear_fx", "btn", 1284, 24, 76, 36, "CLEAR\nFX", ""))
    E.append(("fx", "knob", 1262, 86, 44, 44, "FX", ""))
    E.append(("master_single", "btn", 1284, 148, 110, 40, "MASTER/\nSINGLE", ""))
    for i, (id_, lab) in enumerate([("fx_level", "FX\nLEVEL"), ("high_pass", "HIGH\nPASS"), ("repeater", "REPEATER")]):
        E.append((id_, "btn", 1262 + i * 76, 262, 70, 130, lab, ""))
    E.append(("fx_page", "btn", 1262, 370, 70, 32, "FX PAGE", ""))
    # right side face
    for i, (id_, lab) in enumerate([("bpm_up", "BPM+"), ("bpm_dn", "BPM−"), ("swing", "SWING"), ("project", "PROJECT↑")]):
        E.append((id_, "btn", 1514, 196 + i * 52, 84, 42, lab, ""))
    return E

ELEMS = build_elems()
CROPS = {
    "all": (10, 0, 1570, 400),
    "drums": (20, 0, 740, 400),      # side buttons, drum knobs, Drum keys
    "keys": (130, 222, 970, 150),    # Drum keys + Record/Synth keys
    "synth": (730, 0, 320, 400),     # synth knobs, top-edge buttons, Record/Synth keys
    "sound": (1040, 0, 540, 400),    # Sound Design, FX, right side buttons
}
BODY = (18, 4, 1552, 392, 22)
VIEW_H = 400
AUTO_X = (10, 1570)
FIT_X = True            # auto crops also fit horizontally to the lit controls
MM_PER_UNIT = 0.095     # PDF diagrams print at one scale (labels stay the same size)
FULL_W = 480            # web: a crop this wide (or wider) fills the column
LABEL_RIGHT = [e[0] for e in ELEMS if e[1] == "knob"]
