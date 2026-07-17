# Inline SVG diagrams for Modules 1-4 (electromagnetism-themed).
import math, os, io
OUT=os.path.dirname(os.path.abspath(__file__))
INK='#2b3140'; NAVY='#1b2a4a'; BLUE='#1d4ed8'; RED='#c81e1e'; GREEN='#15803d'
AMBER='#b45309'; MUT='#6b7280'; POS='#c0202e'; NEG='#1d4ed8'
MSVG={}

def head(w,h,ff='DejaVu Serif, serif'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" font-family="{ff}">'
def arrow(defid,color):
    return (f'<marker id="{defid}" markerWidth="9" markerHeight="9" refX="7" refY="3" '
            f'orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{color}"/></marker>')

# 1. Field lines of a positive and negative point charge (side by side)
def field_points():
    w,h=520,240; s=[head(w,h)]
    s.append('<defs>'+arrow('fo',AMBER)+'</defs>')
    for cx,sign,col,lab in [(140,+1,POS,'+'),(380,-1,NEG,'−')]:
        cy=120
        for k in range(12):
            a=math.radians(k*30)
            x2=cx+math.cos(a)*95; y2=cy+math.sin(a)*95
            if sign>0:
                s.append(f'<line x1="{cx+math.cos(a)*16:.1f}" y1="{cy+math.sin(a)*16:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{AMBER}" stroke-width="1.3" marker-end="url(#fo)"/>')
            else:
                s.append(f'<line x1="{x2:.1f}" y1="{y2:.1f}" x2="{cx+math.cos(a)*20:.1f}" y2="{cy+math.sin(a)*20:.1f}" stroke="{AMBER}" stroke-width="1.3" marker-end="url(#fo)"/>')
        s.append(f'<circle cx="{cx}" cy="{cy}" r="15" fill="{col}"/>')
        s.append(f'<text x="{cx}" y="{cy+6}" font-size="20" fill="#fff" text-anchor="middle">{lab}</text>')
    s.append(f'<text x="140" y="232" font-size="12.5" fill="{MUT}" text-anchor="middle">field points OUT of +</text>')
    s.append(f'<text x="380" y="232" font-size="12.5" fill="{MUT}" text-anchor="middle">field points IN to −</text>')
    s.append('</svg>'); return '\n'.join(s)

# 2. Two-charge superposition: forces on a test charge
def superposition():
    w,h=420,260; s=[head(w,h)]
    s.append('<defs>'+arrow('fp',RED)+arrow('fn',BLUE)+arrow('fr',GREEN)+'</defs>')
    # charges A(+) left, B(+) top, test q at origin
    qx,qy=210,170
    s.append(f'<circle cx="70" cy="170" r="13" fill="{POS}"/><text x="70" y="176" font-size="16" fill="#fff" text-anchor="middle">+</text>')
    s.append(f'<circle cx="210" cy="50" r="13" fill="{POS}"/><text x="210" y="56" font-size="16" fill="#fff" text-anchor="middle">+</text>')
    s.append(f'<circle cx="{qx}" cy="{qy}" r="11" fill="{NAVY}"/><text x="{qx}" y="{qy+5}" font-size="13" fill="#fff" text-anchor="middle">q</text>')
    # force from A pushes right, from B pushes down; resultant
    s.append(f'<line x1="{qx}" y1="{qy}" x2="{qx+95}" y2="{qy}" stroke="{RED}" stroke-width="2.4" marker-end="url(#fp)"/>')
    s.append(f'<line x1="{qx}" y1="{qy}" x2="{qx}" y2="{qy+70}" stroke="{BLUE}" stroke-width="2.4" marker-end="url(#fn)"/>')
    s.append(f'<line x1="{qx}" y1="{qy}" x2="{qx+80}" y2="{qy+58}" stroke="{GREEN}" stroke-width="2.6" marker-end="url(#fr)"/>')
    s.append(f'<text x="{qx+100}" y="{qy-4}" font-size="14" fill="{RED}">F₁</text>')
    s.append(f'<text x="{qx-24}" y="{qy+60}" font-size="14" fill="{BLUE}">F₂</text>')
    s.append(f'<text x="{qx+70}" y="{qy+74}" font-size="14" fill="{GREEN}">Fₙₑₜ</text>')
    s.append(f'<text x="210" y="250" font-size="12.5" fill="{MUT}" text-anchor="middle">add the two forces as vectors</text>')
    s.append('</svg>'); return '\n'.join(s)

# 3. Parallel-plate capacitor
def capacitor_plates():
    w,h=380,240; s=[head(w,h)]
    s.append('<defs>'+arrow('ce',AMBER)+'</defs>')
    lx,rx,ty,by=150,230,50,190
    s.append(f'<rect x="{lx-6}" y="{ty}" width="6" height="{by-ty}" fill="{POS}"/>')
    s.append(f'<rect x="{rx}" y="{ty}" width="6" height="{by-ty}" fill="{NEG}"/>')
    for yy in range(ty+16,by-6,24):
        s.append(f'<text x="{lx-20}" y="{yy+5}" font-size="15" fill="{POS}">+</text>')
        s.append(f'<text x="{rx+10}" y="{yy+5}" font-size="15" fill="{NEG}">−</text>')
        s.append(f'<line x1="{lx+4}" y1="{yy}" x2="{rx-4}" y2="{yy}" stroke="{AMBER}" stroke-width="1.4" marker-end="url(#ce)"/>')
    s.append(f'<text x="{(lx+rx)/2}" y="{ty-8}" font-size="15" font-style="italic" fill="{AMBER}" text-anchor="middle">E</text>')
    # d dimension
    s.append(f'<line x1="{lx}" y1="{by+16}" x2="{rx}" y2="{by+16}" stroke="{INK}" stroke-width="1"/>')
    s.append(f'<text x="{(lx+rx)/2}" y="{by+30}" font-size="13" font-style="italic" fill="{INK}" text-anchor="middle">d</text>')
    s.append(f'<text x="{lx-30}" y="{ty-6}" font-size="12.5" fill="{MUT}">plate area A</text>')
    s.append('</svg>'); return '\n'.join(s)

# 4. Series circuit
def circuit_series():
    w,h=300,200; s=[head(w,h)]
    # rectangle loop
    x0,y0,x1,y1=40,40,260,160
    s.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="none" stroke="{INK}" stroke-width="2.2"/>')
    # battery on left
    s.append(f'<line x1="{x0}" y1="90" x2="{x0}" y2="102" stroke="#fff" stroke-width="4"/>')
    s.append(f'<line x1="{x0-7}" y1="88" x2="{x0+7}" y2="88" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<line x1="{x0-4}" y1="104" x2="{x0+4}" y2="104" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<text x="{x0-16}" y="100" font-size="12" fill="{INK}">V</text>')
    # two resistors on top
    def res(cx):
        return (f'<rect x="{cx-22}" y="{y0-7}" width="44" height="14" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
    s.append(res(110)); s.append(f'<text x="110" y="{y0-12}" font-size="12" fill="{INK}" text-anchor="middle">R₁</text>')
    s.append(res(190)); s.append(f'<text x="190" y="{y0-12}" font-size="12" fill="{INK}" text-anchor="middle">R₂</text>')
    s.append(f'<text x="150" y="{y1+28}" font-size="12.5" fill="{MUT}" text-anchor="middle">series: same current everywhere</text>')
    s.append('</svg>'); return '\n'.join(s)

# 5. Parallel circuit
def circuit_parallel():
    w,h=300,210; s=[head(w,h)]
    s.append(f'<line x1="40" y1="40" x2="260" y2="40" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<line x1="40" y1="170" x2="260" y2="170" stroke="{INK}" stroke-width="2.2"/>')
    s.append(f'<line x1="40" y1="40" x2="40" y2="170" stroke="{INK}" stroke-width="2.2"/>')
    # battery left
    s.append(f'<line x1="34" y1="98" x2="46" y2="98" stroke="{INK}" stroke-width="3"/><line x1="37" y1="112" x2="43" y2="112" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<text x="20" y="108" font-size="12" fill="{INK}">V</text>')
    # two vertical branches with resistors
    for bx,lab in [(150,'R₁'),(230,'R₂')]:
        s.append(f'<line x1="{bx}" y1="40" x2="{bx}" y2="80" stroke="{INK}" stroke-width="2"/>')
        s.append(f'<rect x="{bx-13}" y="80" width="26" height="46" fill="#fff" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<line x1="{bx}" y1="126" x2="{bx}" y2="170" stroke="{INK}" stroke-width="2"/>')
        s.append(f'<text x="{bx+18}" y="106" font-size="12" fill="{INK}">{lab}</text>')
    s.append(f'<text x="150" y="196" font-size="12.5" fill="{MUT}" text-anchor="middle">parallel: same voltage across each</text>')
    s.append('</svg>'); return '\n'.join(s)

# 6. Magnetic field into/out of page
def field_in_out():
    w,h=360,150; s=[head(w,h)]
    s.append(f'<text x="90" y="24" font-size="12.5" fill="{MUT}" text-anchor="middle">B out of page</text>')
    for i in range(3):
        for j in range(3):
            cx=40+i*38; cy=50+j*30
            s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
            s.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="{BLUE}"/>')
    s.append(f'<text x="270" y="24" font-size="12.5" fill="{MUT}" text-anchor="middle">B into page</text>')
    for i in range(3):
        for j in range(3):
            cx=220+i*38; cy=50+j*30
            s.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="none" stroke="{RED}" stroke-width="1.5"/>')
            s.append(f'<line x1="{cx-6}" y1="{cy-6}" x2="{cx+6}" y2="{cy+6}" stroke="{RED}" stroke-width="1.5"/>')
            s.append(f'<line x1="{cx-6}" y1="{cy+6}" x2="{cx+6}" y2="{cy-6}" stroke="{RED}" stroke-width="1.5"/>')
    s.append('</svg>'); return '\n'.join(s)

# 7. Helical path of a charge in B
def helical_path():
    w,h=460,200; s=[head(w,h)]
    s.append('<defs>'+arrow('hp',NAVY)+'</defs>')
    # B field lines horizontal
    for yy in (40,90,140):
        s.append(f'<line x1="30" y1="{yy}" x2="430" y2="{yy}" stroke="#c9d2e0" stroke-width="1"/>')
    # helix: x advances, y oscillates
    pts=[]
    for i in range(0,361,4):
        t=i/360
        x=40+t*370; y=90+38*math.sin(math.radians(i*3))
        pts.append((x,y))
    s.append('<path d="M '+' L '.join(f'{x:.1f},{y:.1f}' for x,y in pts)+f'" fill="none" stroke="{RED}" stroke-width="2.4"/>')
    s.append(f'<line x1="410" y1="90" x2="440" y2="90" stroke="{NAVY}" stroke-width="1.5" marker-end="url(#hp)"/>')
    s.append(f'<text x="418" y="80" font-size="13" font-style="italic" fill="{NAVY}">B</text>')
    s.append(f'<text x="230" y="192" font-size="12.5" fill="{MUT}" text-anchor="middle">velocity at an angle to B gives a helix</text>')
    s.append('</svg>'); return '\n'.join(s)

# 8. Current loop / magnetic dipole
def current_loop():
    w,h=280,220; s=[head(w,h)]
    s.append('<defs>'+arrow('cl',NAVY)+arrow('mm',GREEN)+'</defs>')
    s.append(f'<ellipse cx="140" cy="130" rx="80" ry="34" fill="none" stroke="{NAVY}" stroke-width="2.4"/>')
    # current arrow on loop
    s.append(f'<line x1="150" y1="96" x2="120" y2="96" stroke="{NAVY}" stroke-width="2.4" marker-end="url(#cl)"/>')
    s.append(f'<text x="150" y="90" font-size="13" font-style="italic" fill="{NAVY}">I</text>')
    # magnetic moment up
    s.append(f'<line x1="140" y1="130" x2="140" y2="50" stroke="{GREEN}" stroke-width="2.6" marker-end="url(#mm)"/>')
    s.append(f'<text x="148" y="58" font-size="14" font-style="italic" fill="{GREEN}">μ</text>')
    s.append(f'<text x="140" y="205" font-size="12.5" fill="{MUT}" text-anchor="middle">a current loop is a magnetic dipole</text>')
    s.append('</svg>'); return '\n'.join(s)

for name,fn in [('field_points',field_points),('superposition',superposition),
                ('capacitor_plates',capacitor_plates),('circuit_series',circuit_series),
                ('circuit_parallel',circuit_parallel),('field_in_out',field_in_out),
                ('helical_path',helical_path),('current_loop',current_loop)]:
    MSVG[name]=fn()
    io.open(os.path.join(OUT,f'msvg_{name}.svg'),'w',encoding='utf-8').write(MSVG[name])
print('module svgs:',len(MSVG))
