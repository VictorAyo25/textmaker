"""render.py — HTML -> PDF via headless Chromium.

    python render.py in.html out.pdf [nofooter]

WeasyPrint is the natural renderer for print CSS, but its GTK/Pango DLLs are not
available on this machine, so Chromium does the job. Two consequences the rest of
the pipeline depends on:

  * fonts are vendored in build/fonts/ and @font-face'd, so a render does not
    depend on what is installed on the box;
  * the running footer is drawn by Chromium's footerTemplate, not by CSS, because
    only the footer template can see the page number.

House rule: the footer carries the course and the author, never the institution.
"""
import sys, os
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2])
url = 'file:///' + src.replace('\\', '/')

FOOTER = (
    '<div style="width:100%; font-family:DejaVu Sans, sans-serif; font-size:7pt; '
    'color:#8a9099; padding:0 18mm; display:flex; justify-content:space-between;">'
    '<span>COS221 · Computer Programming I (Java) · Victor Ayodeji</span>'
    '<span class="pageNumber" style="color:#161a21; font-weight:bold; font-size:8pt;"></span></div>'
)

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
        pg.pdf(path=out, format='A4', print_background=True,
               display_header_footer=True,
               header_template='<div></div>',
               footer_template=FOOTER,
               margin={'top': '19mm', 'bottom': '16mm', 'left': '18mm', 'right': '18mm'},
               prefer_css_page_size=False)
    b.close()
print('rendered', out)
