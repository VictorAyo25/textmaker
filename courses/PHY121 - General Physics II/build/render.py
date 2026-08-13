import sys, os
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
url = 'file:///' + src.replace('\\', '/')

FOOTER = (
    '<div style="width:100%; font-family:DejaVu Sans, sans-serif; font-size:7pt; '
    'color:#8a8f98; padding:0 18mm; display:flex; justify-content:space-between;">'
    '<span>PHY121 · General Physics II · Victor Ayodeji</span>'
    '<span class="pageNumber" style="color:#1e2430; font-weight:bold; font-size:8pt;"></span></div>'
)

# 'nofooter' mode: full-bleed page, no running footer (used for the cover)
NOFOOTER = len(sys.argv) > 3 and sys.argv[3] == 'nofooter'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    # 'networkidle' is not a reliable barrier for local images: it settles on a
    # quiet network, not on decoded pixels. A snapshot taken early renders the
    # img elements at zero height, and the manual silently came out 64 pages
    # instead of 148 -- with sequential footers and no blank pages, so nothing
    # downstream noticed. Wait for the real conditions instead.
    pg.goto(url, wait_until='load')
    pg.wait_for_function(
        """() => document.fonts.status === 'loaded'
              && Array.from(document.images).every(i => i.complete && i.naturalHeight > 0)""",
        timeout=120000)
    n_img = pg.evaluate('document.images.length')
    bad = pg.evaluate("Array.from(document.images).filter(i => !i.naturalHeight).length")
    if bad:
        raise SystemExit(f'{bad} of {n_img} images failed to load; refusing to render')
    print(f'  {n_img} images loaded, fonts ready')
    if NOFOOTER:
        pg.pdf(path=out, format='A4', print_background=True,
               display_header_footer=False,
               margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'},
               prefer_css_page_size=False)
    else:
        pg.pdf(
            path=out, format='A4', print_background=True,
            display_header_footer=True,
            header_template='<div></div>',
            footer_template=FOOTER,
            margin={'top': '19mm', 'bottom': '16mm', 'left': '18mm', 'right': '18mm'},
            prefer_css_page_size=False,
        )
    b.close()


def link_contents(pdf_path, toc_path):
    """Make the Contents page clickable, and give the PDF a sidebar outline.

    Chromium keeps external URLs when it prints but silently DROPS same-document
    anchors, so href="#t4" survives in the HTML and reaches the PDF as ordinary
    printed text. In a 220-page book that is the difference between a usable
    document and one you scroll.

    Both are rebuilt here from the sidecar the generator wrote, not by parsing
    the rendered page back out, so the links cannot drift from the sections they
    point at. Each entry's landing page is found by searching for its title on
    the pages AFTER the Contents, since the Contents lists every title too.
    """
    import json

    import fitz

    entries = json.load(open(toc_path, encoding='utf8'))
    doc = fitz.open(pdf_path)

    # The Contents page is the first one carrying that heading.
    contents_no = next(
        (p.number for p in doc if p.get_text().lstrip().startswith('Contents')), None
    )
    if contents_no is None:
        contents_no = next((p.number for p in doc if 'Contents' in p.get_text()), None)
    if contents_no is None:
        print('  links: no Contents page found, skipped')
        doc.close()
        return

    def section_page(title):
        """The page where this section's HEADING is, not merely its words.

        Searching for the title alone is wrong, and quietly so: "Transformers"
        and "EMF and Internal Resistance" both appear inside question text
        pages before their own sections begin, so a plain search sent two of
        eleven links to the wrong place while reporting success. The heading is
        set much larger than body text, so the biggest span wins.
        """
        best = None
        for p in doc:
            if p.number <= contents_no:
                continue
            for block in p.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        if title in span['text'] and (best is None or span['size'] > best[1]):
                            best = (p.number, span['size'])
        return best[0] if best else None

    page = doc[contents_no]
    toc, made, missed = [], 0, []
    for e in entries:
        title = e['title']
        dest = section_page(title)
        if dest is None:
            missed.append(title)
            continue
        toc.append([1, f"{e['num']}. {title}", dest + 1])

        hits = page.search_for(title)
        if not hits:
            missed.append(f'{title} (no entry rect)')
            continue
        # Widen the hit to the whole line so the number and the count are
        # clickable too, not just the words of the title.
        r = hits[0]
        rect = fitz.Rect(r.x0 - 18, r.y0 - 2, page.rect.x1 - 40, r.y1 + 2)
        page.insert_link({'kind': fitz.LINK_GOTO, 'from': rect, 'page': dest, 'to': fitz.Point(0, 0)})
        made += 1

    if toc:
        doc.set_toc(toc)
    doc.saveIncr()
    doc.close()
    print(f'  contents: {made} of {len(entries)} entries linked, {len(toc)} outline entries')
    if missed:
        print(f'  contents: NOT linked: {", ".join(missed)}')


if not NOFOOTER:
    toc_file = os.path.splitext(out)[0] + '.toc.json'
    if os.path.exists(toc_file):
        try:
            link_contents(out, toc_file)
        except ImportError:
            print('  contents: PyMuPDF not available, links skipped')

print('rendered', out)
