"""Find devices under ../devices and prepare the shared tools for one guide.

Each device folder holds:
  device.py   DEVICE dict: id, name, guides (content file, names, output names, footer)
  layout.py   panel geometry: ELEMS, CROPS (+ optional BODY, VIEW_H, AUTO_X)
  <guide>.py  booklet content: page(), p1..pN, PADSH/USED if it has a pad table, then `pages = [...]`
"""
import pathlib, runpy
import panel

ROOT = pathlib.Path(__file__).resolve().parent.parent / "devices"


def all_ids():
    return sorted(p.name for p in ROOT.iterdir() if (p / "device.py").is_file())


def device(dev_id):
    return runpy.run_path(str(ROOT / dev_id / "device.py"))["DEVICE"]


def guide(dev_id, guide_id):
    for g in device(dev_id)["guides"]:
        if g["id"] == guide_id:
            return g
    raise KeyError(f"{dev_id} has no guide {guide_id!r}")


def use(dev_id, guide_id=None):
    """Point the panel renderer at this device's layout (and the guide's display caption)."""
    panel.use_layout(runpy.run_path(str(ROOT / dev_id / "layout.py")))
    if guide_id is not None:
        panel.DISP_SUB = guide(dev_id, guide_id)["disp_sub"]


def source(dev_id, guide_id):
    """Text of the guide's content file (the build scripts exec it in parts)."""
    return (ROOT / dev_id / guide(dev_id, guide_id)["content"]).read_text(encoding="utf-8")
