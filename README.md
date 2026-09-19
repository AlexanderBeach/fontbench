# Font bench

A blind A/B instrument for choosing a default typeface that has to carry
papers, slides, a web UI and mathematics.

Nineteen matched text + maths families are typeset through LuaLaTeX and
`unicode-math`, converted to vector outlines, and served as one self-contained
HTML page. No web fonts, no fallbacks: every specimen is the real font.

## Why it is built this way

- **Real typesetting, not CSS.** Maths fonts like Libertinus Math and
  Garamond-Math have no browser renderer. LaTeX is the only way to see them
  honestly, so specimens are compiled PDFs converted by `pdftocairo -svg`.
- **x-height normalised.** 10 pt EB Garamond against 10 pt DejaVu is not a fair
  comparison. `xheight.py` scales every family to a constant x-height.
- **Blind by default.** The tournament labels candidates A and B so that
  lineage prestige does not leak into the judgement.
- **Outlines, not fonts.** The page loads nothing at runtime, so it cannot
  silently fall back to a system serif.

## Layout

    setup.sh              apt + pip dependencies
    scripts/roster.py     the 19 families: file paths for text, sans and maths
    scripts/spec.py       the six specimen bodies, as LaTeX fragments
    scripts/check.py      verify every font path resolves
    scripts/xheight.py    recompute normalisation scales
    scripts/gen.py        compile one family's six specimens to SVG
    scripts/opt.py        round coordinates, gzip, base64
    scripts/build.py      run all of the above, emit dist/font-bench.html
    web/font-bench.html   page template, with __ROSTER__ and __BUNDLE__ slots

## Build

    ./setup.sh
    python3 scripts/build.py

## Adding a family

Add an entry to `ROSTER` in `scripts/roster.py` with paths to its upright,
italic, bold, bold-italic, sans and OpenType MATH files, then rebuild.
`check.py` will tell you which paths are wrong — they differ between TeX Live
builds, so locate files with `find / -name '<filename>'`.

## Changing what the specimens say

Edit `scripts/spec.py`. The fragments are ordinary LaTeX inside a `varwidth`
of 4.7 in. Keep the measure constant across specimens or the comparison stops
being like-for-like.

## Licensing

Specimen output is rendered from fonts under OFL, GUST, Bitstream and
GPL-with-font-exception terms. The terms differ, and they matter if a
derivative font is the goal — see the Licence column in the page's Browse tab,
and confirm upstream before redistributing anything derived.
