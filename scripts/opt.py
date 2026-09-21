"""Shrink the compiled specimens and pack them into the bundle the page embeds."""

import base64
import gzip
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SVG_DIR = os.path.join(ROOT, "svg")
BUNDLE_FILE = os.path.join(HERE, "bundle.b64")
DECIMALS = 2  # coordinate precision kept, in SVG user units
GZIP_LEVEL = 9

NUMBER = re.compile(r"-?\d+\.\d+")


def _shrink(match):
    """Rounds one coordinate to DECIMALS places and drops the trailing zeros."""
    text = f"{round(float(match.group()), DECIMALS):.{DECIMALS}f}"
    text = text.rstrip("0").rstrip(".")
    return text if text not in ("", "-0") else "0"


def optimize(svg, scope):
    """Returns the SVG with its XML prolog dropped, its coordinates rounded, its
    whitespace collapsed and every id prefixed with the scope.

    The page inlines several specimens in one document, and every specimen
    names its glyphs glyph-0-0, glyph-0-1 and so on. Left unprefixed, a <use>
    in the second specimen resolves to the first specimen's glyph definitions
    and its text is drawn in the wrong font.
    """
    svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
    svg = NUMBER.sub(_shrink, svg)
    svg = re.sub(r"\s+", " ", svg)
    svg = svg.replace("> <", "><")
    svg = re.sub(r'\bid="', f'id="{scope}-', svg)
    svg = re.sub(r'href="#', f'href="#{scope}-', svg)
    svg = re.sub(r"url\(#", f"url(#{scope}-", svg)
    return svg.strip()


def main():
    """Packs every compiled specimen into scripts/bundle.b64 and reports the sizes."""
    names = []
    if os.path.isdir(SVG_DIR):
        names = sorted(name for name in os.listdir(SVG_DIR) if name.endswith(".svg"))
    if not names:
        sys.exit(
            f"The svg directory must hold the compiled specimens, but got none in "
            f"{SVG_DIR}. Run python3 scripts/gen.py first."
        )
    raw = optimized = 0
    bundle = {}
    for name in names:
        with open(os.path.join(SVG_DIR, name), encoding="utf-8") as handle:
            text = handle.read()
        bundle[name[:-4]] = optimize(text, name[:-4])
        raw += len(text)
        optimized += len(bundle[name[:-4]])
    packed = gzip.compress(
        json.dumps(bundle, separators=(",", ":")).encode(), GZIP_LEVEL
    )
    encoded = base64.b64encode(packed).decode()
    with open(BUNDLE_FILE, "w") as handle:
        handle.write(encoded)
    print(f"{len(bundle)} specimens packed into {BUNDLE_FILE}")
    print(f"raw   {raw / 1e6:6.2f} MB")
    print(f"opt   {optimized / 1e6:6.2f} MB  ({optimized / raw:.0%})")
    print(f"gzip  {len(packed) / 1e6:6.2f} MB")
    print(f"b64   {len(encoded) / 1e6:6.2f} MB  <- embedded size")


if __name__ == "__main__":
    main()
