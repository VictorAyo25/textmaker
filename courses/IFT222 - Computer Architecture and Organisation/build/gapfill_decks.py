"""One-time deck gap-fill for the IFT222 manual, run 2026-08-20.

WHY. The student asked whether all the lecture decks really had been blended into
this book. The blend WAS done, deck by deck, and the honest answer needed a
measurement rather than a memory, so the 600-fact ledger built for the drill
(webapp/data/ift222/ledger, at least one fact per content slide across all eight
decks, 326 content slides) was run against the manual's own prose as an
independent checklist. 558 of 600 facts were carried. Of the 42 that were not,
most are not manual material at all: the recommended-textbook list, the
motivational "real-life applications" slides, an in-class question with no answer.

Ten were real, and they are what this script inserts. Every one of them is the
LECTURER'S OWN example, named list or case study, which on a course whose
lecturer reuses himself year to year is exactly the material worth carrying:

  Data S39, S40   the Ariane 5 explosion and the Vancouver stock exchange index,
                  the deck's two case studies for why a rounding error matters
  Data S55        the deck's own IEEE-754 example, 64.2 stored as 42806666h
  Data S46        the deck's Excess-3 values for 27, 597 and 14.57
  Data S71        the stated advantages of bit-mapped graphics
  ISA S14, S18    the MC68009 and MC6809 mnemonics for the load/store and the
                  arithmetic/logic instruction types, repeated at Rev S10
  Pipe S10, S11   the formal definition of pipelining, Instruction Level
                  Parallelism by name, and the six levels of parallelism
  RISC S17        the three machines RISC actually grew out of, named
  Intro S31, S54  binary compatibility as the reader meets it (x86 and ARM), and
                  the smartphone worked as an architecture against organization
                  example
  (also)          the ROM family, which the Semiconductor Memory unit did not
                  carry at all, found because EEPROM appeared in the new
                  objective section and the teach-before-use audit caught it

This script is idempotent: every insertion is skipped if its marker text is
already present, so a second run is a no-op and says so.

    cd build && python gapfill_decks.py
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, 'content')

EDITS = []


def edit(fname, marker, kind, anchor, payload):
    """kind: 'before' | 'after' | 'replace' (anchor is a regex for replace)."""
    EDITS.append((fname, marker, kind, anchor, payload))


# --------------------------------------------------------------------------
# 1. Floating point: the deck's two case studies, an anchor, and a key point.
# --------------------------------------------------------------------------
edit('module1_unit3.html', 'Ariane 5', 'before',
     '<div class="box teach"><div class="bar"><span>Teach</span>'
     '<span class="tag">IEEE-754 single precision</span></div>', """<div class="anchor"><span class="alab">Anchor</span>
<p>A kitchen scale reads 1.2 kg whether the pan holds 1.19 kg or 1.24 kg. It is not
broken. It has a fixed number of digits, so anything falling between two of its steps
is pushed to the nearest step it can show. Floating point is that scale, built with
24 binary digits of precision, and anything finer than its smallest step is rounded
away the moment it is stored.</p></div>

<div class="box trap"><div class="bar"><span>Trap</span><span class="tag">what the rounding actually costs</span></div>
<div class="body">
<p>The lecture deck opens this topic with two real failures, and they are worth
carrying, because they are the answer to "why does a rounding error matter" that the
examiner has already read.</p>
<p><b>Ariane 5, 4 June 1996.</b> An unmanned rocket exploded forty seconds after
lift-off, on its first voyage, after a decade of development costing 7 billion
dollars. The cause was a software error. A 64-bit floating point number holding the
rocket's horizontal velocity with respect to the platform was converted into a 16-bit
signed integer. The value was larger than the largest integer a 16-bit signed field
can hold, so the conversion failed and the guidance system stopped.</p>
<p><b>The Vancouver stock exchange, 1982.</b> A new index was started at 1000.000 and
recomputed after every transaction. Each recomputation threw away the digits it could
not hold instead of rounding them, so every transaction lost a sliver. Twenty two
months later the deck records the index at 520. Recomputed correctly it stood at
about 1098, so truncation alone had eaten more than half of it.</p>
<p>Both are one fault in two costumes. A stored floating point number is an
approximation; convert it into a narrower type, or accumulate it over enough steps,
and it becomes a wrong answer that the arithmetic itself never flags.</p>
</div></div>

<div class="box keypoint"><div class="bar"><span>Key point</span></div>
<div class="body">
<p class="formal">Floating point trades exactness for range. It holds numbers far
larger and far smaller than an integer field of the same width, and in exchange
almost none of them are stored exactly.</p>
<p class="blunt"><b>Blunt version:</b> integers are small and exact, floats are huge
and approximate. Never test two floats for equality.</p>
</div></div>

""")

# --------------------------------------------------------------------------
# 2. Floating point: the deck's own 64.2 example, which does NOT terminate.
# --------------------------------------------------------------------------
edit('module1_unit3.html', '42806666', 'after',
     '<p class="redo"><b>Now redo it:</b> the five steps never change. Sign, binary,\n'
     'normalise, exponent plus 127, mantissa to 23 bits.</p>\n</div></div>',
     """

<div class="box work"><div class="bar"><span>Worked example</span><span class="tag">Slide: the deck's own value</span></div>
<div class="body"><p>Represent <b>64.2</b> in IEEE-754 single precision. The previous
example terminated. This one does <b>not</b>, which is exactly why the deck sets it.</p>
<div class="params">
<div class="prow"><span class="plab">Given</span> value = 64.2 &middot; format =
IEEE-754 single precision &middot; layout S=1, E=8, M=23 bits &middot; bias = 127</div>
<div class="prow"><span class="plab">Find</span> the 32-bit stored pattern, written in hex</div>
<div class="prow"><span class="plab">Formula</span> normalise to 1.<i>m</i> &#215;
2<sup>e</sup>, then E = e + bias, and the stored bits are S | E | M</div>
</div>
<div class="wheredef"><span class="wlab">what each symbol means</span>
<b>S</b> = sign bit &middot; <b>e</b> = the true exponent found by normalising &middot;
<b>E</b> = the stored exponent field, e + 127 &middot; <b>M</b> = the 23 bits after the
hidden leading 1 &middot; <b>bias</b> = 127</div>
<ol class="steps">
<li>Sign: the number is positive, so the sign bit is <b>0</b>.</li>
<li>Binary: 64 = 1000000. For the fraction, double 0.2 again and again and read off
the whole part each time: 0.4, 0.8, 1.6, 1.2, and then 0.4 once more. It has come back
to where it started, so the bits repeat: 0.2 = 0.0011 0011 0011&#8230; for ever.
So 64.2 = 1000000.0011001100110011&#8230;</li>
<li>Normalise: move the point 6 places left. 64.2 =
1.0000000011001100110011&#8230; &#215; 2<sup>6</sup>, so the true exponent is 6.</li>
<li>Exponent field: 6 + 127 = 133 = 1000 0101.</li>
<li>Mantissa: take the first 23 bits after the hidden leading 1. That is the six
remaining bits of the integer part, then the repeating pattern:
0000 0000 1100 1100 1100 110. The next bit along is 0, so nothing rounds up.</li>
<li>Assemble sign, exponent, mantissa, then group into fours:
0 1000 0101 0000 0000 1100 1100 1100 110 = 0100 0010 1000 0000 0110 0110 0110 0110.</li>
</ol>
<div class="answerbox">64.2 = 0 10000101 00000000110011001100110 = <b>42806666h</b>
&nbsp;(read that pattern back and you get 64.19999694824219, not 64.2, which is the
whole point of the example).</div>
<p class="redo"><b>Now redo it:</b> and then say out loud what the machine is actually
holding. 64.2 cannot be stored exactly in 32 bits, so what goes in is the nearest
value that can be.</p>
</div></div>""")

# --------------------------------------------------------------------------
# 3. ISA: the deck's real mnemonics for the two instruction types.
# --------------------------------------------------------------------------
edit('module1_unit4.html', 'MC6809', 'before',
     '<h3 class="sub">Zero, one, two and three address formats</h3>',
     """<div class="box slide"><div class="bar"><span>From the slides</span><span class="tag">the deck's own instruction examples</span></div>
<div class="body">
<p class="src">the lecturer's own examples, named processor and all</p>
<p>The deck does not leave the instruction types abstract. It names a real processor
family and prints the actual mnemonics, and the revision class repeats them
unchanged, which on this course is the strongest signal there is that they are worth
knowing.</p>
<table class="data">
<tr><th>Instruction type</th><th>What it does</th><th>The deck's examples</th></tr>
<tr><td><b>Load and store</b></td><td>move a value between memory and a register
without changing it</td><td>LDA, STA, LDB, STB, LDD, STD</td></tr>
<tr><td><b>Arithmetic and logic</b></td><td>combine two operands and produce a
result</td><td>ADDB, SUBA, SUBD, ANDA, EORA</td></tr>
</table>
<p>The mnemonics decode themselves once you see the pattern. <b>LD</b> is load and
<b>ST</b> is store, and the letter after it names the register: LDA loads accumulator
A, STB stores accumulator B, LDD loads the double accumulator D. On the arithmetic
side <b>ADDB</b> adds into accumulator B, <b>SUBA</b> subtracts from accumulator A,
<b>ANDA</b> ands into accumulator A, and <b>EORA</b> is exclusive-OR into accumulator
A. Each of these two-operand instructions requires one of its operands to already be
in an accumulator, which is the one-address style this unit is about to formalise.</p>
<p class="note2"><b>Note.</b> The slides write the load and store family as MC68009
and the arithmetic family as MC6809. The processor family is the Motorola 6809; the
extra zero is a slip on the slide. It is recorded here rather than tidied away,
because a question quoting the slide will quote the slip too.</p>
</div></div>

""")

# --------------------------------------------------------------------------
# 4. Pipelining: the formal definition, ILP by name, the six levels.
# --------------------------------------------------------------------------
edit('module2_unit3.html', 'Instruction Level Parallelism', 'after',
     'cycle</b>. The clock cycle is set by the slowest stage plus the small latch delay\n'
     'between stages.</p>',
     """

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">the deck's definition, and where pipelining sits</span></div>
<div class="body">
<p>The deck states it formally, and the wording is worth having, because a definition
question wants this exact shape: <b>pipelining is a technique of decomposing a
sequential process into sub-operations, with each sub-process executed in a special
dedicated segment that operates concurrently with all other segments</b>.</p>
<p>What a pipeline exploits is the parallelism <i>among instructions</i>, found by
overlapping them, and that has a name: <b>Instruction Level Parallelism (ILP)</b>.
It is one level among several. The deck lists where a typical system finds its
speedup:</p>
<ul class="bul">
<li><b>Multi-user:</b> one machine serving many people at once.</li>
<li><b>Multitasking:</b> one user running several programs at once.</li>
<li><b>Multi-processing:</b> several processors working at once.</li>
<li><b>Multi-programming:</b> several programs resident in memory together, the CPU
switching between them.</li>
<li><b>Multi-threading:</b> several threads of one program running at once.</li>
<li><b>Compiler optimizations:</b> the compiler rearranging code so the hardware can
overlap more of it.</li>
</ul>
<p>Pipelining is the hardware end of that list, and Instruction Level Parallelism is
what it buys.</p>
</div></div>

<div class="box keypoint"><div class="bar"><span>Key point</span></div>
<div class="body">
<p class="formal">Pipelining does not shorten one instruction. It raises throughput,
the number of instructions completed per unit time, while the latency of any single
instruction stays the same, or slightly worsens because of the latches between
stages.</p>
<p class="blunt"><b>Blunt version:</b> no single load of washing dries any faster. You
just get more loads through the evening.</p>
</div></div>""")

# --------------------------------------------------------------------------
# 5. RISC: name the three machines, as the deck does.
# --------------------------------------------------------------------------
edit('module4.html', 'Berkeley RISC 1 and 2', 'replace',
     r'RISC grew out of that early-1980s work,\s+including the IBM 801\s+and\s+the\s+'
     r'academic\s+MIPS and RISC research projects\.',
     'RISC grew out of that early-1980s work: the <b>IBM 801</b>, <b>Stanford MIPS</b> '
     'and <b>Berkeley RISC 1 and 2</b> were all designed on the philosophy that came to '
     'be called RISC.')

# --------------------------------------------------------------------------
# 6. Semiconductor memory: the whole ROM family, which was missing.
# --------------------------------------------------------------------------
edit('module3_unit2.html', 'EEPROM', 'before',
     '<div class="box teach"><div class="bar"><span>Teach</span>'
     '<span class="tag">DRAM and SRAM</span></div>',
     """<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">the ROM family</span></div>
<div class="body"><p>ROM is not one chip but a family, and its members differ in one
thing only: how, and how often, the contents can be written.</p>
<ul class="bul">
<li><b>ROM (mask ROM):</b> written once, at manufacture, by the mask that makes the
chip. It can never be changed. Cheapest per bit in very large quantities.</li>
<li><b>PROM (Programmable ROM):</b> blank when made, written once by the customer on
a device that blows fusible links. After that it is fixed for good.</li>
<li><b>EPROM (Erasable PROM):</b> written electrically, and erased as a whole by
shining ultraviolet light through a quartz window in the package. Rewritable, but only
out of circuit and only all at once.</li>
<li><b>EEPROM (Electrically Erasable PROM):</b> written and erased electrically, in
place, a byte at a time, with no ultraviolet light and no removal from the board.
Writing is far slower than reading.</li>
<li><b>Flash memory:</b> an EEPROM that erases in blocks rather than in bytes, which
makes it much denser and much faster to write in bulk. Solid-state disks and memory
cards are flash.</li>
</ul>
<p>All five are non-volatile. Read down that list and the trend is the one this whole
course keeps meeting: each step buys flexibility and pays for it in money, in speed or
in density.</p></div></div>

<div class="box keypoint"><div class="bar"><span>Key point</span></div>
<div class="body">
<p class="formal">The distinction that earns the mark is volatility against
writability. RAM is volatile and freely writable; every member of the ROM family is
non-volatile, and they differ from each other only in how much trouble a rewrite
is.</p>
<p class="blunt"><b>Blunt version:</b> RAM forgets when the power goes. ROM does not.
The rest is just how hard it is to change your mind.</p>
</div></div>

""")

# --------------------------------------------------------------------------
# 7. Bitmap: the advantages the deck states outright.
# --------------------------------------------------------------------------
edit('module1_unit2.html', 'every single pixel is yours to alter', 'replace',
     r'A photograph, having no simple shapes, does not reduce to vectors\.</li>\s*</ul>',
     'A photograph, having no simple shapes, does not reduce to vectors.</li>\n'
     '</ul>\n<p>The deck states the bitmap side positively, and it is the phrasing to '
     'give back: the advantages of bit-mapped graphics, the ones the paint packages '
     'use, are that <b>every single pixel is yours to alter</b>, and that they look '
     '<b>more realistic for photographs and real-life images</b>. Vector wins on size '
     'and on scaling; bitmap wins on fine control and on realism.</p>')

# --------------------------------------------------------------------------
# 8. Architecture against organization: the deck's formal definition, its
#    smartphone example, and binary compatibility the way the reader meets it.
# --------------------------------------------------------------------------
edit('module1.html', 'smartphone', 'after_box', 'The core idea',
     """

<div class="box mem"><div class="bar"><span>Must memorise</span><span class="tag">the two definitions, formally</span></div>
<div class="body">
<p><b>Computer architecture</b> refers to the attributes of a system visible to the
programmer, those that have a direct impact on the logical execution of a program.</p>
<p><b>Computer organization</b> refers to the operational units and their
interconnections that realize the architectural specifications.</p>
<p>One sentence joins them, and it is the one the objective section keeps asking for:
<b>architecture provides the blueprint and the capabilities, organization determines
the efficiency and the performance, and the two are deeply interconnected</b>.</p>
</div></div>

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">the deck's smartphone example</span></div>
<div class="body">
<p>The deck works the distinction on a phone, and it is the cleanest example on the
course because both halves are things you can feel.</p>
<ul class="bul">
<li><b>Architecture</b> of the phone: the instruction set it runs and the data types
it supports. That is what decides whether an app will run on it at all.</li>
<li><b>Organization</b> of the phone: how fast it feels, how long the battery lasts,
and how well it handles several apps at once. Not one of those is in the instruction
set, and every one of them is a hardware choice.</li>
</ul>
<p>That is why the same question comes back every year in different clothes. A change
you can name in the instruction set is architecture. A change you can only measure is
organization.</p>
</div></div>

<div class="box teach"><div class="bar"><span>Teach</span><span class="tag">binary compatibility, where you have already met it</span></div>
<div class="body">
<p>An application is compiled for one instruction set, and it will run only on
processors that support that instruction set. This is not theory: it is why an app
built for the ARM processors in phones is a different download from the same app for
an x86 laptop, and why a program compiled twenty years ago still runs on a modern x86
chip whose insides bear no resemblance to the machine it was built for.</p>
<p>Hold the instruction set steady and you may rebuild everything underneath it. That
is the whole commercial reason the architecture and organization split exists, and
the reason a manufacturer will keep an awkward old instruction alive for decades.</p>
</div></div>""")


# --------------------------------------------------------------------------
# 9. Excess-3: the deck's own three values, one of them fractional.
# --------------------------------------------------------------------------
edit('module1_unit2.html', 'Excess-3 of 14.57', 'after',
     '<div class="answerbox">24 in Excess-3 is <b>0101 0111</b>; the code 0100 0110 '
     'decodes to' + chr(10) + '<b>13</b>. Going in, add 3 to each digit; coming out, '
     'subtract 3 from each nibble.</div>' + chr(10) + '</div></div>',
     """

<div class="box recall"><div class="bar"><span>Recall and check</span><span class="tag">Slide: the deck's own values</span></div>
<div class="body"><p class="q">Encode <b>27</b>, <b>597</b> and <b>14.57</b> in
Excess-3. Do all three before you look, and watch what happens at the point.</p>
<hr class="cut"><p class="alabel">Answer</p>
<p>Add 3 to each decimal digit, then write that sum in four bits. Nothing else
changes, and the decimal point stays exactly where it was.</p>
<ul class="bul">
<li><b>27</b>: 2 and 7 become 5 and 10, so 0101 1010 = <b>01011010</b>.</li>
<li><b>597</b>: 5, 9 and 7 become 8, 12 and 10, so 1000 1100 1010 =
<b>100011001010</b>.</li>
<li><b>14.57</b>: 1, 4, 5 and 7 become 4, 7, 8 and 10, so
<b>01000111.10001010</b>. The point sits where it sat in the decimal, between the
digit-4 group and the digit-5 group.</li>
</ul>
<p>Excess-3 of 14.57 is the one worth practising: a fractional value is where people
lose the point, and this code makes no special case of it.</p></div></div>""")


def apply_one(fname, marker, kind, anchor, payload):
    path = os.path.join(CONTENT, fname)
    with open(path, encoding='utf-8') as fh:
        s = fh.read()
    if marker in s:
        return f'{fname}: already carries "{marker[:34]}", skipped'

    if kind == 'replace':
        new, n = re.subn(anchor, lambda m: payload, s)
        if n != 1:
            return f'FAIL {fname}: replace anchor matched {n} times, expected 1'
        s = new
    elif kind == 'after_box':
        # Insert after the box whose tag is `anchor`, i.e. at the next blank line
        # followed by a new block-level div.
        i = s.find(anchor)
        if i < 0:
            return f'FAIL {fname}: no box tagged "{anchor}"'
        j = s.find('\n\n<div class="box', i)
        k = s.find('\n\n<h3', i)
        cut = min(x for x in (j, k) if x >= 0)
        s = s[:cut] + payload + s[cut:]
    else:
        n = s.count(anchor)
        if n != 1:
            return f'FAIL {fname}: anchor found {n} times, expected 1'
        i = s.index(anchor)
        at = i if kind == 'before' else i + len(anchor)
        s = s[:at] + payload + s[at:]

    with open(path, 'w', encoding='utf-8') as fh:
        fh.write(s)
    return f'{fname}: inserted "{marker[:34]}"'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    fails = []
    for e in EDITS:
        msg = apply_one(*e)
        print('  ' + msg)
        if msg.startswith('FAIL'):
            fails.append(msg)
    print(f'gapfill_decks: {len(EDITS)} insertions attempted, {len(fails)} failed')
    if fails:
        sys.exit(1)


if __name__ == '__main__':
    main()
