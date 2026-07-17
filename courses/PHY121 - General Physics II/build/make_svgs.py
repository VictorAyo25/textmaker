# Generate Module 5 SVG diagrams programmatically (accurate curves/geometry).
import math, os, io

OUT = os.path.dirname(os.path.abspath(__file__))
SVG = {}

INK='#2b3140'; NAVY='#1b2a4a'; MAG='#c2185b'; AMBER='#b45309'
BLUE='#1d4ed8'; RED='#c81e1e'; GREEN='#15803d'; MUT='#6b7280'; PUR='#5b3a8e'

def sine_path(x0,y0,length,amp,cycles,n=240,phase=0.0):
    pts=[]
    for i in range(n+1):
        t=i/n
        x=x0+length*t
        y=y0-amp*math.sin(2*math.pi*cycles*t+phase)
        pts.append((x,y))
    d='M '+' L '.join(f'{x:.2f},{y:.2f}' for x,y in pts)
    return d

# ---------- 1. EM plane wave (E in y, B in z, propagation +x) ----------
def em_wave():
    W,H=710,360
    ox,oy=120,H/2         # origin
    L=520; amp=86; cyc=2.0
    # z-axis (depth) skew per unit B-amplitude (drawn receding down-left/back)
    zx,zy=-0.60,0.42      # depth direction (dx,dy) per unit z
    zamp=74
    s=[]
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="DejaVu Serif, serif">')
    s.append(f'<defs><marker id="ah" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{INK}"/></marker></defs>')
    # axes: x (right), y (up), z (depth, up-left)
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+L+22}" y2="{oy}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ah)"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-amp-42}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ah)"/>')
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+zx*zamp*1.5:.1f}" y2="{oy+zy*zamp*1.5:.1f}" stroke="{INK}" stroke-width="1.6" marker-end="url(#ah)"/>')
    # B wave (depth plane) - red, drawn FIRST so E overlays; in phase with E
    def bpt(t):
        val=math.sin(2*math.pi*cyc*t)
        bx=ox+L*t + zx*zamp*val
        by=oy      + zy*zamp*val
        return bx,by
    # B stems (from axis to curve) at sampled points
    for i in range(1,int(cyc*10)):
        t=i/(cyc*10)
        bx,by=bpt(t)
        if abs(by-oy)>4 or abs(bx-(ox+L*t))>4:
            s.append(f'<line x1="{ox+L*t:.1f}" y1="{oy}" x2="{bx:.1f}" y2="{by:.1f}" stroke="{RED}" stroke-width="0.9" opacity="0.45"/>')
    bpath='M '+' L '.join('%.2f,%.2f'%bpt(i/240) for i in range(241))
    s.append(f'<path d="{bpath}" fill="none" stroke="{RED}" stroke-width="2.2"/>')
    # E wave (vertical plane) - blue; stems then curve
    for i in range(1,int(cyc*10)):
        t=i/(cyc*10)
        y=oy-amp*math.sin(2*math.pi*cyc*t)
        if abs(y-oy)>4:
            s.append(f'<line x1="{ox+L*t:.1f}" y1="{oy}" x2="{ox+L*t:.1f}" y2="{y:.1f}" stroke="{BLUE}" stroke-width="0.9" opacity="0.5"/>')
    s.append(f'<path d="{sine_path(ox,oy,L,amp,cyc)}" fill="none" stroke="{BLUE}" stroke-width="2.6"/>')
    # labels
    s.append(f'<text x="{ox+L+10}" y="{oy+20}" font-size="19" font-style="italic" fill="{INK}">x</text>')
    s.append(f'<text x="{ox+10}" y="{oy-amp-28}" font-size="19" font-style="italic" fill="{BLUE}">E</text>')
    s.append(f'<text x="{ox+zx*zamp*1.5-16:.1f}" y="{oy+zy*zamp*1.5-4:.1f}" font-size="19" font-style="italic" fill="{RED}">B</text>')
    s.append(f'<text x="{ox+L-130}" y="{oy+64}" font-size="12.5" fill="{MUT}">propagation direction</text>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------- 2. EM spectrum ----------
def spectrum():
    W,H=690,220
    x0,y0=40,70; bw=610; bh=46
    bands=[('Radio','#7c9cc4'),('Micro','#5fa8a0'),('Infrared','#c0563e'),
           ('Visible',None),('UV','#7b4fb0'),('X-ray','#3a6ea5'),('Gamma','#7a3b8f')]
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif">']
    bwid=bw/len(bands)
    rainbow=['#e23b3b','#e8792f','#e8d21f','#3fb54b','#2f6fe0','#7b3fd0']
    for i,(name,col) in enumerate(bands):
        x=x0+i*bwid
        if col is None:
            # visible band: draw rainbow sub-rects (robust across renderers)
            sub=bwid/len(rainbow)
            for j,rc in enumerate(rainbow):
                s.append(f'<rect x="{x+j*sub:.2f}" y="{y0}" width="{sub:.2f}" height="{bh}" fill="{rc}"/>')
            s.append(f'<rect x="{x:.1f}" y="{y0}" width="{bwid:.1f}" height="{bh}" fill="none" stroke="#fff" stroke-width="1"/>')
            s.append(f'<text x="{x+bwid/2:.1f}" y="{y0+bh/2+4}" font-size="11" fill="#1e2430" text-anchor="middle" font-weight="bold">{name}</text>')
        else:
            s.append(f'<rect x="{x:.1f}" y="{y0}" width="{bwid:.1f}" height="{bh}" fill="{col}" stroke="#fff" stroke-width="1"/>')
            s.append(f'<text x="{x+bwid/2:.1f}" y="{y0+bh/2+4}" font-size="11" fill="#fff" text-anchor="middle" font-weight="bold">{name}</text>')
    # wavelength scale (top)
    s.append(f'<text x="{x0}" y="{y0-26}" font-size="11" fill="{INK}" font-weight="bold">Wavelength (m)</text>')
    wl=['10³','1','10⁻³','10⁻⁶','10⁻⁷','10⁻⁹','10⁻¹²']
    for i,t in enumerate(wl):
        x=x0+ (i)*(bw/(len(wl)-1))
        s.append(f'<text x="{x:.1f}" y="{y0-10}" font-size="10" fill="{MUT}" text-anchor="middle">{t}</text>')
    # frequency scale (bottom)
    s.append(f'<text x="{x0}" y="{y0+bh+40}" font-size="11" fill="{INK}" font-weight="bold">Frequency (Hz)</text>')
    fq=['10⁴','10⁸','10¹¹','10¹⁴','10¹⁵','10¹⁷','10²⁰']
    for i,t in enumerate(fq):
        x=x0+ (i)*(bw/(len(fq)-1))
        s.append(f'<text x="{x:.1f}" y="{y0+bh+22}" font-size="10" fill="{MUT}" text-anchor="middle">{t}</text>')
    # arrows for energy/frequency increasing
    s.append(f'<text x="{x0+bw}" y="{y0+bh+40}" font-size="10.5" fill="{AMBER}" text-anchor="end">energy increases →</text>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------- 3. Two-surfaces capacitor (Ampere contradiction) ----------
def capacitor():
    W,H=560,300
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="DejaVu Serif, serif">']
    s.append(f'<defs><marker id="ci" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{NAVY}"/></marker></defs>')
    midy=150
    # left wire with current
    s.append(f'<line x1="20" y1="{midy}" x2="190" y2="{midy}" stroke="{INK}" stroke-width="3"/>')
    s.append(f'<line x1="60" y1="{midy}" x2="120" y2="{midy}" stroke="{NAVY}" stroke-width="3" marker-end="url(#ci)"/>')
    s.append(f'<text x="80" y="{midy-10}" font-size="16" font-style="italic" fill="{NAVY}">I</text>')
    # plates
    s.append(f'<rect x="190" y="{midy-58}" width="7" height="116" fill="{INK}"/>')
    s.append(f'<rect x="330" y="{midy-58}" width="7" height="116" fill="{INK}"/>')
    s.append(f'<line x1="337" y1="{midy}" x2="500" y2="{midy}" stroke="{INK}" stroke-width="3"/>')
    # plus/minus
    for yy in range(midy-45,midy+46,18):
        s.append(f'<text x="178" y="{yy+5}" font-size="15" fill="{RED}">+</text>')
        s.append(f'<text x="342" y="{yy+5}" font-size="15" fill="{BLUE}">−</text>')
    # E field lines between plates
    for yy in range(midy-42,midy+43,17):
        s.append(f'<line x1="200" y1="{yy}" x2="326" y2="{yy}" stroke="{AMBER}" stroke-width="1.4" marker-end="url(#ci)" opacity="0.85"/>')
    s.append(f'<text x="250" y="{midy-66}" font-size="16" font-style="italic" fill="{AMBER}">E</text>')
    # Surface S1 (flat disc cutting the wire) - green dashed ellipse
    s.append(f'<ellipse cx="150" cy="{midy}" rx="16" ry="70" fill="{GREEN}" fill-opacity="0.10" stroke="{GREEN}" stroke-width="1.8" stroke-dasharray="5,3"/>')
    s.append(f'<text x="120" y="{midy+92}" font-size="13" fill="{GREEN}" font-weight="bold">S₁ (cuts wire)</text>')
    # Surface S2 (bag passing between plates) - red dashed
    s.append(f'<path d="M150,{midy-70} C 150,{midy-70} 300,{midy-95} 300,{midy} C 300,{midy+95} 150,{midy+70} 150,{midy+70}" fill="{RED}" fill-opacity="0.07" stroke="{RED}" stroke-width="1.8" stroke-dasharray="5,3"/>')
    s.append(f'<text x="250" y="{midy+92}" font-size="13" fill="{RED}" font-weight="bold">S₂ (between plates)</text>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------- 4. Poynting vector ----------
def poynting():
    W,H=300,240
    ox,oy=90,150
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="DejaVu Serif, serif">']
    s.append(f'<defs>'
             f'<marker id="pe" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{BLUE}"/></marker>'
             f'<marker id="pb" markerWidth="9" markerHeight="9" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{RED}"/></marker>'
             f'<marker id="ps" markerWidth="10" markerHeight="10" refX="8" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 Z" fill="{GREEN}"/></marker></defs>')
    # E up
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox}" y2="{oy-95}" stroke="{BLUE}" stroke-width="2.6" marker-end="url(#pe)"/>')
    s.append(f'<text x="{ox-22}" y="{oy-88}" font-size="18" font-style="italic" fill="{BLUE}">E</text>')
    # B depth (down-left)
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox-80}" y2="{oy+52}" stroke="{RED}" stroke-width="2.6" marker-end="url(#pb)"/>')
    s.append(f'<text x="{ox-100}" y="{oy+58}" font-size="18" font-style="italic" fill="{RED}">B</text>')
    # S right (propagation)
    s.append(f'<line x1="{ox}" y1="{oy}" x2="{ox+130}" y2="{oy}" stroke="{GREEN}" stroke-width="3" marker-end="url(#ps)"/>')
    s.append(f'<text x="{ox+108}" y="{oy-10}" font-size="18" font-style="italic" fill="{GREEN}">S</text>')
    s.append(f'<text x="{ox+40}" y="{oy+24}" font-size="12.5" fill="{MUT}">S = (1/μ₀) E × B</text>')
    s.append('</svg>')
    return '\n'.join(s)

# ---------- 5. Chain reaction ----------
def chain():
    W,H=720,120
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="DejaVu Sans, sans-serif">']
    s.append(f'<defs><marker id="chA" markerWidth="10" markerHeight="10" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{AMBER}"/></marker></defs>')
    boxes=[('Changing\\nE field',BLUE),('creates\\nB field',RED),('creates\\nE field',BLUE),('creates\\nB field',RED)]
    bw=118; gap=40; x=30; y=30; bh=58
    for i,(txt,col) in enumerate(boxes):
        s.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="5" fill="none" stroke="{col}" stroke-width="2"/>')
        lines=txt.split('\\n')
        for j,ln in enumerate(lines):
            s.append(f'<text x="{x+bw/2}" y="{y+26+j*17}" font-size="13" fill="{INK}" text-anchor="middle">{ln}</text>')
        if i<len(boxes)-1:
            ax=x+bw; s.append(f'<line x1="{ax+4}" y1="{y+bh/2}" x2="{ax+gap-4}" y2="{y+bh/2}" stroke="{AMBER}" stroke-width="2.2" marker-end="url(#chA)"/>')
        x+=bw+gap
    s.append(f'<text x="{x+2}" y="{y+bh/2+5}" font-size="20" fill="{MUT}">· · · ∞</text>')
    s.append('</svg>')
    return '\n'.join(s)

SVG['em_wave']=em_wave()
SVG['spectrum']=spectrum()
SVG['capacitor']=capacitor()
SVG['poynting']=poynting()
SVG['chain']=chain()

for k,v in SVG.items():
    io.open(os.path.join(OUT,f'svg_{k}.svg'),'w',encoding='utf-8').write(v)

# test page
html=['<!doctype html><meta charset="utf-8"><body style="font-family:sans-serif">']
for k in SVG:
    html.append(f'<h3>{k}</h3><div style="border:1px solid #ccc;display:inline-block">{SVG[k]}</div>')
html.append('</body>')
io.open(os.path.join(OUT,'svg_test.html'),'w',encoding='utf-8').write('\n'.join(html))
print('wrote', len(SVG), 'svgs')

# ---------- 6. Field-line divider motif (subtle, for module dividers) ----------
def fieldlines():
    import math as _m
    W,H=680,150
    cx1,cy=200,75; cx2=480
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">']
    # dipole-like field loops between two poles at cx1 and cx2
    col='#2f6fe0'
    for k,rr in enumerate([28,60,95,135,180]):
        # ellipse-ish loops linking the two poles, bulging above and below
        bx=(cx1+cx2)/2
        yb=rr*0.62
        s.append(f'<path d="M{cx1},{cy} C {cx1+30},{cy-yb} {cx2-30},{cy-yb} {cx2},{cy} C {cx2-30},{cy+yb} {cx1+30},{cy+yb} {cx1},{cy} Z" '
                 f'fill="none" stroke="{col}" stroke-width="1.1" opacity="{max(0.05,0.22-k*0.03):.2f}"/>')
    # poles
    s.append(f'<circle cx="{cx1}" cy="{cy}" r="4" fill="#c0202e" opacity="0.5"/>')
    s.append(f'<circle cx="{cx2}" cy="{cy}" r="4" fill="#17307d" opacity="0.5"/>')
    s.append('</svg>')
    return '\n'.join(s)

SVG['fieldlines']=fieldlines()
import io as _io, os as _os
_io.open(_os.path.join(OUT,'svg_fieldlines.svg'),'w',encoding='utf-8').write(SVG['fieldlines'])
print('added fieldlines motif')
