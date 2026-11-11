# Vector schematic of the Roland SP-404MKII top panel (not to scale).
# Layout verified against Roland's SP-404MK2 Reference Manual panel photos.
LIGHT = dict(bg="#fff", body="#EDEBE4", bodystroke="#222", disp="#1b1b1d", dispstroke="#000", dispfg="#fff", dispsub="#ddd",
  btn="#fff", stroke="#111", hlstroke="#111", hlring="#111", txt="#111", hltxt="#111", shbar="#E8590C", shtxt="#fff",
  badge="#111", badgest="#fff", badgetxt="#fff",
  role={"hold": ("#FFB703", "#7a4a00"), "press": ("#8ECAE6", "#12506b"), "turn": ("#95D5B2", "#1b5e3a")})
DRACULA = dict(bg="#282a36", body="#343746", bodystroke="#6272a4", disp="#1e1f29", dispstroke="#6272a4", dispfg="#f8f8f2", dispsub="#bd93f9",
  btn="#44475a", stroke="#6272a4", hlstroke="#f8f8f2", hlring="#282a36", txt="#f8f8f2", hltxt="#282a36", shbar="#ffb86c", shtxt="#282a36",
  badge="#ff79c6", badgest="#282a36", badgetxt="#282a36",
  role={"hold": ("#ffb86c", "#282a36"), "press": ("#8be9fd", "#282a36"), "turn": ("#50fa7b", "#282a36")})
T = LIGHT
ROLE = T["role"]
def set_theme(name):
    global T, ROLE
    T = DRACULA if name == "dracula" else LIGHT
    ROLE = T["role"]

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

def esc(s): return s.replace("&", "&amp;")

def text_lines(label, cx, cy, size, fill, weight=700):
    lines = label.split("\n")
    out = []
    off = (len(lines) - 1) * size * 0.55
    for i, ln in enumerate(lines):
        out.append(f'<text x="{cx}" y="{cy - off + i*size*1.1 + size*0.35:.1f}" text-anchor="middle" font-size="{size}" font-weight="{weight}" fill="{fill}">{esc(ln)}</text>')
    return "".join(out)

DISP_SUB = "DOOM OS grid"

def panel(hl=None, crop="all", labels=True, width_mm=None, fs=1.0, bigfs=1.0, disp_sub=None, shift_labels=True, show_all_labels=True, aria="SP-404MKII panel diagram"):
    """hl: dict id -> (role, order or None). roles: hold/press/turn"""
    hl = hl or {}
    if disp_sub is None: disp_sub = DISP_SUB
    if crop == "auto":
        mg = {"btn": 6, "pad": 4.5, "pad2": 4.5, "knob": 14, "disp": 10}
        ys = [(cy - eh/2 - mg[kind], cy + eh/2 + mg[kind]) for (id_, kind, cx, cy, ew, eh, lab, sub) in ELEMS if id_ in hl]
        y0 = max(0, min(a for a, b in ys)); y1 = min(750, max(b for a, b in ys))
        x, y, w, h = 60, y0, 880, max(y1 - y0, 60)
    else:
        x, y, w, h = CROPS[crop]
    dim = bool(hl)
    parts = []
    parts.append(f'<rect x="{x-20}" y="{y-20}" width="{w+40}" height="{h+40}" fill="{T['bg']}"/>')
    # body
    parts.append(f'<rect x="52" y="4" width="896" height="738" rx="26" fill="{T['body']}" stroke="{T['bodystroke']}" stroke-width="3"/>')
    # pad well hint
    for (id_, kind, cx, cy, ew, eh, lab, sub) in ELEMS:
        role = hl.get(id_)
        r = role[0] if role else None
        op = 1 if (r or not dim) else 0.42
        st = T["hlstroke"] if r else T["stroke"]
        tx = T["hltxt"] if r else T["txt"]
        g = [f'<g opacity="{op}">']
        if kind == "disp":
            g.append(f'<circle cx="{cx}" cy="{cy}" r="{ew}" fill="{T['disp']}" stroke="{T['dispstroke']}" stroke-width="3"/>')
            g.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="{22*fs}" font-weight="800" fill="{T['dispfg']}" letter-spacing="1">DISPLAY</text>')
            g.append(f'<text x="{cx}" y="{cy+20}" text-anchor="middle" font-size="{15*fs}" fill="{T['dispsub']}">{disp_sub}</text>')
        elif kind == "knob":
            fill, ink = (ROLE[r] if r else (T["btn"], "#111"))
            g.append(f'<circle cx="{cx}" cy="{cy}" r="{ew*0.62}" fill="{fill}" stroke="{st}" stroke-width="{4 if r else 2.5}"/>')
            g.append(f'<line x1="{cx}" y1="{cy}" x2="{cx}" y2="{cy-ew*0.55}" stroke="{T['hlring'] if r else T['txt']}" stroke-width="3.5" stroke-linecap="round"/>')
            ly = cy + ew * 0.62 + 18 * fs if id_ != "value" else cy + ew * 0.62 + 18 * fs
            if id_ in ("vol", "c1", "c2", "c3"):
                ly = cy - ew * 0.62 - 6
                # label to the right instead
                g.append(f'<text x="{cx+ew*0.62+8}" y="{cy+6*fs}" font-size="{17*fs}" font-weight="800" fill="{T['txt']}">{lab}</text>')
            else:
                g.append(f'<text x="{cx-ew*0.62-8}" y="{cy+6*fs}" text-anchor="end" font-size="{17*fs}" font-weight="800" fill="{T['txt']}">{lab}</text>')
        elif kind == "btn":
            fill, ink = (ROLE[r] if r else (T["btn"], "#111"))
            sw = 4 if r == "hold" else (3 if r else 2)
            g.append(f'<rect x="{cx-ew/2}" y="{cy-eh/2}" width="{ew}" height="{eh}" rx="7" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>')
            if r == "hold":
                g.append(f'<rect x="{cx-ew/2+5}" y="{cy-eh/2+5}" width="{ew-10}" height="{eh-10}" rx="4" fill="none" stroke="{T['hlring']}" stroke-width="1.6"/>')
            if show_all_labels or r:
                fsz = (15 if "\n" not in lab and len(lab) < 8 else 14) * fs
                if "SHIFT" == lab: fsz = 17 * fs
                if r and fs >= 1.0:
                    mx = max(len(t) for t in lab.split("\n"))
                    fsz = max(fsz, min(21, 72 / (mx * 0.64))) * (bigfs)
                g.append(text_lines(lab, cx, cy, fsz, tx))
        else:  # pad / pad2
            fill, ink = (ROLE[r] if r else (T["btn"], "#111"))
            sw = 4 if r == "hold" else (3 if r else 2)
            g.append(f'<rect x="{cx-ew/2}" y="{cy-eh/2}" width="{ew}" height="{eh}" rx="9" fill="{fill}" stroke="{st}" stroke-width="{sw}"/>')
            if r == "hold":
                g.append(f'<rect x="{cx-ew/2+6}" y="{cy-eh/2+6}" width="{ew-12}" height="{eh-12}" rx="5" fill="none" stroke="{T['hlring']}" stroke-width="1.6"/>')
            if kind == "pad":
                g.append(f'<text x="{cx}" y="{cy-2*fs}" text-anchor="middle" font-size="{(42 if r else 34)*fs}" font-weight="800" fill="{tx}">{lab}</text>')
            else:
                g.append(text_lines(lab, cx, cy - 8, 20 * fs if "\n" not in lab else 17 * fs, tx))
            if shift_labels and sub:
                g.append(f'<rect x="{cx-ew/2+8}" y="{cy+eh/2-23}" width="{ew-16}" height="17" rx="3" fill="{T['shbar']}"/>')
                g.append(f'<text x="{cx}" y="{cy+eh/2-10}" text-anchor="middle" font-size="{12.5*fs}" font-weight="800" fill="{T['shtxt']}" letter-spacing=".3">{sub}</text>')
        if role and role[1]:
            bx, by = cx - ew / 2 + 2, cy - eh / 2 + 2
            g.append(f'<circle cx="{bx}" cy="{by}" r="12" fill="{T['badge']}" stroke="{T['badgest']}" stroke-width="2"/>')
            g.append(f'<text x="{bx}" y="{by+5}" text-anchor="middle" font-size="15" font-weight="800" fill="{T['badgetxt']}">{role[1]}</text>')
        g.append("</g>")
        parts.append("".join(g))
    vb = f"{x} {y} {w} {h}"
    wh = f' width="{width_mm}mm"' if width_mm else ""
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}"{wh} role="img" aria-label="{aria}" font-family="Inter, Helvetica, Arial, sans-serif">' + "".join(parts) + "</svg>"
