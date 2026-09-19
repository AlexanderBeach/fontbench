"""Verify every font file named in roster.py exists. Run this first."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER

missing = []
for r in ROSTER:
    for k in ("up", "it", "bf", "bfit"):
        p = os.path.join(r["path"], r[k])
        if not os.path.exists(p):
            missing.append(f"{r['key']}.{k}: {p}")
    if not os.path.exists(r["math"]):
        missing.append(f"{r['key']}.math: {r['math']}")
    p = os.path.join(r["sans_path"], r["sans"])
    if not os.path.exists(p):
        missing.append(f"{r['key']}.sans: {p}")

if missing:
    print(f"{len(missing)} font files not found. Font paths differ between TeX Live")
    print("builds; locate each with:  find / -name '<filename>' 2>/dev/null\n")
    print("\n".join(missing))
    sys.exit(1)
print(f"all {len(ROSTER)} families resolve")
