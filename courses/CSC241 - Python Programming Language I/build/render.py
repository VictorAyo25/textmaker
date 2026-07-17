import sys, os
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
url = 'file:///' + src.replace('\\', '/')

# Footer carries the course and the author, and nothing else.
FOOTER = (
    '<div style="width:100%; font-family:DejaVu Sans, sans-serif; font-size:7pt; '
    'color:#8a8f98; padding:0 18mm; display:flex; justify-content:space-between;">'
    '<span>CSC241 · Python Programming Language I · Victor Ayodeji</span>'
    '<span class="pageNumber" style="color:#1a2332; font-weight:bold; font-size:8pt;"></span></div>'
)

# 'nofooter' mode: full-bleed page, no running footer (used for the cover)
NOFOOTER = len(sys.argv) > 3 and sys.argv[3] == 'nofooter'

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.goto(url, wait_until='networkidle')
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
