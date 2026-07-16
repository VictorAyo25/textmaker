# Structure-aware extractor: use colored box header bars to group/order text.
import fitz, io, os, sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(BASE, 'sources', 'PHY121_Study_Manual.pdf')

HEADER_COLORS = {  # hex -> box type
    '#1b2a4a': 'teach',      # also table header / formula
    '#c2185b': 'mem',
    '#b91c1c': 'trap',
    '#b45309': 'work',
    '#4a5568': 'recall',
    '#5b3a8e': 'fill',
}

def hx(c):
    if c is None: return None
    return '#%02x%02x%02x' % tuple(int(round(x*255)) for x in c)

def near(hexcol, target, tol=12):
    if hexcol is None: return False
    a=[int(hexcol[i:i+2],16) for i in (1,3,5)]
    b=[int(target[i:i+2],16) for i in (1,3,5)]
    return all(abs(x-y)<=tol for x,y in zip(a,b))

def classify_bar(colhex):
    for tgt,typ in HEADER_COLORS.items():
        if near(colhex,tgt): return typ,tgt
    return None,None

KEYWORDS=('TEACH','MUST-MEMORISE','TRAP','WORKED EXAMPLE','RECALL AND CHECK',
          'FILL IN THE GAP','FORMULA','SECTION','QUESTION','EXERCISE','ANSWER KEY',
          'MOCK','THE ','A ','TWO ','MODULE')  # header labels (loose)

def bar_label(page,b):
    hdr=spans_in(page,b['y0']-2,b['y1']+2)
    return ' '.join(s[2] for s in hdr).strip()

def page_boxes(page):
    """Return list of header bars validated by white label text starting with a keyword."""
    cand=[]
    for d in page.get_drawings():
        r=d['rect']; fill=hx(d.get('fill'))
        if fill and r.width>300 and 14<=r.height<=34:
            typ,tgt=classify_bar(fill)
            if typ:
                cand.append(dict(type=typ,y0=r.y0,y1=r.y1,x0=r.x0,x1=r.x1,color=fill))
    cand.sort(key=lambda b:b['y0'])
    out=[]
    for b in cand:
        if out and abs(b['y0']-out[-1]['y0'])<6:
            continue
        # validate: header must contain WHITE text (the uppercase label)
        hdr=spans_in(page,b['y0']-1,b['y1']+1)
        white=[s for s in hdr if s[4]==16777215]  # #ffffff
        if not white:
            continue
        label=' '.join(s[2] for s in white).strip().upper()
        if not any(label.startswith(k) or k in label for k in
                   ('TEACH','MUST','TRAP','WORKED','RECALL','FILL','FORMULA','SECTION','QUESTION','MOCK','EXERCISE','ANSWER')):
            # still accept if label is fully uppercase and reasonably long (section-specific headers)
            if not (label==label.upper() and len(label)>6):
                continue
        b['label']=label
        out.append(b)
    return out

def spans_in(page, y0, y1):
    """Ordered (y,x) text spans with center y in [y0,y1)."""
    d=page.get_text('dict')
    items=[]
    for b in d['blocks']:
        for l in b.get('lines',[]):
            for s in l.get('spans',[]):
                cy=(s['bbox'][1]+s['bbox'][3])/2
                if y0<=cy<y1:
                    items.append((round(s['bbox'][1],1),round(s['bbox'][0],1),s['text'],round(s['size'],1),s['color'],s['flags']))
    items.sort(key=lambda t:(round(t[0]/2), t[1]))
    return items

if __name__=='__main__':
    doc=fitz.open(PDF)
    pgnum=int(sys.argv[1]) if len(sys.argv)>1 else 8
    page=doc[pgnum-1]
    bars=page_boxes(page)
    out=io.open(os.path.join(os.path.dirname(__file__),'struct_out.txt'),'w',encoding='utf-8')
    out.write(f'PAGE {pgnum}: found {len(bars)} box header bars\n')
    ph=page.rect.height
    for i,b in enumerate(bars):
        nexty = bars[i+1]['y0'] if i+1<len(bars) else ph-40
        out.write(f'\n===== BOX {i}: {b["type"].upper()} (color {b["color"]}, y {b["y0"]:.0f}-{nexty:.0f}) =====\n')
        # header label text (in bar)
        hdr=spans_in(page,b['y0']-2,b['y1']+2)
        out.write('  HEADER: '+' '.join(s[2] for s in hdr)+'\n')
        # body text
        body=spans_in(page,b['y1']+1,nexty-1)
        for y,x,txt,sz,col,fl in body:
            out.write(f'    [y{y:.0f} x{x:.0f} sz{sz} #{col:06x}] {txt}\n')
    out.close()
    print(f'page {pgnum}: {len(bars)} boxes -> struct_out.txt')
