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

    setup.sh              apt dependencies: TeX Live, fonts, poppler, fontTools
    scripts/roster.py     the 19 families: file paths for text, sans and maths
    scripts/spec.py       the six specimen bodies, as LaTeX fragments
    scripts/check.py      verify every font path resolves
    scripts/xheight.py    recompute normalisation scales
    scripts/gen.py        compile one family's six specimens to SVG
    scripts/opt.py        round coordinates, gzip, base64
    scripts/build.py      run all of the above, emit dist/font-bench.html
    web/font-bench.html   page template, with __ROSTER__ and __BUNDLE__ slots
    web/font-final.html   round-robin final among chosen finalists, same slots, fed a
                          subset of the bundle
    web/glyph-round.html  one glyph at a time across every family, with __FONTS__ and
                          __GLYPHS__ slots, fed outlines cut from the character specimens
    web/taste-round.html  browser-rendered prose round over 32 families, self-contained

`build.py` assembles only `font-bench.html`. The final and glyph pages were assembled
by hand from the same bundle and their build steps are still to be written.

## Build

Three routes, in increasing order of what they ask of your machine. All three
run on Ubuntu 24.04: the font paths in `scripts/roster.py` are the ones that
release's TeX Live packages install to, and `check.py` names any that do not
resolve.

**Nothing installed, no session.** Push to GitHub. The workflow in
`.github/workflows/build.yml` installs TeX Live on an Ubuntu 24.04 runner,
rebuilds the page and attaches it to the run as an artifact named `font-bench`.
Download it from the Actions tab. Free without a minute cap on public
repositories. Good for occasional rebuilds, useless for an iterative design
loop.

**Nothing installed, full shell.** Open the repo in a GitHub Codespace. The
`.devcontainer` provisions TeX Live and the Python tools on first launch, and
you get a Linux machine in a browser tab. Free tier is 120 core-hours a month,
which is about 60 hours on the default 2-core box, plus 15 GB of storage.
Delete codespaces rather than stopping them: a stopped one still consumes the
storage quota.

**Local.**

    bash setup.sh
    python3 scripts/build.py

`build.py` checks every roster path, recomputes the x-height scales, compiles
all 114 specimens, packs them and writes `dist/font-bench.html`. It stops with
a message naming the missing specimens if any failed to compile. To change only
the metadata table without recompiling anything:

    python3 scripts/build.py --page-only

## Adding a family

Add an entry to `ROSTER` in `scripts/roster.py` with paths to its upright,
italic, bold, bold-italic, sans and OpenType MATH files, give it a display name
in `MATH` and a licence summary in `LIC` in `scripts/build.py`, then rebuild.
`check.py` will tell you which paths are wrong. They differ between TeX Live
builds, so locate files with `find / -name '<filename>'`.

## Changing what the specimens say

Edit `scripts/spec.py`. The fragments are ordinary LaTeX inside a `varwidth`
of 4.7 in. Keep the measure constant across specimens or the comparison stops
being like-for-like.

## Licensing

Specimen output is rendered from fonts under OFL, GUST, Bitstream and
GPL-with-font-exception terms. The terms differ, and they matter if a
derivative font is the goal. See the Licence column in the page's Browse tab,
and confirm upstream before redistributing anything derived.
