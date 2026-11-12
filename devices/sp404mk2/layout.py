# Roland SP-404MKII top panel: element geometry for the schematic (not to scale).
# Layout verified against Roland's SP-404MK2 Reference Manual panel photos.
# Each element: (id, kind, cx, cy, w, h, label, sublabel). Kinds the renderer knows:
#   knob, btn, disp (round display), pad (number + SHIFT bar), pad2 (named pad + SHIFT bar).
# The viewBox is 1000 x 750; CROPS are named (x, y, w, h) windows into it.

def build_elems():
    E = []  # (id, kind, cx, cy, w, h, label, sublabel)
    # knobs
    for i, (id_, x, lab) in enumerate([("vol", 200, "VOLUME"), ("c1", 390, "CTRL 1"), ("c2", 580, "CTRL 2"), ("c3", 800, "CTRL 3")]):
        E.append((id_, "knob", x, 38, 34, 34, lab, ""))
    # fx buttons
    for i, (id_, lab) in enumerate([("fx_fd", "FILTER\n+DRIVE"), ("fx_res", "RESONATOR"), ("fx_delay", "DELAY")]):
        E.append((id_, "btn", 200, 100 + i * 46, 140, 38, lab, ""))
    for i, (id_, lab) in enumerate([("fx_iso", "ISOLATOR"), ("fx_djfx", "DJFX\nLOOPER"), ("fx_mfx", "MFX")]):
        E.append((id_, "btn", 800, 100 + i * 46, 140, 38, lab, ""))
    # display
    E.append(("display", "disp", 500, 146, 92, 92, "DISPLAY", ""))
    # left block 3x3
    L = [["pattern_select", "pattern_edit", "record_setting"], ["del", "rec", "resample"], ["exit", "copy", "remain"]]
    LAB = {"pattern_select": "PATTERN\nSELECT", "pattern_edit": "PATTERN\nEDIT", "record_setting": "RECORD\nSETTING", "del": "DEL", "rec": "REC", "resample": "RESAMPLE", "exit": "EXIT", "copy": "COPY", "remain": "REMAIN"}
    ys = [262, 316, 370]
    for r, row in enumerate(L):
        for c, id_ in enumerate(row):
            E.append((id_, "btn", 141 + c * 88, ys[r], 78, 42, LAB[id_], ""))
    # right block
    for id_, x, lab in [("start_end", 413, "START/\nEND"), ("pitch_speed", 523, "PITCH/\nSPEED"), ("mark", 633, "MARK")]:
        E.append((id_, "btn", x, ys[0], 82, 42, lab, ""))
    E.append(("value", "knob", 853, ys[0] - 2, 40, 40, "VALUE", ""))
    for id_, x, lab in [("bpm_sync", 413, "BPM\nSYNC"), ("gate", 523, "GATE"), ("loop", 633, "LOOP"), ("reverse", 743, "REVERSE"), ("roll", 853, "ROLL")]:
        E.append((id_, "btn", x, ys[1], 82, 42, lab, ""))
    for i, (id_, lab) in enumerate([("bank_AF", "A/F"), ("bank_BG", "B/G"), ("bank_CH", "C/H"), ("bank_DI", "D/I"), ("bank_EJ", "E/J"), ("shift", "SHIFT")]):
        E.append((id_, "btn", 413 + i * 88, ys[2], 78, 42, lab, ""))
    # pads  (pad 1 top-left ... 16 bottom-right)
    SH = ["FIXED VELOCITY", "16 VELOCITY", "CUE", "CHROMATIC", "EXCHANGE", "INIT PARAM", "PAD LINK", "MUTE GROUPS", "METRONOME", "COUNT-IN", "TAP TEMPO", "GAIN", "UTILITY", "IMPORT/EXPORT", "PAD SETTING", "EFX SETTING"]
    for n in range(16):
        r, c = divmod(n, 4)
        E.append((f"p{n+1}", "pad", 175 + c * 162.5, 452 + r * 77, 150, 68, str(n + 1), SH[n]))
    for r, (id_, lab, sh) in enumerate([("bus_fx", "BUS FX", "MUTE BUS"), ("hold", "HOLD", "PAUSE"), ("ext_source", "EXT\nSOURCE", "INPUT SETTING"), ("sub_pad", "SUB PAD", "PROJECT")]):
        E.append((id_, "pad2", 825, 452 + r * 77, 150, 68, lab, sh))
    return E

ELEMS = build_elems()
CROPS = {
    "all": (44, 0, 912, 750),
    "buttons": (60, 232, 880, 160),
    "lower": (60, 244, 880, 506),
    "knobs": (60, 6, 880, 66),
    "pads": (60, 412, 880, 338),
    "top": (60, 0, 880, 235),
    "ctrl_fx": (80, 0, 840, 405),
}
BODY = (52, 4, 896, 738, 26)   # unit outline: x, y, w, h, corner radius
VIEW_H = 750
AUTO_X = (60, 880)
LABEL_RIGHT = ["vol", "c1", "c2", "c3"]   # knobs whose label sits to the right (others: left)
