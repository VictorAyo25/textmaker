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
print('=== END QA ===')
