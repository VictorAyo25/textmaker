# Survey the extracted manual text: page count, section headers, box markers.
import re, io, json, os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(BASE, 'sources', 'extracted', 'manual_text.txt')
raw = io.open(SRC, encoding='utf-8').read()

# split into pages
pages = re.split(r'===== PAGE (\d+) =====\n', raw)
# pages[0] is '' ; then alternating number, content
pagemap = {}
for i in range(1, len(pages), 2):
    num = int(pages[i]); pagemap[num] = pages[i+1]

footer_re = re.compile(r'^PHY121 .General Physics II .Victor Ayodeji\s+\d+\s*$')

out = io.open(os.path.join(os.path.dirname(__file__), 'survey_out.txt'), 'w', encoding='utf-8')
markers = ['TEACH', 'MUST-MEMORISE', 'TRAP', 'WORKED EXAMPLE', 'RECALL AND CHECK',
           'FILL IN THE GAP', 'FORMULA', 'METHOD', 'SLIDE', 'CLASSWORK']
sec_re = re.compile(r'^(FOUNDATIONS|UNIT|REFERENCE)\s+[A-Z0-9.]+\s*$')
partish = re.compile(r'^(P A R T|PART|GETTING STARTED|M\.\d|S\.\d|R\.\d|Section [AB]|QUESTION)')

for pn in sorted(pagemap):
    body = pagemap[pn]
    for ln in body.split('\n'):
        s = ln.strip()
        if not s or footer_re.match(s):
            continue
        hit = None
        for m in markers:
            if s == m or s.startswith(m + ' ') or ('·' in s and m in s) or s.endswith(m):
                # only when marker at line start (allow glued tag prefix)
                if re.match(r'^(SLIDE|CLASSWORK|METHOD)?\s*[●⚠]?\s*' + re.escape(m), s):
                    hit = m; break
        if hit:
            out.write(f'p{pn:>3} BOX  | {s[:78]}\n')
        elif sec_re.match(s):
            out.write(f'p{pn:>3} SEC  | {s}\n')
out.close()
print('done; pages:', len(pagemap))
