import re, os, gzip, base64, json, sys

NUM = re.compile(r'-?\d+\.\d+')
def shrink(m):
    v = round(float(m.group()), 2)
    s = f'{v:.2f}'.rstrip('0').rstrip('.')
    return s if s not in ('', '-0') else '0'

def optimize(txt):
    txt = re.sub(r'<\?xml[^>]*\?>\s*', '', txt)
    txt = NUM.sub(shrink, txt)
    txt = re.sub(r'\s+', ' ', txt)
    txt = txt.replace('> <', '><')
    return txt.strip()

src = '/home/claude/gen/svg'
raw = opt = 0
bundle = {}
for fn in sorted(os.listdir(src)):
    if not fn.endswith('.svg'): continue
    t = open(os.path.join(src, fn)).read()
    raw += len(t)
    o = optimize(t)
    opt += len(o)
    bundle[fn[:-4]] = o
blob = json.dumps(bundle, separators=(',',':')).encode()
gz = gzip.compress(blob, 9)
b64 = base64.b64encode(gz).decode()
open('/home/claude/gen/bundle.b64','w').write(b64)
print(f'raw   {raw/1e6:6.2f} MB')
print(f'opt   {opt/1e6:6.2f} MB  ({opt/raw:.0%})')
print(f'gzip  {len(gz)/1e6:6.2f} MB')
print(f'b64   {len(b64)/1e6:6.2f} MB  <- embedded size')
