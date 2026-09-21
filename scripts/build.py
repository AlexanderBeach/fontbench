"""Full rebuild: specimens, then the compressed bundle, then the self-contained page.

python3 scripts/build.py              everything, four minutes once TeX Live is present
python3 scripts/build.py --page-only  reassemble the page from the existing bundle
"""

import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from gen import BUILD_DIR, SVG_DIR
from opt import BUNDLE_FILE
from roster import ROSTER
from spec import SPECIMENS

TEMPLATE = os.path.join(ROOT, "web", "font-bench.html")
PAGE = os.path.join(ROOT, "dist", "font-bench.html")
ROSTER_SLOT = "__ROSTER__"
BUNDLE_SLOT = "__BUNDLE__"
JOBS = 8  # lualatex processes run at once

# Display names of the maths fonts, as the page's metadata table shows them. Every
# family in roster.py needs an entry here and in LIC.
MATH = {
    "newcm": "NewCMMath-Regular",
    "lmodern": "latinmodern-math",
    "stixtwo": "STIXTwoMath",
    "pagella": "texgyrepagella-math",
    "termes": "texgyretermes-math",
    "schola": "texgyreschola-math",
    "bonum": "texgyrebonum-math",
    "libertinus": "LibertinusMath",
    "ebgaramond": "Garamond-Math",
    "xcharter": "XCharter-Math",
    "erewhon": "Erewhon-Math",
    "kproman": "KpMath-Regular",
    "oldstandard": "OldStandard-Math",
    "berenis": "BerenisADFProMath",
    "concrete": "Euler-Math",
    "dejavu": "DejaVu Math TeX Gyre",
    "fira": "FiraMath",
    "kpsans": "KpMath-Sans",
    "neohellenic": "GFSNeohellenicMath",
}

# Licence summaries for the same table. Confirm upstream before redistributing
# anything derived from a family.
LIC = {
    "newcm": "GUST, some faces GPL 3 with font exception",
    "lmodern": "GUST",
    "stixtwo": "OFL 1.1",
    "pagella": "GUST",
    "termes": "GUST",
    "schola": "GUST",
    "bonum": "GUST",
    "libertinus": "OFL 1.1",
    "ebgaramond": "OFL 1.1",
    "xcharter": "Bitstream Charter (text), OFL 1.1 (maths)",
    "erewhon": "Utopia lineage, permissive (verify upstream)",
    "kproman": "OFL 1.1 and LPPL 1.3",
    "oldstandard": "OFL 1.1",
    "berenis": "GPL with font exception (verify upstream)",
    "concrete": "OFL 1.1",
    "dejavu": "DejaVu / Bitstream Vera, permissive",
    "fira": "OFL 1.1",
    "kpsans": "OFL 1.1 and LPPL 1.3",
    "neohellenic": "OFL 1.1",
}


def run(script):
    """Runs one build stage as its own process and stops the build if it fails."""
    try:
        subprocess.run([sys.executable, os.path.join(HERE, script)], check=True)
    except subprocess.CalledProcessError:
        sys.exit(f"The {script} stage failed. Its message is above.")


def generate():
    """Compiles every specimen from scratch and packs them into the bundle."""
    run("check.py")
    run("xheight.py")
    for directory in (BUILD_DIR, SVG_DIR):
        shutil.rmtree(directory, ignore_errors=True)
    keys = [candidate["key"] for candidate in ROSTER]
    gen = os.path.join(HERE, "gen.py")
    subprocess.run(
        ["xargs", "-P", str(JOBS), "-I", "{}", sys.executable, gen, "{}"],
        input="\n".join(keys),
        text=True,
    )
    expected = {f"{key}_{spec_key}" for key in keys for spec_key in SPECIMENS}
    present = set()
    if os.path.isdir(SVG_DIR):
        present = {name[:-4] for name in os.listdir(SVG_DIR) if name.endswith(".svg")}
    missing = sorted(expected - present)
    if missing:
        sys.exit(
            f"The specimen set must hold all {len(expected)} files "
            f"({len(keys)} families by {len(SPECIMENS)} specimens), but got "
            f"{len(present)}. Missing: {', '.join(missing)}. "
            "The FAIL lines above quote each LaTeX error."
        )
    run("opt.py")


def assemble():
    """Writes the page: the template with the roster JSON and the bundle filled in."""
    unlisted = [
        candidate["key"]
        for candidate in ROSTER
        if candidate["key"] not in MATH or candidate["key"] not in LIC
    ]
    if unlisted:
        sys.exit(
            "The MATH and LIC tables in build.py must have an entry for every family "
            f"in roster.py, but got none for {', '.join(unlisted)}."
        )
    if not os.path.exists(BUNDLE_FILE):
        sys.exit(
            "The bundle must exist before the page can be assembled, but got nothing "
            f"at {BUNDLE_FILE}. Run build.py without --page-only to generate it."
        )
    with open(TEMPLATE, encoding="utf-8") as handle:
        template = handle.read()
    counts = {slot: template.count(slot) for slot in (ROSTER_SLOT, BUNDLE_SLOT)}
    if any(count != 1 for count in counts.values()):
        sys.exit(f"The template must contain each slot exactly once, but got {counts}.")
    with open(BUNDLE_FILE) as handle:
        bundle = handle.read().strip()
    roster = [
        dict(
            key=candidate["key"],
            label=candidate["label"],
            lineage=candidate["lineage"],
            math=MATH[candidate["key"]],
            lic=LIC[candidate["key"]],
        )
        for candidate in ROSTER
    ]
    page = template.replace(
        ROSTER_SLOT, json.dumps(roster, ensure_ascii=False, separators=(",", ":"))
    )
    page = page.replace(BUNDLE_SLOT, bundle)
    os.makedirs(os.path.dirname(PAGE), exist_ok=True)
    with open(PAGE, "w", encoding="utf-8") as handle:
        handle.write(page)
    size = os.path.getsize(PAGE) / 1e6
    print(f"built {PAGE}  ({size:.2f} MB, {len(roster)} families)")


def main(arguments):
    """Runs the full build, or only the page assembly with --page-only."""
    if arguments not in ([], ["--page-only"]):
        sys.exit(f"The only option is --page-only, but got {' '.join(arguments)}.")
    if not arguments:
        generate()
    assemble()


if __name__ == "__main__":
    main(sys.argv[1:])
