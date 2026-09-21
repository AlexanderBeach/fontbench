"""Compile one family's six specimens to SVG through LuaLaTeX and pdftocairo."""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from roster import ROSTER
from spec import SPECIMENS

SCALES_FILE = os.path.join(HERE, "scales.json")
BUILD_DIR = os.path.join(ROOT, "build")
SVG_DIR = os.path.join(ROOT, "svg")
LUALATEX_TIMEOUT = 180  # seconds allowed per specimen
ERROR_LINES = 4  # log lines quoted when a specimen fails

# Every specimen is set through fontspec and unicode-math with the family's own
# maths font, at the x-height scale that xheight.py computed for the family.
PREAMBLE = r"""\documentclass[border=10pt,varwidth]{standalone}
\usepackage{varwidth}
\usepackage{amsmath,amssymb}
\usepackage{fontspec}
\usepackage{unicode-math}
\setmainfont{%(up)s}[Path=%(path)s, ItalicFont=%(it)s, BoldFont=%(bf)s,
  BoldItalicFont=%(bfit)s, Scale=%(scale).4f, Ligatures=TeX]
\setsansfont{%(sans)s}[Path=%(sans_path)s, Scale=%(scale).4f, Ligatures=TeX]
\setmathfont{%(mathfile)s}[Path=%(mathdir)s, Scale=%(scale).4f]
\begin{document}
%(body)s
\end{document}
"""


class SpecimenError(Exception):
    """LuaLaTeX produced no PDF. The message quotes the log lines that say why."""


def compile_specimen(candidate, spec_key, body, scales):
    """Typesets one specimen and returns the path of its SVG.

    :param candidate: one entry of ROSTER
    :param spec_key: one key of SPECIMENS
    :param body: the LaTeX fragment for that specimen
    :param scales: the per-family x-height scales read from scales.json
    """
    fields = dict(candidate)
    fields["scale"] = scales[candidate["key"]]
    fields["mathdir"] = os.path.dirname(candidate["math"]) + "/"
    fields["mathfile"] = os.path.basename(candidate["math"])
    fields["body"] = body
    job = f"{candidate['key']}_{spec_key}"
    tex = os.path.join(BUILD_DIR, job + ".tex")
    with open(tex, "w", encoding="utf-8") as handle:
        handle.write(PREAMBLE % fields)
    result = subprocess.run(
        [
            "lualatex",
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-output-directory",
            BUILD_DIR,
            tex,
        ],
        capture_output=True,
        text=True,
        errors="replace",
        timeout=LUALATEX_TIMEOUT,
    )
    pdf = os.path.join(BUILD_DIR, job + ".pdf")
    if result.returncode != 0 or not os.path.exists(pdf):
        raise SpecimenError(_explain(job, result.stdout))
    svg = os.path.join(SVG_DIR, job + ".svg")
    subprocess.run(["pdftocairo", "-svg", pdf, svg], check=True, capture_output=True)
    return svg


def _explain(job, stdout):
    """Returns the log lines that say why LuaLaTeX failed, joined on one line."""
    log = os.path.join(BUILD_DIR, job + ".log")
    if os.path.exists(log):
        with open(log, encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    else:
        text = stdout
    lines = [
        line
        for line in text.splitlines()
        if line.startswith("!") or "Missing character" in line
    ]
    return " | ".join(lines[:ERROR_LINES]) or f"no error line in the log, see {log}"


def main(keys):
    """Compiles every specimen of the named families and exits 1 if any failed."""
    known = [candidate["key"] for candidate in ROSTER]
    unknown = [key for key in keys if key not in known]
    if unknown:
        choices = ", ".join(f"'{key}'" for key in known)
        arrived = ", ".join(f"'{key}'" for key in unknown)
        sys.exit(f"The family key can be {choices}, but got {arrived}.")
    with open(SCALES_FILE, encoding="utf-8") as handle:
        scales = json.load(handle)
    os.makedirs(BUILD_DIR, exist_ok=True)
    os.makedirs(SVG_DIR, exist_ok=True)
    failed = 0
    for candidate in ROSTER:
        if candidate["key"] not in keys:
            continue
        for spec_key, body in SPECIMENS.items():
            try:
                svg = compile_specimen(candidate, spec_key, body, scales)
            except SpecimenError as error:
                failed += 1
                print(f"FAIL {candidate['key']:14s} {spec_key:9s} {error}")
                continue
            size = os.path.getsize(svg) // 1024
            print(f"  ok {candidate['key']:14s} {spec_key:9s} {size:4d} KB")
    if failed:
        sys.exit(
            f"{failed} specimens did not compile. "
            "Each FAIL line above quotes the LaTeX error."
        )


if __name__ == "__main__":
    main(sys.argv[1:] or [candidate["key"] for candidate in ROSTER])
