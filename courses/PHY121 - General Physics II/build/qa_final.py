# Final QA of the assembled full_manual.pdf + full_manual.html
import fitz, io, os, re
HERE=os.path.dirname(os.path.abspath(__file__))
pdf=os.path.join(HERE,'full_manual.pdf')
d=fitz.open(pdf)
N=d.page_count
print(f'=== FULL MANUAL QA ===\npages: {N}')

# 1. blank pages
blanks=[]
for i in range(N):
    pg=d[i]; t=re.sub(r'PHY121.*Ayodeji','',pg.get_text()).strip()
    if not pg.get_images() and len(t)<40 and len(pg.get_drawings())<8: blanks.append(i+1)
print('near-blank pages:', blanks if blanks else 'NONE')

# 2. footers sequential
bad_footer=[]
for i in range(N):
    t=d[i].get_text()
    m=re.search(r'General Physics II . Victor Ayodeji\s*\n?\s*(\d+)', t)
    num=int(m.group(1)) if m else None
    if num!=i+1: bad_footer.append((i+1,num))
print('footer mismatches:', bad_footer[:10] if bad_footer else 'NONE (all sequential)')

# 3. dashes + banned terms in HTML (source of truth for text sections)
html=io.open(os.path.join(HERE,'full_manual.html'),encoding='utf-8').read()
# strip base64 image data (crops) to only check real text
html_text=re.sub(r'data:image/png;base64,[A-Za-z0-9+/=]+','',html)
em=html_text.count(chr(0x2014)); en=html_text.count(chr(0x2013))
print(f'em-dashes in HTML text: {em}  en-dashes: {en}')
for term in ['stroud','covenant','ccodel']:
    c=len(re.findall(term, html_text, re.I))
    print(f'  \"{term}\" in HTML text: {c}')

# 4. Contents present with page numbers
toc_pg=d[1].get_text()+d[2].get_text() if N>2 else ''
import re as _re
nums=_re.findall(r'\b(1?\d{1,2})\b', toc_pg)
# case-insensitive: the TOC is uppercased by CSS, so the text layer holds "FOUNDATIONS"
_toc=toc_pg.upper()
print('Contents pages 2-3 have', toc_pg.count('.'), 'dots-ish; sample entries present:',
      'FOUNDATIONS' in _toc, 'MAXWELL' in _toc, 'GLOSSARY' in _toc)

# 5. rendered text banned terms across whole doc
alltext=''.join(d[i].get_text() for i in range(N))
for term in ['stroud','covenant university','ccodel']:
    print(f'rendered \"{term}\":', alltext.lower().count(term))
print('rendered em/en dashes:', alltext.count(chr(0x2014)), alltext.count(chr(0x2013)))

# 6. structural gates. A text diff is blind to formatting, drawn elements and
# block order, so every one of these defects once passed a "byte-identical" check.
# A count collapsing to zero means a detector broke, not that the manual changed.
import glob, io
CONTENT = os.path.join(HERE, 'content')
src = ' '.join(io.open(f, encoding='utf-8').read() for f in glob.glob(os.path.join(CONTENT, '*.html')))
# Floors sit just under the observed counts: high enough that a detector going
# dark trips them, loose enough that ordinary editing does not.
# blank=100 is exact and deliberate. The original has 108 blank-shaped rects, but
# 8 of those are the decorative rule on the 8 part-divider pages, which
# divider_html draws itself. 100 is the true number of fill-in blanks.
# tablefig=13, not 14: two back-matter answer keys used to print twice, once as a
# cropped image and again as a real table underneath, because the box was assumed
# to run to the next bar. box_end() ended that, and with it the duplicate crops.
FLOOR = {'<b>': 1100, '<sub>': 480, '<sup>': 750, 'class="blank"': 100,
         '<li>': 560, 'class="sub"': 30, '<table': 15, 'tablefig': 13,
         # every worked example and solved question carries a Shortcut, bar the one
         # multi-question answer-key box: 130 today, floor a little under
         'class="shortcut"': 128}
print('--- structural counts (floor):')
# shortcuts are injected at assemble time and live in the ASSEMBLED html, plus the
# authored tutorial and module5, not in the frozen content/ files; count them there
assembled = io.open(os.path.join(HERE, 'full_manual.html'), encoding='utf-8').read()
bad = 0
for k, floor in FLOOR.items():
    n = (assembled if k == 'class="shortcut"' else src).count(k)
    ok = n >= floor
    bad += 0 if ok else 1
    print(f'    {k:16s} {n:5d}  (>= {floor})  {"" if ok else "<-- BELOW FLOOR"}')

# doubled list markers: an <li> whose text still opens with its own marker
dbl = [m for m in re.findall(r'<li>(.{0,40})', src)
       if re.match(r'^\s*(?:<[^>]+>\s*)*\s*(?:\d+\.\s|[▸•▪])', m)]
# a paragraph broken across a hyphen, and any surviving soft hyphen
split = re.findall(r'[a-z]‐</p>', src)
soft = re.findall('‐', re.sub(r'<[^>]+>', '', src))
print('doubled list markers:', len(dbl), '| mid-word paragraph splits:', len(split),
      '| stray soft hyphens:', len(soft))
bad += (len(dbl) > 0) + (len(split) > 0) + (len(soft) > 0)

# A truncated render is the failure that hides best: when the images had not
# decoded the manual came out 64 pages instead of 148, and every other gate still
# passed (footers were sequential, no page was blank). Page count is the only
# thing that catches it.
PAGE_FLOOR = 140
print(f'page count: {N} (floor {PAGE_FLOOR})', '' if N >= PAGE_FLOOR else '<-- TRUNCATED RENDER')
bad += (N < PAGE_FLOOR)
print('STRUCTURAL GATES:', 'PASS' if bad == 0 else f'FAIL ({bad})')
print('=== END QA ===')
