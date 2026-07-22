"""Assemble the CSC242 manual from content/*.html, then render to PDF.

    cd build && python assemble.py            # full build
    cd build && python assemble.py --no-pdf   # HTML only, skip Chromium

The cover is full bleed and carries no running footer, so it is rendered as its
own PDF and merged in front of the body. The body carries the footer and page
numbers.

The Contents cannot be written until the book has been rendered, so the body is
rendered repeatedly until the numbers it prints match the book it prints them
for. See contents.py.

The gates are not advisory: a violation stops the build, and nothing reaches the
merged PDF without passing them. See gates.py and verify_code.py.
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
sys.path.insert(0, HERE)

from contents import (ANCHOR, TOC, build_contents, check_toc, heading_text,
                      inject_anchors, link_pages, mkid)

COVER = 'cover.html'
# BODY_PARTS grows as units are authored; it must stay in sync with contents.TOC
# (every heading needs a Contents row and vice versa, or the build stops).
BODY_PARTS = [
    'front.html', 'foundations.html', 'foundations_f2.html', 'p1_logic.html',
    'p1_12.html', 'p1_13.html', 'p1_14.html', 'p1_15.html', 'p2_sets.html',
    'p2_22.html', 'p2_23.html', 'p3_relations.html', 'p3_32.html',
    'p3_33.html', 'p3_34.html', 'p4_functions.html', 'p4_42.html',
    'p4_43.html', 'p5_counting.html', 'p5_52.html', 'p5_53.html',
    'p5_54.html', 'p6_graphs.html', 'p6_62.html', 'p6_63.html', 'p6_64.html',
    'p6_65.html', 'p6_66.html', 'p6_67.html', 'p6_68.html', 'p7_trees.html',
    'p7_72.html', 'p7_73.html', 'p8_boolean.html', 'p9_proof.html',
    'p9_92.html', 'p9_93.html', 'p9_94.html', 'p10_stats.html',
    'p10_102.html', 'p11_cpp.html', 'p11_112.html', 'reference.html',
    'reference_r2.html', 'reference_r3.html', 'papers.html',
    'paper_2425.html', 'paper_2324.html', 'paper_2122.html',
    'paper_2021.html', 'mock1.html', 'mock1_answers.html', 'mock2.html',
    'mock2_answers.html', 'mock3.html', 'mock3_answers.html']
MAX_PASSES = 5

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CSC242 - Discrete Structures - Study Manual</title>
<link rel="stylesheet" href="manual.css">
</head>
<body>
"""
TAIL = "\n</body>\n</html>\n"

# The cover is one full-bleed page: kill the page margin for that render only.
COVER_HEAD = HEAD.replace('</head>',
    '<style>@page{ size:A4; margin:0; } body{ margin:0; }</style>\n</head>')


def read(name):
    with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
        return f'<!-- ===== {name} ===== -->\n' + fh.read()


def write(path, text):
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(text)


def render(src_html, out_pdf, mode=None):
    cmd = [sys.executable, os.path.join(HERE, 'render.py'), src_html, out_pdf]
    if mode:
        cmd.append(mode)
    subprocess.run(cmd, check=True)


def stop(msg, detail=()):
    print('\nBUILD STOPPED: ' + msg, file=sys.stderr)
    for d in detail:
        print('  x ' + d, file=sys.stderr)
    sys.exit(1)


def build_body(contents_html):
    """The whole book as one HTML: Contents first, then content, anchors in."""
    marked, found = inject_anchors('\n'.join(read(p) for p in BODY_PARTS))
    problems = check_toc(found)
    if problems:
        stop('the Contents and the book disagree.', problems)
    return HEAD + contents_html + marked + TAIL


def number_the_book(body_path, body_pdf):
    """Render until the Contents prints the page numbers the book actually has.

    Pass one prints no numbers at all, so inserting them can push a section over
    a page boundary and change the answer. Repeat until a render agrees with the
    Contents it was built from.
    """
    pages = None
    for attempt in range(1, MAX_PASSES + 1):
        print(f'pass {attempt}: ' + ('locating sections' if pages is None
                                     else 'rebuilding Contents'))
        body_html = build_body(build_contents(pages))
        write(body_path, body_html)
        render(body_path, body_pdf)
        actual = link_pages(body_pdf)
        if actual == pages:
            print(f'  page numbers settled after {attempt} passes')
            return body_html, pages
        pages = actual
    stop(f'the Contents page numbers did not settle in {MAX_PASSES} passes.')


def footer_number(page):
    """The page number the reader sees, read out of the running footer."""
    import fitz
    r = page.rect
    text = page.get_textbox(fitz.Rect(r.x0, r.y1 - 42, r.x1, r.y1))
    nums = re.findall(r'\b(\d+)\b', text)
    return int(nums[-1]) if nums else None


def contents_links(doc, named):
    """Every Contents link in the document, as (source page, target page, id).

    Before the merge the links still carry the anchor they name, so a row is tied
    to its section by name. After it they are plain page links and the id is None.
    """
    import fitz
    out = []
    for i in range(doc.page_count):
        for lk in doc[i].get_links():
            name = lk.get('nameddest') or ''
            if named:
                if not name.startswith(ANCHOR) or lk.get('page', -1) < 0:
                    continue
                out.append((i, lk['page'], name[len(ANCHOR):], lk['from']))
            elif lk.get('kind') == fitz.LINK_GOTO:
                out.append((i, lk['page'], None, lk['from']))
    return sorted(out, key=lambda r: (r[0], round(r[3].y0, 1), r[3].x0))


def verify_body(body_pdf):
    """Check the Contents against the book, before the cover is merged in.

    The rows are checked against the book, not against themselves. An internally
    consistent Contents can still be uniformly wrong, so the binding check is
    that the heading really is on the page the row sends the reader to, and that
    the number the row prints is the number that page's own footer prints.
    """
    import fitz
    doc = fitz.open(body_pdf)
    want = {mkid(k, t): (lbl, t) for _, lbl, k, t in TOC}
    links = contents_links(doc, named=True)
    problems = []

    found_ids = [mid for _, _, mid, _ in links]
    for mid, (lbl, _) in want.items():
        n = found_ids.count(mid)
        if n != 1:
            problems.append(f'"{lbl}" has {n} links in the Contents, expected 1')
    for mid in found_ids:
        if mid not in want:
            problems.append(f'a link points at {mid}, which is not a Contents row')

    for src, target, mid, rect in links:
        if mid not in want:
            continue
        lbl, title = want[mid]
        head = heading_text(title)
        printed = re.search(r'(\d+)\s*$', doc[src].get_textbox(rect).strip())
        printed = int(printed.group(1)) if printed else None
        footer = footer_number(doc[target])
        if not doc[target].search_for(head):
            problems.append(f'"{lbl}" sends the reader to page {target + 1}, which '
                            f'does not carry the heading "{head}"')
        if printed != footer:
            problems.append(f'"{lbl}" prints page {printed} but lands on a page whose '
                            f'footer reads {footer}')
    out = [(s, t) for s, t, _, _ in links]
    doc.close()
    return out, problems


def merge(cover_pdf, body_pdf, out_pdf):
    """Cover in front of the body.

    The body's Contents links are made explicit first. Chromium leaves them as
    named destinations, which the merge would not renumber; as explicit page
    links the merge shifts them past the cover along with the pages they target.
    """
    import fitz
    doc = fitz.open(body_pdf)
    converted = 0
    for page in doc:
        for lk in page.get_links():
            if lk.get('kind') == fitz.LINK_NAMED and lk.get('page', -1) >= 0:
                target = lk['page']
                page.delete_link(lk)
                page.insert_link({'kind': fitz.LINK_GOTO, 'from': lk['from'],
                                  'page': target, 'to': lk.get('to', fitz.Point(0, 0))})
                converted += 1
    doc.saveIncr()
    doc.close()

    out = fitz.open()
    for src in (cover_pdf, body_pdf):
        with fitz.open(src) as d:
            out.insert_pdf(d)
    out.save(out_pdf)
    out.close()
    return converted


def verify_merged(out_pdf, before):
    """The cover displaced every body page by one. Every link must have followed.

    A link left pointing at its old number would land the reader one page early,
    on the last page of the previous section, which reads as almost right.
    """
    import fitz
    doc = fitz.open(out_pdf)
    after = [(s, t) for s, t, _, _ in contents_links(doc, named=False)]
    pages = doc.page_count
    doc.close()
    want = [(s + 1, t + 1) for s, t in before]
    if after != want:
        moved = [f'link on page {s + 1} points at {t + 1}, expected {w}'
                 for (s, t), (_, w) in zip(after, want) if t != w]
        return pages, (moved or [f'{len(before)} links before the merge, {len(after)} after'])
    return pages, []


def main():
    from gates import run_gates

    # ---- numeric gate: recompute every worked number (this course's analogue of
    #      CSC241's verify_code). Runs before the renders when present. ----
    ng = os.path.join(HERE, 'verify_numbers.py')
    if os.path.exists(ng):
        r = subprocess.run([sys.executable, ng])
        if r.returncode != 0:
            stop('numeric gate failed, a worked answer disagrees with a recompute.')

    # ---- formula gate: no formula appears without saying what its symbols mean.
    #      Reads content/, so it runs before anything is assembled. ----
    fg = os.path.join(HERE, 'qa_formulas.py')
    if os.path.exists(fg):
        r = subprocess.run([sys.executable, fg])
        if r.returncode != 0:
            stop('formula gate failed: a formula is stated without defining its symbols.')

    # ---- verbatim gate: every quoted past question really is the examiner's
    #      words, checked both ways against the transcripts. Reads content/, so
    #      it runs before anything is assembled. MANUAL_METHODOLOGY 4c. ----
    vg = os.path.join(HERE, 'qa_verbatim.py')
    if os.path.exists(vg):
        r = subprocess.run([sys.executable, vg])
        if r.returncode != 0 and '--skip-verbatim' not in sys.argv:
            stop('verbatim gate failed: a past question is paraphrased, or a '
                 'question we hold is quoted nowhere.')

    cover_html = COVER_HEAD + read(COVER) + TAIL
    draft = build_body(build_contents())
    if not run_gates(cover_html + draft):
        stop('house-style gate failed.')

    # first-use audit: no notation is used before the book introduces it. On this
    # course that matters more than usual, because the official text teaches none
    # of the graph/tree/relation material, so the manual is the only source.
    if os.path.exists(os.path.join(HERE, 'qa_firstuse.py')):
        import qa_firstuse
        if not qa_firstuse.report(draft) and '--skip-firstuse' not in sys.argv:
            stop('first-use audit failed: the manual is not sufficient on its own.')

    body_path = os.path.join(HERE, 'full_manual.html')
    cover_path = os.path.join(HERE, 'cover_page.html')
    write(cover_path, cover_html)

    if '--no-pdf' in sys.argv:
        write(body_path, build_body(build_contents()))
        print(f'wrote {body_path}')
        return

    body_pdf = os.path.join(HERE, '_body.pdf')
    cover_pdf = os.path.join(HERE, '_cover.pdf')
    render(cover_path, cover_pdf, 'nofooter')

    body_html, pages = number_the_book(body_path, body_pdf)

    # ---- the Contents changed the text, so gate what actually ships ----
    if not run_gates(cover_html + body_html):
        stop('house-style gate failed on the assembled book.')

    before, problems = verify_body(body_pdf)
    if problems:
        stop('the Contents does not lead where it says.', problems)

    out = os.path.join(HERE, 'CSC242_checkpoint.pdf')
    merge(cover_pdf, body_pdf, out)
    count, problems = verify_merged(out, before)
    if problems:
        stop('merging the cover broke the Contents links.', problems)

    print(f'CONTENTS GATE: pass ({len(before)} rows)')
    print('  . every row links to a page carrying that section\'s heading')
    print('  . every printed number matches the footer of the page it reaches')
    print('  . every link followed the cover offset through the merge')

    import qa_layout
    if not qa_layout.check(out):
        stop('layout QA failed on the merged book.')
    print(f'merged -> {out}  ({count} pages)')


if __name__ == '__main__':
    # Two chats building the same course would overwrite each other's content and
    # PDF. Different courses share no paths and need no lock.
    from buildlock import build_lock
    with build_lock('assemble.py'):
        main()
