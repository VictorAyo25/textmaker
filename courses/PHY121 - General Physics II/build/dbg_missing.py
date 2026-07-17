import re
from recon_back import gen_back
from reconstruct import PDF, raw_spans, FOOTER_RE
import fitz

d = fitz.open(PDF)
for pn in [122, 124]:
    sp = [s for s in sorted(raw_spans(d[pn - 1], 40, 795), key=lambda s: (s['y'], s['x']))
          if not FOOTER_RE.match(s['t'])]
    orig = ' '.join(s['t'] for s in sp)
    got = re.sub(r'<[^>]+>', '', gen_back(pn, pn))
    ow = set(re.findall(r'[A-Za-z]{4,}', orig))
    gw = set(re.findall(r'[A-Za-z]{4,}', got))
    miss = sorted(ow - gw)
    print(f'--- p{pn}: orig {len(ow)} word types, missing {len(miss)}')
    if miss:
        print('    MISSING:', miss[:14])
        for s in sp:
            if any(w in s['t'] for w in miss[:4]):
                print(f"      y={s['y']:.0f} x={s['x']:.0f} sz={s['sz']} col=#{s['col']:06x} | {s['t'][:64]!r}")
