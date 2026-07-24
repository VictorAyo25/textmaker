"""render.py -- HTML -> PDF via headless Chromium.

    python render.py in.html out.pdf [nofooter]

WAIT FOR THE FONTS. This is not a nicety, it is the difference between a book and
a lottery ticket. 'networkidle' means the network went quiet; it does NOT mean the
@font-face faces finished loading and the text was re-laid-out in them. Render the
same HTML repeatedly without waiting and Chromium returns different page counts:
every line measured in fallback metrics is the wrong width, so it wraps
differently, so the whole book paginates differently, and the count is whatever the
race happened to decide.

That is the exact bug that shipped a defective PHY121 v2 (148 pages collapsed to
64) and every gate stayed green, because a short book with sequential footers and
no blank pages looks perfectly healthy. It is invisible to any gate that checks the
PDF for self-consistency, because the PDF *is* internally consistent: it is
consistently wrong.

So we wait for document.fonts to load, then verify the faces actually loaded rather
than trusting the wait did anything. Ported from COS221 / PHY121, where the lesson
was paid for. This book uses three families, so all three are checked.
"""
import sys, os
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
url = 'file:///' + src.replace('\\', '/')

# Footer carries the course and the author, and nothing else.
FOOTER = (
    '<div style="width:100%; font-family:DejaVu Sans, sans-serif; font-size:7pt; '
    'color:#8a8f98; padding:0 18mm; display:flex; justify-content:space-between;">'
    '<span>ENT221 · Agripreneurship · Victor Ayodeji</span>'
    '<span class="pageNumber" style="color:#1a2332; font-weight:bold; font-size:8pt;"></span></div>'
)

# 'nofooter' mode: full-bleed page, no running footer (used for the cover)
NOFOOTER = len(sys.argv) > 3 and sys.argv[3] == 'nofooter'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(url, wait_until='load')

    # 1. wait for the real conditions, not for the network to go quiet.
    pg.wait_for_function(
        """() => document.fonts.status === 'loaded'
              && Array.from(document.images).every(i => i.complete && i.naturalHeight > 0)""",
        timeout=120000)

    # 2. trust nothing: prove the faces we paginate against are actually loaded. A
    #    404 on a .ttf also "settles" document.fonts, and then we would silently
    #    paginate in a fallback font and produce a confidently wrong book.
    faces = pg.evaluate("""() => {
        const want = ['DejaVu Sans', 'DejaVu Sans Mono', 'DejaVu Serif'];
        return want.map(f => [f, document.fonts.check('12pt "' + f + '"')]);
    }""")
    missing = [f for f, ok in faces if not ok]
    if missing:
        b.close()
        raise SystemExit(f'render.py: these @font-face faces did not load: {missing}. '
                         f'Pagination would be measured in fallback metrics and the '
                         f'page count would be wrong. Refusing to render.')

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
print('rendered', out)
