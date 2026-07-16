# Master assembler: build the full blended manual (Modules 1-5) as one HTML,
# with regenerated Contents (correct page numbers) via a 2-pass render.
import fitz, io, os, re, subprocess, sys
from reconstruct import PDF, raw_spans, reflow, FOOTER_RE
import gen_html
from gen_html import gen_pages, crop_datauri, set_diagram_map
from recon_back import gen_back

HERE=os.path.dirname(os.path.abspath(__file__))
doc=fitz.open(PDF)
def load(p): return io.open(os.path.join(HERE,p),encoding='utf-8').read()

def split_module5():
    body=load('module5_body.html'); assess=load('module5_assess.html')
    svgs={n:load(f'svg_{n}.svg') for n in ['em_wave','spectrum','capacitor','poynting','chain','fieldlines']}
    inj=lambda t: re.sub(r'\{\{SVG:(\w+)\}\}', lambda m:svgs.get(m.group(1),''), t)
    body=inj(body)
    def between(t,a,b):
        i=t.find(a); j=t.find(b) if b else len(t); return t[i:j]
    def _mk(m):
        mid=re.sub(r'[^A-Za-z0-9]','',m.group(1)).upper()
        return f'<span class="tocm" id="sec-{mid}">TOCM{mid}TOCM</span><div class="kick">{m.group(1)}</div>'
    def mark(t):  # inject TOC markers before each kick div
        return re.sub(r'<div class="kick">([^<]+)</div>', _mk, t)
    found=mark(between(body,'<!-- ============ FOUNDATIONS ADD-ONS','<!-- ============ PART DIVIDER'))
    module=between(body,'<!-- ============ PART DIVIDER', None)
    module=mark(module).replace('<div class="kicker">Part VI</div>',
                                '<span class="tocm">TOCMPARTVITOCM</span><div class="kicker">Part VI</div>')
    s7=mark(between(assess,'<!-- ============ MODULE 5 EXERCISES','<!-- ============ MODULE 5 MOCK'))
    m5=mark(between(assess,'<!-- ============ MODULE 5 MOCK','<!-- ============ REFERENCE ADDITIONS'))
    refadd=mark(between(assess,'<!-- ============ REFERENCE ADDITIONS', None))
    return dict(foundations=found, module=module, s7=s7, m5=m5, refadd=refadd)

def crop_page(pagenum, dpi=170, marker=None):
    uri=crop_datauri(doc[pagenum-1], 40, 30, 556, 800, dpi=dpi)
    mk=f'<span class="tocm" id="sec-{marker}">TOCM{marker}TOCM</span>' if marker else ''
    return f'<div class="fullpage">{mk}<img src="{uri}" alt="p{pagenum}"/></div>'

FIELDLINES=None
def divider_html(roman, pagenum, marker):
    global FIELDLINES
    if FIELDLINES is None: FIELDLINES=load('svg_fieldlines.svg')
    sp=[s for s in raw_spans(doc[pagenum-1],60,700) if not FOOTER_RE.match(s['t'])]
    lines=reflow(sp)
    if not lines: return crop_page(pagenum)
    maxsz=max(l['sz'] for l in lines)
    ti_last=max(i for i,l in enumerate(lines) if l['sz']>=maxsz-0.5)
    title=' '.join(l['html'] for l in lines if l['sz']>=maxsz-0.5)
    blurb=' '.join(l['html'] for l in lines[ti_last+1:])
    return (f'<div class="part fullpage-part"><span class="tocm" id="sec-{marker}">TOCM{marker}TOCM</span>'
            f'<div class="kicker">Part {roman}</div><h1>{title}</h1><p class="blurb">{blurb}</p>'
            f'<div class="divider-motif">{FIELDLINES}</div></div>')

def load_msvg(n): return load(f'msvg_{n}.svg')
def build_diagram_map():
    return {
      'ELECTRIC FIELD LINES AND HOW TO READ':(load_msvg('field_points'),'Field lines point out of a positive charge and in to a negative charge.'),
      'PRINCIPLE OF SUPERPOSITION':(load_msvg('superposition'),'Work out each force separately, then add them as vectors.'),
      'THE PARALLEL PLATE CAPACITOR':(load_msvg('capacitor_plates'),'Two plates, area A, separation d, with a uniform field E between them.'),
      'RESISTORS IN SERIES':(load_msvg('circuit_series'),'In series the same current flows through every resistor.'),
      'RESISTORS IN PARALLEL':(load_msvg('circuit_parallel'),'In parallel every branch has the same voltage across it.'),
      'FIELD INTO AND OUT OF THE PAGE':(load_msvg('field_in_out'),'Dots show the field out of the page; crosses show it into the page.'),
      'THE THREE CASES OF MOTION':(load_msvg('helical_path'),'A velocity at an angle to B produces a helical path.'),
      'A CURRENT LOOP IS A MAGNET':(load_msvg('current_loop'),'A current loop behaves as a magnetic dipole with moment along its axis.'),
    }

# TOC: (level, label, marker)
TOC=[
 (1,'How to use this manual','ORIENTATION'),
 (0,'PART I · FOUNDATIONS','PARTI'),
 (2,'F.1 Powers of ten, prefixes and calculator discipline','FOUNDATIONSF1'),
 (2,'F.2 Rearranging formulas','FOUNDATIONSF2'),
 (2,'F.3 Scalars, vectors and components','FOUNDATIONSF3'),
 (2,'F.4 Trigonometry, and the angles that matter','FOUNDATIONSF4'),
 (2,'F.5 Simultaneous equations','FOUNDATIONSF5'),
 (2,'F.6 Reciprocal arithmetic','FOUNDATIONSF6'),
 (2,'F.7 Proportional reasoning','FOUNDATIONSF7'),
 (2,'F.8 The small amount of calculus you need','FOUNDATIONSF8'),
 (2,'F.9 Circles, areas and the geometry you need','FOUNDATIONSF9'),
 (2,'F.10 Rate of change, and the flux that changes','FOUNDATIONSF10'),
 (2,'F.11 Divergence and curl, just enough to read Maxwell','FOUNDATIONSF11'),
 (0,'PART II · MODULE 1: ELECTROSTATICS','PARTII'),
 (2,'1.1 Forces in nature and the idea of charge','UNIT11'),
 (2,"1.2 Coulomb's law and the electric field",'UNIT12'),
 (2,'1.3 Electric potential and energy','UNIT13'),
 (2,"1.4 Gauss's law",'UNIT14'),
 (0,'PART III · MODULE 2: ELECTRIC CIRCUITS AND MATERIALS','PARTIII'),
 (2,'2.1 Conductors, insulators and the electric dipole','UNIT21'),
 (2,'2.2 Capacitance and dielectrics','UNIT22'),
 (0,'PART IV · MODULE 3: ELECTRICITY AND CIRCUIT ANALYSIS','PARTIV'),
 (2,'3.1 Electric current, resistance and semiconductors','UNIT31'),
 (2,'3.2 Series, parallel and combination circuits','UNIT32'),
 (2,'3.3 Voltage dividers and current dividers','UNIT33'),
 (2,"3.4 Kirchhoff's laws",'UNIT34'),
 (0,'PART V · MODULE 4: MAGNETISM AND EM INDUCTION','PARTV'),
 (2,'4.1 Magnetic fields and the Lorentz force','UNIT41'),
 (2,'4.2 Sources of magnetic fields','UNIT42'),
 (2,'4.3 Electromagnetic induction','UNIT43'),
 (2,'4.4 emf, internal resistance and terminal voltage','UNIT44'),
 (2,'4.5 Inductance and energy stored in an inductor','UNIT45'),
 (2,'4.6 Torque on a current loop and the magnetic dipole moment','UNIT46'),
 (0,"PART VI · MODULE 5: MAXWELL'S EQUATIONS & EM WAVES",'PARTVI'),
 (2,"5.1 Maxwell's equations",'UNIT51'),
 (2,'5.2 Electromagnetic waves','UNIT52'),
 (0,'PART VII · EVERY EXERCISE, FULLY SOLVED','PARTVII'),
 (2,'S.1 Module 1 classwork','SOLUTIONSS1'),
 (2,'S.2 Module 2 classwork','SOLUTIONSS2'),
 (2,'S.3 Module 3 classwork and circuit questions','SOLUTIONSS3'),
 (2,'S.4 Module 4 tutorial questions','SOLUTIONSS4'),
 (2,'S.5 CBT Test 1: all fifteen questions','SOLUTIONSS5CBTTEST1'),
 (2,'S.6 CBT Test 2: all fifteen questions','SOLUTIONSS6CBTTEST2'),
 (2,'S.7 Module 5 exercises, fully solved','S7'),
 (0,'PART VIII · MOCK EXAMINATIONS','PARTVIII'),
 (2,'M.1 Mock exam paper','M1'),
 (2,'M.2 Mock exam: worked answer key','M2'),
 (2,'M.3 Second practice paper','M3'),
 (2,'M.4 Second paper: worked answer key','M4'),
 (2,'M.5 Module 5 mock: Maxwell & EM waves','M5'),
 (0,'PART IX · REFERENCE','PARTIX'),
 (2,'R.1 Complete formula and constant sheet','REFERENCER1'),
 (2,'R.2 The must-memorise list','REFERENCER2'),
 (2,'R.3 A general problem-solving method','REFERENCER3'),
 (2,'R.4 Glossary','REFERENCER4'),
 (2,'R.1b Module 5 formulas & must-memorise additions','REFERENCER1ADDITION'),
]

CONTENT=os.path.join(HERE,'content')

def frozen(name):
    """Return frozen editable HTML for a section, or None if not frozen yet."""
    p=os.path.join(CONTENT,name+'.html')
    if os.path.exists(p):
        return io.open(p,encoding='utf-8').read()
    return None

def section(name, lo, hi, gen=None):
    """Frozen content if available (editable), else re-derive from the v1 PDF."""
    return frozen(name) or (gen or gen_pages)(lo,hi)

def part(name, roman, pg, marker):
    return frozen(name) or divider_html(roman,pg,marker)

def assemble(contents_html=''):
    m5=split_module5()
    set_diagram_map(build_diagram_map())
    S=[]
    S.append(crop_page(1))
    S.append(f'<div class="contents-page">{contents_html}</div>')
    S.append(section('howto',4,5,gen_back))
    S.append(part('partI','I',6,'PARTI'))
    S.append(section('foundations',7,20)); S.append(m5['foundations'])
    S.append(part('partII','II',21,'PARTII')); S.append(section('module1',22,40))
    S.append(part('partIII','III',41,'PARTIII')); S.append(section('module2',42,53))
    S.append(part('partIV','IV',54,'PARTIV')); S.append(section('module3',55,79))
    S.append(part('partV','V',80,'PARTV')); S.append(section('module4',81,106))
    S.append(m5['module'])                                    # Module 5 (Part VI)
    S.append(part('partVII','VII',107,'PARTVII'))
    S.append(section('exercises',108,143,gen_back))
    S.append(m5['s7'])
    S.append(part('partVIII','VIII',144,'PARTVIII'))
    S.append(section('mocks',145,164,gen_back))
    S.append(m5['m5'])
    S.append(part('partIX','IX',165,'PARTIX'))
    S.append(section('reference',166,174,gen_back))
    S.append(m5['refadd'])
    body='\n'.join(S)
    html=(f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
          f'<title>PHY121 Complete Study Manual</title>'
          f'<link rel="stylesheet" href="manual.css"></head><body>{body}</body></html>')
    io.open(os.path.join(HERE,'full_manual.html'),'w',encoding='utf-8').write(html)
    return html

def marker_pages(pdfpath):
    d=fitz.open(pdfpath); pages={}
    for i in range(d.page_count):
        for m in re.findall(r'TOCM([A-Z0-9]+)TOCM', d[i].get_text()):
            if m not in pages: pages[m]=i+1
    d.close(); return pages

def build_contents(pages):
    rows=['<div class="toc-head">Contents</div>',
          '<p class="toc-note">Every entry maps to its page in this blended edition. Page numbers are generated automatically.</p>']
    for lvl,label,mk in TOC:
        real = mk if mk in pages else next((k for k in pages if k.startswith(mk)), mk)
        pg=pages.get(real,'')
        cls={0:'toc-part',1:'toc-l1',2:'toc-l2'}[lvl]
        rows.append(f'<a class="{cls} toc-link" href="#sec-{real}"><span class="toc-label">{label}</span><span class="toc-dots"></span><span class="toc-pg">{pg}</span></a>')
    return '\n'.join(rows)

if __name__=='__main__':
    print('pass 1: assemble + render to locate sections...')
    assemble('')
    subprocess.run([sys.executable,'render.py','full_manual.html','full_manual.pdf'],cwd=HERE,check=True)
    pages=marker_pages(os.path.join(HERE,'full_manual.pdf'))
    print(f'located {len(pages)} section markers')
    toc=build_contents(pages)
    print('pass 2: assemble with Contents + render...')
    assemble(toc)
    subprocess.run([sys.executable,'render.py','full_manual.html','full_manual.pdf'],cwd=HERE,check=True)
    # re-check stability (page numbers may shift by contents length)
    pages2=marker_pages(os.path.join(HERE,'full_manual.pdf'))
    if pages2!=pages:
        print('page numbers shifted; final pass...')
        assemble(build_contents(pages2))
        subprocess.run([sys.executable,'render.py','full_manual.html','full_manual.pdf'],cwd=HERE,check=True)
    # convert Contents named-destination links to explicit GoTo (universal compatibility)
    fp=os.path.join(HERE,'full_manual.pdf')
    d=fitz.open(fp); conv=0
    for i in range(min(4,d.page_count)):
        for lk in d[i].get_links():
            if lk.get('kind')==fitz.LINK_NAMED and lk.get('page',-1)>=0:
                tgt=lk['page']; d[i].delete_link(lk)
                d[i].insert_link({'kind':fitz.LINK_GOTO,'from':lk['from'],'page':tgt,'to':lk.get('to',fitz.Point(0,0))})
                conv+=1
    d.saveIncr(); print('converted',conv,'contents links to GoTo')
    # strip invisible section-marker text from the text layer (keeps layout/links intact)
    d=fitz.open(fp); removed=0
    for page in d:
        rects=[]
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines',[]):
                for s in l.get('spans',[]):
                    if 'TOCM' in s.get('text',''): rects.append(fitz.Rect(s['bbox']))
        for r in rects: page.add_redact_annot(r, fill=None)
        if rects:
            page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                                  graphics=fitz.PDF_REDACT_LINE_ART_NONE)
            removed+=len(rects)
    print('stripped',removed,'invisible markers')
    # swap in the real (non-image, footer-free) cover, updated for Module 5
    covpdf=os.path.join(HERE,'cover.pdf')
    if not os.path.exists(covpdf):
        subprocess.run([sys.executable, os.path.join(HERE,'render.py'),
                        os.path.join(HERE,'cover.html'), covpdf, 'nofooter'], check=True)
    cov=fitz.open(covpdf)
    d.delete_page(0)
    d.insert_pdf(cov, from_page=0, to_page=0, start_at=0)
    print('swapped in new cover (page 1)')
    d.save(os.path.join(HERE,'full_manual_clean.pdf'), garbage=4, deflate=True)
    d=fitz.open(os.path.join(HERE,'full_manual_clean.pdf'))
    print('DONE. pages:', d.page_count)
