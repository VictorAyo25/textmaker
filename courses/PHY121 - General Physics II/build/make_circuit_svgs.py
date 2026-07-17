"""
make_circuit_svgs.py — circuit diagrams as SVG, drawn from geometry rather than
by hand.

Two reasons this exists.

1. The loop arrows in the original manual's Kirchhoff figures have their
   arrowheads rotated ~80 degrees off the arc. The head's tip sits exactly on the
   arc's endpoint, so it is attached correctly; only the angle is wrong, and it is
   the SAME angle on all three arrows even though it should follow each arc. It
   was a constant, not a computed tangent. Here the head is an SVG marker with
   orient="auto", so the renderer takes the tangent from the path itself and the
   bug cannot recur.

2. Resistors are drawn as zigzags. The original's eight circuit figures all use
   zigzags; two diagrams added later used boxes, so the book taught two symbols
   for one component. One helper now draws them all.

Run: python make_circuit_svgs.py     (writes msvg_*.svg next to this file)
"""
import io, os, math

HERE = os.path.dirname(os.path.abspath(__file__))

INK   = '#1e2430'   # wires, resistors, labels
ORANGE= '#b45309'   # loop 1 / traverse
RED   = '#b91c1c'   # loop 2
GREEN = '#0b6b5f'   # branch current


def zig(x1, y1, x2, y2, n=6, amp=5.0):
    """A resistor: n zigzag teeth along the segment, with a short lead each end."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L          # along
    px, py = -uy, ux                 # across
    lead = L * 0.16
    pts = [(x1, y1), (x1 + ux * lead, y1 + uy * lead)]
    span = L - 2 * lead
    for i in range(n):
        t = lead + span * (i + 0.5) / n
        s = amp if i % 2 == 0 else -amp
        pts.append((x1 + ux * t + px * s, y1 + uy * t + py * s))
    pts += [(x1 + ux * (L - lead), y1 + uy * (L - lead)), (x2, y2)]
    d = ' '.join(f'{x:.2f},{y:.2f}' for x, y in pts)
    return f'<polyline points="{d}" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>'


def arc(cx, cy, r, a0_deg, sweep_deg, colour, marker):
    """A loop arrow: an arc of `sweep_deg` clockwise from a0, arrowhead at the end.

    SVG y grows downward, so increasing angle runs clockwise on screen. The head
    is a marker with orient="auto": the renderer reads the tangent off the path,
    which is the whole point (see module docstring)."""
    a1 = a0_deg + sweep_deg
    x0, y0 = cx + r * math.cos(math.radians(a0_deg)), cy + r * math.sin(math.radians(a0_deg))
    x1, y1 = cx + r * math.cos(math.radians(a1)),     cy + r * math.sin(math.radians(a1))
    large = 1 if abs(sweep_deg) > 180 else 0
    sweep = 1 if sweep_deg > 0 else 0
    return (f'<path d="M {x0:.2f} {y0:.2f} A {r} {r} 0 {large} {sweep} {x1:.2f} {y1:.2f}" '
            f'fill="none" stroke="{colour}" stroke-width="1.7" marker-end="url(#{marker})"/>')


def arrow(x1, y1, x2, y2, colour, marker, w=1.7):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" '
            f'stroke-width="{w}" marker-end="url(#{marker})"/>')


def battery(x, y, tall=True):
    """Cell symbol: long plate = positive. Drawn on a vertical wire."""
    g = [f'<line x1="{x}" y1="{y-9}" x2="{x}" y2="{y+9}" stroke="#fff" stroke-width="5"/>']
    g.append(f'<line x1="{x-8}" y1="{y-3}" x2="{x+8}" y2="{y-3}" stroke="{INK}" stroke-width="2.6"/>')
    g.append(f'<line x1="{x-4.5}" y1="{y+3}" x2="{x+4.5}" y2="{y+3}" stroke="{INK}" stroke-width="1.8"/>')
    return '\n'.join(g)


def defs():
    """One marker per ink. refX sits at the tip so the tip lands on the path end."""
    out = ['<defs>']
    for name, col in [('ahO', ORANGE), ('ahR', RED), ('ahG', GREEN), ('ahK', INK)]:
        out.append(f'<marker id="{name}" viewBox="0 0 10 10" refX="9.2" refY="5" '
                   f'markerWidth="5.2" markerHeight="5.2" orient="auto">'
                   f'<path d="M 0 0.6 L 10 5 L 0 9.4 z" fill="{col}"/></marker>')
    out.append('</defs>')
    return '\n'.join(out)


def head(vb):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" '
            f'font-family="DejaVu Serif, serif">\n' + defs())


def txt(x, y, s, size=9, col=INK, anchor='middle', bold=True):
    w = ' font-weight="bold"' if bold else ''
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{col}" text-anchor="{anchor}"{w}>{s}</text>'


# ---------------------------------------------------------------- the figures
def kvl_single_loop():
    """12 V, 7 ohm, 3 ohm: one loop, traversed clockwise (up the cell, along the
    top with the current, down the 3 ohm). That is what the worked example's signs
    describe: I(7) + I(3) - 12 = 0, two drops and a rise."""
    L, R, T, B = 60, 250, 50, 150
    s = [head('0 20 300 150')]
    s.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    s.append(zig(125, T, 185, T))                      # 7 ohm on the top wire
    s.append(zig(R, 75, R, 125))                       # 3 ohm on the right wire
    s.append(battery(L, 100))
    s.append(txt(L - 26, 103, '12 V'))
    s.append(txt(155, T - 9, '7 &#937;'))
    s.append(txt(R + 18, 103, '3 &#937;'))
    s.append(f'<circle cx="{L}" cy="{T}" r="2.6" fill="{INK}"/>')
    s.append(f'<circle cx="{R}" cy="{T}" r="2.6" fill="{INK}"/>')
    s.append(f'<circle cx="{R}" cy="{B}" r="2.6" fill="{INK}"/>')
    s.append(txt(L - 8, T - 7, 'A'))
    s.append(txt(R + 8, T - 7, 'B'))
    s.append(txt(R + 8, B + 12, 'C'))
    # traverse: clockwise, gap on the left, head ends lower-left
    s.append(arc(155, 100, 20, 215, 290, ORANGE, 'ahO'))
    s.append(txt(155, 104, 'traverse', 7.5, ORANGE))
    s.append('</svg>')
    return '\n'.join(s)


def kirchhoff_two_loop():
    """50 V with 10, 8, 6 and 4 ohm in two meshes. Both loops are traversed
    CLOCKWISE, which is what the worked example's signs say: the cell is a rise
    (-50), the resistors are drops, and loop 2 goes UP the 8 ohm against I2."""
    L, R, T, B = 60, 280, 50, 150
    A = 170                                            # node A / B column
    s = [head('0 20 320 150')]
    s.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<line x1="{A}" y1="{T}" x2="{A}" y2="{B}" stroke="{INK}" stroke-width="1.8"/>')
    s.append(zig(95, T, 145, T))                       # 10 ohm
    s.append(zig(200, T, 250, T))                      # 6 ohm
    s.append(zig(A, 75, A, 125))                       # 8 ohm (middle branch)
    s.append(zig(R, 75, R, 125))                       # 4 ohm
    s.append(battery(L, 100))
    s.append(txt(L - 26, 103, '50 V'))
    s.append(txt(120, T - 9, '10 &#937;'))
    s.append(txt(225, T - 9, '6 &#937;'))
    s.append(txt(A - 20, 103, '8 &#937;'))
    s.append(txt(R + 18, 103, '4 &#937;'))
    s.append(f'<circle cx="{A}" cy="{T}" r="3" fill="{INK}"/>')
    s.append(f'<circle cx="{A}" cy="{B}" r="3" fill="{INK}"/>')
    s.append(txt(A, T - 9, 'A'))
    s.append(txt(A, B + 13, 'B'))
    # branch currents
    s.append(arrow(98, 64, 143, 64, ORANGE, 'ahO'))
    s.append(txt(120, 76, 'I&#8321;', 8.5, ORANGE))
    s.append(arrow(203, 64, 248, 64, RED, 'ahR'))
    s.append(txt(225, 76, 'I&#8323;', 8.5, RED))
    s.append(arrow(A + 14, 72, A + 14, 128, GREEN, 'ahG'))
    s.append(txt(A + 26, 103, 'I&#8322;', 8.5, GREEN))
    # the two mesh loops, both clockwise
    s.append(arc(115, 100, 19, 215, 290, ORANGE, 'ahO'))
    s.append(txt(115, 103, '1', 9, ORANGE))
    s.append(arc(228, 100, 19, 215, 290, RED, 'ahR'))
    s.append(txt(228, 103, '2', 9, RED))
    s.append('</svg>')
    return '\n'.join(s)


def circuit_series():
    """Resistors in series, zigzag symbols to match the rest of the book."""
    L, R, T, B = 55, 265, 45, 150
    s = [head('0 15 320 155')]
    s.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    s.append(zig(90, T, 145, T))
    s.append(zig(180, T, 235, T))
    s.append(battery(L, 97))
    s.append(txt(L - 15, 100, 'V'))
    s.append(txt(117, T - 9, 'R&#8321;'))
    s.append(txt(207, T - 9, 'R&#8322;'))
    s.append(arrow(120, 168, 200, 168, ORANGE, 'ahO'))
    s.append(txt(160, 163, 'same I everywhere', 8, ORANGE))
    s.append('</svg>')
    return '\n'.join(s)


def circuit_parallel():
    """Resistors in parallel, zigzag symbols to match the rest of the book."""
    L, R, T, B = 55, 265, 45, 150
    s = [head('0 15 320 155')]
    s.append(f'<rect x="{L}" y="{T}" width="{R-L}" height="{B-T}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<line x1="150" y1="{T}" x2="150" y2="{B}" stroke="{INK}" stroke-width="1.8"/>')
    s.append(f'<line x1="220" y1="{T}" x2="220" y2="{B}" stroke="{INK}" stroke-width="1.8"/>')
    s.append(zig(150, 72, 150, 122))
    s.append(zig(220, 72, 220, 122))
    s.append(battery(L, 97))
    s.append(txt(L - 15, 100, 'V'))
    s.append(txt(133, 100, 'R&#8321;'))
    s.append(txt(203, 100, 'R&#8322;'))
    for x in (150, 220):
        s.append(f'<circle cx="{x}" cy="{T}" r="3" fill="{INK}"/>')
        s.append(f'<circle cx="{x}" cy="{B}" r="3" fill="{INK}"/>')
    s.append(txt(160, 168, 'same V across each branch', 8, ORANGE))
    s.append('</svg>')
    return '\n'.join(s)


FIGS = {
    'kvl_single_loop':     kvl_single_loop,
    'kirchhoff_two_loop':  kirchhoff_two_loop,
    'circuit_series':      circuit_series,
    'circuit_parallel':    circuit_parallel,
}

if __name__ == '__main__':
    for name, fn in FIGS.items():
        p = os.path.join(HERE, f'msvg_{name}.svg')
        io.open(p, 'w', encoding='utf-8').write(fn())
        print(f'  wrote msvg_{name}.svg')
