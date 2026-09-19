"""Recompute the per-family x-height normalisation scales.

Comparing 10 pt EB Garamond with 10 pt DejaVu is not a fair test: their
x-heights differ by about 30 %. Every specimen is therefore scaled so that
x-height, not em size, is held constant. Re-run this after editing roster.py.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER
from fontTools.ttLib import TTFont
from fontTools.pens.boundsPen import BoundsPen

TARGET = 0.462          # reference x-height as a fraction of the em

scales = {}
for r in ROSTER:
    f = TTFont(os.path.join(r["path"], r["up"]), lazy=True)
    upm = f["head"].unitsPerEm
    xh = getattr(f["OS/2"], "sxHeight", None)
    if not xh:                                  # some fonts omit it; measure 'x'
        gs = f.getGlyphSet()
        bp = BoundsPen(gs)
        gs["x"].draw(bp)
        xh = bp.bounds[3]
    scales[r["key"]] = round(TARGET / (xh / upm), 4)
    f.close()

out = os.path.join(os.path.dirname(__file__), "scales.json")
json.dump(scales, open(out, "w"), indent=1)
print(f"wrote {len(scales)} scales to {out}")
