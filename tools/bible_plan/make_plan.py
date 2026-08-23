"""Build the reading plan, in two shapes, and measure both.

THE RULE THAT SHAPES IT: a day may only END at a section boundary, so the job is
not "divide 898 chapters by N" but "choose N of the legal break points so the
daily loads come out as even as they can". A fixed set of legal cuts makes that a
partition problem, solved exactly by dynamic programming rather than by walking
forward and hoping.

Load is measured in VERSES, not chapters: a Psalms chapter averages 16 verses and
a Kings chapter over 30, so counting chapters alone would make some days twice the
reading of others. Ending a book earns a small bonus, so where two cuts are
otherwise equal the plan prefers to finish the book.
"""
import datetime, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bible_data import OT, NT

sys.stdout.reconfigure(encoding='utf-8')
CH = {b[0]: b[1] for b in OT + NT}


def stream(books):
    out = []
    for name, nch, nvs, breaks in books:
        per, bs = nvs / nch, set(breaks)
        for c in range(1, nch + 1):
            out.append((name, c, per, c in bs, c == nch))
    return out


def partition(items, ndays, book_end_bonus=0.25):
    n = len(items)
    cuts = [i for i, it in enumerate(items) if it[3]]
    pre = [0.0]
    for it in items:
        pre.append(pre[-1] + it[2])
    target = pre[n] / ndays
    pos = [0] + [i + 1 for i in cuts]
    P = len(pos)
    INF = float('inf')
    best = [[INF] * P for _ in range(ndays + 1)]
    back = [[-1] * P for _ in range(ndays + 1)]
    best[0][0] = 0.0
    for d in range(1, ndays + 1):
        row, prev = best[d], best[d - 1]
        for b in range(1, P):
            pb = pos[b]
            adj = -book_end_bonus * target if items[pb - 1][4] else 0.0
            for a in range(b):
                if prev[a] == INF:
                    continue
                load = pre[pb] - pre[pos[a]]
                cost = prev[a] + (load - target) ** 2 + adj
                if cost < row[b]:
                    row[b] = cost
                    back[d][b] = a
    if best[ndays][P - 1] == INF:
        raise SystemExit(f'no partition into {ndays} days exists')
    segs, b, d = [], P - 1, ndays
    while d > 0:
        a = back[d][b]
        segs.append((pos[a], pos[b]))
        b, d = a, d - 1
    return list(reversed(segs)), target


def label(items, lo, hi):
    parts, i = [], lo
    while i < hi:
        bk = items[i][0]
        j = i
        while j < hi and items[j][0] == bk:
            j += 1
        a, b, tot = items[i][1], items[j - 1][1], CH[bk]
        if a == 1 and b == tot:
            parts.append(bk if tot == 1 else f'{bk} 1 to {b}')
        elif a == b:
            parts.append(f'{bk} {a}')
        else:
            parts.append(f'{bk} {a} to {b}')
        i = j
    return '; '.join(parts)


START, END = datetime.date(2026, 8, 24), datetime.date(2026, 11, 30)
DAYS = (END - START).days + 1


def build(pattern, name):
    seq = [pattern[i % len(pattern)] for i in range(DAYS)]
    n_ot, n_nt = seq.count('OT'), seq.count('NT')
    oti, nti = stream(OT), stream(NT)
    os_, ot_t = partition(oti, n_ot)
    ns_, nt_t = partition(nti, n_nt)
    rows, oi, ni, d = [], 0, 0, START
    for kind in seq:
        if kind == 'OT':
            a, b = os_[oi]; oi += 1; items = oti
        else:
            a, b = ns_[ni]; ni += 1; items = nti
        vs = sum(items[i][2] for i in range(a, b))
        rows.append({'date': d.isoformat(), 'kind': kind, 'ref': label(items, a, b),
                     'ch': b - a, 'vs': round(vs), 'prov': d.day,
                     'book_end': items[b - 1][4]})
        d += datetime.timedelta(days=1)

    prov_vs = 915 / 31
    loads = [r['vs'] + prov_vs for r in rows]
    ot_l = [r['vs'] for r in rows if r['kind'] == 'OT']
    nt_l = [r['vs'] for r in rows if r['kind'] == 'NT']
    print(f'--- {name}: {n_ot} OT days, {n_nt} NT days over {DAYS} days')
    print(f'    OT day: {min(ot_l)} to {max(ot_l)} verses  (avg {sum(ot_l)//len(ot_l)})')
    print(f'    NT day: {min(nt_l)} to {max(nt_l)} verses  (avg {sum(nt_l)//len(nt_l)})')
    print(f'    heaviest day is {max(loads)/min(loads):.1f}x the lightest')
    print(f'    minutes/day at 180 wpm, ~26 words a verse: '
          f'{min(loads)*26/180:.0f} to {max(loads)*26/180:.0f}')
    print(f'    days ending exactly at a book end: '
          f'{sum(1 for r in rows if r["book_end"])} of {DAYS}')
    json.dump(rows, open(f'plan_{name}.json', 'w', encoding='utf-8'))
    return rows

from emit import verify, emit

# Plan A is strict alternation, the shape as first specified. It is built and
# measured so the comparison in README.md stays honest, but B is what ships:
# alternation swings 4.2x between the heaviest and lightest day, B swings 2.1x.
a = build(['OT', 'NT'], 'A')
b = build(['OT', 'NT', 'OT'], 'B')

verify(b, OT, NT, START)
emit(b)
