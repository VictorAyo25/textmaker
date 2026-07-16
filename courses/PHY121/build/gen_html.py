# Generate clean styled HTML for teaching sections (Foundations + Modules 1-4).
import fitz, io, os, re, html, sys
from reconstruct import (PDF, bars, raw_spans, reflow, _linegroup, FOOTER_RE, WHITE, esc, hx, classify, blank_spans, near)

doc=fitz.open(PDF)
MUT=0x6b7280; FAINT=0x8a8f98; MAG=0xc2185b; AMBER=0xb45309; BROWN=0x7a6a52
LABELMAP={'teach':'Teach','mem':'Must-memorise','trap':'Trap','work':'Worked example',
          'recall':'Recall and check','fill':'Fill in the gap','qgroup':'The questions'}

def cnear(c,t,tol=0x14):
    return all(abs(((c>>s)&255)-((t>>s)&255))<=tol for s in (16,8,0))

def spans_to_html(spans):
    """Reflow a set of raw spans into inline HTML (with sub/sup), joining wrapped lines."""
    lines=reflow(spans)
    return lines

# ---------- table detection ----------
import base64
def is_dark(f):
    if not f: return False
    r=int(f[1:3],16); g=int(f[3:5],16); b=int(f[5:7],16)
    return (r+g+b)/3 < 0x55

def table_headers_in(page,y0,y1):
    raw=[]
    for d in page.get_drawings():
        r=d['rect']; f=hx(d.get('fill'))
        if f and is_dark(f) and r.width>70 and 12<=r.height<=42 and y0-2<=r.y0<=y1:
            sp=raw_spans(page,r.y0-1,r.y1+1)
            white=[s for s in sp if s['col']==WHITE]
            # A box bar is identified by its COLOUR, not by its wording. Every table
            # header in the manual is #1e2430, which classify() rejects; every box bar
            # uses the semantic palette. Testing the label text instead used to fail
            # both ways: "QUANTITY FORMULA NOTES" (a table) contains FORMULA, and
            # "Q4 - POTENTIAL..." (a box) contains no keyword at all.
            if white and classify(f) is None:
                raw.append(dict(y0=r.y0,y1=r.y1,x0=r.x0,x1=r.x1))
    # merge column-rects on the same row into one table header
    raw.sort(key=lambda h:(h['y0'],h['x0']))
    heads=[]
    for h in raw:
        if heads and abs(h['y0']-heads[-1]['y0'])<6:
            heads[-1]['x0']=min(heads[-1]['x0'],h['x0']); heads[-1]['x1']=max(heads[-1]['x1'],h['x1'])
            heads[-1]['y1']=max(heads[-1]['y1'],h['y1'])
        else:
            heads.append(dict(h))
    return heads

def table_extent(page,head,boxend):
    """Return (x0,y0,x1,y1) of the full table: header + body rows, using per-column
    row-background fills and horizontal separator rules below the header."""
    y0=head['y0']; x0=head['x0']; x1=head['x1']; bottom=head['y1']
    xlo=x0-6; xhi=x1+6
    for d in page.get_drawings():
        r=d['rect']; f=hx(d.get('fill'))
        # light row-background fills (any column) inside the table x-range
        if f and not is_dark(f) and r.width>50 and r.height<26 \
           and head['y1']-1<=r.y0<boxend and xlo<=r.x0 and r.x1<=xhi+30:
            bottom=max(bottom,r.y1)
        # thin horizontal separator rules (any column width) inside x-range
        for it in d.get('items',[]):
            if it[0]=='l':
                p1,p2=it[1],it[2]
                if abs(p1.y-p2.y)<1 and abs(p1.x-p2.x)>50 \
                   and head['y1']-1<=p1.y<boxend and xlo<=min(p1.x,p2.x) and max(p1.x,p2.x)<=xhi+30:
                    bottom=max(bottom,p1.y)
    return x0,y0,x1,bottom

def crop_datauri(page,x0,y0,x1,y1,dpi=300):
    clip=fitz.Rect(x0,y0,x1,y1)
    pix=page.get_pixmap(clip=clip,dpi=dpi)
    png=pix.tobytes('png')
    return 'data:image/png;base64,'+base64.b64encode(png).decode()

def figures_in(page):
    """Framed vector diagrams (the circuit networks). They are line art, so they cannot
    be rebuilt as text: a text-only pass drops the drawing and leaves its labels
    ('series', 'pair', 'parallel') stranded as loose prose. Crop them instead."""
    drs=page.get_drawings(); out=[]
    for dr in drs:
        r=dr['rect']
        if hx(dr.get('fill'))!='#ffffff' or r.width<300 or r.height<60: continue
        inner=[x for x in drs if x['rect'] is not r
               and r.x0-1<=x['rect'].x0 and x['rect'].x1<=r.x1+1
               and r.y0+1<=x['rect'].y0 and x['rect'].y1<=r.y1-1
               and x['rect'].width<r.width-8]
        if len(inner)>=3 and not any(abs(r.y0-o.y0)<4 for o in out):
            out.append(r)
    return sorted(out,key=lambda r:r.y0)

def col_bounds(headerspans):
    hs=sorted(headerspans,key=lambda s:s['x'])
    xs=[]
    for s in hs:
        if not xs or s['x']-xs[-1]>22: xs.append(s['x'])
    return xs

def build_table_html(page,hy0,hy1,endy):
    hspans=[s for s in raw_spans(page,hy0-1,hy1+2) if s['col']==WHITE]
    colx=col_bounds(hspans)
    ncol=len(colx)
    def row_cells(spans):
        cells=['']*ncol
        for s in sorted(spans,key=lambda s:s['x']):
            ci=0
            for i in range(ncol):
                if s['x']>=colx[i]-10: ci=i
            # sub/sup within cell
            cells[ci]+=s['t']
        return cells
    # header row
    hdr=row_cells(hspans)
    # body: group spans below header into visual rows
    body=[s for s in raw_spans(page,hy1+1,endy) if not FOOTER_RE.match(s['t'])]
    rows=[]
    for ln in _linegroup(body):
        rows.append(row_cells(ln))
    th=''.join(f'<th>{esc(c.strip())}</th>' for c in hdr)
    trs=[]
    for r in rows:
        if not any(c.strip() for c in r): continue
        tds=''.join(f'<td>{esc(c.strip())}</td>' for c in r)
        trs.append(f'<tr>{tds}</tr>')
    return f'<table class="data"><thead><tr>{th}</tr></thead><tbody>{"".join(trs)}</tbody></table>'

# ---------- box body rendering ----------
NUMRE=re.compile(r'^\s*\d+\.\s')
BULRE=re.compile(r'^\s*[▸•▪]\s*')
MARKRE=re.compile(r'^\s*(?:\d+\.\s*|[▸•▪]\s*)')
# a run-in answer line: "<b>2. add</b>, and this is the opposite..."
# Not an <ol> item (the number is fused into the bold run, no hanging indent), but
# it does start its own paragraph -- each numbered answer is a line of its own.
ANSRE=re.compile(r'^<b>\s*\d+\.')

def render_lines(lines):
    """Turn reflow lines (non-table) into HTML: paragraphs, steps, notes, hooks, redo, bullets, answer."""
    out=[]; para=[]; steps=[]; cur_step=None
    items=[]; cur_item=None; list_kind=None; item_x=None
    def flush_list():
        nonlocal items,cur_item,list_kind,item_x
        if cur_item is not None: items.append(cur_item); cur_item=None
        if items:
            tag,cls=('ol','qlist') if list_kind=='ol' else ('ul','bul')
            out.append(f'<{tag} class="{cls}">'+''.join(f'<li>{i}</li>' for i in items)+f'</{tag}>')
            items=[]
        list_kind=None; item_x=None
    def flush_para():
        nonlocal para
        if para:
            txt=''
            for i,h in enumerate(para):
                if i==0: txt=h
                elif txt.endswith(('‐','-')): txt=txt[:-1]+h
                else: txt+=' '+h
            out.append(f'<p>{txt}</p>'); para=[]
    def flush_steps():
        nonlocal steps,cur_step
        if cur_step is not None: steps.append(cur_step); cur_step=None
        if steps:
            lis=[]
            for st in steps:
                note=f'<span class="note">{st["note"]}</span>' if st.get('note') else ''
                lis.append(f'<li>{st["html"]}{note}</li>')
            out.append('<ol class="steps">'+''.join(lis)+'</ol>'); steps=[]
    for ln in lines:
        t=ln['text'].strip(); c=ln['col']; h=ln['html']
        if ln['badge'] is not None:
            flush_para()
            if cur_step is not None: steps.append(cur_step)
            cur_step={'html':h,'note':''}
            continue
        # large centered formula line -> eq block (only when not mid-step)
        if ln['sz']>=11.4 and cur_step is None and not t.startswith('Now redo'):
            flush_para(); flush_steps()
            out.append(f'<div class="eq">{h}</div>')
            continue
        # --- numbered / bulleted list items (marker is its own span, hanging indent) ---
        # Test the HTML, not the text. A real list item's marker is its own unstyled
        # span, so the html starts "4. A dielectric...". An answer line reads
        # "<b>1. geometry.</b> Double the..." -- there the number is fused into the
        # bold answer run and is NOT a list marker. Matching on the text cannot tell
        # them apart, and turns the answers into an <ol> that prints the number twice.
        if cur_step is None and ln['badge'] is None:
            mnum=NUMRE.match(h); mbul=BULRE.match(h)
            if mnum or mbul:
                flush_para()
                kind='ol' if mnum else 'ul'
                if list_kind and list_kind!=kind: flush_list()
                if cur_item is not None: items.append(cur_item)
                list_kind=kind; item_x=ln['x0']
                cur_item=MARKRE.sub('',h,count=1)
                continue
            if cur_item is not None:
                # a wrapped continuation line sits indented under the item text
                if ln['x0']>(item_x or 0)+6 and not cnear(c,MUT) and not cnear(c,FAINT):
                    cur_item=(cur_item[:-1]+h) if cur_item.endswith(('‐','-')) else cur_item+' '+h
                    continue
                flush_list()
        # each numbered answer begins a fresh paragraph, else all of them run
        # together into one block of prose
        if cur_step is None and ANSRE.match(h):
            flush_para()
        role='body'
        if t.upper() in ('ANSWER','ANSWERS'): role='anslabel'
        elif t.startswith('MEMORY HOOK') or (cnear(c,MAG) and t.upper().startswith('MEMORY')): role='hook'
        elif t.startswith('Now redo it'): role='redo'
        elif cnear(c,AMBER) or cnear(c,BROWN): role='redo'
        elif cnear(c,MUT) or cnear(c,FAINT): role='note'
        if role=='hook':
            flush_para(); flush_steps()
            hh=re.sub(r'^(MEMORY HOOK:?)',r'<b>\1</b>',h)
            out.append(f'<p class="hook">{hh}</p>')
        elif role=='redo':
            flush_para(); flush_steps()
            hh=re.sub(r'^(Now redo it:?)',r'<b>\1</b>',h)
            out.append(f'<p class="redo">{hh}</p>')
        elif role=='anslabel':
            flush_para(); flush_steps()
            out.append(f'<hr class="cut"><p class="alabel">{esc(t.title())}</p>')
        elif role=='note':
            if cur_step is not None and not cur_step.get('note'):
                cur_step['note']=h
            else:
                flush_para()
                out.append(f'<p class="small">{h}</p>')
        else:
            if cur_step is not None:
                # continuation of step text
                if cur_step['html'].endswith(('‐','-')): cur_step['html']=cur_step['html'][:-1]+h
                else: cur_step['html']+=' '+h
            else:
                para.append(h)
    flush_para(); flush_list(); flush_steps()
    return '\n'.join(out)

def render_box(page,b,nexty):
    typ=b['type']; label=b['label']
    # tag chip (SLIDE/CLASSWORK/METHOD/GUIDED/MCQ) sometimes prefixes label
    tag=''
    m=re.match(r'^((?:SLIDE|CLASSWORK|METHOD|GUIDED|MCQ|,|\s)+)\b',label)
    # detect known tags
    tagwords=re.findall(r'SLIDE|CLASSWORK|METHOD|GUIDED|MCQ',label)
    core=label
    for tw in tagwords: core=core.replace(tw,'')
    # strip leading marker glyphs (CSS re-adds them) and stray punctuation
    core=core.lstrip('●⚠•●⚠↻ ,·').strip(' ,·')
    if tagwords: tag=f'<span class="tag">{", ".join(dict.fromkeys(tagwords)).title()}</span>'
    # a right-aligned chip carried on the bar itself, e.g. the back matter's "ANSWER: C"
    if not tag and b.get('tag'): tag=f'<span class="tag">{esc(b["tag"])}</span>'
    # sentence-case the label (keep existing case for mixed)
    barlabel=core if core else LABELMAP.get(typ,typ).upper()
    if barlabel.isupper():
        barlabel=barlabel[:1]+barlabel[1:].lower()
    # body: handle tables via crop
    y0=b['y1']+2
    heads=table_headers_in(page,y0,nexty)
    segments=[]; cursor=y0
    boxx0=b.get('x0',51); boxx1=b.get('x1',544)
    def _txt(a,bnd):
        # merge the drawn fill-in blanks in as pseudo-spans so reflow places them
        sp=[s for s in raw_spans(page,a,bnd) if not FOOTER_RE.match(s['t'])]
        return sp+blank_spans(page,a,bnd) if sp else sp
    # the boxed final answer: an amber full-width rect holding bold monospace text
    abox=[]
    for d in page.get_drawings():
        r=d['rect']; f=hx(d.get('fill'))
        if f and near(f,'#b45309') and r.width>400 and 16<=r.height<=46 and y0<=r.y0<nexty:
            abox.append((r.y0,r.y1))
    abox.sort()
    # regions that cannot flow as text and must be cropped, in page order
    regions=[]
    for h in heads:
        _,ty0,_,ty1=table_extent(page,h,nexty-2)
        regions.append((ty0,ty1,'table',(boxx0,ty0,boxx1,ty1)))
    for r in figures_in(page):
        if y0<=r.y0<nexty:
            regions.append((r.y0,r.y1,'figure',(r.x0-1,r.y0-1,r.x1+1,r.y1+1)))
    regions.sort()
    for ry0,ry1,kind,payload in regions:
        if ry0>cursor+2:
            pre=_txt(cursor,ry0-1)
            if pre: segments.append(('text',pre))
        segments.append((kind,payload))
        cursor=ry1+1
    post=_txt(cursor,nexty-2)
    if post: segments.append(('text',post))
    # carve the boxed answer out of whichever text segment contains it
    if abox:
        newseg=[]
        for kind,payload in segments:
            if kind!='text':
                newseg.append((kind,payload)); continue
            rest=payload
            for ay0,ay1 in abox:
                inside=[s for s in rest if ay0-1<=(s['y']+s['y1'])/2<=ay1+1]
                if not inside: continue
                before=[s for s in rest if (s['y']+s['y1'])/2<ay0-1]
                after=[s for s in rest if (s['y']+s['y1'])/2>ay1+1]
                if before: newseg.append(('text',before))
                newseg.append(('answer',inside))
                rest=after
            if rest: newseg.append(('text',rest))
        segments=newseg
    body_html=[]
    for kind,payload in segments:
        if kind=='text':
            body_html.append(render_lines(reflow(payload)))
        elif kind=='answer':
            txt=' '.join(l['html'] for l in reflow(payload))
            body_html.append(f'<div class="answerbox">{txt}</div>')
        elif kind=='figure':
            uri=crop_datauri(page,*payload)
            body_html.append(f'<img class="figure" src="{uri}" alt="diagram"/>')
        else:
            tx0,ty0,tx1,ty1=payload
            uri=crop_datauri(page,tx0-2,ty0-1,tx1+2,ty1+2)
            body_html.append(f'<img class="tablefig" src="{uri}" alt="table"/>')
    cls=typ   # box type IS the CSS class; every type in HEADER_COLORS has a rule
    boxhtml=(f'<div class="box {cls}"><div class="bar"><span>{esc(barlabel)}</span>{tag}</div>'
             f'<div class="body">{"".join(body_html)}</div></div>')
    # optional diagram injection after a box whose label matches
    fig=''
    for key,(svg,cap) in (DIAGRAM_MAP or {}).items():
        if key.upper() in label.upper():
            fig=f'<figure>{svg}<figcaption>{cap}</figcaption></figure>'
            break
    return boxhtml+fig

DIAGRAM_MAP=None
def set_diagram_map(m):
    global DIAGRAM_MAP; DIAGRAM_MAP=m

def render_section_header(page,first_y):
    sp=[s for s in raw_spans(page,40,first_y-3) if not FOOTER_RE.match(s['t'])]
    lines=reflow(sp)
    if not lines: return ''
    maxsz=max(l['sz'] for l in lines)
    if maxsz<12.5: return ''   # not a real section header page
    ti=next(i for i,l in enumerate(lines) if l['sz']>=maxsz-0.3)
    parts=[]
    kick=' '.join(l['html'] for l in lines[:ti]).strip()
    if kick:
        # strip inline tags first: the kicker html may contain <b>/<i>, whose letters
        # would otherwise survive into the marker id (e.g. BFOUNDATIONSF1B)
        mid=re.sub(r'[^A-Za-z0-9]','',re.sub(r'<[^>]+>','',kick)).upper()
        parts.append(f'<span class="tocm" id="sec-{mid}">TOCM{mid}TOCM</span>')
        parts.append(f'<div class="kick">{kick}</div>')
    parts.append(f'<h2 class="title">{lines[ti]["html"]}</h2><hr class="rule">')
    lead=[]
    for l in lines[ti+1:]:
        cls='lead' if cnear(l['col'],MUT) else ('lo' if 'outcomes' in l['text'].lower() else '')
        lead.append((cls,l['html']))
    # merge consecutive lead lines
    buf=[]; curcls=None; outp=[]
    for cls,h in lead:
        if cls!=curcls and buf:
            outp.append((curcls,' '.join(buf))); buf=[]
        curcls=cls; buf.append(h)
    if buf: outp.append((curcls,' '.join(buf)))
    for cls,h in outp:
        parts.append(f'<p class="{cls}">{h}</p>' if cls else f'<p>{h}</p>')
    return '\n'.join(parts)

def gen_pages(lo,hi):
    chunks=[]
    for p in range(lo,hi+1):
        page=doc[p-1]; ph=page.rect.height
        bb=bars(page)
        if not bb:
            continue
        # section header only if this page starts a section (kicker present above first box)
        hdr=render_section_header(page,bb[0]['y0'])
        if hdr and ('kick' in hdr):
            chunks.append(f'<section>{hdr}')
            close_needed=True
        for i,b in enumerate(bb):
            nexty=bb[i+1]['y0'] if i+1<len(bb) else ph-40
            chunks.append(render_box(page,b,nexty))
    return '\n'.join(chunks)

if __name__=='__main__':
    lo,hi=int(sys.argv[1]),int(sys.argv[2])
    body=gen_pages(lo,hi)
    doc_html=f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="manual.css"></head><body>{body}</body></html>'
    io.open('recon_test.html','w',encoding='utf-8').write(doc_html)
    print(f'generated recon_test.html for pages {lo}-{hi}, {len(body)} bytes')
