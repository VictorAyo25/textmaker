"""
recon_back.py — reconstruct the BACK MATTER (exercises, mocks, reference) as real
text, replacing the 300-dpi page images.

The teaching sections (gen_html.gen_pages) are box-driven: every page is a stack
of coloured box bars. The back matter is NOT — only 7 of its ~67 pages have a box
bar at all. It is free-flowing: headings, question lists, prose, and a lot of
tables. So it needs its own generator.

Two things this gets right that the old table code did not:

1. sup/sub inside table cells. PyMuPDF sets flags bit 0 for superscript; a
   subscript has no flag and must be detected geometrically (smaller size AND
   sitting lower than the cell's base text). Without this, "8.99 x 10^9" is
   extracted as "8.99 x 109", which is not a typo but a wrong constant.
2. Wrapped rows. A table row whose cell wraps onto a second visual line must not
   become a second row. A new row starts only when column 0 has content.
"""
import re
import fitz
from reconstruct import (PDF, bars, raw_spans, reflow, _linegroup, FOOTER_RE, WHITE, esc,
                         join_wrapped, hx)
from gen_html import (table_headers_in, col_bounds, render_box, render_section_header,
                      table_extent, crop_datauri, figures_in, split_runs, box_end)

doc = fitz.open(PDF)
PAGE_BOTTOM = 792.0


# ---------------------------------------------------------------- table cells
def cell_html(spans):
    """Inline HTML for one table cell, preserving superscripts and subscripts."""
    if not spans:
        return ''
    base = max(s['sz'] for s in spans)
    bs = [s for s in spans if s['sz'] >= base - 0.2]
    base_y = sum(s['y'] for s in bs) / len(bs)
    out = []
    for s in sorted(spans, key=lambda s: s['x']):
        t = esc(s['t'])
        if s['flags'] & 1:                                   # PyMuPDF bit0 = superscript
            out.append(f'<sup>{t}</sup>')
        elif s['sz'] < base - 0.2 and s['y'] > base_y + 1.5:  # smaller + lower = subscript
            out.append(f'<sub>{t}</sub>')
        else:
            out.append(t)
    h = ''.join(out)
    for tag in ('sup', 'sub'):                                # merge adjacent runs
        h = h.replace(f'</{tag}><{tag}>', '')
    return h.strip()


def row_edges(page, head_y1, endy):
    """Row boundaries taken from the table's own zebra shading.

    Grouping by "column 0 is empty" only catches a wrap in a later column. When it
    is column 0 that wraps, the tail starts a bogus row with every other cell
    blank: "Like repels, unlike / attracts" became two entries, the second with an
    empty hook. Each shaded band is exactly one row and the gaps between bands are
    the unshaded rows, so the shading settles it. Returns [] if unshaded."""
    bands = sorted((d['rect'].y0, d['rect'].y1) for d in page.get_drawings()
                   if d.get('fill') and hx(d.get('fill')) in ('#fafbfc', '#f4f7fc')
                   and d['rect'].width > 300 and head_y1 - 1 <= d['rect'].y0 < endy)
    if not bands:
        return []
    edges = [head_y1]
    for a, b in bands:
        if a > edges[-1] + 1.5:
            edges.append(a)
        edges.append(min(b, endy))
    if endy > edges[-1] + 1.5:
        edges.append(endy)
    return edges


def build_table(page, head, endy):
    """Reconstruct one table, honouring wrapped rows."""
    hspans = [s for s in raw_spans(page, head['y0'] - 1, head['y1'] + 2) if s['col'] == WHITE]
    if not hspans:
        return ''
    colx = col_bounds(hspans)
    ncol = len(colx)
    if ncol < 2:
        return ''

    def split(spans):
        cells = [[] for _ in range(ncol)]
        for s in spans:
            ci = 0
            for i in range(ncol):
                if s['x'] >= colx[i] - 10:
                    ci = i
            cells[ci].append(s)
        return cells

    hdr = [cell_html(c) for c in split(hspans)]
    body = [s for s in raw_spans(page, head['y1'] + 1, endy) if not FOOTER_RE.match(s['t'])]

    rows = []
    edges = row_edges(page, head['y1'] + 1, endy)
    if edges:
        # group every line into the shaded band (or gap) it sits in: one band = one row
        for i in range(len(edges) - 1):
            a, b = edges[i], edges[i + 1]
            sp = [s for s in body if a - 1 <= (s['y'] + s['y1']) / 2 <= b + 1]
            if not sp:
                continue
            cells = ['' for _ in range(ncol)]
            for ln in _linegroup(sp):
                for j, c in enumerate(split(ln)):
                    h = cell_html(c)
                    if h:
                        cells[j] = join_wrapped(cells[j], h) if cells[j] else h
            if any(cells):
                rows.append(cells)
    else:
        for ln in _linegroup(body):
            cells = [cell_html(c) for c in split(ln)]
            if not any(cells):
                continue
            # unshaded table: a row continues when column 0 is empty
            if rows and not cells[0]:
                for i, c in enumerate(cells):
                    if c:
                        rows[-1][i] = (rows[-1][i] + ' ' + c).strip()
            else:
                rows.append(cells)

    if not rows:
        return ''
    th = ''.join(f'<th>{c}</th>' for c in hdr)
    trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)
    return f'<table class="data"><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table>'


# ---------------------------------------------------------------- prose blocks
BULLET = re.compile(r'^[▸•▪]\s*')


def render_free(lines):
    """Render non-table, non-box lines: headings, labels, bullets, prose."""
    out = []
    buf, buf_cls = [], None

    def flush():
        if not buf:
            return
        txt = ''
        for i, x in enumerate(buf):
            txt = x if i == 0 else join_wrapped(txt, x)
        if buf_cls == 'ul':
            items = ''.join(f'<li>{i}</li>' for i in buf)
            out.append(f'<ul class="bul">{items}</ul>')
        elif buf_cls:
            out.append(f'<p class="{buf_cls}">{txt}</p>')
        else:
            out.append(f'<p>{txt}</p>')
        buf.clear()

    for l in lines:
        h, sz, txt = l['html'], l['sz'], l['text'].strip()
        if not txt:
            continue
        if sz >= 11.0:                                   # subheading, e.g. "Section A"
            flush(); buf_cls = None
            # the .sub rule is already bold, so <b> around the whole line is redundant
            m = re.fullmatch(r'<b>(.*)</b>', h)
            if m and '<b>' not in m.group(1):
                h = m.group(1)
            out.append(f'<h3 class="sub">{h}</h3>')
            continue
        if sz <= 8.6 and txt == txt.upper() and len(txt) > 3:   # small caps label
            flush(); buf_cls = None
            out.append(f'<div class="slabel">{h}</div>')
            continue
        # match the html, not the text: a bullet fused inside a styled run
        # ("<b>* note</b>") is not a list marker, and stripping it would fail
        # while CSS still drew its own glyph, showing the bullet twice
        if BULLET.match(h):
            if buf_cls != 'ul':
                flush(); buf_cls = 'ul'
            buf.append(BULLET.sub('', h))
            continue
        cls = 'small' if sz <= 9.6 else None
        if cls != buf_cls:
            flush(); buf_cls = cls
        buf.append(h)
    flush()
    return '\n'.join(out)


# ---------------------------------------------------------------- page driver
def gen_back(lo, hi, marker_first=None):
    """Reconstruct back-matter pages lo..hi into flowing HTML."""
    chunks = []
    carry = None   # a table that ran to the foot of the previous page (colx, ncol)
    for pn in range(lo, hi + 1):
        page = doc[pn - 1]
        sp = [s for s in raw_spans(page, 40, PAGE_BOTTOM) if not FOOTER_RE.match(s['t'])]
        if not sp:
            carry = None
            continue

        blocks = []          # (y, html)
        taken = []           # consumed y-ranges

        # 0. a table continuing from the previous page (no repeated header)
        if carry and not table_headers_in(page, 40, PAGE_BOTTOM) and not bars(page):
            colx, ncol = carry
            rows_html = _cont_rows(page, colx, ncol, 40, PAGE_BOTTOM)
            if rows_html:
                blocks.append((0, f'<table class="data cont"><tbody>{rows_html}</tbody></table>'))
                taken.append((0, PAGE_BOTTOM))
        carry = None

        # 1. section header (kicker + big title at the top of a section's first page)
        hdr = render_section_header(page, 100)
        if hdr and 'class="title"' in hdr:
            top = max((s['y1'] for s in sp if s['y'] < 100), default=95)
            blocks.append((0, f'<section>{hdr}'))
            taken.append((0, top + 2))

        # 2. boxes (rare here, but they exist)
        bb = bars(page)
        for i, b in enumerate(bb):
            nexty = bb[i + 1]['y0'] if i + 1 < len(bb) else PAGE_BOTTOM - 8
            end = box_end(page, b, nexty)      # the tint's bottom, not the next bar
            blocks.append((b['y0'], render_box(page, b, end)))
            taken.append((b['y0'] - 1, end))

        # 2b. figures (vector line art) -> cropped image, before the prose pass so
        # their internal labels are not stranded as loose paragraphs
        for r in figures_in(page):
            if any(a <= r.y0 <= b for a, b in taken):
                continue
            uri = crop_datauri(page, r.x0 - 1, r.y0 - 1, r.x1 + 1, r.y1 + 1)
            blocks.append((r.y0, f'<img class="figure" src="{uri}" alt="circuit diagram"/>'))
            taken.append((r.y0 - 1, r.y1 + 1))

        # 3. tables. The end of a table must come from its own row shading /
        # separator rules (table_extent), NOT from "wherever the next heading is":
        # otherwise the prose that follows the table gets swallowed in as rows.
        heads = table_headers_in(page, 40, PAGE_BOTTOM)
        stops = sorted([h['y0'] for h in heads] + [b['y0'] for b in bb] +
                       [l['y'] for l in _lines(sp) if l['sz'] >= 11.0])
        for h in heads:
            hard = next((y for y in stops if y > h['y1'] + 4), PAGE_BOTTOM - 8)
            _, _, _, ty1 = table_extent(page, h, hard)
            endy = min(ty1 + 1, hard)
            html = build_table(page, h, endy)
            if html:
                blocks.append((h['y0'], html))
                taken.append((h['y0'] - 1, endy))
                # if this table runs to the foot of the page it probably continues
                # onto the next one (the header is not repeated there)
                if endy >= PAGE_BOTTOM - 60:
                    hs = [s for s in raw_spans(page, h['y0'] - 1, h['y1'] + 2) if s['col'] == WHITE]
                    cx = col_bounds(hs)
                    if len(cx) >= 2:
                        carry = (cx, len(cx))

        # 4. everything else -> free-flowing prose
        free = [s for s in sp if not any(a <= (s['y'] + s['y1']) / 2 <= b for a, b in taken)]
        if free:
            for grp, y in _split_runs(free, taken):
                html = render_free(reflow(grp))
                if html.strip():
                    blocks.append((y, html))

        blocks.sort(key=lambda t: t[0])
        chunks.append('\n'.join(h for _, h in blocks))
    return '\n'.join(chunks) + '\n</section>'


def _cont_rows(page, colx, ncol, y0, y1):
    """Rows of a table continuing from the previous page (its header is not repeated)."""
    def split(spans):
        cells = [[] for _ in range(ncol)]
        for s in spans:
            ci = 0
            for i in range(ncol):
                if s['x'] >= colx[i] - 10:
                    ci = i
            cells[ci].append(s)
        return cells
    body = [s for s in raw_spans(page, y0, y1) if not FOOTER_RE.match(s['t'])]
    if not body:
        return ''
    rows = []
    for ln in _linegroup(body):
        cells = [cell_html(c) for c in split(ln)]
        if not any(cells):
            continue
        if rows and not cells[0]:
            for i, c in enumerate(cells):
                if c:
                    rows[-1][i] = (rows[-1][i] + ' ' + c).strip()
        else:
            rows.append(cells)
    return ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows)


def _lines(sp):
    out = []
    for ln in _linegroup(sp):
        out.append(dict(y=min(s['y'] for s in ln), sz=max(s['sz'] for s in ln)))
    return out


_split_runs = split_runs   # shared with gen_pages
