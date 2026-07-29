"""
make_tutorial_svgs.py — the four capacitor-network figures for Tutorial 1.

Drawn in code so the topology is exact and the capacitor glyphs are consistent.
Each network is the one printed on the lecturer's tutorial slide (slides 3-4).
Renders to tut_net1.svg .. tut_net4.svg; eyeball them before embedding.
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
INK = '#2b3140'; LAB = '#1e2430'

def head(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'font-family="DejaVu Serif, serif">')

def wire(x1, y1, x2, y2, w=1.8):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{INK}" stroke-width="{w}"/>'

def cap_h(x, y, lead=14, plate=11, gap=5):
    """Horizontal-run capacitor centred at (x,y): two vertical plates with leads."""
    s = []
    s.append(wire(x - lead - gap/2, y, x - gap/2, y))
    s.append(f'<line x1="{x-gap/2}" y1="{y-plate}" x2="{x-gap/2}" y2="{y+plate}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<line x1="{x+gap/2}" y1="{y-plate}" x2="{x+gap/2}" y2="{y+plate}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(wire(x + gap/2, y, x + lead + gap/2, y))
    return ''.join(s)

def cap_v(x, y, lead=14, plate=11, gap=5):
    """Vertical-run capacitor centred at (x,y): two horizontal plates with leads."""
    s = []
    s.append(wire(x, y - lead - gap/2, x, y - gap/2))
    s.append(f'<line x1="{x-plate}" y1="{y-gap/2}" x2="{x+plate}" y2="{y-gap/2}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<line x1="{x-plate}" y1="{y+gap/2}" x2="{x+plate}" y2="{y+gap/2}" stroke="{INK}" stroke-width="2.2"/>')
    s.append(wire(x, y + gap/2, x, y + lead + gap/2))
    return ''.join(s)

def dot(x, y):
    return f'<circle cx="{x}" cy="{y}" r="2.4" fill="{INK}"/>'

def lab(x, y, t, size=11, anchor='middle', col=LAB):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}">{t}</text>'

def term(x, y, t):
    return f'<circle cx="{x}" cy="{y}" r="2.6" fill="none" stroke="{INK}" stroke-width="1.6"/>' + lab(x, y - 8, t, 11)


def net1():
    # C1 (top) parallel with (C2 series C3) (bottom), between A and B
    w, h = 260, 132
    s = [head(w, h)]
    xa, xb = 26, 234; ytop, ybot = 40, 96
    s.append(term(xa, 68, 'A')); s.append(term(xb, 68, 'B'))
    # verticals from terminals to the two rails
    s.append(wire(xa, 68, xa, ytop)); s.append(wire(xa, 68, xa, ybot))
    s.append(wire(xb, 68, xb, ytop)); s.append(wire(xb, 68, xb, ybot))
    # top branch: C1
    s.append(wire(xa, ytop, 110, ytop)); s.append(cap_h(130, ytop)); s.append(wire(150, ytop, xb, ytop))
    s.append(lab(130, ytop - 16, 'C₁ = 3 µF'))
    # bottom branch: C2 then C3 in series
    s.append(wire(xa, ybot, 78, ybot)); s.append(cap_h(98, ybot)); s.append(wire(116, ybot, 144, ybot))
    s.append(cap_h(164, ybot)); s.append(wire(182, ybot, xb, ybot))
    s.append(lab(98, ybot + 24, 'C₂ = 6 µF')); s.append(lab(164, ybot + 24, 'C₃ = 2 µF'))
    s.append('</svg>')
    return ''.join(s)


def net2():
    # (C1 series C2) left branch parallel with C3 right branch, between two rails
    w, h = 260, 140
    s = [head(w, h)]
    xL, xR = 108, 198; ytop, ybot = 26, 114
    s.append(wire(xL, ytop, xR, ytop)); s.append(wire(xL, ybot, xR, ybot))  # rails
    s.append(dot(xL, ytop)); s.append(dot(xR, ytop)); s.append(dot(xL, ybot)); s.append(dot(xR, ybot))
    # left vertical: C1 upper, C2 lower
    s.append(cap_v(xL, 50)); s.append(wire(xL, 64, xL, 76)); s.append(cap_v(xL, 90))
    s.append(lab(xL - 16, 54, 'C₁ = 1 µF', anchor='end'))
    s.append(lab(xL - 16, 94, 'C₂ = 5 µF', anchor='end'))
    # right vertical: C3
    s.append(cap_v(xR, 70))
    s.append(lab(xR + 14, 74, 'C₃ = 8 µF', anchor='start'))
    s.append('</svg>')
    return ''.join(s)


def net3():
    # [C1 parallel (C2 series C3)] then series C5, between A and B
    w, h = 300, 132
    s = [head(w, h)]
    xa, xmid, xb = 24, 180, 276; ytop, ybot = 40, 96
    s.append(term(xa, 68, 'A')); s.append(term(xb, 68, 'B'))
    s.append(wire(xa, 68, xa, ytop)); s.append(wire(xa, 68, xa, ybot))
    s.append(wire(xmid, 68, xmid, ytop)); s.append(wire(xmid, 68, xmid, ybot)); s.append(dot(xmid, 68))
    # top: C1
    s.append(wire(xa, ytop, 82, ytop)); s.append(cap_h(102, ytop)); s.append(wire(120, ytop, xmid, ytop))
    s.append(lab(102, ytop - 16, 'C₁ = 6 µF'))
    # bottom: C2 series C3
    s.append(wire(xa, ybot, 60, ybot)); s.append(cap_h(80, ybot)); s.append(wire(98, ybot, 122, ybot))
    s.append(cap_h(142, ybot)); s.append(wire(160, ybot, xmid, ybot))
    s.append(lab(80, ybot + 24, 'C₂ = 3 µF')); s.append(lab(142, ybot + 24, 'C₃ = 6 µF'))
    # mid to B: C5
    s.append(wire(xmid, 68, 216, 68)); s.append(cap_h(236, 68)); s.append(wire(254, 68, xb, 68))
    s.append(lab(236, 52, 'C₅ = 12 µF'))
    s.append('</svg>')
    return ''.join(s)


def net4():
    # [C1 parallel C2] then series C3, between A and B
    w, h = 300, 132
    s = [head(w, h)]
    xa, xmid, xb = 24, 176, 276; ytop, ybot = 40, 96
    s.append(term(xa, 68, 'A')); s.append(term(xb, 68, 'B'))
    s.append(wire(xa, 68, xa, ytop)); s.append(wire(xa, 68, xa, ybot))
    s.append(wire(xmid, 68, xmid, ytop)); s.append(wire(xmid, 68, xmid, ybot)); s.append(dot(xmid, 68))
    s.append(wire(xa, ytop, 82, ytop)); s.append(cap_h(102, ytop)); s.append(wire(120, ytop, xmid, ytop))
    s.append(lab(102, ytop - 16, 'C₁ = 4 µF'))
    s.append(wire(xa, ybot, 82, ybot)); s.append(cap_h(102, ybot)); s.append(wire(120, ybot, xmid, ybot))
    s.append(lab(102, ybot + 24, 'C₂ = 8 µF'))
    s.append(wire(xmid, 68, 214, 68)); s.append(cap_h(234, 68)); s.append(wire(252, 68, xb, 68))
    s.append(lab(234, 52, 'C₃ = 5 µF'))
    s.append('</svg>')
    return ''.join(s)


if __name__ == '__main__':
    for name, fn in [('tut_net1', net1), ('tut_net2', net2), ('tut_net3', net3), ('tut_net4', net4)]:
        io.open(os.path.join(HERE, f'{name}.svg'), 'w', encoding='utf-8').write(fn())
        print('wrote', name)
