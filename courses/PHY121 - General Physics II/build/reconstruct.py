# Structure-aware reconstruction of the PHY121 manual: PDF -> structured HTML.
import fitz, io, os, re, html, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(BASE, 'sources', 'manual_v1', 'PHY121_Study_Manual.pdf')

# Every box bar in the manual, keyed by its bar fill. This is the ONLY way a box is
# identified: table headers are #1e2430 and are absent here on purpose, so classify()
# returning None is what marks a bar as a table header.
HEADER_COLORS = {'#1b2a4a':'teach','#c2185b':'mem','#b91c1c':'trap',
                 '#b45309':'work','#4a5568':'recall','#5b3a8e':'fill',
                 # teal: FORMULA and CASE boxes ("FORMULA - THE BIOT-SAVART LAW")
                 '#0b6b5f':'formula',
                 # back-matter only: the violet bar that opens a group of questions
                 # ("THE QUESTIONS - MODULE 1", "INSTRUCTIONS"). Distinct from the
                 # teaching FILL purple (#5b3a8e), so it needs its own entry.
                 '#4c1d95':'qgroup'}
WHITE=16777215
FOOTER_RE=re.compile(r'^PHY121.+Victor Ayodeji')

def hx(c):
    return None if c is None else '#%02x%02x%02x'%tuple(int(round(x*255)) for x in c)
def near(h,t,tol=14):
    if not h: return False
    a=[int(h[i:i+2],16) for i in (1,3,5)]; b=[int(t[i:i+2],16) for i in (1,3,5)]
    return all(abs(x-y)<=tol for x,y in zip(a,b))
def classify(h):
    for t,typ in HEADER_COLORS.items():
        if near(h,t): return typ
    return None

def raw_spans(page,y0,y1,x0=0,x1=9999):
    d=page.get_text('dict'); items=[]
    for b in d['blocks']:
        for l in b.get('lines',[]):
            for s in l.get('spans',[]):
                bx0,by0,bx1,by1=s['bbox']; cy=(by0+by1)/2; cx=(bx0+bx1)/2
                if y0<=cy<y1 and x0<=cx<x1 and s['text']:
                    items.append(dict(y=by0,y1=by1,x=bx0,x1=bx1,t=s['text'],
                                      sz=round(s['size'],1),col=s['col'] if 'col' in s else s['color'],flags=s['flags']))
    return items

def bars(page):
    cand=[]
    for d in page.get_drawings():
        r=d['rect']; f=hx(d.get('fill'))
        if f and r.width>300 and 14<=r.height<=46:
            typ=classify(f)
            if typ: cand.append(dict(type=typ,y0=r.y0,y1=r.y1,x0=r.x0,x1=r.x1))
    cand.sort(key=lambda b:b['y0']); out=[]
    for b in cand:
        if out and abs(b['y0']-out[-1]['y0'])<6: continue
        hdr=raw_spans(page,b['y0']-1,b['y1']+1)
        white=[s for s in hdr if s['col']==WHITE]
        if not white: continue
        white.sort(key=lambda s:s['x'])
        # Do NOT gate on keywords. That was written for the teaching sections, where
        # every bar starts with TEACH/WORKED/RECALL/..., and it silently discarded 54
        # real back-matter boxes labelled "Q4 - POTENTIAL AT TWO DISTANCES" etc.
        # Table headers are already rejected upstream by colour: they are #1e2430,
        # which is not in HEADER_COLORS, so classify() returns None for them.
        # A right-aligned span separated by a wide gap is the bar's tag chip
        # ("ANSWER: C"), not part of the label. Joining it on would weld it to the
        # last word ("...TWO DISTANCESANSWER: C").
        tag=''
        if len(white)>1:
            gaps=[(white[i+1]['x']-white[i]['x1'],i) for i in range(len(white)-1)]
            g,i=max(gaps)
            if g>40 and white[i+1]['x'] > b['x0']+0.55*(b['x1']-b['x0']):
                tag=' '.join(s['t'] for s in white[i+1:]).strip()
                white=white[:i+1]
        b['label']=' '.join(s['t'] for s in white).strip()
        b['tag']=tag
        out.append(b)
    return out

def esc(t): return html.escape(t,quote=False)

def _is_letterspaced(t):
    """Spaces outnumbering the glyphs means the extractor put one in every gap.

    Not a regex over "single char, space, single char": kerning fuses some pairs,
    so the real extractions read "O R I E N TAT I O N" and "S O LU T I O N S S . 1".
    Ordinary prose sits near one space per six characters and never trips this."""
    nsp=t.count(' '); other=len(t)-nsp
    return other>=4 and nsp>=other*0.5

def unletterspace(page,span):
    """Undo the spaces PyMuPDF invents inside a letterspaced label.

    The kickers are tracked so wide that every letter gap exceeds the extractor's
    space threshold, so "REFERENCE R.3" comes out as "R E F E R E N C E R . 3".
    Re-emitting that with the CSS letter-spacing on top doubles the tracking AND
    hides the real word break, leaving "REFERENCER.3" on the page.

    The word space is physically wider than the letter gaps (3.13pt vs 1.61pt in
    the R.3 kicker), so measure the space glyphs and keep only the wide ones.

    Only ever call this on a kicker. The same shape occurs in real text whose
    spaces are all genuine ("F = k · q" is 4 uniform 4.44pt spaces), and there the
    rule would close up every one of them."""
    t=span['t']
    if not _is_letterspaced(t):
        return t
    for b in page.get_text('rawdict')['blocks']:
        for l in b.get('lines',[]):
            for s in l.get('spans',[]):
                if abs(s['bbox'][0]-span['x'])>0.6 or abs(s['bbox'][1]-span['y'])>0.6:
                    continue
                chars=s['chars']
                w=sorted(c['bbox'][2]-c['bbox'][0] for c in chars if c['c']==' ')
                if not w: return t
                med=w[len(w)//2]
                out=''.join('' if (c['c']==' ' and (c['bbox'][2]-c['bbox'][0])<med*1.5)
                            else c['c'] for c in chars)
                return out.strip()
    return t

def _linegroup(spans):
    """Group spans into visual lines by vertical OVERLAP, so superscripts and
    subscripts stay on the same line as their base."""
    spans=sorted(spans,key=lambda s:s['y'])
    lines=[]; cur=[]; cur_bot=None; cur_top=None
    for s in spans:
        if cur and s['y'] < cur_bot-2:   # vertically overlaps current line band
            cur.append(s); cur_bot=max(cur_bot,s['y1']); cur_top=min(cur_top,s['y'])
        else:
            if cur: lines.append(cur)
            cur=[s]; cur_top=s['y']; cur_bot=s['y1']
    if cur: lines.append(cur)
    return lines

BLANK = ''   # sentinel for a fill-in-the-gap blank (drawn, not text)

def blank_spans(page, y0, y1):
    """The fill-in-the-gap blanks are thin filled rects (~62 x 1pt), not text, so a
    text-only extraction silently drops them and the exercise becomes unanswerable.
    Return them as pseudo-spans positioned on their text line."""
    out = []
    for d in page.get_drawings():
        r = d['rect']
        if d.get('fill') and 0.7 <= r.height <= 1.6 and 40 <= r.width <= 90 and y0 <= r.y0 <= y1:
            out.append(dict(y=r.y0 - 9.0, y1=r.y0 + 0.5, x=r.x0, x1=r.x1,
                            t=BLANK, sz=10.2, col=0x2b3140, flags=0))
    return out



def _mergeruns(h):
    """Collapse adjacent identical inline tags: <b>a</b><b>b</b> -> <b>ab</b>."""
    for tag in ('b','i','code','sup','sub'):
        h=h.replace(f'</{tag}><{tag}>','')
    return h

def reflow(spans, body_sz_hint=10.2):
    """Merge spans into visual lines; wrap sub/superscripts. Returns list of dicts:
       {y, html, text, col, sz, badge(None|int), x0}."""
    from collections import Counter
    out=[]
    for ln in _linegroup(spans):
        ln=sorted(ln,key=lambda s:s['x'])
        base=max(s['sz'] for s in ln)
        # baseline = the plurality bottom-edge (y1), weighted by character count
        cnt=Counter()
        for s in ln: cnt[round(s['y1'])]+=max(1,len(s['t'].strip()))
        baseline=cnt.most_common(1)[0][0]
        htmlparts=[]; textparts=[]; cols={}; badge=None
        for k,s in enumerate(ln):
            txt=esc(s['t']); raw=s['t']
            if raw==BLANK:
                htmlparts.append('<span class="blank"></span>'); textparts.append(' ')
                continue
            cols[s['col']]=cols.get(s['col'],0)+len(raw.strip())
            # white lone-digit at line start in a work box = step badge
            if s['col']==WHITE and raw.strip().isdigit() and k==0 and len(raw.strip())<=2:
                badge=int(raw.strip()); continue
            not_bigger = s['sz']<=base+0.4
            if not_bigger and s['y1'] < baseline-2.0:
                piece=f'<sup>{txt}</sup>'
            elif not_bigger and s['y1'] > baseline+2.0:
                piece=f'<sub>{txt}</sub>'
            else:
                piece=txt
            # PyMuPDF flags: bit1(2)=italic, bit3(8)=monospaced, bit4(16)=bold.
            # The manual uses all three meaningfully (emphasis, code-style formulas),
            # so dropping them loses real information.
            if s['flags'] & 8:
                piece=f'<code>{piece}</code>'
            if s['flags'] & 2:
                piece=f'<i>{piece}</i>'
            if s['flags'] & 16:
                piece=f'<b>{piece}</b>'
            htmlparts.append(piece); textparts.append(raw)
        domcol=max(cols,key=cols.get) if cols else 0
        out.append(dict(y=min(s['y'] for s in ln), x0=min(s['x'] for s in ln),
                        html=_mergeruns(''.join(htmlparts)), text=''.join(textparts),
                        col=domcol, sz=base, badge=badge))
    return out

# A line-break hyphen is U+2010, a real hyphen is ASCII. The typesetter distinguishes
# them, so this needs no guessing: across the whole manual all 49 U+2010 line ends are
# words the hyphenator split ("capa-citor", "substi-tution") and all 6 ASCII line ends
# are genuine compounds ("cross-sectional", "T-joint", "problem-solving").
_SOFTHYPH=re.compile('‐(?=(?:</[^>]+>)*\\s*$)')

def join_wrapped(txt,h):
    """Append a wrapped line's html to the previous line's, resolving a line-end hyphen.
    Dropping every hyphen yields "crosssectional" and "Tjoint"; keeping every one
    yields "capa-citor"."""
    plain=re.sub(r'<[^>]+>','',txt).rstrip()
    if not plain.endswith(('-','‐')):
        return _mergeruns(txt+' '+h)
    if plain.endswith('-'):
        return _mergeruns(txt+h)                             # real hyphen: keep it, no space
    return _mergeruns(_SOFTHYPH.sub('',txt,count=1)+h)       # line-break hyphen: close the word up

if __name__=='__main__':
    doc=fitz.open(PDF)
    p=int(sys.argv[1])
    page=doc[p-1]; ph=page.rect.height
    bb=bars(page)
    out=io.open('recon_dbg.txt','w',encoding='utf-8')
    out.write(f'PAGE {p}: {len(bb)} boxes\n')
    for i,b in enumerate(bb):
        nexty=bb[i+1]['y0'] if i+1<len(bb) else ph-40
        out.write(f'\n[{b["type"]}] {b["label"]}\n')
        body=[s for s in raw_spans(page,b['y0']+ (b["y1"]-b["y0"]) +2, nexty-2) if not FOOTER_RE.match(s['t'])]
        for ln in reflow(body):
            out.write(f'   #{ln["col"]:06x} sz{ln["sz"]}: {ln["html"]}\n')
    out.close(); print(f'page {p}: {len(bb)} boxes -> recon_dbg.txt')
