"""Numeric gate: recompute every worked number, then prove the manual prints it.

This is IFT222's analogue of "run every listing" on a code course. Architecture is
folklore-ridden with off-by-one bit errors, bias mistakes and truncation slips, and a
worked answer nobody recomputed is a guess wearing a fact's clothes (MANUAL_METHODOLOGY
item 4 and 8). So for every worked result in the manual we:

  1. compute it here from first principles, with the standard library, not by copying
     the number out of the HTML, and
  2. assert the string the manual actually prints for it is present in the content.

A check is (label, computed_value, shown_in_book). The gate fails if the recompute
disagrees with what we expected to write, OR if that string is missing from the book
(a typo in the HTML). Binary and separators are normalised away, so "0000 1100 1100"
and "000011001100", and "41 806" and "41806", match. The book writes minus as the
entity &#8722; (U+2212); both it and an ASCII '-' read the same here. Control-tested
by flipping a digit in the HTML: the gate then fails on that value.
"""
import html as _html
import os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')


def book_text():
    parts = []
    for name in sorted(os.listdir(CONTENT)):
        if name.endswith('.html'):
            with open(os.path.join(CONTENT, name), encoding='utf-8') as fh:
                parts.append(fh.read())
    text = _html.unescape('\n'.join(parts))
    return text.replace(chr(0x2212), '-').replace(chr(0x00A0), ' ')


# ---- independent recomputation helpers ----
def to_hex_f(x):
    return format(struct.unpack('>I', struct.pack('>f', x))[0], '08X')

def from_hex_f(h):
    return struct.unpack('>f', struct.pack('>I', int(h, 16)))[0]

def twos(n, bits):
    return format(n % (1 << bits), f'0{bits}b')

def sign_mag(n, bits):
    return ('1' if n < 0 else '0') + format(abs(n), f'0{bits-1}b')

def ones(n, bits):
    if n >= 0:
        return format(n, f'0{bits}b')
    return ''.join('1' if c == '0' else '0' for c in format(abs(n), f'0{bits}b'))


# ---- the checks: (label, computed, shown-in-book) ----
CHECKS = []
def add(label, computed, shown):
    CHECKS.append((label, computed, shown))

# Foundations
add('1011B', int('1011', 2), '11')
add('10110B', int('10110', 2), '22')
add('A34EH->dec', int('A34E', 16), '41 806')
add('13->bin', bin(13)[2:], '1101')
add('11010110B->hex', format(int('11010110', 2), 'X'), 'D6')
add('2FH->bin', format(int('2F', 16), '08b'), '0010 1111')
add('2^10', 2**10, '1024')
add('binhex 6B5D', format(int('110101101011101', 2), 'X'), '6B5D')

# Unit 2: signed representations, 12-bit
add('204 in 12b', format(204, '012b'), '0000 1100 1100')
add('-139 sign-mag 12b', sign_mag(-139, 12), '1000 1000 1011')
add('-139 ones 12b', ones(-139, 12), '1111 0111 0100')
add('-139 twos 12b', twos(-139, 12), '1111 0111 0101')
# Unit 2: 16-bit twos complement (25/26 Q1c)
add('16b range low', -(2**15), '-32768')
add('16b range high', 2**15 - 1, '32767')
add('-182 twos16', twos(-182, 16), '1111 1111 0100 1010')
add('-182 hex', format(int(twos(-182, 16), 2), '04X'), 'FF4A')
add('487 twos16', twos(487, 16), '0000 0001 1110 0111')
add('487 hex', format(int(twos(487, 16), 2), '04X'), '01E7')
add('-1023 twos16', twos(-1023, 16), '1111 1100 0000 0001')
add('-1023 hex', format(int(twos(-1023, 16), 2), '04X'), 'FC01')
add('(-182)+487 dec', -182 + 487, '305')
add('(-182)+487 hex', format((-182 + 487) % (1 << 16), '04X'), '0131')
# Unit 2: overflow, end-around, image
add('214+65 true', 214 + 65, '279')
add('214+65 wrap', (214 + 65) % 256, '23')
add('214+65 wrap bin', format((214 + 65) % 256, '08b'), '0001 0111')
add('153-142 result', 153 - 142, '11')
add('153-142 bin10', format(153 - 142, '010b')[2:], '0000 1011')
add('image pixels', '10 111 500', '10 111 500')
add('image bytes', '1 263 937.5', '1 263 937.5')

# Unit 3: IEEE-754
add('-452.25->hex', to_hex_f(-452.25), 'C3E22000')
add('-1240.56 trunc hex', 'C49B11EB', 'C49B11EB')     # hand truncation
add('-1240.56 round hex', to_hex_f(-1240.56), 'C49B11EC')
add('C4F2E000->dec', int(from_hex_f('C4F2E000')), '-1943')
add('X=C1400000', int(from_hex_f('C1400000')), '-12')
add('Y=42100000', int(from_hex_f('42100000')), '36')
add('Z=41400000', int(from_hex_f('41400000')), '12')

# Unit 4: instruction counts + bytes + effective addresses
add('3addr count simple', 3, '3 instructions')
add('0addr count simple', 8, '8 instructions')
add('3addr bytes expr', 7 * 7, '49')
add('2addr bytes expr', 12 * 5, '60')
add('1addr bytes expr', 17 * 3, '51')
add('0addr bytes expr', 8 * 3 + 1 * 3 + 7 * 1, '34')
add('direct operand', 4500, 'M[1200] = 4500')
add('indirect operand', 999, 'M[4500] = 999')
add('reg-indirect operand', 6000, 'M[1500] = 6000')
add('relative EA', 7000 + 1200, 'PC + 1200 = 8200')

# Module Two: processor components + performance
add('2^18 addr space', 2**18, '262 144')
add('4GB/2B word addr bits', (2**32 // 2).bit_length() - 1, '31')
add('2^20 = 1MB', 2**20, '1 048 576')
# CPU performance (25/26 Q1d)
_mix = [(0.40, 1), (0.20, 1), (0.15, 2), (0.10, 4), (0.10, 3), (0.05, 2)]
_cpi = round(sum(f * c for f, c in _mix), 2)
add('Q1d avg CPI', _cpi, '1.70')
add('Q1d total cycles', int(_cpi * 1_000_000), '1 700 000')
add('Q1d new CPI', round(_cpi - 0.10 * 4 + 0.10 * 2, 2), '1.50')
add('Q1d improvement', round((_cpi - 1.5) / _cpi * 100, 2), '11.76')
# CPI with penalties (25/26 Q1b, stated reading)
_cpi1b = round(1 + 0.20 * 2 + 0.35 * (2 + 0.10 * 4) + 0.05 * 4, 2)
add('Q1b clock', 6 + 1, '7 ns')
add('Q1b actual CPI', _cpi1b, '2.44')
add('Q1b nonpipe s', 20_000_000 * 25 / 1e9, '0.5 s')
# Amdahl (25/26 Q3c)
add('Amdahl speedup', round(1 / ((1 - 0.85) + 0.85 / 10), 2), '4.26')
# Pipelining (25/26 Q5b)
add('Q5b cycle', max(60, 50, 90, 80) + 10, '100 ns')
add('Q5b nonpipe1', 60 + 50 + 90 + 80, '280 ns')
add('Q5b ideal speedup', round((60 + 50 + 90 + 80) / (90 + 10), 1), '2.8')
add('Q5b pipe500', (4 + 499) * 100, '50 300')
add('Q5b seq500', 500 * 280, '140 000')
# Pipelining (20/21 Q1b)
add('20/21 nonpipe4', 4 * (8 + 9 + 11 + 13 + 16), '228')
add('20/21 pipe4', (5 + 3) * 16, '128')
add('20/21 speedup', round(4 * 57 / 128, 2), '1.78')
# RISC hazard total (25/26 Q2b)
add('Q2b total cycles', 5 + 6 - 1 + 1 + 2, '13 cycles')
# Multi-cycle EX schedule (25/26 Q3b), verified by simulation (see project notes)
add('Q3b with forwarding', 15, '15 cycles')
add('Q3b without forwarding', 17, '17 cycles')

# Module Three: cache
# 25/26 Q2a block lookup (direct, 32-bit, 16 words/block, 256 blocks)
for _h, _shown in [('CA2DFC12', '193'), ('F24F25FF', '95'),
                   ('24BBABCD', '188'), ('C1D9EEF2', '239')]:
    add(f'Q2a {_h}', (int(_h, 16) >> 4) & 0xFF, _shown)
# 25/26 Q3a
add('Q3a lines', 128 * 1024 // 64, '2048')
add('Q3a direct tag', 26 - 11 - 6, '9')
add('Q3a 4way tag', 26 - 9 - 6, '11')
# 25/26 Q2c
add('Q2c blocks', 512 * 1024 // 128, '4096')
add('Q2c sets', (512 * 1024 // 128) // 4, '1024')
add('Q2c tag', 30 - 10 - 7, '13')
add('Q2c AMAT', 2 + 0.04 * 80, '5.2')
# 23/24 Q1d
add('Q1d line B', 4 * 4, '16 bytes')
add('Q1d set B', 8 * 16, '128 bytes')
add('Q1d cache KB', 4096 * 128 // 1024, '512')
# AMAT simultaneous vs hierarchical (24/25 Q1b, 23/24 Q3a)
add('AMAT simultaneous', int(0.8 * 5 + 0.2 * 100), '24 ns')
add('AMAT hierarchical', int(5 + 0.2 * 100), '25 ns')

# ---- Mock One (fresh numbers, all recomputed) ----
add('MA CPI', round(0.45 + 0.25 * 4 + 0.15 * 2 + 0.15 * 3, 2), '2.20')
add('MA total cycles', int(2.2 * 2_000_000), '4 400 000')
add('MA new CPI', round(0.45 + 0.25 * 2 + 0.15 * 2 + 0.15 * 3, 2), '1.70')
add('MA improvement', round((2.2 - 1.7) / 2.2 * 100, 2), '22.73')
add('MA 150 bin', twos(150, 12), '0000 1001 0110')
add('MA -95 twos', twos(-95, 12), '1111 1010 0001')
add('MA 39.5 hex', to_hex_f(39.5), '421E0000')
add('MA 42480000 dec', int(from_hex_f('42480000')), '50')
add('MA cache tag', 32 - 10 - 5, '17')
add('MA pipe cycle', 25 + 5, '30 ns')
add('MA pipe1000', (5 + 999) * 30, '30 120')
add('MA Q3 blocks', 64 * 1024 // 32, '2048')
add('MA Q3 tag', 28 - 9 - 5, '14')
add('MA AMAT sim', 0.9 * 3 + 0.1 * 60, '8.7')
add('MA AMAT hier', int(3 + 0.1 * 60), '9.0')
add('MA Amdahl', round(1 / (0.1 + 0.9 / 8), 2), '4.71')

# ---- Mock Two ----
add('MB 300 hex', format(int(twos(300, 16), 2), '04X'), '012C')
add('MB -200 hex', format(int(twos(-200, 16), 2), '04X'), 'FF38')
add('MB -5000 hex', format(int(twos(-5000, 16), 2), '04X'), 'EC78')
add('MB 85.75 hex', to_hex_f(85.75), '42AB8000')
add('MB C2960000 dec', int(from_hex_f('C2960000')), '-75')
add('MB block ABCD1234', (0xABCD1234 >> 3) & 0x1FF, '70')
add('MB block 5678FEDC', (0x5678FEDC >> 3) & 0x1FF, '475')
add('MB -75 twos10', twos(-75, 10), '1110110101')
add('MB end-around', 200 - 75, '125')
add('MB image bytes', 8 * 200 * 10 * 200 // 8, '400 000')
add('MB 43A00000 dec', int(from_hex_f('43A00000')), '320')
add('MB pipe cycle', 50 + 5, '55 ns')
add('MB pipe200', (4 + 199) * 55, '11 165')
add('MB AMAT hier', 4 + 0.15 * 70, '14.5')

# ---- slide-coverage additions (blended from the lecturer decks) ----
# Unit 2: shifting, coded decimal, character codes, bitmap sizing
add('3FC dec', int('3FC', 16), '1020')
add('1FE dec', int('1FE', 16), '510')
add('BCD 9', format(9, '04b'), '1001')
add('BCD 2', format(2, '04b'), '0010')
add('5421 nine', '1100', '1100')                 # weighted code, hand-derived (5+4)
add('4221 nine', '1111', '1111')                 # weighted code, hand-derived (4+2+2+1)
add('XS3 24', ''.join(format(d + 3, '04b') for d in (2, 4)), '0101 0111')
add('XS3 decode 0100 0110', ''.join(str(int(n, 2) - 3) for n in ('0100', '0110')), '13')
add('ASCII A', ord('A'), '65')
add('ASCII a', ord('a'), '97')
add('ASCII 0', ord('0'), '48')
add('bitmap px across', 4 * 300, '1200')
add('bitmap px down', 6 * 300, '1800')
add('bitmap total px', 4 * 300 * 6 * 300, '2 160 000')
add('bitmap bytes', 4 * 300 * 6 * 300 // 8, '270 000')
add('bitmap KB', round(4 * 300 * 6 * 300 / 8 / 1024, 2), '263.67')
# Unit 3: double precision bias
add('double bias', 2**10 - 1, '1023')
# Unit 4: instruction decode, indirect add/store, backward branch
add('decode 202', int('11001010', 2), '202')
add('indirect ADD R1', 10 + 5, '15')
add('indirect STORE', 30, 'M[800] = 30')
add('BNE -40 EA', 1000 - 40, '960')
# M3 Unit 1: memory sizing, two-level average access
add('4MB bytes', 4 * 1024 * 1024, '4 194 304')
add('4MB bits', 4 * 1024 * 1024 * 8, '33 554 432')
add('4MB addr lines', (4 * 1024 * 1024).bit_length() - 1, '22')
add('two-level miss cost', round(0.01 + 0.1, 2), '0.11')
add('two-level average', round(0.95 * 0.01 + 0.05 * 0.11, 3), '0.015')
# M3 Unit 3: tag directory across the three mappings (16 KB cache, 256 B block, 128 KB MM)
add('tagdir addr bits', (128 * 1024).bit_length() - 1, '17')
add('tagdir lines', 16 * 1024 // 256, '64')
add('tagdir direct bits', 64 * (17 - 6 - 8), '192')
add('tagdir direct bytes', 64 * (17 - 6 - 8) // 8, '24 bytes')
add('tagdir assoc bits', 64 * (17 - 8), '576')
add('tagdir assoc bytes', 64 * (17 - 8) // 8, '72 bytes')
add('tagdir 2way bits', 64 * (17 - 5 - 8), '256')
add('tagdir 2way bytes', 64 * (17 - 5 - 8) // 8, '32 bytes')


# ---- Amdahl ceilings: the limit the law states, as s grows without bound ----
add('Amdahl ceiling f=0.85', round(1 / (1 - 0.85), 2), '6.67')
add('Amdahl ceiling f=0.90', int(round(1 / (1 - 0.90))), '10')
add('Amdahl ceiling f=0.75', int(round(1 / (1 - 0.75))), '4')

# ---- Past papers solved in full: numbers not worked anywhere else ----
# 24/25 Q1c: 24-bit address, 16 words/block, direct-mapped 256 blocks
add('2425 Q1c tag', 24 - 8 - 4, '12')
for _h, _shown in [('1A2BC0', '188'), ('FFFF00', '240'),
                   ('123456', '69'), ('C109D5', '157')]:
    add(f'2425 Q1c {_h}', (int(_h, 16) >> 4) & 0xFF, _shown)
# 24/25 Q2a: cache 1 KB, block 16 B, MM 64 KB, 16-bit address
_lines = 1024 // 16
add('2425 Q2a lines', _lines, '64')
add('2425 Q2a direct tag', 16 - 6 - 4, '6')
add('2425 Q2a direct dir', _lines * (16 - 6 - 4), '384')
add('2425 Q2a direct bytes', _lines * (16 - 6 - 4) // 8, '48 bytes')
add('2425 Q2a fully tag', 16 - 4, '12')
add('2425 Q2a fully dir', _lines * (16 - 4), '768')
add('2425 Q2a fully bytes', _lines * (16 - 4) // 8, '96 bytes')
add('2425 Q2a 2way tag', 16 - 5 - 4, '7')
add('2425 Q2a 2way dir', _lines * (16 - 5 - 4), '448')
add('2425 Q2a 2way bytes', _lines * (16 - 5 - 4) // 8, '56 bytes')
# 24/25 Q5c: -421.55 with the mantissa truncated after 12 bits


def _trunc_ieee(x, keep):
    """Sign|exponent|mantissa with only the first `keep` mantissa bits retained."""
    sign = '1' if x < 0 else '0'
    x = abs(x)
    e = 0
    while x >= 2:
        x /= 2
        e += 1
    while x < 1:
        x *= 2
        e -= 1
    frac, bits = x - 1, ''
    for _ in range(23):
        frac *= 2
        bits += str(int(frac))
        frac -= int(frac)
    return sign + format(e + 127, '08b') + bits[:keep] + '0' * (23 - keep)


_q5c = _trunc_ieee(-421.55, 12)
add('2425 Q5c exponent', 8 + 127, '135')
add('2425 Q5c mantissa', _q5c[9:], '1010 0101 1000 0000 0000 000')
add('2425 Q5c hex', format(int(_q5c, 2), '08X'), 'C3D2C000')

# ---- Mock Three (all fresh, all recomputed) ----
add('MC 178 in 11b', format(178, '011b'), '000 1011 0010')
add('MC -92 sign-mag', sign_mag(-92, 11), '100 0101 1100')
add('MC -92 ones', ones(-92, 11), '111 1010 0011')
add('MC -92 twos', twos(-92, 11), '111 1010 0100')
add('MC 11b range low', -(2**10), '-1024')
add('MC 11b range high', 2**10 - 1, '1023')
add('MC 92.375 hex', to_hex_f(92.375), '42B8C000')
add('MC 92.375 exponent', 6 + 127, '133')
_mcmix = [(0.35, 1), (0.25, 2), (0.20, 3), (0.12, 4), (0.08, 5)]
_mccpi = round(sum(f * c for f, c in _mcmix), 2)
add('MC avg CPI', _mccpi, '2.33')
add('MC total cycles', int(_mccpi * 2_500_000), '5 825 000')
add('MC new CPI', round(_mccpi - 0.12 * 4 + 0.12 * 2, 2), '2.09')
add('MC improvement', round((_mccpi - 2.09) / _mccpi * 100, 2), '10.30')
add('MC Q1e tag', 24 - 9 - 5, '10')
for _h, _shown in [('A5C3E7', '31'), ('7F0044', '2'), ('C0FFEE', '511')]:
    add(f'MC Q1e {_h}', (int(_h, 16) >> 5) & 0x1FF, _shown)
add('MC Q1e A5C3E7 dec', int('A5C3E7', 16), '10 863 591')
add('MC Q1e 7F0044 dec', int('7F0044', 16), '8 323 140')
add('MC Q1e C0FFEE dec', int('C0FFEE', 16), '12 648 430')
_st = [40, 55, 45, 60, 50]
add('MC pipe cycle', max(_st) + 5, '65 ns')
add('MC pipe one task', sum(_st), '250 ns')
add('MC pipe ideal speedup', round(sum(_st) / (max(_st) + 5), 2), '3.85')
add('MC pipe 800', (5 + 800 - 1) * (max(_st) + 5), '52 260')
add('MC seq 800', 800 * sum(_st), '200 000')
add('MC pipe speedup 800', round(800 * sum(_st) / ((5 + 800 - 1) * 65), 2), '3.83')
add('MC throughput', round(800 / ((5 + 799) * 65) * 1e9 / 1e6, 2), '15.31')
add('MC Amdahl', round(1 / ((1 - 0.75) + 0.75 / 8), 2), '2.91')
add('MC Q3a lines', 32 * 1024 // 64, '512')
add('MC Q3a sets', (32 * 1024 // 64) // 8, '64')
add('MC Q3a tag', 24 - 6 - 6, '12')
add('MC Q3a dir bits', (32 * 1024 // 64) * 12, '6144')
add('MC Q3a dir bytes', (32 * 1024 // 64) * 12 // 8, '768 bytes')
add('MC AMAT hier', round(3 + 0.08 * 70, 2), '8.6')
add('MC AMAT sim', round(0.92 * 3 + 0.08 * 70, 2), '8.36')
add('MC Q4a result', 245 - 178, '67')
add('MC Q4a 245 bin', format(245, '010b'), '00 1111 0101')
add('MC Q4a 178 bin', format(178, '010b'), '00 1011 0010')
add('MC Q4a -178 ones', ones(-178, 10), '11 0100 1101')
add('MC XS3 507', ''.join(format(d + 3, '04b') for d in (5, 0, 7)), '1000 0011 1010')
add('MC XS3 decode', ''.join(str(int(n, 2) - 3) for n in ('0111', '1001', '0110')), '463')
add('MC 3addr bytes', 4 * (1 + 3 * 2), '28')
add('MC 2addr bytes', 7 * (1 + 2 * 2), '35')
add('MC 1addr bytes', 8 * (1 + 1 * 2), '24')
add('MC 0addr bytes', 5 * 3 + 1 * 3 + 4 * 1, '22')
add('MC C2C60000 dec', int(from_hex_f('C2C60000')), '-99')
add('MC addr space', 2**21, '2 097 152')
add('MC capacity MB', 2**21 * 4 // 1024 // 1024, '8 MB')
add('MC img across', int(8.5 * 200), '1700')
add('MC img down', 11 * 200, '2200')
add('MC img px', int(8.5 * 200) * 11 * 200, '3 740 000')
add('MC img bytes', int(8.5 * 200) * 11 * 200 // 8, '467 500')
add('MC img KB', round(int(8.5 * 200) * 11 * 200 / 8 / 1024, 2), '456.54')


def norm(s):
    return str(s).replace(' ', '').replace(',', '')


def report(_ignored_html=None):
    text = book_text()
    fails = []
    for label, computed, shown in CHECKS:
        if shown not in text:
            fails.append(f'{label}: the book does not contain {shown!r} '
                         f'(recompute says {computed})')
            continue
        want, got = norm(computed), norm(shown)
        if want not in got and got not in want:
            fails.append(f'{label}: book shows {shown!r} but recompute is {computed}')

    print(f'NUMERIC GATE: {len(CHECKS)} worked values recomputed')
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
