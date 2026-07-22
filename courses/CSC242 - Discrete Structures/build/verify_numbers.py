"""Numeric gate: recompute every worked number, then prove the manual prints it.

Discrete maths is deceptively easy to get wrong in exactly the places that cost
marks: an off-by-one in a permutation, a combination where a permutation was
meant, an inclusion-exclusion term subtracted twice, a degree sum that comes out
odd (which is impossible), a tree with the wrong leaf count. A worked answer
nobody recomputed is a guess wearing a fact's clothes (MANUAL_METHODOLOGY items
4 and 8). So for every worked result in the manual we:

  1. compute it here from first principles, with the standard library, not by
     copying the number out of the HTML, and
  2. assert the string the manual actually prints for it is present in content/.

A check is (label, computed_value, shown_in_book). The gate fails if the
recompute disagrees with what we expected to write, OR if that string is missing
from the book (a typo in the HTML). Separators are normalised away, so
"3 628 800" and "3628800" match. The book writes minus as the entity &#8722;
(U+2212); both it and an ASCII '-' read the same here.

Control-test it by flipping a digit in the HTML: the gate must then fail on that
value. A gate you have not tried to break is one you are trusting on faith
(MANUAL_METHODOLOGY item 9).
"""
import html as _html
import os, sys
from itertools import permutations, product
from fractions import Fraction
from math import comb, factorial, perm

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')


def _prepare(raw):
    text = _html.unescape(raw)
    text = text.replace(chr(0x2212), '-').replace(chr(0x00A0), ' ')
    # Collapse every run of whitespace to one space. The content files are
    # hand-wrapped at about 78 columns, so a printed value like "2, 3, 3, 2" can
    # fall across a line break and then not appear as a substring at all. That is
    # a fact about the source layout, not about the book, and a gate that fails
    # on it teaches the author to fight the wrapping instead of the maths.
    return ' '.join(text.split())


def book_text():
    parts = []
    for name in sorted(os.listdir(CONTENT)):
        if name.endswith('.html'):
            with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
                parts.append(fh.read())
    return _prepare('\n'.join(parts))


_FILE_CACHE = {}


def file_text(name):
    """One content file, prepared the same way as the whole book."""
    if name not in _FILE_CACHE:
        with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
            _FILE_CACHE[name] = _prepare(fh.read())
    return _FILE_CACHE[name]


# ---- independent recomputation helpers ----
def bitstring(subset, universe):
    """The bit string of a subset: 1 where that universe element is present."""
    return ''.join('1' if u in subset else '0' for u in universe)


def tsp_best(dist, start):
    """Exact shortest Hamiltonian cycle, by brute force over every order.

    Small graphs only. This is the honest way to answer a travelling-salesman
    question: the greedy nearest-neighbour tour is NOT guaranteed to be optimal,
    and the manual must not present it as though it were.
    """
    others = [c for c in dist if c != start]
    best, best_route = None, None
    for order in permutations(others):
        route = (start,) + order + (start,)
        total = sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
        if best is None or total < best:
            best, best_route = total, route
    return best, best_route


def perms_with_repeats(word):
    """Distinct arrangements of a word with repeated letters."""
    from collections import Counter
    n = factorial(len(word))
    for c in Counter(word).values():
        n //= factorial(c)
    return n


# Small counts are spelled out in the prose, as ordinary English does. Convert
# the recomputed number to the same word so the comparison is like for like,
# rather than weakening the check to accept either form.
_WORD = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
         6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
         11: 'eleven', 12: 'twelve'}


# ---- the checks: (label, computed, shown, where) ----
#
# WHY `where` AND `near` EXIST. The original form of this gate asked only
# "does the string appear anywhere in content/". Control-testing the Part Nine
# and Ten checks showed how weak that is: flipping the printed Bayes posterior
# from 0.625 to 0.635 did NOT fail the gate, because 0.625 also appears two
# lines below in the arithmetic check; flipping a recurrence table cell from 46
# to 48 did not fail either, because the two characters "46" occur 89 times in
# this book, inside 146, 460, 1046 and so on. A gate that passes on a corrupted
# value is not measuring the book, and short numbers are exactly where a typo
# is most likely and least visible.
#
# So a check may now say WHERE the value must appear, naming the one content
# file that prints it, and `shown` is written as a distinctive slice of that
# line rather than a bare number: not '46' but '5 x 14 - 6 x 4 = 46'. Together
# those two make a corrupted value fail. `where` is optional, and the older
# checks that omit it behave exactly as before, which is honest for the long
# distinctive values (a bit string, 2684483063360) where a book-wide search
# really is decisive.
#
# Many of the Part Nine and Ten checks go one step further: the expected string
# is BUILT from the recomputation rather than typed, so `computed` and `shown`
# are the same object and the presence test carries the whole check. That is the
# strongest form available here, and it is what the table rows use.
CHECKS = []


def add(label, computed, shown, where=None):
    CHECKS.append((label, computed, shown, where))


# Checks are added as each part is authored, grouped by the section that prints
# them, so a failure names the place to look.

# ---------------------------------------------------------------- Foundations
add('6!/4!', factorial(6) // factorial(4), '30')
add('10!/8!', factorial(10) // factorial(8), '90')
add('0!', factorial(0), '1')
add('7!', factorial(7), '5040')
add('sum 2i+1 to 3', sum(2 * i + 1 for i in range(1, 4)), '15')
add('sum i^2 to 4', sum(i * i for i in range(1, 5)), '30')

# ---------------------------------------------------------------- Part One
add('rows for 5 letters', 2 ** 5, '32')
add('rows for 4 letters', 2 ** 4, '16')

# ---------------------------------------------------------------- Part Two
add('subsets of 4', 2 ** 4, '16')
add('subsets of 6', 2 ** 6, '64')
add('power set of 3', 2 ** 3, '8')
add('n(AxB) 4 by 7', 4 * 7, '28')
add('SxC size', 3 * 2, '6')
add('union 20+15-6', 20 + 15 - 6, '29')
add('union 5+5-3', 5 + 5 - 3, '7')

# Bit strings. Position i holds element i of U = {1..10}.
U10 = list(range(1, 11))
add('bits {3,4,5}', bitstring({3, 4, 5}, U10), '0011100000')
add('bits {1,3,6,10}', bitstring({1, 3, 6, 10}, U10), '1010010001')
add('bits {2,3,4,7,8,9}', bitstring({2, 3, 4, 7, 8, 9}, U10), '0111001110')
add('bits {1,3,5,7,9}', bitstring({1, 3, 5, 7, 9}, U10), '1010101010')
add('complement of odds', bitstring({2, 4, 6, 8, 10}, U10), '0101010101')
add('bits {1,2,3,4,5}', bitstring({1, 2, 3, 4, 5}, U10), '11 1110 0000')
add('union bits', bitstring({1, 2, 3, 4, 5} | {1, 3, 5, 7, 9}, U10), '1111101010')
add('meet bits', bitstring({1, 2, 3, 4, 5} & {1, 3, 5, 7, 9}, U10), '1010100000')
add('xor bits', bitstring({1, 2, 3, 4, 5} ^ {1, 3, 5, 7, 9}, U10), '01 0100 1010')
add('bits {2,5} over 5', bitstring({2, 5}, [1, 2, 3, 4, 5]), '01001')

# ---------------------------------------------------------------- Part Three
# The six relations of 2024/2025 Q4(b), classified by brute force rather than by
# eye. The book prints a summary table; these assert the verdicts it prints.
_A4 = {1, 2, 3, 4}
_RELS = {
    'R1': {(1, 1), (1, 2), (2, 1), (2, 2), (3, 4), (4, 1), (4, 4)},
    'R2': {(1, 1), (1, 2), (2, 1)},
    'R3': {(1, 1), (1, 2), (1, 4), (2, 1), (2, 2), (3, 3), (4, 1), (4, 4)},
    'R4': {(2, 1), (3, 1), (3, 2), (4, 1), (4, 2), (4, 3)},
    'R5': {(1, 1), (1, 2), (1, 3), (1, 4), (2, 2), (2, 3), (2, 4),
           (3, 3), (3, 4), (4, 4)},
    'R6': {(3, 4)},
}


def _reflexive(r, a=_A4):
    return all((x, x) in r for x in a)


def _symmetric(r):
    return all((b, x) in r for (x, b) in r)


def _antisymmetric(r):
    return all(x == b for (x, b) in r if (b, x) in r)


def _transitive(r):
    return all((x, c) in r for (x, b) in r for (b2, c) in r if b == b2)


def _irreflexive(r, a=_A4):
    return all((x, x) not in r for x in a)


_props = {name: (_reflexive(r), _symmetric(r), _antisymmetric(r),
                 _transitive(r), _irreflexive(r))
          for name, r in _RELS.items()}

# Which relations hold each property, computed, then asserted against the text
# the book actually prints for that part.
def _holds(i):
    """The relations with property i, written the way the book writes a list."""
    names = sorted(n for n in _RELS if _props[n][i])
    if len(names) <= 1:
        return ''.join(names)
    return ', '.join(names[:-1]) + ' and ' + names[-1]
add('24/25 Q4b reflexive', _holds(0), 'R3 and R5')
add('24/25 Q4b symmetric', _holds(1), 'R2 and R3')
add('24/25 Q4b antisymmetric', _holds(2), 'R4, R5 and R6')
add('24/25 Q4b transitive', _holds(3), 'R4, R5 and R6')
add('24/25 Q4b irreflexive', _holds(4), 'R4 and R6')

# The divides relation on {1,2,3,4}: 2023/2024 Q3(d)(i).
_divides = {(a, b) for a in _A4 for b in _A4 if b % a == 0}
add('divides pair count', len(_divides), '8')

# Relations on a 3-set and a 4-set.
add('relations on 3', 2 ** (3 ** 2), '512')

# ---------------------------------------------------------------- Part Five
# 5.1 product, sum and subtraction rules.
add('21/22 Q2a chairs', 26 * 100, '2600')
add('21/22 Q2a two-letter variant', 26 * 26 * 100, '67600')
add('25/26 Q6b 4-digit', 10 ** 4, '10000')
add('25/26 Q6b 5-digit', 10 ** 5, '100000')
add('25/26 Q6b 6-digit', 10 ** 6, '1000000')
add('25/26 Q6b total', 10 ** 4 + 10 ** 5 + 10 ** 6, '1110000')
add('25/26 Q6b nonzero-start variant',
    9 * 10 ** 3 + 9 * 10 ** 4 + 9 * 10 ** 5, '999000')
add('25/26 Q6c three-digit', 9 * 10 * 10, '900')
add('25/26 Q6c by range', 999 - 100 + 1, '900')
add('25/26 Q6c no repeats variant', 9 * 9 * 8, '648')

# 2020/2021 Q5(b), the password question. Each length is (all strings over the
# 36 symbols) minus (those over the 26 letters alone), which is the subtraction
# rule; the three lengths are then added.
_pw = {n: 36 ** n - 26 ** n for n in (6, 7, 8)}
add('20/21 Q5b symbols', 26 + 10, '36')
add('20/21 Q5b 36^6', 36 ** 6, '2176782336')
add('20/21 Q5b 26^6', 26 ** 6, '308915776')
add('20/21 Q5b 36^7', 36 ** 7, '78364164096')
add('20/21 Q5b 26^7', 26 ** 7, '8031810176')
add('20/21 Q5b 36^8', 36 ** 8, '2821109907456')
add('20/21 Q5b 26^8', 26 ** 8, '208827064576')
add('20/21 Q5b length 6', _pw[6], '1867866560')
add('20/21 Q5b length 7', _pw[7], '70332353920')
add('20/21 Q5b length 8', _pw[8], '2612282842880')
add('20/21 Q5b total', sum(_pw.values()), '2684483063360')
add('20/21 Q5b at-least-one-letter variant', 36 ** 6 - 10 ** 6, '2175782336')

# 5.2 permutations and combinations.
add('P(6,4)', perm(6, 4), '360')
add('P(6,4) counted down', 6 * 5 * 4 * 3, '360')
add('10!/7! cancelling', factorial(10) // factorial(7), '720')
add('P(3,2)', perm(3, 2), '6')
add('C(3,2)', comb(3, 2), '3')
add('P(8,3)', perm(8, 3), '336')
add('C(8,3)', comb(8, 3), '56')
add('8!', factorial(8), '40320')
add('10!', factorial(10), '3628800')

# 2025/2026 Q4(d): the word SCHOOL. Counted twice over, once by the repeated-
# letter formula and once by brute force over the distinct orderings, because
# the whole trap in this question is the factor of 2! that 6! alone misses.
_school = sorted(set(permutations('SCHOOL')))
add('25/26 Q4d SCHOOL formula', factorial(6) // factorial(2), '360')
add('25/26 Q4d SCHOOL by listing', len(_school), '360')
add('25/26 Q4d 6! trap value', factorial(6), '720')
add('25/26 Q4d LEVEL variant',
    factorial(5) // (factorial(2) * factorial(2)), '30')

# 2025/2026 Q3(b): 6 boys, 4 girls, choose 4, at least one boy. Done by the
# subtraction rule and again case by case, since the book prints both.
_atleast1boy = comb(10, 4) - comb(4, 4)
_bycases = sum(comb(6, b) * comb(4, 4 - b) for b in range(1, 5))
add('25/26 Q3b total selections', comb(10, 4), '210')
add('25/26 Q3b all-girl selections', comb(4, 4), '1')
add('25/26 Q3b subtraction', _atleast1boy, '209')
add('25/26 Q3b by cases', _bycases, '209')
add('25/26 Q3b case 1 boy', comb(6, 1) * comb(4, 3), '24')
add('25/26 Q3b case 2 boys', comb(6, 2) * comb(4, 2), '90')
add('25/26 Q3b case 3 boys', comb(6, 3) * comb(4, 1), '80')
add('25/26 Q3b case 4 boys', comb(6, 4) * comb(4, 0), '15')
add('25/26 Q3b at-least-one-girl variant', comb(10, 4) - comb(6, 4), '195')

# 2025/2026 Q3(c): the prayer partners.
add('25/26 Q3c units', 10 * 10, '100')
add('25/26 Q3c partners', factorial(10), '3628800')
add('25/26 Q3c five-a-side variant', factorial(5), '120')

# 5.3 inclusion and exclusion. The Ibibio and Efik figures are checked as a
# partition: the three regions must add back to the group exactly.
_both = 72 + 43 - 100
add('25/26 Q3a both', _both, '15')
add('25/26 Q3a Ibibio only', 72 - _both, '57')
add('25/26 Q3a Efik only', 43 - _both, '28')
add('25/26 Q3a regions total', (72 - _both) + _both + (43 - _both), '100')
add('25/26 Q3a redo both', 50 + 45 - 80, '15')
add('21/22 Q5b class size', 25 + 13 - 8, '30')
add('21/22 Q5b CS only', 25 - 8, '17')
add('21/22 Q5b Maths only', 13 - 8, '5')
add('21/22 Q5b redo variant', 30 + 20 - 12, '38')
add('incl-excl drill', 40 + 30 - 12, '58')

# 5.4 the binomial theorem.
add('row 4 sum', sum(comb(4, r) for r in range(5)), '16')
add('row 5 sum', sum(comb(5, r) for r in range(6)), '32')
add('C(4,2)', comb(4, 2), '6')
add('C(5,2)', comb(5, 2), '10')
add('(x+2)^4 x^3 coeff', comb(4, 1) * 2 ** 1, '8')
add('(x+2)^4 x^2 coeff', comb(4, 2) * 2 ** 2, '24')
add('(x+2)^4 x coeff', comb(4, 3) * 2 ** 3, '32')
add('(x+2)^4 constant', comb(4, 4) * 2 ** 4, '16')
add('(x+2)^4 sum at x=1', sum(comb(4, r) * 2 ** r for r in range(5)), '81')
add('(2x+1)^5 x^3 coeff', comb(5, 2) * 2 ** 3, '80')
add('(x+3)^4 x^2 coeff', comb(4, 2) * 3 ** 2, '54')


# ---------------------------------------------------------------- Part Six
# 6.1 degrees read off the worked figure. The figure is drawn by hand in SVG, so
# the degrees are recomputed here from the edge list the book says it shows, and
# the handshaking identity is asserted on both readings of the unreadable e6.
_fig61 = [('a', 'b'), ('b', 'c'), ('b', 'c'), ('c', 'c'), ('a', 'd')]
_deg61 = {}
for _u, _v in _fig61:
    _deg61[_u] = _deg61.get(_u, 0) + 1
    _deg61[_v] = _deg61.get(_v, 0) + 1
_deg61['e'] = 0
add('6.1 figure deg(b)', _deg61['b'], '3')
add('6.1 figure deg(c)', _deg61['c'], '4')      # the loop counts twice
add('6.1 figure size', len(_fig61), '5')

# 2020/2021 Q1(c): the e1 to e6 figure, on the reading the book states (e6 a
# loop at vertex 2) and on the alternative (e6 joining 2 to 3). Both must give a
# degree sum of twice the six edges, which is the check the answer prints.
def _degsum(edges):
    d = {}
    for u, v in edges:
        d[u] = d.get(u, 0) + 1
        d[v] = d.get(v, 0) + 1
    return d


_loop = [(1, 2), (1, 2), (1, 3), (2, 3), (2, 3), (2, 2)]
_alt = [(1, 2), (1, 2), (1, 3), (2, 3), (2, 3), (2, 3)]
_dl, _da = _degsum(_loop), _degsum(_alt)
add('20/21 Q1c deg(1)', _dl[1], '3')
add('20/21 Q1c deg(2) loop reading', _dl[2], '6')
add('20/21 Q1c deg(3) loop reading', _dl[3], '3')
add('20/21 Q1c degree sum', sum(_dl.values()), '12')
add('20/21 Q1c deg(2) other reading', _da[2], '5')
add('20/21 Q1c deg(3) other reading', _da[3], '4')
add('20/21 Q1c degree sum, other reading', sum(_da.values()), '12')

# 6.2 complete graphs. C(n, 2) is recomputed against a brute-force pair count so
# the formula and the listing cannot both be wrong in the same way.
def _pairs(n):
    return len([(a, b) for a in range(n) for b in range(a + 1, n)])


for _n, _shown in ((2, '1'), (3, '3'), (4, '6'), (5, '10'), (6, '15'), (7, '21')):
    add(f'edges of K{_n}', _pairs(_n), _shown)
    assert _pairs(_n) == comb(_n, 2) == _n * (_n - 1) // 2
add('20/21 Q1b five buildings', comb(5, 2), '10')
add('20/21 Q1b by listing', 4 + 3 + 2 + 1, '10')
add('21/22 Q2b four buildings', comb(4, 2), '6')
add('21/22 Q2b by listing', 3 + 2 + 1, '6')
add('K7 vertex degree', 7 - 1, '6')

# 6.3 the Handshaking theorem, and 2024/2025 Question Five. Part (a) is solved
# here by SEARCH rather than by repeating the book's algebra: every split of the
# remaining vertices between degree 3 and degree 4 is tried, and the gate asserts
# there is exactly one fit. If the book's x = 4 were wrong, or if the question
# admitted a second answer, this would say so.
_Q5_V, _Q5_E = 24, 30
_Q5_SUM = 2 * _Q5_E
_Q5_KNOWN = ((5, 4), (7, 1), (7, 2))     # (count, degree); pendant means degree 1
_Q5_used_v = sum(c for c, _ in _Q5_KNOWN)
_Q5_used_d = sum(c * d for c, d in _Q5_KNOWN)
_Q5_rem_v = _Q5_V - _Q5_used_v
_Q5_rem_d = _Q5_SUM - _Q5_used_d
_Q5_fits = [(x, _Q5_rem_v - x) for x in range(_Q5_rem_v + 1)
            if 4 * x + 3 * (_Q5_rem_v - x) == _Q5_rem_d]
assert len(_Q5_fits) == 1, f'24/25 Q5 has {len(_Q5_fits)} fits, not one'
_Q5_x, _Q5_y = _Q5_fits[0]
add('24/25 Q5 degree sum', _Q5_SUM, '60')
add('24/25 Q5 accounted vertices', _Q5_used_v, '19')
add('24/25 Q5 accounted degree', _Q5_used_d, '41')
add('24/25 Q5 remaining vertices', _Q5_rem_v, '5')
add('24/25 Q5 remaining degree', _Q5_rem_d, '19')
add('24/25 Q5 remainder of degree 4', _Q5_x, '4')
add('24/25 Q5 remainder of degree 3', _Q5_y, '1')
add('24/25 Q5a total degree 4', 5 + _Q5_x, '9')
add('24/25 Q5 inventory check',
    (5 + _Q5_x) * 4 + _Q5_y * 3 + 7 * 2 + 7 * 1, '60')
add('24/25 Q5b K24 degree', _Q5_V - 1, '23')
add('24/25 Q5b K5 degree', 5 - 1, '4')
add('24/25 Q5 redo remaining degree', 2 * 12 - (4 * 1 + 4 * 2), '12')

# 2023/2024 Q5(b): five cities each of degree 3. The obstruction is parity.
add('23/24 Q5b degree sum', 5 * 3, '15')
add('23/24 Q5b edges implied', 5 * 3 / 2, '7.5')
add('23/24 Q5b four cities works', 4 * 3, '12')
add('23/24 Q5b four cities edges', 4 * 3 // 2, '6')
add('23/24 Q5b six cities sum', 6 * 3, '18')
add('23/24 Q5b six cities edges', 6 * 3 // 2, '9')
add('handshaking drill 7 vertices degree 4', 7 * 4, '28')
add('handshaking drill edges', 7 * 4 // 2, '14')
add('data comm 40 nodes 6 ports', 40 * 6 // 2, '120')

# 6.4 digraphs. In and out degrees are recomputed from the arc list, and the two
# column totals must each equal the arc count, which is the check the book tells
# the reader to perform.
def _digraph(arcs):
    verts = sorted({v for arc in arcs for v in arc})
    out = {v: sum(1 for u, _ in arcs if u == v) for v in verts}
    inn = {v: sum(1 for _, w in arcs if w == v) for v in verts}
    assert sum(out.values()) == sum(inn.values()) == len(arcs)
    return out, inn


# The book's own clearly drawn figure in 6.4.
_o, _i = _digraph([('a', 'b'), ('b', 'a'), ('b', 'c'), ('c', 'd'),
                   ('d', 'c'), ('a', 'c')])
add('6.4 method figure arcs', 6, '6')
add('6.4 method out-degree c', _o['c'], '1')
add('6.4 method in-degree c', _i['c'], '3')

# The p,q,r,s digraph drawn beside the Handshaking-for-digraphs box.
_o2, _i2 = _digraph([('p', 'q'), ('q', 'r'), ('r', 's'), ('s', 'p'), ('p', 'r')])
add('6.4 pqrs out-degree p', _o2['p'], '2')
add('6.4 pqrs in-degree r', _i2['r'], '2')

# 2023/2024 Q5(c) on the reading the book states. Two arcs are flagged uncertain;
# the totals are asserted so a change to the reading cannot pass unnoticed.
_Q5C = ([('b', 'a')] + [('a', 'b')] * 2 + [('d', 'a')] * 2 + [('b', 'c')] * 2
        + [('d', 'c')] * 3 + [('a', 'c')] * 2 + [('b', 'd')])
_o3, _i3 = _digraph(_Q5C)
add('23/24 Q5c arc count', len(_Q5C), '13')
add('23/24 Q5c out-degree a', _o3['a'], '4')
add('23/24 Q5c out-degree b', _o3['b'], '4')
add('23/24 Q5c out-degree d', _o3['d'], '5')
add('23/24 Q5c in-degree a', _i3['a'], '3')
add('23/24 Q5c in-degree b', _i3['b'], '2')
add('23/24 Q5c in-degree c', _i3['c'], '7')
add('23/24 Q5c in-degree d', _i3['d'], '1')

# The alternative reading of the two crossing diagonals, which the book also
# prints: one arc a to c and one c to a instead of two a to c.
_ALT = ([('b', 'a')] + [('a', 'b')] * 2 + [('d', 'a')] * 2 + [('b', 'c')] * 2
        + [('d', 'c')] * 3 + [('a', 'c'), ('c', 'a')] + [('b', 'd')])
_o4, _i4 = _digraph(_ALT)
add('23/24 Q5c alt arc count', len(_ALT), '13')
add('23/24 Q5c alt out-degree a', _o4['a'], '3')
add('23/24 Q5c alt out-degree c', _o4['c'], '1')
add('23/24 Q5c alt in-degree c', _i4['c'], '6')
add('23/24 Q5c alt in-degree a', _i4['a'], '4')

# 6.5 adjacency matrices. Every printed entry of A squared is recomputed by
# actual matrix multiplication, because a hand-multiplied 4 by 4 is exactly the
# kind of thing that comes out plausible and wrong.
def _matmul(X, Y):
    n = len(X)
    return [[sum(X[i][k] * Y[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


_A65 = [[0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0]]
_A65_2 = _matmul(_A65, _A65)
_A65_3 = _matmul(_A65_2, _A65)
add('6.5 A edge count', sum(sum(r) for r in _A65) // 2, '4')
add('6.5 A2 entry (1,1)', _A65_2[0][0], '2')
add('6.5 A2 entry (3,3)', _A65_2[2][2], '3')

# A matrix cannot be checked the way a scalar is. "1 1 3 0" never appears as a
# string in the book, because each entry is its own table cell; and asserting
# that the character "3" appears somewhere in a 200-page book proves nothing at
# all. So the printed tables are PARSED back out of the HTML and compared cell by
# cell against the recomputation. This is the only check in this file that reads
# the book's structure rather than its text, and it is the only one strong enough
# for a grid of single digits.
def matrix_from(fname, header):
    """The 4 by 4 grid printed under `header` in content/<fname>, as ints."""
    import re
    with open(os.path.join(CONTENT, fname), encoding='utf-8') as fh:
        html = fh.read()
    at = html.find(header)
    if at == -1:
        return None
    table = html[at:html.find('</table>', at)]
    rows = []
    for tr in re.findall(r'<tr>(.*?)</tr>', table, re.S)[1:]:   # skip the head row
        cells = re.findall(r'<td>\s*(-?\d+)\s*</td>', tr)
        if cells:
            rows.append([int(c) for c in cells])
    return rows or None


# Grid checks report through their own list rather than through CHECKS, because
# a CHECKS entry has to name a string the book contains, and for a grid of single
# digits no such string carries information. Here the comparison IS the check.
MATRIX_CHECKS = []
MATRIX_PROBLEMS = []


def check_matrix(label, computed, fname, header):
    """Assert the book prints exactly this grid, cell by cell."""
    printed = matrix_from(fname, header)
    MATRIX_CHECKS.append(label)
    if printed is None:
        MATRIX_PROBLEMS.append(f'{label}: no table found in {fname} under '
                               f'{header[:40]!r}')
    elif printed != computed:
        MATRIX_PROBLEMS.append(f'{label}: the book prints {printed}, '
                               f'the recompute says {computed}')


check_matrix('6.5 adjacency matrix', _A65, 'p6_65.html',
             '<tr><th></th><th>1</th><th>2</th><th>3</th><th>4</th></tr>')
check_matrix('6.5 A squared', _A65_2, 'p6_65.html',
             '<tr><th>A<sup>2</sup></th>')
check_matrix('6.5 the less-than relation matrix',
             [[0, 1, 1], [0, 0, 1], [0, 0, 0]], 'p6_65.html',
             '<tr><th></th><th>1</th><th>2</th><th>3</th></tr>')
# The path matrix is all ones: every vertex reaches every other, so the graph is
# connected. Asserted rather than eyeballed off the sum of the powers.
_reach = [[1 if (_A65[i][j] or _A65_2[i][j] or _A65_3[i][j]) else 0
           for j in range(4)] for i in range(4)]
assert all(all(row) for row in _reach), '6.5 path matrix is not all ones'
check_matrix('6.5 path matrix', _reach, 'p6_65.html', '<tr><th>P</th>')
# Memory costs quoted in the answer to 25/26 Q6(a)(ii).
add('25/26 Q6aii matrix cells for 500', 500 ** 2, '250000')
add('25/26 Q6aii list cells for 500', 500 + 2 * 800, '2100')
add('25/26 Q6aii sparse illustration', 1000 ** 2, '1000000')

# 6.6 Euler and Hamilton. The Euler verdict is derived from the degrees rather
# than asserted, and the Euler path the book prints is walked edge by edge to
# prove it really uses each edge once.
def _euler_verdict(edges):
    d = _degsum(edges)
    return sum(1 for deg in d.values() if deg % 2)


_G66 = [(1, 2), (1, 3), (2, 3), (3, 4)]
add('6.6 odd-degree vertices', _euler_verdict(_G66), '2')
_walk = [4, 3, 1, 2, 3]
_used = sorted(tuple(sorted((_walk[i], _walk[i + 1]))) for i in range(len(_walk) - 1))
assert _used == sorted(tuple(sorted(e)) for e in _G66), \
    '6.6 the printed Euler path does not use each edge exactly once'
add('6.6 Euler path edge count', len(_used), '4')
# Konigsberg: four land masses, seven bridges, every degree odd.
_KONIG = [('A', 'B'), ('A', 'B'), ('A', 'C'), ('A', 'C'), ('A', 'D'),
          ('B', 'D'), ('C', 'D')]
_kd = _degsum(_KONIG)
assert sorted(_kd.values()) == [3, 3, 3, 5], f'Konigsberg degrees are {_kd}'
add('Konigsberg bridges', _WORD[len(_KONIG)], 'seven')
add('Konigsberg odd vertices', _WORD[_euler_verdict(_KONIG)], 'four')
add('Konigsberg degree sum', sum(_kd.values()), '14')
_ks = sorted(_kd.values())
add('Konigsberg degrees',
    ', '.join(str(d) for d in _ks[:-1]) + ' and ' + str(_ks[-1]),
    '3, 3, 3 and 5')
# After adding edge 2-4 the degree sequence changes but the Euler verdict does not.
_G66b = _G66 + [(2, 4)]
add('6.6 redo odd-degree vertices', _euler_verdict(_G66b), '2')
add('6.6 redo degree sequence',
    ', '.join(str(_degsum(_G66b)[v]) for v in (1, 2, 3, 4)), '2, 3, 3, 2')

# 6.7 planarity. The two verdicts are DERIVED from the bounds rather than
# asserted, so a wrong edge count in the book cannot agree with a wrong verdict.
def _planar_bound(v, e, triangle_free=False):
    """(bound, breaks_it). A graph breaking its bound is certainly non-planar."""
    bound = (2 * v - 4) if triangle_free else (3 * v - 6)
    return bound, e > bound


_k5_bound, _k5_breaks = _planar_bound(5, comb(5, 2))
_k33_bound, _k33_breaks = _planar_bound(6, 3 * 3, triangle_free=True)
_k33_general, _k33_general_breaks = _planar_bound(6, 3 * 3)
_k4_bound, _k4_breaks = _planar_bound(4, comb(4, 2))
_k6_bound, _k6_breaks = _planar_bound(6, comb(6, 2))
assert _k5_breaks and _k33_breaks and _k6_breaks, 'a non-planar graph passed its bound'
assert not _k4_breaks, 'K4 is planar and must satisfy its bound'
assert not _k33_general_breaks, \
    'the general bound must FAIL to settle K3,3; that is why the paper gives two'
add('K5 vertices', 5, '5')
add('K5 edges', comb(5, 2), '10')
add('K5 bound 3v-6', _k5_bound, '9')
add('K3,3 vertices', 3 + 3, '6')
add('K3,3 edges', 3 * 3, '9')
add('K3,3 bound 2v-4', _k33_bound, '8')
add('K3,3 general bound, too weak', _k33_general, '12')
add('K4 edges', comb(4, 2), '6')
add('K4 bound 3v-6', _k4_bound, '6')
add('K6 edges', comb(6, 2), '15')
add('K6 bound 3v-6', _k6_bound, '12')
# Euler's formula on the plane drawing of K4: v - e + f = 2 gives f = 4.
_k4_faces = 2 - 4 + comb(4, 2)
assert 4 - comb(4, 2) + _k4_faces == 2, "Euler's formula does not close on K4"
add('K4 faces by Euler', _k4_faces, '4')
add('K4 faces by inspection', 3 + 1, '4')

# 2021/2022 Q1(a): five sets described in set-builder form, listed by brute
# force rather than by hand, since two of the five are traps (one empty, one a
# singleton) and hand-listing is exactly where those get missed.
def _is_prime(k):
    return k > 1 and all(k % d for d in range(2, int(k ** 0.5) + 1))


add('21/22 Q1a(ii) primes under 20',
    ', '.join(str(k) for k in range(2, 20) if _is_prime(k)),
    '2, 3, 5, 7, 11, 13, 17, 19')
add('21/22 Q1a(ii) how many',
    _WORD[sum(1 for k in range(2, 20) if _is_prime(k))], 'eight')
_squares = [k * k for k in range(0, 100) if k * k < 100]
add('21/22 Q1a(iii) perfect squares',
    ', '.join(str(s) for s in _squares), '0, 1, 4, 9, 16, 25, 36, 49, 64, 81')
add('21/22 Q1a(iii) how many', _WORD[len(_squares)], 'ten')
add('21/22 Q1a(iii) without zero', _WORD[len(_squares) - 1], 'nine')
# (iv) is empty and (v) is a singleton: assert it rather than trusting the prose.
assert not [x for x in range(-100, 101) if x * x == 2], 'x^2 = 2 has an integer root?'
assert [x for x in range(-100, 101) if 2 * x == x] == [0], '2x = x is not just 0'
# ---------------------------------------------------------------- Part Seven
# 7.1 the terminology diagram, checked against e = v - 1 and Handshaking.
_T71 = [('a','b'), ('a','c'), ('b','d'), ('b','e'), ('c','f'), ('c','g'),
        ('e','h'), ('e','i')]
_T71_V = {v for edge in _T71 for v in edge}
assert len(_T71) == len(_T71_V) - 1, '7.1 figure is not a tree: e is not v - 1'
add('7.1 figure vertices', len(_T71_V), '9')
add('7.1 figure edges', len(_T71), '8')
add('7.1 figure degree sum', 2 * len(_T71), '16')
add('7.1 17-vertex tree edges', 17 - 1, '16')

# 7.2 the full m-ary formulas. Solved here from the leaf count, and then the
# whole tree is BUILT and walked to confirm the counts describe a real tree,
# rather than trusting the algebra twice.
def _full_mary(m, internal):
    """Vertices and leaves of a full m-ary tree with `internal` internal nodes,
    counted by construction: grow the tree one internal vertex at a time."""
    nodes, leaves = 1, 1          # start: a single vertex, which is a leaf
    for _ in range(internal):
        leaves += m - 1           # a leaf becomes internal and gains m children
        nodes += m
    return nodes, leaves


# The chain letter / convocation cards: m = 4, 100 leaves.
_M, _LEAVES = 4, 100
_i_chain = (_LEAVES - 1) // (_M - 1)
assert (_LEAVES - 1) % (_M - 1) == 0, 'the chain-letter leaf count is not attainable'
_n_chain, _l_chain = _full_mary(_M, _i_chain)
assert _l_chain == _LEAVES, f'construction gives {_l_chain} leaves, not {_LEAVES}'
add('chain letter senders', _i_chain, '33')
add('chain letter total seen', _n_chain, '133')
add('chain letter check i + l', _i_chain + _LEAVES, '133')
add('chain letter edges sent', _M * _i_chain, '132')
# The m = 3 variant the book says is impossible: (l - 1) must divide by m - 1.
assert (100 - 1) % (3 - 1) != 0, 'the m = 3 chain-letter variant IS attainable'
add('chain letter m=3 impossible', (100 - 1) / (3 - 1), '49.5')

# 2024/2025 Q6(b) vi: the quinary tree of height 3, both ways.
add('quinary height 3 leaves', 5 ** 3, '125')
_i_quin = 1 + 5 + 25                      # internal vertices on levels 0, 1, 2
_n_quin, _l_quin = _full_mary(5, _i_quin)
assert _l_quin == 5 ** 3, 'the two leaf formulas disagree on the quinary tree'
add('quinary internal vertices', _i_quin, '31')
add('quinary leaves by the other formula', _l_quin, '125')
add('quinary total vertices', _n_quin, '156')
add('binary height 4 leaves', 2 ** 4, '16')

# 2020/2021 Q4(a): the playoff. Counted by exhaustive recursion over the series,
# so the combination argument in the book is checked against the actual tree.
def _playoff(target=3):
    out = []

    def rec(a, b, seq):
        if a == target or b == target:
            out.append(seq)
            return
        rec(a + 1, b, seq + 'A')
        rec(a, b + 1, seq + 'B')

    rec(0, 0, '')
    return out


_series = _playoff()
_a_wins = [s for s in _series if s.count('A') == 3]
add('playoff total ways', len(_series), '20')
add('playoff A wins', len(_a_wins), '10')
add('playoff A in 3', sum(1 for s in _a_wins if len(s) == 3), '1')
add('playoff A in 4', sum(1 for s in _a_wins if len(s) == 4), '3')
add('playoff A in 5', sum(1 for s in _a_wins if len(s) == 5), '6')
assert len(_series) == 2 * (comb(2, 2) + comb(3, 2) + comb(4, 2)), \
    'the combination argument disagrees with the enumerated tree'
add('playoff naive wrong answer', 2 ** 5, '32')
add('playoff best of three', len(_playoff(2)), '6')

# 7.3 traversals. The three lists the book prints are generated from the tree
# structure recorded in the transcript, not copied from the book, and each is
# asserted to contain all 17 vertices exactly once.
_KIDS = {'a': ['b', 'c'], 'b': ['d', 'e', 'f'], 'e': ['j', 'k'], 'k': ['n', 'o'],
         'c': ['g', 'h', 'i'], 'h': ['l', 'm'], 'm': ['p', 'q']}
_ALL = sorted({'a'} | {c for cs in _KIDS.values() for c in cs})


def _preorder(v):
    return [v] + [x for c in _KIDS.get(v, []) for x in _preorder(c)]


def _postorder(v):
    return [x for c in _KIDS.get(v, []) for x in _postorder(c)] + [v]


def _inorder(v):
    """Rosen's general rule: leftmost subtree, then the root, then the rest.

    NOT the binary rule. Two vertices of this tree have three children, and
    applying "left, root, right" to them is the standard way to get this wrong.
    """
    cs = _KIDS.get(v, [])
    if not cs:
        return [v]
    out = _inorder(cs[0]) + [v]
    for c in cs[1:]:
        out += _inorder(c)
    return out


for _name, _walk in (('preorder', _preorder('a')),
                     ('inorder', _inorder('a')),
                     ('postorder', _postorder('a'))):
    assert sorted(_walk) == _ALL, f'{_name} does not list every vertex once'
    add(f'24/25 Q6a {_name}', ', '.join(_walk), ', '.join(_walk))
add('24/25 Q6a vertex count', len(_ALL), '17')
assert _preorder('a')[0] == 'a' and _postorder('a')[-1] == 'a', \
    'preorder must start at the root and postorder must end there'

# The expression (3 - 4 * 2) - (5 + (5 - 2)): tree, notations and value. The
# postfix string the book prints is EVALUATED here with a stack, so a wrongly
# built tree cannot pass by looking plausible.
_POSTFIX = ['3', '4', '2', '*', '-', '5', '5', '2', '-', '+', '-']


def _eval_postfix(tokens):
    st = []
    for t in tokens:
        if t.isdigit():
            st.append(int(t))
        else:
            b, a = st.pop(), st.pop()
            st.append(a + b if t == '+' else a - b if t == '-' else a * b)
    assert len(st) == 1, 'the postfix expression is malformed'
    return st[0]


add('24/25 Q6b expression value', _eval_postfix(_POSTFIX), '-13')
assert _eval_postfix(_POSTFIX) == (3 - 4 * 2) - (5 + (5 - 2)), \
    'the printed postfix form does not evaluate to the printed expression'
add('24/25 Q6b left bracket value', 3 - 4 * 2, '-5')
add('24/25 Q6b right bracket value', 5 + (5 - 2), '8')
# The trap table: two infix expressions differing only by brackets.
add('7.3 trap without brackets', 3 - 4 * 2, '-5')
add('7.3 trap with brackets', (3 - 4) * 2, '-2')

add('21/22 Q1a redo x^2 < 5',
    ', '.join(str(x) for x in range(-9, 10) if x * x < 5),
    '-2, -1, 0, 1, 2')

# 6.8 the travelling salesman. The book prints all twelve tours with their
# totals, so all twelve are recomputed here from the distance table and the
# printed table is parsed back out and compared row for row. Nothing about this
# answer is taken on trust: not the optimum, not the ordering, not the claim
# that nearest neighbour happens to find it.
_MILES_RAW = {
    ('GR', 'S'): 113, ('GR', 'K'): 56, ('GR', 'T'): 167, ('GR', 'D'): 147,
    ('K', 'S'): 137, ('K', 'D'): 135, ('K', 'T'): 133,
    ('S', 'T'): 142, ('S', 'D'): 98, ('D', 'T'): 58,
}
_MILES = {}
for (_a, _b), _w in _MILES_RAW.items():
    _MILES[(_a, _b)] = _MILES[(_b, _a)] = _w
_CITIES = ['GR', 'S', 'K', 'T', 'D']
assert len(_MILES_RAW) == comb(5, 2), 'the five-city map must have all 10 edges'


def _tours(start='D'):
    """Every distinct tour from `start`, as (total, route), cheapest first.

    A tour and its reverse use the same edges, so only one of each pair is kept.
    That is the same halving the book explains as (n - 1)!/2.
    """
    rest = [c for c in _CITIES if c != start]
    seen, out = set(), []
    for order in permutations(rest):
        if order[::-1] in seen:
            continue
        seen.add(order)
        route = (start,) + order + (start,)
        total = sum(_MILES[(route[i], route[i + 1])] for i in range(len(route) - 1))
        out.append((total, route))
    return sorted(out)


_TOURS = _tours()
assert len(_TOURS) == factorial(4) // 2 == 12, f'{len(_TOURS)} tours, expected 12'
_best_total, _best_route = _TOURS[0]
add('TSP tour count', len(_TOURS), '12')
add('TSP minimum', _best_total, '458')
add('TSP worst', _TOURS[-1][0], '728')
add('TSP best route', ' '.join(_best_route), 'D S GR K T D')
add('TSP six cities', factorial(5) // 2, '60')
add('TSP ten cities', factorial(9) // 2, '181440')

# Nearest neighbour from Detroit. The book claims it "happens to" find the
# optimum here; that claim is checked, not asserted.
_cur, _unv, _nn_total = 'D', {c for c in _CITIES if c != 'D'}, 0
_nn_route = ['D']
while _unv:
    _nxt = min(_unv, key=lambda c: _MILES[(_cur, c)])
    _nn_total += _MILES[(_cur, _nxt)]
    _nn_route.append(_nxt)
    _unv.discard(_nxt)
    _cur = _nxt
_nn_total += _MILES[(_cur, 'D')]
_nn_route.append('D')
assert _nn_total == _best_total, \
    'the book says nearest neighbour finds the optimum here; it does not'
assert _nn_route[::-1] == list(_best_route), \
    'the book says the NN route is the optimal tour reversed; it is not'
add('TSP nearest neighbour total', _nn_total, '458')
# The route itself is asserted above rather than string-matched: the book prints
# it as a five-row decision table with full city names, not as a sequence.
add('TSP nearest neighbour first leg', _MILES[('D', _nn_route[1])], '58')
add('TSP nearest neighbour last leg', _MILES[(_nn_route[-2], 'D')], '98')

# Parse the printed twelve-row table and compare it to the recomputation.
def _printed_tours():
    import re
    with open(os.path.join(CONTENT, 'p6_68.html'), encoding='utf-8') as fh:
        html = fh.read()
    at = html.find('<tr><th>Tour</th>')
    if at == -1:
        return None
    rows = []
    for tr in re.findall(r'<tr>(.*?)</tr>',
                         html[at:html.find('</table>', at)], re.S)[1:]:
        cells = re.findall(r'<td>(.*?)</td>', tr, re.S)
        if len(cells) == 3:
            route = ' '.join(cells[0].split())
            legs = [int(n) for n in re.findall(r'\d+', cells[1])]
            total = int(re.sub(r'<[^>]+>', '', cells[2]).strip())
            rows.append((route, legs, total))
    return rows


_printed = _printed_tours()
if _printed is None:
    MATRIX_PROBLEMS.append('6.8: the twelve-tour table was not found in p6_68.html')
else:
    MATRIX_CHECKS.append('6.8 the twelve printed tours')
    if len(_printed) != 12:
        MATRIX_PROBLEMS.append(f'6.8: the book prints {len(_printed)} tours, not 12')
    # A tour and its reverse are the same route, so compare them in a canonical
    # form. Demanding one particular direction would fail a correct table for
    # writing "D K GR T S D" where the recomputation happened to enumerate
    # "D S T GR K D", which is the identical circuit driven the other way.
    def _canon(seq):
        inner = tuple(seq[1:-1])
        return min(inner, inner[::-1])

    for (route, legs, total), (want_total, want_route) in zip(_printed, _TOURS):
        if _canon(route.split()) != _canon(want_route):
            MATRIX_PROBLEMS.append(f'6.8: printed tour {route!r} is out of order; '
                                   f'expected {" ".join(want_route)!r}')
        elif sum(legs) != total:
            MATRIX_PROBLEMS.append(f'6.8: tour {route} adds {legs} to {sum(legs)} '
                                   f'but prints {total}')
        elif total != want_total:
            MATRIX_PROBLEMS.append(f'6.8: tour {route} prints {total}, '
                                   f'recompute says {want_total}')


# ---------------------------------------------------------------- Part Nine
# Every value below is pinned to the file that prints it, and the ones whose
# printed form is short enough to collide with unrelated digits elsewhere are
# pinned to a place within that file as well. See the note above CHECKS: three
# of these passed a corrupted book before `where` and `near` existed.
P9A, P9B, P9C, P9D = 'p9_proof.html', 'p9_92.html', 'p9_93.html', 'p9_94.html'

# 9.1 Proof techniques. Every proof here is symbolic, so the only numbers to
# check are the arithmetic the proofs lean on. They are checked anyway, because
# a proof that substitutes a value and gets it wrong is worse than one that
# never substitutes at all: a reader trusts a printed evaluation.
add('9.1 x=10 in the cubic', 10 ** 3 - 7 * 10 ** 2 + 10 - 7,
    '1000 - 700 + 10 - 7 = <b>303</b>', P9A)
add('9.1 156 as 5q+r', 156 // 5, '156 = 5 × 31 + 1', P9A)
add('9.1 n^3-n at n=3', 3 ** 3 - 3, '27 - 3 = 24', P9A)
add('9.1 n^3-n at n=4', 4 ** 3 - 4, '64 - 4 = 60', P9A)
# The convention trap: n^2+3n+2 = (n+1)(n+2), prime only at n = 0.
add('9.1 n^2+3n+2 at n=0', 0 ** 2 + 3 * 0 + 2, '0 + 0 + 2 = <b>2</b>', P9A)
add('9.1 n^2+3n+2 at n=1', 1 + 3 + 2, 'n = 1 gives 6', P9A)
add('9.1 n^2+3n+2 at n=2', 4 + 6 + 2, 'n = 2 gives 12', P9A)
add('9.1 n^2+3n+2 at n=3', 9 + 9 + 2, 'n = 3 gives 20', P9A)
# The two expansions the trap box corrects. The book must print the RIGHT one
# in its own proof and quote the wrong one only as the defect being named.
add('9.1 correct even-case factor', 8 // 2, '2(4k<sup>3</sup> - k)', P9A)
add('9.1 correct cube expansion', 3 * 2 ** 2, '8k<sup>3</sup> + 12k<sup>2</sup> + 6k + 1', P9A)

# 9.2 Induction. The claims are general; these are the evaluated instances the
# book prints, which are exactly the places an induction proof can go wrong.
add('9.2 sum to 100', sum(range(1, 101)), '100 × 101 / 2 = <b>5050</b>', P9B)
add('9.2 sum to 101', sum(range(1, 102)), '101 × 102 / 2 = 5151', P9B)
add('9.2 the step at k=100', 5050 + 101, '5050 + 101 = <b>5151</b>', P9B)
add('9.2 odd sum to 4 terms', 1 + 3 + 5 + 7, '1 + 3 + 5 + 7 = <b>16</b>', P9B)
add('9.2 n^3+2n at n=1', 1 + 2, '1 + 2 =\n      <b>3</b>'.replace('\n      ', ' '), P9B)
add('9.2 n^3+2n at n=2', 8 + 4, '8 + 4 = <b>12</b>', P9B)
add('9.2 n^3+2n at n=3', 27 + 6, '27 + 6 = <b>33</b>', P9B)
add('9.2 n^3+2n at n=4', 64 + 8, '64 + 8 = <b>72</b>', P9B)
add('9.2 6^n-1 at n=1', 6 ** 1 - 1, 'n = 1 gives <b>5</b>', P9B)
add('9.2 6^n-1 at n=2', 6 ** 2 - 1, 'n = 2 gives <b>35</b>', P9B)
add('9.2 6^n-1 at n=3', 6 ** 3 - 1, 'n = 3 gives <b>215</b>', P9B)
add('9.2 the 30j+5 step', 6 * 5, '30j + 5 = 5(6j + 1)', P9B)
# The table that justifies starting the inequality at 5, row by row. Each row is
# asserted whole, so a single wrong cell cannot hide behind a digit elsewhere.
for _n in (1, 2, 3, 4, 5, 6):
    _row = f'<td>{_n}</td><td>{_n ** 2}</td><td>{2 ** _n}</td>'
    add(f'9.2 inequality table n={_n}', _row, _row, P9B)

# 9.3 Sequences. The arithmetic and geometric progressions the book works.
add('9.3 AP 10th term', 7 + 9 * 5, '7 + 45 = <b>52</b>', P9C)
add('9.3 AP listed to ten', 7 + 9 * 5,
    '7, 12, 17, 22, 27, 32, 37, 42, 47, <b>52</b>', P9C)
add('9.3 AP general term', 5 * 1 + 2, '7 + 5n - 5 = <b>5n + 2</b>', P9C)
add('9.3 AP sum of 10', 10 * (7 + 52) // 2, '10 × 59 / 2 = <b>295</b>', P9C)
add('9.3 AP 2..20 sum', sum(range(2, 21, 2)), '10 × (2 + 20) / 2 = <b>110</b>', P9C)
add('9.3 GP 10th term', 4 * 2 ** 9, '2<sup>11</sup> = <b>2048</b>', P9C)
add('9.3 2^10-1', 2 ** 10 - 1, '4 × 1023 = <b>4092</b>', P9C)
add('9.3 GP sum of 10', 4 * (2 ** 10 - 1), '4 × 1023 = <b>4092</b>', P9C)
add('9.3 infinite GP sum', '3/2', '1 / (2/3) = <b>3/2</b>', P9C)
add('9.3 sum of first 5', sum(range(1, 6)), '5 × 6 / 2 = 15', P9C)
add('9.3 sum of first 5 squares', sum(i * i for i in range(1, 6)),
    '5 × 6 × 11 / 6 = 55', P9C)
add('9.3 sum of first 5 cubes', sum(i ** 3 for i in range(1, 6)),
    '15<sup>2</sup> = 225', P9C)
add('9.3 geometric row at r=2,n=5', sum(2 ** i for i in range(6)),
    '2<sup>6</sup> - 1 = 63', P9C)
add('9.3 10*11*21', 10 * 11 * 21, f'{10 * 11 * 21} / 6', P9C)
add('9.3 sum of first 10 squares', sum(i * i for i in range(1, 11)),
    '2310 / 6 = <b>385</b>', P9C)
add('9.3 sum of first 10 inside the split', sum(range(1, 11)),
    '3 × 55 + 20', P9C)
add('9.3 sum of 3k+2 to 10', sum(3 * k + 2 for k in range(1, 11)),
    '165 + 20 = <b>185</b>', P9C)
# The "times three plus two" table that finds the rule behind 1, 5, 17, ...
_SEQ317 = [1, 5, 17, 53, 161, 485]
for _i in range(1, len(_SEQ317)):
    add(f'9.3 rule-finding row {_i + 1}', 3 * _SEQ317[_i - 1] + 2,
        f'<td>3 × {_SEQ317[_i - 1]} = {3 * _SEQ317[_i - 1]}</td>'
        f'<td>{_SEQ317[_i]}</td><td>2</td>', P9C)


# 9.4 Recurrences. Each closed form is generated from the RELATION here and the
# whole printed table row is asserted, so a sign error in the solution or a
# mistyped cell cannot pass by matching two digits somewhere else in the book.
def _iterate(first, step, n):
    """The first n terms from initial values `first` and a step function."""
    terms = list(first)
    while len(terms) < n:
        terms.append(step(terms))
    return terms


_hanoi = _iterate([1], lambda t: 2 * t[-1] + 1, 5)
for _i in range(2, 6):
    add(f'9.4 Hanoi row {_i}', _hanoi[_i - 1],
        f'<td>2 × {_hanoi[_i - 2]} + 1</td><td>{_hanoi[_i - 1]}</td>'
        f'<td>{2 ** _i} - 1</td>', P9D)
add('9.4 Hanoi closed form', 2 ** 5 - 1, '<td>31</td><td>32 - 1</td>', P9D)

# a_n = 3a_(n-1) + 2, a_1 = 1, printed as 1, 5, 17, 53, 161, 485.
_a32 = _iterate([1], lambda t: 3 * t[-1] + 2, 6)
for _i, _v in enumerate(_a32, start=1):
    assert _v == 2 * 3 ** (_i - 1) - 1
    add(f'9.4 3a+2 row {_i}', _v,
        f'<td>2 × {3 ** (_i - 1)} - 1</td><td>{_v}</td><td>{_v}</td>', P9D)

# a_n = 5a_(n-1) - 6a_(n-2), a_0 = 1, a_1 = 4, closed form 2*3^n - 2^n.
_d = _iterate([1, 4], lambda t: 5 * t[-1] - 6 * t[-2], 5)
for _i, _v in enumerate(_d):
    assert _v == 2 * 3 ** _i - 2 ** _i
    if _i >= 2:
        add(f'9.4 distinct-root relation row {_i}', _v,
            f'<td>5 × {_d[_i - 1]} - 6 × {_d[_i - 2]} = {_v}</td>', P9D)
    add(f'9.4 distinct-root formula row {_i}', _v,
        f'<td>{2 * 3 ** _i} - {2 ** _i} = {_v}</td>', P9D)

# a_n = 10a_(n-1) - 25a_(n-2), a_0 = 3, a_1 = 17, closed form 3*5^n + 2n*5^(n-1).
_r = _iterate([3, 17], lambda t: 10 * t[-1] - 25 * t[-2], 4)
for _i, _v in enumerate(_r):
    if _i:
        assert _v == 3 * 5 ** _i + 2 * _i * 5 ** (_i - 1)
    if _i >= 2:
        add(f'9.4 repeated-root relation row {_i}', _v,
            f'<td>10 × {_r[_i - 1]} - 25 × {_r[_i - 2]} = {_v}</td>', P9D)
        add(f'9.4 repeated-root formula row {_i}', _v,
            f'<td>{3 * 5 ** _i} + {2 * _i * 5 ** (_i - 1)} = {_v}</td>', P9D)
add('9.4 repeated-root at n=1', _r[1], '<td>15 + 2 = 17</td>', P9D)
add('9.4 B is two fifths', Fraction(17, 5) - 3,
    'B = 17/5 - 3 = <b>2/5</b>', P9D)
add('9.4 Fibonacci discriminant', (-1) ** 2 - 4 * 1 * -1,
    '4ac = 1 + 4 = 5', P9D)
add('9.4 Fibonacci ratio 13/8', 13 / 8, '13 / 8 = 1.625', P9D)

# ---------------------------------------------------------------- Part Ten
P10A, P10B = 'p10_stats.html', 'p10_102.html'

# 10.1 The ten scores the section works end to end. Recomputed with the standard
# library rather than trusted from the table the book prints, and every row of
# the deviation table is asserted whole.
_SCORES = [21, 15, 33, 12, 21, 18, 24, 15, 20, 21]
_srt = sorted(_SCORES)
_mean = sum(_SCORES) / len(_SCORES)
add('10.1 sorted data', ', '.join(str(x) for x in _srt),
    '12, 15, 15, 18, 20, 21, 21, 21, 24, 33', P10A)
add('10.1 total', sum(_SCORES), '21 + 24 + 33 = <b>200</b>', P10A)
add('10.1 mean', int(_mean), '200 / 10 = <b>20</b>', P10A)
add('10.1 median', (_srt[4] + _srt[5]) / 2, '(20 + 21) / 2 = <b>20.5</b>', P10A)
add('10.1 mode', max(set(_SCORES), key=_SCORES.count), 'mode = <b>21</b>', P10A)
add('10.1 range', max(_SCORES) - min(_SCORES), 'range = 33 - 12 = <b>21</b>', P10A)
_ss = sum((x - _mean) ** 2 for x in _SCORES)
for _x in _srt:
    _dev = int(_x - _mean)
    add(f'10.1 deviation row for {_x}', f'<td>{_x}</td><td>{_dev}</td>',
        f'<td>{_x}</td><td>{_dev}</td><td>{_dev * _dev}</td>', P10A)
add('10.1 sum of squared deviations', int(_ss), '<b>306</b>', P10A)
add('10.1 population variance', round(_ss / len(_SCORES), 4),
    '306 / 10 =\n      <b>30.6</b>'.replace('\n      ', ' '), P10A)
add('10.1 sample variance', int(_ss / (len(_SCORES) - 1)), '306 / 9 = <b>34</b>', P10A)
add('10.1 population sd', round((_ss / len(_SCORES)) ** 0.5, 2),
    '&#8730;30.6 &#8776; <b>5.53</b>'.replace('&#8730;', chr(0x221A))
    .replace('&#8776;', chr(0x2248)), P10A)
add('10.1 sample sd', round((_ss / (len(_SCORES) - 1)) ** 0.5, 2),
    '34 ' + chr(0x2248) + ' <b>5.83</b>', P10A)
# The outlier variant: 33 replaced by 133.
_OUT = [133 if x == 33 else x for x in _SCORES]
add('10.1 outlier total', sum(_OUT), 'new total = 300', P10A)
add('10.1 outlier mean', sum(_OUT) // len(_OUT), 'mean becomes <b>30</b>', P10A)
# The frequency table: 20 assignments, 36 errors in total.
_FREQ = [(0, 3), (1, 5), (2, 7), (3, 3), (4, 2)]
_run = 0
for _x, _f in _FREQ:
    _run += _f
    add(f'10.1 frequency row {_x}', _x * _f,
        f'<td>{_x}</td><td>{_f}</td><td>{_x * _f}</td><td>{_run}</td>', P10A)
add('10.1 frequency count', sum(f for _, f in _FREQ), '<b>20</b></td><td><b>36</b>', P10A)
add('10.1 frequency mean', sum(x * f for x, f in _FREQ) / sum(f for _, f in _FREQ),
    '36 / 20 = <b>1.8</b>', P10A)

# 10.2 Probability. Each is a count divided by a count, so both halves are
# recomputed and the printed fraction is checked where it is printed.
add('10.2 three tosses outcomes', 2 ** 3, '2<sup>3</sup> = <b>8</b>', P10B)
_TOSS = ', '.join(''.join(t) for t in product('HT', repeat=3))
add('10.2 the eight outcomes', _TOSS, _TOSS, P10B)
add('10.2 exactly two heads', Fraction(3, 8),
    'P(exactly two heads) = <b>3/8</b>', P10B)
add('10.2 by combination', comb(3, 2), 'C(3, 2) = 3', P10B)
add('10.2 an ace', Fraction(4, 52), 'P(ace) = 4 / 52 = <b>1/13</b>', P10B)
add('10.2 a diamond', Fraction(13, 52), 'P(diamond) = 13 / 52 = <b>1/4</b>', P10B)
add('10.2 a red queen', Fraction(2, 52), 'P(red queen) = 2 / 52 = <b>1/26</b>', P10B)
add('10.2 ace or diamond', Fraction(4, 52) + Fraction(13, 52) - Fraction(1, 52),
    '4/52 + 13/52 - 1/52 = <b>16/52 = 4/13</b>', P10B)
add('10.2 the double count', 4 + 13, 'would give 17/52', P10B)
add('10.2 marbles total', 7 + 3 + 4, '7 + 3 + 4 = <b>14</b>', P10B)
add('10.2 P(not blue)', Fraction(10, 14), 'P(not blue) = 10 / 14 = <b>5/7</b>', P10B)
add('10.2 P(blue)', Fraction(4, 14), 'P(blue) = 4 / 14 = 2/7', P10B)
add('10.2 complement route', Fraction(10, 14), '1 - 2/7 = <b>5/7</b>', P10B)
add('10.2 committees of 4 from 10', comb(10, 4),
    'total committees = C(10, 4) = <b>210</b>', P10B)
add('10.2 committees with no boy', comb(4, 4),
    'committees with no boy = C(4, 4) = <b>1</b>', P10B)
add('10.2 committees with a boy', comb(10, 4) - comb(4, 4),
    '210 - 1 = <b>209</b>', P10B)
add('10.2 P(at least one boy)', Fraction(209, 210),
    'P(at least one boy) = <b>209 / 210</b>', P10B)
add('10.2 conditional cycle/bike', round(0.3 / 0.5, 4),
    '0.3 / 0.5 = <b>0.6</b>', P10B)
add('10.2 two defectives', Fraction(3, 9) * Fraction(2, 8),
    '(3/9) × (2/8) = 6 / 72 = <b>1/12</b>', P10B)
add('10.2 the independence trap', Fraction(3, 9) * Fraction(3, 9),
    '(3/9) × (3/9) = 1/9', P10B)
add('10.2 defectives by counting', comb(3, 2), 'C(3, 2) = 3, and', P10B)
add('10.2 any two of nine', comb(9, 2), 'C(9, 2) = 36', P10B)
add('10.2 counting cross-check', Fraction(3, 36), '3 / 36 = 1/12', P10B)
add('10.2 Bayes P(F) from A', round(0.02 * 0.6, 4), '0.012 + 0.020', P10B)
add('10.2 Bayes P(F)', round(0.02 * 0.6 + 0.05 * 0.4, 4), '= <b>0.032</b>', P10B)
add('10.2 Bayes P(B|F)', round((0.05 * 0.4) / (0.02 * 0.6 + 0.05 * 0.4), 4),
    '0.020 / 0.032 = <b>0.625</b>', P10B)
add('10.2 Bayes as a percentage', 62.5, 'Answer: 62.5 per cent', P10B)
add('10.2 Bayes P(A|F)', round((0.02 * 0.6) / 0.032, 3), '0.012 / 0.032 = 0.375', P10B)
add('10.2 the two posteriors sum to one',
    int(round((0.05 * 0.4) / 0.032 + (0.02 * 0.6) / 0.032)),
    '0.625 + 0.375 = 1', P10B)
add('10.2 Bayes even split P(F)', round(0.02 * 0.5 + 0.05 * 0.5, 4),
    '0.05 &#215; 0.5 = 0.035'.replace('&#215;', chr(0xD7)), P10B)


# ---------------------------------------------------------------- reporting
def norm(s):
    return str(s).replace(' ', '').replace(',', '')


def report(_ignored_html=None):
    whole = book_text()
    fails = []
    scoped = 0
    for label, computed, shown, where in CHECKS:
        if where is None:
            haystack = whole
        else:
            scoped += 1
            haystack = file_text(where)
        if shown not in haystack:
            fails.append(f'{label}: {where or "the book"} does not contain '
                         f'{shown!r} (recompute says {computed})')
            continue
        want, got = norm(computed), norm(shown)
        if want not in got and got not in want:
            fails.append(f'{label}: book shows {shown!r} but recompute is {computed}')

    fails.extend(MATRIX_PROBLEMS)

    print(f'NUMERIC GATE: {len(CHECKS)} worked values and '
          f'{len(MATRIX_CHECKS)} printed grids recomputed '
          f'({scoped} pinned to the one file that prints them)')
    if fails:
        print('NUMERIC GATE: FAIL')
        for f in fails:
            print('  x ' + f)
        return False
    print('  . every worked number matches an independent recomputation')
    print('  . every recomputed value appears in the manual')
    return True


if __name__ == '__main__':
    sys.exit(0 if report() else 1)
