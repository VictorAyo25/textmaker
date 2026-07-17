"""assemble.py — build the COS221 study manual.

    python assemble.py            # -> build/full_manual_clean.pdf

This course is AUTHORED, not rebuilt. PHY121 had a prior manual of ours to
reproduce verbatim, so its assembler carried a structure-aware PDF extractor and
a word-level fidelity audit. The only manual here belongs to someone else and is
a *source*, so none of that machinery exists: content/*.html IS the manual, hand
written, and this file only stitches, paginates and links it.

What it does:
  1. concatenates content/*.html in ORDER;
  2. injects an invisible marker before every part and section heading;
  3. renders, reads back which page each marker landed on, rebuilds the Contents
     with real page numbers, and re-renders until pagination stops moving
     (the Contents changes the pagination it is describing);
  4. converts the Contents' named destinations to explicit GoTo links, because
     many viewers ignore named ones;
  5. redacts the marker text out of the text layer;
  6. swaps in the footer-free cover.

The Contents is DERIVED from the headings, never hand-listed: a hand-kept list
silently drifts from the content it claims to describe.
"""
import fitz, io, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

# Reading order. Each name is content/<name>.html.
ORDER = [
    'howto',
    'part_foundations', 'foundations',
    'part_m1', 'module1',
    'part_m2', 'module2',
    'part_m3', 'module3',
]

TITLE = 'COS221 · Computer Programming I (Java) · Study Manual'


def load(name):
    p = os.path.join(CONTENT, name + '.html')
    if not os.path.exists(p):
        raise SystemExit(f'missing content file: {p}')
    return io.open(p, encoding='utf-8').read()


def slug(text):
    """A stable marker id from a heading. Must survive PDF text extraction, so
    letters and digits only (punctuation and spacing are not reliably preserved)."""
    return re.sub(r'[^A-Za-z0-9]', '', text).upper()[:40]


def strip_tags(html):
    return re.sub(r'<[^>]+>', '', html).strip()


TOC = []   # (level, label, marker) in document order, rebuilt on every assemble


def mark(html):
    """Inject an invisible marker before each part divider and each section kick,
    recording the Contents entry as we go."""
    def part_sub(m):
        label = strip_tags(m.group('h1'))
        mk = slug(label)
        TOC.append((0, label, mk))
        return (f'{m.group("open")}<span class="tocm" id="sec-{mk}">TOCM{mk}TOCM</span>'
                f'{m.group("mid")}{m.group("h1full")}')

    # <div class="part"> ... <div class="kicker">Part I</div> <h1>Foundations</h1>
    html = re.sub(
        r'(?P<open><div class="part[^"]*">)(?P<mid>\s*(?:<div class="kicker">[^<]*</div>\s*)?)'
        r'(?P<h1full><h1[^>]*>(?P<h1>.*?)</h1>)',
        part_sub, html, flags=re.S)

    def kick_sub(m):
        label = strip_tags(m.group('kick'))
        mk = slug(label)
        TOC.append((1, label, mk))
        return f'<span class="tocm" id="sec-{mk}">TOCM{mk}TOCM</span>{m.group(0)}'

    html = re.sub(r'<div class="kick">(?P<kick>[^<]+)</div>', kick_sub, html)
    return html


def assemble(contents_html=''):
    del TOC[:]
    # A placeholder page 1, replaced by cover.pdf at the very end.
    #
    # It must exist during the render, not just at the end. Chromium numbers the
    # pages it renders; if the cover were only spliced in afterwards, every body
    # page would shift down by one and its printed footer would be one less than
    # the page it sits on, with the Contents off by one to match. Rendering a slot
    # means the body is numbered from 2 from the start, and swapping page 1 for the
    # cover afterwards changes nothing else.
    body = ['<div class="coverslot"></div>',
            f'<div class="contents-page">{contents_html}</div>']
    for name in ORDER:
        body.append(mark(load(name)))
    html = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>{TITLE}</title>'
            '<link rel="stylesheet" href="manual.css"></head><body>'
            + '\n'.join(body) + '</body></html>')
    io.open(os.path.join(HERE, 'full_manual.html'), 'w', encoding='utf-8').write(html)
    return html


def marker_pages(pdfpath):
    d = fitz.open(pdfpath)
    pages = {}
    for i in range(d.page_count):
        for m in re.findall(r'TOCM([A-Z0-9]+)TOCM', d[i].get_text()):
            if m not in pages:
                pages[m] = i + 1
    d.close()
    return pages


def build_contents(pages, entries):
    rows = ['<div class="toc-head">Contents</div>',
            '<p class="toc-note">Page numbers are generated from the rendered book, '
            'not typed by hand. Every line below is a link.</p>']
    for lvl, label, mk in entries:
        # exact, then prefix: a real marker can carry a suffix the label does not
        real = mk if mk in pages else next((k for k in pages if k.startswith(mk)), mk)
        pg = pages.get(real, '')
        cls = {0: 'toc-part', 1: 'toc-l1', 2: 'toc-l2'}[lvl]
        rows.append(f'<a class="{cls} toc-link" href="#sec-{real}">'
                    f'<span class="toc-label">{label}</span>'
                    f'<span class="toc-dots"></span>'
                    f'<span class="toc-pg">{pg}</span></a>')
    return '\n'.join(rows)


def render(src, out, mode=None):
    cmd = [sys.executable, 'render.py', src, out] + ([mode] if mode else [])
    subprocess.run(cmd, cwd=HERE, check=True)


if __name__ == '__main__':
    from buildlock import build_lock
    with build_lock('assemble.py'):
        fp = os.path.join(HERE, 'full_manual.pdf')

        print('pass 1: assemble + render to locate sections...')
        assemble('')
        entries = list(TOC)
        render('full_manual.html', 'full_manual.pdf')
        pages = marker_pages(fp)
        print(f'located {len(pages)} section markers ({len(entries)} contents entries)')
        missing = [(l, m) for _, l, m in entries if m not in pages
                   and not any(k.startswith(m) for k in pages)]
        if missing:
            raise SystemExit(f'unresolved contents entries: {missing}')

        print('pass 2: assemble with Contents + render...')
        assemble(build_contents(pages, entries))
        entries = list(TOC)
        render('full_manual.html', 'full_manual.pdf')

        # the Contents changes the pagination it describes: iterate to a fixed point
        for _ in range(4):
            pages2 = marker_pages(fp)
            if pages2 == pages:
                break
            print('page numbers shifted; re-paginating...')
            pages = pages2
            assemble(build_contents(pages, entries))
            entries = list(TOC)
            render('full_manual.html', 'full_manual.pdf')
        else:
            raise SystemExit('pagination did not settle after 4 passes')

        # Chromium emits NAMED destinations; many viewers ignore them.
        d = fitz.open(fp)
        conv = 0
        for i in range(min(6, d.page_count)):
            for lk in d[i].get_links():
                if lk.get('kind') == fitz.LINK_NAMED and lk.get('page', -1) >= 0:
                    tgt = lk['page']
                    d[i].delete_link(lk)
                    d[i].insert_link({'kind': fitz.LINK_GOTO, 'from': lk['from'],
                                      'page': tgt, 'to': lk.get('to', fitz.Point(0, 0))})
                    conv += 1
        d.saveIncr()
        print('converted', conv, 'contents links to GoTo')

        # strip the invisible markers out of the text layer
        d = fitz.open(fp)
        removed = 0
        for page in d:
            rects = []
            for b in page.get_text('dict')['blocks']:
                for l in b.get('lines', []):
                    for s in l.get('spans', []):
                        if 'TOCM' in s.get('text', ''):
                            rects.append(fitz.Rect(s['bbox']))
            for r in rects:
                page.add_redact_annot(r, fill=None)
            if rects:
                page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE,
                                      graphics=fitz.PDF_REDACT_LINE_ART_NONE)
                removed += len(rects)
        print('stripped', removed, 'invisible markers')

        # cover: rendered without the running footer, then swapped INTO the slot
        covpdf = os.path.join(HERE, 'cover.pdf')
        render('cover.html', 'cover.pdf', 'nofooter')
        cov = fitz.open(covpdf)
        d.delete_page(0)                                    # the empty slot
        d.insert_pdf(cov, from_page=0, to_page=0, start_at=0)
        print('swapped cover into page 1')

        out = os.path.join(HERE, 'full_manual_clean.pdf')
        d.save(out, garbage=4, deflate=True)
        print('DONE. pages:', fitz.open(out).page_count, '->', out)
