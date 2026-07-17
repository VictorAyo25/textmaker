import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))

def load(p): return io.open(os.path.join(HERE, p), encoding='utf-8').read()

svgs = {}
for name in ['em_wave','spectrum','capacitor','poynting','chain','fieldlines']:
    svgs[name] = load(f'svg_{name}.svg')

body = load('module5_body.html') + '\n' + load('module5_assess.html')

def inject(m):
    key = m.group(1)
    return svgs.get(key, f'<!--missing svg {key}-->')
body = re.sub(r'\{\{SVG:(\w+)\}\}', inject, body)

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<title>PHY121 Module 5</title>
<link rel="stylesheet" href="manual.css"></head><body>
{body}
</body></html>'''

io.open(os.path.join(HERE, 'module5.html'), 'w', encoding='utf-8').write(html)
print('assembled module5.html; injected', len(svgs), 'svgs;', len(html), 'bytes')
