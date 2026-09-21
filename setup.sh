#!/usr/bin/env bash
# Everything the specimen generator needs, all from apt. Ubuntu 24.04, about 2 GB,
# several minutes. The font paths in scripts/roster.py are the ones this release's
# TeX Live packages install to.
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  texlive-xetex texlive-luatex texlive-fonts-extra texlive-latex-extra \
  texlive-plain-generic poppler-utils python3-fonttools \
  fonts-texgyre fonts-texgyre-math fonts-ebgaramond fonts-cmu fonts-dejavu-core
sudo fc-cache -f

echo
echo "Check every roster path resolves before generating:"
echo "  python3 scripts/check.py"
