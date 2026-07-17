"""
freeze.py — one-time 'eject' of the reconstructed sections into editable HTML.

Normally assemble.py re-derives the Modules 1-4 / Foundations prose from the
original v1 PDF on every build. That guarantees fidelity, but it means you
cannot edit that prose (the next build would overwrite it).

Running this script writes those sections out to build/content/*.html. From then
on assemble.py READS those files instead of re-deriving, so they become the
editable source of truth.

    python freeze.py            # freeze (refuses to clobber existing content/)
    python freeze.py --force    # re-freeze from the PDF, discarding your edits

After freezing, edit build/content/*.html freely and re-run `python assemble.py`.
"""
import io, os, re, sys, base64, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')
ASSETS = os.path.join(CONTENT, 'assets')

# teaching sections: name -> (first_page, last_page) in the ORIGINAL v1 PDF
SECTIONS = {
    'foundations': (7, 20),
    'module1':     (22, 40),
    'module2':     (42, 53),
    'module3':     (55, 79),
    'module4':     (81, 106),
}
# back matter uses the free-flow generator (recon_back), not the box generator
BACK = {
    'howto':      (4, 5),
    'exercises':  (108, 143),
    'mocks':      (145, 164),
    'reference':  (166, 174),
}
# part dividers: name -> (roman, source_page, marker)
DIVIDERS = {
    'partI':   ('I',   6,   'PARTI'),
    'partII':  ('II',  21,  'PARTII'),
    'partIII': ('III', 41,  'PARTIII'),
    'partIV':  ('IV',  54,  'PARTIV'),
    'partV':   ('V',   80,  'PARTV'),
    'partVII': ('VII', 107, 'PARTVII'),
    'partVIII':('VIII',144, 'PARTVIII'),
    'partIX':  ('IX',  165, 'PARTIX'),
}

DATAURI = re.compile(r'data:image/png;base64,([A-Za-z0-9+/=]+)')


def externalise(html, tag):
    """Replace inline base64 PNGs with files under content/assets/, return new html."""
    os.makedirs(ASSETS, exist_ok=True)
    out, n = [], [0]

    def repl(m):
        raw = base64.b64decode(m.group(1))
        h = hashlib.md5(raw).hexdigest()[:8]
        name = f'{tag}_{n[0]:02d}_{h}.png'
        n[0] += 1
        with open(os.path.join(ASSETS, name), 'wb') as f:
            f.write(raw)
        # path is relative to build/ (where full_manual.html is written)
        return f'content/assets/{name}'

    return DATAURI.sub(repl, html), n[0]


def main():
    force = '--force' in sys.argv
    if os.path.isdir(CONTENT) and not force:
        existing = [f for f in os.listdir(CONTENT) if f.endswith('.html')]
        if existing:
            print('content/ already exists and holds your edits. Refusing to overwrite.')
            print('Use --force ONLY if you want to discard those edits and re-derive from the PDF.')
            return 1

    from gen_html import gen_pages, set_diagram_map, set_figure_svg
    from assemble import build_diagram_map, build_figure_svg, divider_html
    from recon_back import gen_back
    set_diagram_map(build_diagram_map()); set_figure_svg(build_figure_svg())
    os.makedirs(CONTENT, exist_ok=True)

    banner = ('<!-- FROZEN CONTENT. This file is now the source of truth for this section.\n'
              '     assemble.py reads it as-is; edit it freely and re-run assemble.py.\n'
              '     It was generated once from sources/manual_v1/PHY121_Study_Manual.pdf.\n'
              '     Re-running `python freeze.py --force` would DISCARD your edits. -->\n')

    import corrections
    total_imgs = 0
    for name, (lo, hi) in SECTIONS.items():
        html = gen_pages(lo, hi)
        html = corrections.apply(name, html)     # errata against the original
        html, k = externalise(html, name)
        total_imgs += k
        io.open(os.path.join(CONTENT, name + '.html'), 'w', encoding='utf-8').write(banner + html)
        print(f'  froze {name:12s} (v1 pages {lo}-{hi})  {len(html)/1024:7.1f} KB, {k} images externalised')

    for name, (lo, hi) in BACK.items():
        html = gen_back(lo, hi)
        html = corrections.apply(name, html)     # errata against the original
        html, k = externalise(html, name)
        total_imgs += k
        io.open(os.path.join(CONTENT, name + '.html'), 'w', encoding='utf-8').write(banner + html)
        print(f'  froze {name:12s} (v1 pages {lo}-{hi}, free-flow)  {len(html)/1024:7.1f} KB')

    for name, (roman, pg, marker) in DIVIDERS.items():
        html = divider_html(roman, pg, marker)
        html, k = externalise(html, name)
        total_imgs += k
        io.open(os.path.join(CONTENT, name + '.html'), 'w', encoding='utf-8').write(banner + html)
        print(f'  froze {name:12s} (divider)')

    print(f'\nFrozen into {CONTENT}')
    print(f'{total_imgs} images written to content/assets/')
    print('assemble.py will now read these files instead of re-deriving from the PDF.')
    return 0


if __name__ == '__main__':
    # --force rewrites every file in content/. If a second chat is building this
    # same course, that pulls the rug out from under it mid-run.
    from buildlock import build_lock
    with build_lock('freeze.py'):
        sys.exit(main())
