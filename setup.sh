#!/usr/bin/env bash
# Everything the specimen generator needs. Ubuntu/Debian; ~2 GB, several minutes.
set -euo pipefail

sudo apt-get update
sudo apt-get install -y \
  texlive-xetex texlive-luatex texlive-fonts-extra texlive-latex-extra \
  texlive-plain-generic poppler-utils \
  fonts-texgyre fonts-texgyre-math fonts-ebgaramond fonts-cmu fonts-dejavu-core
sudo fc-cache -f

pip install fontTools uharfbuzz brotli

echo
echo "Check every roster path resolves before generating:"
echo "  python3 scripts/check.py"
