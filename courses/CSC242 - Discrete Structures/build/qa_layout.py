"""Layout QA over the finished PDF: look at every page, not a sample.

    cd build && python qa_layout.py [CSC241_checkpoint.pdf]

Hard failures (these stop a release):
  * text outside the content box, on any side
  * anything in the bottom margin that is not the running footer
  * a box cut in half by a page break when it would have fit whole on the next
    page. A box is one idea, and half an idea either side of a page turn is not
    the grammar this manual is built on. A box genuinely taller than a page has
    to be cut and is not counted.
  * a code line that runs out past the panel drawn around it. Staying inside the
    page margins is not enough: code sits in a teaching box, which is narrower
    than the page, so a line can clear every margin and still hang over the box.
  * a body that did not render at its designed size, which means Chromium shrank
    the whole document to fit something too wide. gates.py catches the usual
    cause (an over-long code line) precisely and early; this catches the effect
    whatever the cause, and it is the check that matters, because a shrunk book
    has nothing overflowing and looks perfect to every other test here.

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

FOOTER_TEXT = 'CSC242'
SPARSE = 0.30          # fraction of the content height below which a page is odd
BODY_PT = 10.5         # the body size manual.css asks for
BODY_TOL = 0.02        # pt: allow rounding, nothing more
HEAD_BAND = 45         # pt: how far above a box a heading welded to it can sit
BLOCK_GAP = 6          # pt: the margin between two boxes (.55em), which the next
                       # block also needs and which no rectangle shows


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


def welded_top(page, rects):
    """Where the topmost block really begins, heading included.

    manual.css gives every heading `break-after: avoid`, so a heading and the box
    under it travel to a new page as one piece. Measuring the box alone and asking
    "would it have fitted in the room left on the page before" answers a question
    the renderer never faced: it had to place the heading too, and a heading is
    22pt of this book's page. Two short pages were reported for exactly that
    reason, and both turned out to be correct typesetting.

    Only text within HEAD_BAND of the box counts. Text further up is a paragraph,
    and a paragraph may be split across the page turn, so it is welded to nothing
    and the page before could always have taken part of it.
    """
    body = [s for s in spans(page) if not is_footer(s, page)]
    if not body:
        return rects[0].y0
    top = min(s['bbox'][1] for s in body)
    return top if rects[0].y0 - HEAD_BAND <= top < rects[0].y0 else rects[0].y0


def first_block(page):
    """Height of the whole topmost block on the page, if it has one.

    Every teaching box paints a background, so this is what the page above had to
    make room for. Walk down from the topmost rectangle while they keep touching,
    so the answer is the box entire (bar, body and border) and not one part of it,
    and start from any heading welded above it.
    """
    rects = sorted([d['rect'] for d in page.get_drawings() if d['rect'].height > 3],
                   key=lambda r: r.y0)
    if not rects:
        return None
    top, bottom = welded_top(page, rects), rects[0].y1
    for r in rects[1:]:
        if r.y0 > bottom + 3:      # a real gap: the next block is a separate one
            break
        bottom = max(bottom, r.y1)
    return bottom - top


def looks_like_a_bar(rect, wide):
    """True when this rect is a box's coloured header strip, not a continuation.

    A box paints its bar flush against the top of its body, so a bar always has
    another full-width rect beginning exactly where it ends. A fragment carried
    over from the page before has no bar: it opens straight into body, and the
    next rect beneath it is a different box, a margin away.

    Without this test, a page that merely ENDS with a box, followed by a page that
    merely BEGINS with one, reads as a single box cut in half. That is how body
    page 64 came to be reported: a gap chip closing 1pt clear of the bottom
    margin, and an unrelated teaching box opening the page after it.
    """
    return any(abs(o.y0 - rect.y1) < 1.5 for o in wide if o is not rect)


def lead_above(page, boxtop):
    """Height of the heading welded above a box, or 0 when there is none."""
    body = [s for s in spans(page) if not is_footer(s, page)]
    tops = [s['bbox'][1] for s in body
            if s['bbox'][3] <= boxtop + 1 and s['bbox'][1] >= boxtop - HEAD_BAND]
    return boxtop - min(tops) if tops else 0.0


def split_boxes(doc):
    """Boxes cut by a page break, with the height they would have needed whole.

    A box that runs off the bottom of one page and resumes at the top of the next
    was cut. If the two halves together would have fitted on a page, the cut was
    avoidable and the box should have moved down entire.

    "Together" includes the heading welded above the box, for the reason
    welded_top gives: the renderer could only have moved the box by moving its
    heading with it. The two 735pt answer boxes in this book clear the usable
    743pt on their own and do not clear it once their headings come along, so
    those splits are forced, and reporting them told the author to fix something
    that cannot be fixed.
    """
    out = []
    for i in range(doc.page_count - 1):
        r = doc[i].rect
        bot, top = r.y1 - BOTTOM, TOP
        wide = [d['rect'] for d in doc[i].get_drawings()
                if d['rect'].width > 400 and d['rect'].height > 8]
        tail = [x for x in wide if x.y1 > bot - 1.5]
        if not tail:
            continue
        nxt_wide = [d['rect'] for d in doc[i + 1].get_drawings()
                    if d['rect'].width > 400 and d['rect'].height > 8]
        head = [x for x in nxt_wide
                if x.y0 < top + 1.5 and not looks_like_a_bar(x, nxt_wide)]
        if not head:
            continue
        tallest = max(tail, key=lambda x: x.height)
        boxtop, moved = tallest.y0, True
        while moved:                      # climb to the top of this box's own run
            moved = False
            for o in wide:
                if o.y0 < boxtop and abs(o.y1 - boxtop) < 1.5:
                    boxtop, moved = o.y0, True
        whole = (tallest.height + max(x.height for x in head)
                 + lead_above(doc[i], boxtop))
        out.append((i, whole, whole <= (r.y1 - BOTTOM - TOP)))
    return out


def panel_overruns(doc):
    """Code lines that run out past the panel drawn around them.

    gates.py caps code at a column count, but that is a proxy standing in for
    this: the real rule is that code must not outrun its own box. The column cap
    was set by measuring against the PAGE, and almost all code sits inside a
    teaching box, which is about 20pt narrower. Two lines cleared the page,
    stayed inside every margin, and still hung over the panel edge. Every check
    here passed them, because none of them was looking at the box.

    A line is matched to the innermost rectangle that vertically contains it and
    starts to its left. Narrow rectangles are ignored: an inline highlight sits
    behind a word or two, and picking one as the container reports a 1-character
    line overflowing by 150pt, which is how the first version of this read.
    """
    out = []
    for i in range(1, doc.page_count):
        page = doc[i]
        panels = [d['rect'] for d in page.get_drawings()
                  if d['rect'].width > 300 and d['rect'].height > 5]
        for b in page.get_text('dict')['blocks']:
            for l in b.get('lines', []):
                sp = [s for s in l.get('spans', []) if s['text'].strip()]
                if not sp or not all('Mono' in s['font'] for s in sp):
                    continue
                y = (sp[0]['bbox'][1] + sp[0]['bbox'][3]) / 2
                x0 = min(s['bbox'][0] for s in sp)
                x1 = max(s['bbox'][2] for s in sp)
                encl = [r for r in panels if r.y0 <= y <= r.y1 and r.x0 <= x0 - 4]
                if not encl:
                    continue
                panel = min(encl, key=lambda r: r.width)
                if x1 > panel.x1 + 0.5:
                    txt = ''.join(s['text'] for s in sp).strip()
                    out.append((i, x1 - panel.x1, len(txt), txt))
    return out


def content_bottom(page, body):
    """How far down the page anything reaches: text, or the box drawn around it.

    A box extends below its last line by its padding, border and margin, so
    measuring the gap from the text alone overstates the room left by a good
    15pt and reports a block that missed by a hair as one that should have fit.
    """
    text = max(s['bbox'][3] for s in body)
    drawn = max((d['rect'].y1 for d in page.get_drawings()), default=0)
    return max(text, drawn)


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

        top, bot = min(s['bbox'][1] for s in body), content_bottom(page, body)
        if (bot - top) >= SPARSE * box.height:
            continue
        free = box.y1 - bot - BLOCK_GAP
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

    for i, whole, avoidable in split_boxes(doc):
        if avoidable:
            fails.append(f'page {i}: a box is cut by the page break, and at {whole:.0f}pt '
                         f'with its heading it would have fitted whole on the '
                         f'next page')

    for i, over, n, txt in panel_overruns(doc):
        fails.append(f'page {i}: a {n}-character code line hangs {over:.1f}pt past the '
                     f'panel drawn around it: {txt[:56]!r}')

    # The body is set in DejaVu Serif at BODY_PT. If it came back smaller, every
    # page was scaled and the size the manual was designed at is not the size it
    # prints at.
    #
    # MEASURE THE MODE, NOT THE MAXIMUM. An earlier version took max() over serif
    # spans and compared it with `< BODY_PT`. Two things were wrong with that.
    # The font test `endswith('DejaVuSerif')` excludes DejaVuSerif-Bold and
    # -Italic, so the maximum landed on whichever incidental non-bold serif run
    # happened to be largest, at one point a figure label at 15.56pt, and the
    # gate cheerfully reported that as "the body". Worse, any value at or above
    # BODY_PT passed, so a book shrunk to 92.9% (the COS221 failure) would still
    # have shown a 14.5pt maximum and sailed through. The size that covers the
    # most characters IS the body, and it is compared in BOTH directions: too
    # large means the stylesheet changed without this gate being told.
    weight = {}
    for i in range(1, doc.page_count):
        for s in spans(doc[i]):
            if 'DejaVuSerif' in s['font'] and 'Bold' not in s['font'] \
                    and 'Italic' not in s['font']:
                weight[round(s['size'], 2)] = (weight.get(round(s['size'], 2), 0)
                                               + len(s['text']))
    if not weight:
        body = None
        fails.append('no body text found: cannot tell whether the page was scaled')
    else:
        body = max(weight, key=weight.get)
        share = weight[body] / sum(weight.values())
        if body < BODY_PT - BODY_TOL:
            fails.append(f'the body rendered at {body:.2f}pt, not {BODY_PT}pt: Chromium '
                         f'shrank every page to {body / BODY_PT:.1%} to fit something too '
                         f'wide. Run gates.py: it names the line.')
        elif body > BODY_PT + BODY_TOL:
            fails.append(f'the body rendered at {body:.2f}pt, larger than the '
                         f'{BODY_PT}pt manual.css asks for. The stylesheet and this '
                         f'gate disagree; one of them is out of date.')
        elif share < 0.30:
            fails.append(f'the most common body size covers only {share:.0%} of the '
                         f'running text, so "the body size" is not well defined and '
                         f'this check is not measuring what it claims to.')

    pages = doc.page_count
    doc.close()

    print(f'LAYOUT QA: {pages} pages examined')
    if body and abs(body - BODY_PT) <= BODY_TOL:
        print(f'  . body renders at {body:.2f}pt across {weight[body]} characters, '
              f'its designed size: nothing was scaled')
    if fails:
        print('LAYOUT QA: FAIL')
        for f in fails:
            print('  x ' + f)
    else:
        print('  . no text outside the content box on any page')
        print('  . nothing in the bottom margin but the running footer')
        print('  . no box cut by a page break that could have fitted whole')
        print('  . no code line hanging past the panel drawn around it')
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
    src = sys.argv[1] if len(sys.argv) > 1 else 'CSC242_checkpoint.pdf'
    sys.exit(0 if check(src) else 1)
