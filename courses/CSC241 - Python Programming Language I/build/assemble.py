"""Assemble the CSC241 manual from content/*.html, then render to PDF.

    cd build && python assemble.py            # checkpoint build (Modules 1 to 2)
    cd build && python assemble.py --no-pdf   # HTML only, skip Chromium

The cover is full bleed and carries no running footer, so it is rendered as its
own PDF and merged in front of the body. The body carries the footer and page
numbers.

The house-style gate runs before anything is written. It is not advisory: a
violation stops the build. See gates.py.
"""
import os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

COVER = 'cover.html'
BODY_PARTS = ['front.html', 'module1.html', 'module2.html', 'module2_unit4.html',
              'module3.html', 'module4.html', 'module5.html',
              'mock1.html', 'mock1_answers.html']

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>CSC241 - Python Programming Language I - Study Manual</title>
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


def render(src_html, out_pdf, mode=None):
    cmd = [sys.executable, os.path.join(HERE, 'render.py'), src_html, out_pdf]
    if mode:
        cmd.append(mode)
    subprocess.run(cmd, check=True)


def main():
    body_html = HEAD + '\n'.join(read(p) for p in BODY_PARTS) + TAIL
    cover_html = COVER_HEAD + read(COVER) + TAIL

    # ---- gates before write, not after; gate everything that ships ----
    sys.path.insert(0, HERE)

    # 1. every claimed output must have come from a real run
    r = subprocess.run([sys.executable, os.path.join(HERE, 'verify_code.py')])
    if r.returncode != 0:
        print('\nBUILD STOPPED: code gate failed, a claimed output is wrong.',
              file=sys.stderr)
        sys.exit(1)

    # 2. house style
    from gates import run_gates
    if not run_gates(cover_html + body_html):
        print('\nBUILD STOPPED: house-style gate failed.', file=sys.stderr)
        sys.exit(1)

    body_path = os.path.join(HERE, 'full_manual.html')
    cover_path = os.path.join(HERE, 'cover_page.html')
    for path, html in ((body_path, body_html), (cover_path, cover_html)):
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(html)
    print(f'wrote {body_path}  ({len(body_html):,} bytes)')

    if '--no-pdf' in sys.argv:
        return

    body_pdf = os.path.join(HERE, '_body.pdf')
    cover_pdf = os.path.join(HERE, '_cover.pdf')
    render(body_path, body_pdf)
    render(cover_path, cover_pdf, 'nofooter')

    import pypdf
    w = pypdf.PdfWriter()
    for p in pypdf.PdfReader(cover_pdf).pages:
        w.add_page(p)
    for p in pypdf.PdfReader(body_pdf).pages:
        w.add_page(p)
    out = os.path.join(HERE, 'CSC241_checkpoint.pdf')
    with open(out, 'wb') as fh:
        w.write(fh)
    print(f'merged -> {out}  ({len(w.pages)} pages)')


if __name__ == '__main__':
    main()
