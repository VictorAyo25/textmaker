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
print('rendered', out)
