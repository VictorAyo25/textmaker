"""Pedagogy retrofit for the IFT222 manual, run 2026-08-20.

WHY. The house pedagogy was settled on 2026-08-08 and recorded as owed to the
study manuals: teaching must be KEY-POINT LED as well as worked, and every hard
idea opens on an ordinary-life anchor before any symbol. Key points fix recall,
the worked steps fix understanding, and a lesson with only one of the two is
either a formula sheet or a wall.

WHAT THIS ADDS. One or two KEY POINT boxes per unit, never ten, each said twice:
once in formal words and once bluntly, because the blunt version is the one that
survives the exam hall. Plus the two ordinary-life anchors this book was missing,
for the memory hierarchy and for the cache address split. The units that already
opened on an anchor keep theirs untouched: architecture against organization has
the car, pipelining has the laundry, and floating point got the kitchen scale
with the deck gap-fill.

Idempotent: an insertion whose marker text is already present is skipped.

    cd build && python gapfill_pedagogy.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

EDITS = []


def kp(fname, marker, anchor, formal, blunt, where='before'):
    EDITS.append((fname, marker, anchor, where,
                  '<div class="box keypoint"><div class="bar"><span>Key point</span>'
                  '</div>\n<div class="body">\n'
                  f'<p class="formal">{formal}</p>\n'
                  f'<p class="blunt"><b>Blunt version:</b> {blunt}</p>\n'
                  '</div></div>\n\n'))


def raw(fname, marker, anchor, payload, where='before'):
    EDITS.append((fname, marker, anchor, where, payload))


H3 = '<h3 class="sub">%s</h3>'

# -- Foundations: base conversion is one idea, not four procedures ------------
kp('front.html', 'the same idea read twice',
   H3 % 'Decimal to any base: divide and collect remainders',
   'A base is a promise about place value, and every conversion in this course is '
   'that promise applied in one direction or the other. Multiplying and adding goes '
   'from a base into decimal; dividing and collecting remainders goes from decimal '
   'into a base. They are the same idea read twice, not two procedures to memorise.',
   'one rule, run forwards or backwards. If you are memorising two, you have missed it.')

# -- Module One Unit 1: the distinction, in a form you can apply -------------
kp('module1.html', 'If you can only measure it',
   H3 % 'How a computer runs a program: the instruction cycle',
   'Architecture is the set of attributes a program can see, so a change to it can '
   'break a program that already runs. Organization is everything underneath, so a '
   'change to it can only make the same program faster, slower, hotter or cheaper.',
   'if you can name it in the instruction set, it is architecture. If you can only '
   'measure it, it is organization.')

kp('module1.html', 'one road or two',
   H3 % 'The Von Neumann bottleneck',
   'Von Neumann and Harvard differ in exactly one thing: whether instructions and '
   'data share a memory and a bus, or have their own. Every other difference between '
   'them, the cost, the flexibility, the bottleneck, follows from that one choice.',
   'one road or two. Everything else is traffic.')

# -- Module One Unit 2: a bit pattern means nothing on its own ---------------
kp('module1_unit2.html', 'the bits do not know',
   H3 % 'Adding in binary, and when it overflows',
   'A bit pattern carries no meaning by itself. 1111 1111 is 255 as an unsigned '
   'integer, minus 1 in two\'s complement, minus 127 in sign and magnitude, and a '
   'perfectly ordinary character in a text file. The interpretation is a decision '
   'made outside the bits, and every question of this type tells you which one to '
   'make.',
   'the bits do not know what they are. Read the question for the code before you '
   'read the pattern.')

# -- Module One Unit 4: the address-count trade ------------------------------
kp('module1_unit4.html', 'pay in instruction width or pay in instruction count',
   H3 % 'Addressing modes: where the operand really is',
   'The number of addresses an instruction carries trades instruction WIDTH against '
   'instruction COUNT. Three addresses name everything at once, so each instruction '
   'is long and few are needed; zero addresses name nothing, so each instruction is '
   'tiny and many are needed. The total work is conserved.',
   'pay in instruction width or pay in instruction count. You do not get to skip '
   'both.')

# -- Module Two Unit 1: the cycle is all a CPU ever does ---------------------
kp('module2.html', 'It is the only thing it ever does',
   H3 % 'What is inside the processor',
   'Every component inside the processor exists to serve one repeating loop: fetch '
   'the next instruction, decode what it asks for, execute it. The program counter '
   'says where, the instruction register holds what, the control unit turns it into '
   'signals, and the arithmetic and logic unit does the work.',
   'a CPU fetches, decodes and executes. Forever. It is the only thing it ever does.')

# -- Module Two Unit 2: everything reduces to three factors ------------------
kp('module2_unit2.html', 'trace a speedup to one of those three',
   H3 % "Amdahl's law: the limit on any speedup",
   'CPU time = IC &#215; CPI &#215; T, where IC is the instruction count, CPI is the '
   'average cycles per instruction and T is the seconds per clock cycle. Every claim '
   'that something made a processor faster must show which of those three it '
   'changed, and a change that improves one at the expense of another may be no '
   'improvement at all.',
   'three numbers decide the whole thing. If an answer does not trace a speedup to '
   'one of those three, it is not an answer.')

# -- Module Three Unit 1: the hierarchy, with its anchor ---------------------
raw('module3.html', 'designed that as a hierarchy', H3 % 'The memory hierarchy',
    """<div class="anchor"><span class="alab">Anchor</span>
<p>Think of where you keep things while working. The two or three pages actually
under your hand are on the desk: instantly reachable, and there is room for almost
nothing. The rest of the file is in the drawer, a second away. The other files are on
the shelf across the room, and the archive is in a warehouse across town. Nobody
designed that as a hierarchy. It happened because fast access and large capacity cost
each other, and a computer's memory is organised the same way for the same reason.</p>
</div>

""")

kp('module3.html', 'fast, big, cheap: pick two',
   H3 % 'The memory hierarchy',
   'Memory technologies trade speed, capacity and cost against each other, and no '
   'technology wins on all three at once. The hierarchy exists so that the small '
   'fast expensive store holds what is being used now, and the large slow cheap '
   'store holds everything else, giving the average speed of the fast one at close '
   'to the price of the slow one.',
   'fast, big, cheap: pick two. The hierarchy is how a machine fakes all three.',
   where='before')

# -- Module Three Unit 3: the cache address split, with its anchor -----------
raw('module3_unit3.html', 'A coat-check ticket',
    H3 % 'Splitting the address: tag, index, offset',
    """<div class="anchor"><span class="alab">Anchor</span>
<p>A coat-check ticket answers three questions with one number: which rail your coat
is on, which hook on that rail, and, if several coats hang on that hook, which one is
yours. A memory address does the same job in the same order. The offset says which
byte inside the block, the index says which slot of the cache the block may occupy,
and the tag says which of the many blocks that share that slot is actually sitting
there. Read the split in that order and it stops being three formulas.</p>
</div>

""")

kp('module3_unit3.html', 'which byte, which slot, which block',
   H3 % 'Elements of cache design',
   'The three fields of an address are not three separate calculations. The offset '
   'is fixed by the block size, the index is fixed by the number of slots, and the '
   'tag is whatever is left of the address. Work them out in that order and the tag '
   'never needs its own formula.',
   'which byte, which slot, which block. Offset and index first, tag is the '
   'remainder.')

# -- Module Four: where the complexity is put -------------------------------
kp('module4.html', 'somebody has to do the hard work',
   '<div class="box teach"><div class="bar"><span>Teach</span>'
   '<span class="tag">Advantages and disadvantages</span></div>',
   'RISC and CISC do not disagree about what a program must do. They disagree about '
   'WHERE the complexity should live. CISC puts it in the hardware, in rich '
   'instructions and a microprogrammed control unit. RISC puts it in the compiler, '
   'building complex operations out of simple fast instructions.',
   'somebody has to do the hard work. CISC makes the chip do it, RISC makes the '
   'compiler do it.')

# -- Supplement: what a K-map actually is ------------------------------------
kp('supplement.html', 'so that neighbours differ by one bit',
   H3 % 'The Karnaugh map',
   'A Karnaugh map is a truth table with its rows rearranged so that any two cells '
   'sharing an edge differ in exactly one variable. That is the whole trick: '
   'adjacency becomes algebraic cancellation, so grouping neighbouring ones is the '
   'same operation as applying the law that a variable and its complement sum to '
   'one.',
   'it is a truth table folded so that neighbours differ by one bit. Grouping is '
   'cancelling.')


def apply_one(fname, marker, anchor, where, payload):
    path = os.path.join(CONTENT, fname)
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    if marker in s:
        return f'{fname}: already carries "{marker[:38]}", skipped'
    n = s.count(anchor)
    if n != 1:
        return f'FAIL {fname}: anchor found {n} times, expected 1 ({anchor[:52]})'
    i = s.index(anchor)
    at = i if where == 'before' else i + len(anchor)
    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s[:at] + payload + s[at:])
    return f'{fname}: inserted "{marker[:38]}"'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    fails = []
    for e in EDITS:
        msg = apply_one(*e)
        print('  ' + msg)
        if msg.startswith('FAIL'):
            fails.append(msg)
    print(f'gapfill_pedagogy: {len(EDITS)} insertions attempted, {len(fails)} failed')
    if fails:
        sys.exit(1)


if __name__ == '__main__':
    main()
