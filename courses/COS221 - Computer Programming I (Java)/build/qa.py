"""qa.py — gate the rendered manual. Every count must be zero.

    python qa.py            # after assemble.py

These are the checks a text diff cannot see, plus the house rules. Each one is
here because it caught a real defect in this book:

  * footer numbering   caught the cover being spliced in after the render, which
                       left every footer one less than the page it sat on and the
                       Contents one out to match;
  * margin overflow    caught the cover title running off the right edge, clipped;
  * heading orphans    caught a section title stranded at the foot of a page with
                       its first box overleaf.

The snippet gate lives in check_code.py and is the important one: it compiles and
runs every listing. Run both.
"""
import fitz, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(HERE, 'full_manual_clean.pdf')

FOOTER = 'COS221 · Computer Programming I (Java) · Victor Ayodeji'
BANNED = [('em dash', '—'), ('en dash', '–'),
          ('institution', '(?i)covenant'), ('platform', '(?i)ccodel'),
          ('pedagogy source', '(?i)stroud'), ('marker text', 'TOCM')]

fails = []


def check(name, n, detail=''):
    print(f'  {name:<34}: {n}' + ('   FAIL' if n else '   ok') + (f'  {detail}' if n and detail else ''))
    if n:
        fails.append(name)


def main():
    if not os.path.exists(PDF):
        raise SystemExit('no full_manual_clean.pdf: run assemble.py first')
    d = fitz.open(PDF)
    text = ''.join(p.get_text() for p in d)
    W, H = d[0].rect.width, d[0].rect.height

    print(f'{PDF}\n{d.page_count} pages\n')

    print('house style')
    for label, pat in BANNED:
        check(label, len(re.findall(pat, text)))

    print('\nstructure')
    # page 1 is the cover and carries no running footer
    foot = [i + 1 for i in range(1, d.page_count)
            if not re.search(re.escape(FOOTER).replace('\\ ', r'\s*') + r'\s*' + str(i + 1),
                             d[i].get_text().replace('\n', ' '))]
    check('footer number != page', len(foot), str(foot[:6]))
    check('footer on the cover', 1 if FOOTER in d[0].get_text() else 0)

    blank = [i + 1 for i in range(d.page_count) if len(d[i].get_text().strip()) < 90]
    check('near-blank pages', len(blank), str(blank))

    links = [l for p in d for l in p.get_links()]
    check('links that are not GoTo',
          sum(1 for l in links if l.get('kind') != fitz.LINK_GOTO))
    check('no links at all', 1 if not links else 0)

    # every Contents row must link to the page it prints
    toc = next((i for i in range(d.page_count) if d[i].get_text().lstrip().startswith('Contents')), None)
    check('no Contents page found', 1 if toc is None else 0)
    if toc is not None:
        mism = 0
        for l in d[toc].get_links():
            r = fitz.Rect(l['from'])
            row = d[toc].get_text('text', clip=fitz.Rect(r.x0, r.y0 - 2, W, r.y1 + 2)).strip()
            m = re.search(r'(\d+)\s*$', row)
            if m and int(m.group(1)) != l['page'] + 1:
                mism += 1
        check('Contents page numbers wrong', mism)

    print('\nlayout')
    over = []
    for i in range(d.page_count):
        for b in d[i].get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                for s in ln.get('spans', []):
                    if s['bbox'][2] > W - 8 or s['bbox'][0] < 8:
                        over.append(i + 1)
    check('text outside the margins', len(over), str(sorted(set(over))[:6]))

    # A section title (16.5pt) low on the page is only ORPHANED if its first box is
    # overleaf, which is what the docstring promises and what looks wrong. A title
    # sitting low but WITH its first box beneath it on the same page is an ordinary
    # heading-near-a-page-foot, and forcing it to the next page would only trade the
    # heading for a half-empty page, a worse defect. So the test is: low AND no box
    # begins below it here. A box is a wide filled panel (its bar or its body); the
    # thin heading rule and a bare intro line are not, so a genuine stranding, where
    # only the rule and maybe one line follow, still fails.
    def box_below(pg, y):
        for dr in pg.get_drawings():
            if dr.get('fill') is None:
                continue
            r = dr['rect']
            if r.width > 200 and r.height > 8 and r.y0 > y + 2 and r.y1 < H - 20:
                return True
        return False

    orph = []
    for i in range(d.page_count):
        pg = d[i]
        for b in pg.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                for s in ln.get('spans', []):
                    if 15.5 < s['size'] < 17.5 and s['bbox'][1] > H * 0.80:
                        if not box_below(pg, s['bbox'][3]):
                            orph.append(i + 1)
    check('section heading orphaned', len(orph), str(sorted(set(orph))))

    print('\nrender fidelity')
    # THE SHRINK CHECK (MANUAL_METHODOLOGY 2b). Chromium scales the WHOLE document
    # down to fit its widest box, so one over-long code line shrinks the body font of
    # every page. It is invisible to every check above: after the shrink nothing
    # overflows, the footers are sequential, the Contents agrees with itself. The
    # only fingerprint is the type coming back smaller than the CSS asked for. The
    # section title is 16.5pt in manual.css; measure what it actually rendered at.
    # This book shipped once at 92.9% (title 15.32pt) before this check existed.
    from collections import Counter
    titles = Counter()
    for i in range(d.page_count):
        for b in d[i].get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                for s in ln.get('spans', []):
                    if 14 < s['size'] < 18 and 'Serif' in s['font']:
                        titles[round(s['size'], 2)] += 1
    rendered = max((s for s, _ in titles.most_common(3)), default=0)
    shrunk = 1 if rendered < 16.4 else 0
    check('body shrunk below its design size', shrunk,
          f'section title rendered at {rendered}pt, css asks 16.5pt '
          f'({rendered / 16.5:.1%} of design size)')

    # And the tighter of the two limits: code must stay inside its own panel, not
    # merely inside the page. A line 88-90 chars wide clears the page margin, so it
    # triggers no shrink and no margin-overflow, yet its tail prints outside the box
    # drawn around it. Measure the code panel (the wide pale fill behind pre.src) and
    # check every mono run against it.
    spill = []
    for i in range(d.page_count):
        pg = d[i]
        panels = [dr['rect'] for dr in pg.get_drawings()
                  if dr.get('fill') and dr['rect'].width > 300 and 18 < dr['rect'].height < 800]
        for b in pg.get_text('dict')['blocks']:
            for ln in b.get('lines', []):
                for s in ln.get('spans', []):
                    if 'Mono' not in s['font']:
                        continue
                    for r in panels:
                        if r.y0 - 2 <= s['bbox'][1] and s['bbox'][3] <= r.y1 + 2 and r.x0 < s['bbox'][0]:
                            if s['bbox'][2] > r.x1 + 1.0:
                                spill.append(i + 1)
                            break
    check('code spilling past its panel', len(spill), str(sorted(set(spill))[:6]))

    print()
    if fails:
        print('FAILED:', ', '.join(fails))
        sys.exit(1)
    print('all gates pass')


if __name__ == '__main__':
    main()
