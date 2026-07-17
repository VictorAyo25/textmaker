"""Layout QA over the finished PDF: look at every page, not a sample.

    cd build && python qa_layout.py [CSC241_checkpoint.pdf]

Hard failures (these stop a release):
  * text outside the content box, on any side
  * anything in the bottom margin that is not the running footer

Advisory (printed for a human to look at):
  * pages holding very little, reported with the space left on them and the size
    of the block that follows, because that is what decides whether the gap is a
    fault or physics. A box is never split, so a page ends early whenever the
    next box is taller than the room left. That is the price of never breaking a
    worked example across a page, and it is worth paying. A short page whose
    successor WOULD have fit is the real defect, and the numbers here show which
    it is at a glance.

The running footer lives in the bottom margin by design, so it has to be
excluded by identity rather than by position. An early version of this check did
not, decided the footer was overflowing text, and reported every page in the
book as broken, which is the same as reporting nothing.
"""
import re, sys

import fitz

MM = 2.834645          # pt per mm, and the render margins from render.py
LEFT, RIGHT, TOP, BOTTOM = 18 * MM, 18 * MM, 19 * MM, 16 * MM
SLACK = 2.0            # pt: glyph bboxes sit a hair proud of the text edge

FOOTER_TEXT = 'CSC241'
SPARSE = 0.30          # fraction of the content height below which a page is odd


def spans(page):
    for b in page.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            for s in l.get('spans', []):
                if s.get('text', '').strip():
                    yield s


def is_footer(s, page):
    """The running footer: the course line, or the page number beside it."""
    if s['bbox'][1] < page.rect.y1 - BOTTOM:
        return False
    t = s['text'].strip()
    return t.startswith(FOOTER_TEXT) or re.fullmatch(r'\d+', t) is not None


def forced_starts(doc):
    """Physical pages a section is required to begin on.

    Read from the Contents links, which assemble.py has already checked row by
    row against the anchor each one names. A page sitting before one of these is
    short because the next section demanded a fresh page, not because anything
    is wrong.
    """
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from contents import TOC, forced_ids, mkid

    targets = []
    for i in range(doc.page_count):
        got = [lk for lk in doc[i].get_links() if lk.get('kind') == fitz.LINK_GOTO]
        got.sort(key=lambda lk: (round(lk['from'].y0, 1), lk['from'].x0))
        targets += [lk['page'] for lk in got]
    if len(targets) != len(TOC):
        print(f'  ! {len(targets)} Contents links for {len(TOC)} rows: cannot tell which '
              f'pages are section starts, so every short page is reported below')
        return frozenset()
    forced = forced_ids()
    return frozenset(p for p, (lvl, lbl, k, t) in zip(targets, TOC)
                     if mkid(k, t) in forced)


def first_block(page):
    """Height of the topmost drawn box on the page, if it has one.

    Every teaching box paints a background, so this is what the page below had to
    make room for.
    """
    rects = [d['rect'] for d in page.get_drawings() if d['rect'].height > 20]
    return min(rects, key=lambda r: r.y0).height if rects else None


def check(pdf_path):
    doc = fitz.open(pdf_path)
    fails, sparse = [], []
    forced = forced_starts(doc)

    for i in range(doc.page_count):
        page = doc[i]
        if i == 0:
            continue           # the cover is full bleed: it has no content box
        r = page.rect
        box = fitz.Rect(LEFT, TOP, r.x1 - RIGHT, r.y1 - BOTTOM)
        body = [s for s in spans(page) if not is_footer(s, page)]
        if not body:
            sparse.append((i, 'no text at all'))
            continue

        for s in body:
            x0, y0, x1, y1 = s['bbox']
            t = s['text'].strip()[:40]
            if x1 > box.x1 + SLACK:
                fails.append(f'page {i}: text runs {x1 - box.x1:.1f}pt past the right '
                             f'margin: {t!r}')
            if x0 < box.x0 - SLACK:
                fails.append(f'page {i}: text starts {box.x0 - x0:.1f}pt left of the '
                             f'margin: {t!r}')
            if y1 > box.y1 + SLACK:
                fails.append(f'page {i}: text sits {y1 - box.y1:.1f}pt below the content '
                             f'area, in the footer margin: {t!r}')
            if y0 < box.y0 - SLACK:
                fails.append(f'page {i}: text sits {box.y0 - y0:.1f}pt above the content '
                             f'area: {t!r}')

        top, bot = min(s['bbox'][1] for s in body), max(s['bbox'][3] for s in body)
        if (bot - top) >= SPARSE * box.height:
            continue
        free = box.y1 - bot
        nxt = first_block(doc[i + 1]) if i + 1 < doc.page_count else None
        if i + 1 in forced:
            continue                    # the next section must start on a fresh page
        if i + 1 == doc.page_count:
            continue                    # the last page of the book ends where it ends
        if nxt is not None and nxt > free:
            continue                    # the next block could not fit: nothing to fix
        why = (f'{free:.0f}pt free and the next block is '
               + (f'only {nxt:.0f}pt, so it should have fit' if nxt else 'not a box')
               + '. Look at this one.')
        sparse.append((i, f'text covers {(bot - top) / box.height:.0%}, {why}'))

    pages = doc.page_count
    doc.close()

    print(f'LAYOUT QA: {pages} pages examined')
    if fails:
        print('LAYOUT QA: FAIL')
        for f in fails:
            print('  x ' + f)
    else:
        print('  . no text outside the content box on any page')
        print('  . nothing in the bottom margin but the running footer')
    if sparse:
        print(f'  ? {len(sparse)} short pages that a forced break or an oversized next '
              f'block does not explain:')
        for i, why in sparse:
            print(f'      page {i}: {why}')
    else:
        print('  . every short page is accounted for: a section that must start fresh, '
              'or a next block too tall to fit')
    return not fails


if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else 'CSC241_checkpoint.pdf'
    sys.exit(0 if check(src) else 1)
