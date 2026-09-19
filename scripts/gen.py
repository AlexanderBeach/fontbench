import sys, os, json, subprocess, shutil
sys.path.insert(0,'/home/claude/gen')
from roster import ROSTER
from spec import SPECIMENS

SCALES = json.load(open('/home/claude/gen/scales.json'))
BUILD = '/home/claude/gen/build'
OUT   = '/home/claude/gen/svg'
os.makedirs(OUT, exist_ok=True)

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

def build(cand, spec_key, body):
    d = dict(cand)
    d['scale']    = SCALES[cand['key']]
    d['mathdir']  = os.path.dirname(cand['math']) + '/'
    d['mathfile'] = os.path.basename(cand['math'])
    d['body']     = body
    job = f"{cand['key']}_{spec_key}"
    tex = os.path.join(BUILD, job + '.tex')
    open(tex, 'w').write(PREAMBLE % d)
    r = subprocess.run(['lualatex','-interaction=nonstopmode','-halt-on-error',
                        '-output-directory', BUILD, tex],
                       capture_output=True, text=True, timeout=180)
    pdf = os.path.join(BUILD, job + '.pdf')
    if r.returncode != 0 or not os.path.exists(pdf):
        log = open(os.path.join(BUILD, job + '.log')).read() if os.path.exists(os.path.join(BUILD,job+'.log')) else r.stdout
        err = [l for l in log.splitlines() if l.startswith('!') or 'Missing character' in l][:4]
        return None, err
    svg = os.path.join(OUT, job + '.svg')
    subprocess.run(['pdftocairo','-svg', pdf, svg], check=True, capture_output=True)
    return svg, None

if __name__ == '__main__':
    keys = sys.argv[1:] or [c['key'] for c in ROSTER]
    for cand in ROSTER:
        if cand['key'] not in keys: continue
        for sk, body in SPECIMENS.items():
            svg, err = build(cand, sk, body)
            if svg: print(f"  ok {cand['key']:14s} {sk:9s} {os.path.getsize(svg)//1024:4d} KB")
            else:   print(f"FAIL {cand['key']:14s} {sk:9s} {err}")
