"""Full rebuild: specimens -> compressed bundle -> self-contained HTML page."""
import base64, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
from roster import ROSTER

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

MATH = {}   # display names for the metadata table; fill in as you add families
LIC  = {}

def main():
    subprocess.run([sys.executable, f"{HERE}/check.py"], check=True)
    subprocess.run([sys.executable, f"{HERE}/xheight.py"], check=True)

    keys = [c["key"] for c in ROSTER]
    subprocess.run(["xargs", "-P", "8", "-I", "{}", sys.executable, f"{HERE}/gen.py", "{}"],
                   input="\n".join(keys), text=True, check=True)

    subprocess.run([sys.executable, f"{HERE}/opt.py"], check=True)

    tpl = open(f"{ROOT}/web/font-bench.html").read()
    roster = [dict(key=r["key"], label=r["label"], lineage=r["lineage"],
                   math=MATH.get(r["key"], os.path.basename(r["math"])),
                   lic=LIC.get(r["key"], "check upstream")) for r in ROSTER]
    page = (tpl.replace("__ROSTER__", json.dumps(roster, ensure_ascii=False,
                                                 separators=(",", ":")))
               .replace("__BUNDLE__", open(f"{HERE}/bundle.b64").read().strip()))
    out = f"{ROOT}/dist/font-bench.html"
    os.makedirs(f"{ROOT}/dist", exist_ok=True)
    open(out, "w").write(page)
    print(f"built {out}  ({len(page)/1e6:.2f} MB)")

if __name__ == "__main__":
    main()
