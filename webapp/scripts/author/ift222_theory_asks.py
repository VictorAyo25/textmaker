"""Every theory ask on the IFT222 past papers, quoted and answered.

    python scripts/author/ift222_theory_asks.py

The theory solutions book is organised by PAPER, which is right for practice and
wrong for revision: the asks that need no calculator are scattered across four
papers and five questions each, so the reader meets "State Amdahl's law" once,
in the middle of a cache calculation. This gathers them into one front section,
grouped by what the examiner asks you to DO: define it, list it, explain it,
compare it, and the one line "explain why" asks tacked onto a calculation.

Every quote is SLICED OUT OF THE PRINTED TEXT in data/ift222/lessons.json, never
retyped, so the examiner's words, and his typos ("in an 10-bit register", the
stray apostrophe after "State Amdahl's law'"), survive by construction. The gate
then re-checks every one of them independently and fails the build on a
paraphrase, on an ask that no paper contains, and on a theory ask in the papers
that this file has left out.

Writes data/ift222/theory-asks.json. Idempotent.
"""
import html
import json
import re
from pathlib import Path

WEBAPP = Path(__file__).resolve().parent.parent.parent
LESSONS = WEBAPP / "data" / "ift222" / "lessons.json"
OUT = WEBAPP / "data" / "ift222" / "theory-asks.json"


def plain(s: str) -> str:
    """The printed question as a reader sees it: no markup, single spaces."""
    s = re.sub(r"<(figure|svg)[\s\S]*?</\1>", " ", s or "")
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


LESSON_DATA = json.loads(LESSONS.read_text(encoding="utf-8"))
# (tag, printed text) for every As printed block, which is every part of every
# paper the course owns.
PRINTED = [
    ((b.get("tag") or ""), plain(b["printed"]))
    for lesson in LESSON_DATA
    for b in lesson["blocks"]
    if b.get("kind") == "asprinted"
]


def cut(tag, start, end=None):
    """The examiner's own words for one sub-ask, sliced from the printed text.

    tag is the paper part it was printed in, start the first words of the
    sub-ask, end the first words of the NEXT one (None runs to the end of the
    part). It raises rather than guessing: a start no paper carries means the
    ask has been mistyped, and a silent miss would put a paraphrase in front of
    the reader as though the examiner had written it.
    """
    for t, text in PRINTED:
        if not t.startswith(tag):
            continue
        at = text.find(start)
        if at == -1:
            continue
        stop = len(text)
        if end:
            found = text.find(end, at + len(start))
            if found == -1:
                raise SystemExit(f"{tag}: found {start!r} but not the following {end!r}")
            stop = found
        return text[at:stop].strip()
    raise SystemExit(f"{tag}: no printed question contains {start!r}")


def src(paper, part, marks, tag, start, end=None, note=None):
    """One occurrence of an ask: which paper, which part, what it was worth."""
    out = {"paper": paper, "part": part, "marks": marks, "quote": cut(tag, start, end)}
    if note:
        out["note"] = note
    return out


def architecture_figures():
    """The Von Neumann and Harvard diagrams already drawn under 25/26 Q1(a).

    The compare ask carries the same pair rather than a second copy, so a
    correction to either diagram reaches both places.
    """
    for lesson in LESSON_DATA:
        blocks = lesson["blocks"]
        for i, b in enumerate(blocks):
            if b.get("kind") == "asprinted" and (b.get("tag") or "") == "25/26 Q1(a)":
                worked = next(n for n in blocks[i + 1 : i + 4] if n.get("kind") == "worked")
                body = (worked.get("working") or "") + (worked.get("answer") or "")
                figs = re.findall(r"<figure>.*?</figure>", body, re.S)
                if len(figs) < 2:
                    raise SystemExit("25/26 Q1(a) no longer carries both architecture diagrams")
                return "".join(figs[:2])
    raise SystemExit("25/26 Q1(a) not found")


LEAD = (
    "Every ask on the four papers that needs no calculator: the definitions, the lists, the "
    "comparisons and the explanations. Each one is quoted in the examiner's own words, with every "
    "paper that set it and the marks it carried, and answered at the length those marks buy. "
    "Where he reworded an ask between papers, every wording is printed."
)


def groups(figs):
    return [
        {
            "kind": "Define it",
            "when": (
                "The ask opens with What is, What do you understand by, or State. It wants the "
                "thing named and bounded in a sentence or two, not a description of how it is used."
            ),
            "asks": [
                {
                    "id": "what-is-pipelining",
                    "topic": "Pipelining",
                    "papers": [
                        src("2020/2021", "Q1(b)(i)", 2, "2020/2021, Question 1(b)",
                            "i) What is pipelining?", "ii) Calculate how long")
                    ],
                    "answer": (
                        "<p><b>Pipelining</b> is an implementation technique in which the execution "
                        "of an instruction is split into a fixed sequence of stages, each with its "
                        "own hardware, so that several instructions occupy different stages at the "
                        "same instant. The classic five stage pipeline is fetch, decode, execute, "
                        "memory and write back.</p>"
                        "<p>It does not make one instruction finish sooner, it raises how many "
                        "finish per unit time. Once the pipeline is full, a k stage pipeline "
                        "completes one instruction every clock cycle, so n instructions take "
                        "(k + n &#8722; 1) cycles instead of n &#215; k.</p>"
                    ),
                },
                {
                    "id": "von-neumann-concept",
                    "topic": "Von Neumann",
                    "papers": [
                        src("2024/2025", "Q3(a)(i)", 1, "2024/2025, Question 3(a)",
                            "i) What do you understand by Von Neumann Concept?",
                            "ii) Mention any 2")
                    ],
                    "answer": (
                        "<p>The <b>Von Neumann concept</b>, also called the stored program concept, "
                        "is that a computer keeps its program and its data together in the same "
                        "memory, and runs the program by fetching those instructions from that "
                        "memory and obeying them one after another.</p>"
                    ),
                },
                {
                    "id": "amdahls-law",
                    "topic": "CPU performance",
                    "papers": [
                        src("2025/2026", "Q3(c)(i)", 2, "2025/2026, Question 3(c)",
                            "i) State Amdahl's law", "ii) Assume in hypothetical"),
                        src("2023/2024", "Q1(b)(i)", 2.5, "2023/2024, Question 1(b)",
                            "i) State Amdahl's law", "ii) Assume in hypothetical"),
                    ],
                    "answer": (
                        "<p><b>Amdahl's law</b> states that the overall speedup a system gains by "
                        "improving one of its parts is limited by the fraction of the total time "
                        "that part is actually in use.</p>"
                        "<p>With <b>f</b> the fraction of the time that is sped up and <b>s</b> the "
                        "speedup of that part:</p>"
                        "<p><b>S = 1 / ((1 &#8722; f) + f/s)</b></p>"
                        "<p>The part left untouched sets the ceiling: even making the improved part "
                        "infinitely fast leaves S no greater than 1 / (1 &#8722; f). A cache ten times "
                        "faster than memory, hit 85% of the time, gives "
                        "1 / (0.15 + 0.085) = 4.26, not 10.</p>"
                    ),
                },
                {
                    "id": "cache-miss",
                    "topic": "Memory and cache",
                    "papers": [
                        src("2024/2025", "Q2(b)(ii)", 1.5, "2024/2025, Question 2(b)",
                            "ii) What happens when there is a Cache Miss?")
                    ],
                    "answer": (
                        "<p>On a <b>cache miss</b> the word the CPU asked for is not in the cache, "
                        "so:</p>"
                        "<ol>"
                        "<li>the cache signals the miss and the CPU stalls;</li>"
                        "<li>the address is passed out to main memory;</li>"
                        "<li>main memory returns the <b>whole block</b> that contains the word, not "
                        "the word alone, because of spatial locality;</li>"
                        "<li>that block is written into a cache line, a line being evicted first if "
                        "none is free, chosen by the replacement policy such as LRU;</li>"
                        "<li>the tag and valid bit are set and the word is delivered to the CPU, so "
                        "the next access to that block hits.</li>"
                        "</ol>"
                        "<p>The time those steps cost is the <b>miss penalty</b>, which is why a "
                        "miss rate of a few per cent still dominates the average access time.</p>"
                    ),
                },
                {
                    "id": "overflow-underflow",
                    "topic": "Signed numbers",
                    "papers": [
                        src("2024/2025", "Q4(b)(ii)", 3, "2024/2025, Question 4(b)",
                            "ii) What do you understand by Overflow")
                    ],
                    "answer": (
                        "<p><b>Overflow</b> is a result too large for the number of bits available, "
                        "so the value stored is not the value computed. Example: 8 bit two's "
                        "complement holds &#8722;128 to +127, so 100 + 50 = 150 overflows, and the bits "
                        "stored, 1001 0110, read back as &#8722;106.</p>"
                        "<p><b>Underflow</b> is a result too small for the representation to hold. "
                        "For integers that is a value below the most negative one storable: "
                        "&#8722;100 &#8722; 50 = &#8722;150 underflows that same 8 bit range. In floating point it "
                        "is a value so close to zero that the exponent cannot go low enough, so it "
                        "rounds away to zero: 10<sup>&#8722;40</sup> underflows IEEE 754 single "
                        "precision, whose smallest normalised magnitude is about "
                        "1.18 &#215; 10<sup>&#8722;38</sup>.</p>"
                        "<p>Both are <b>range</b> errors, one off the top of the range and one off "
                        "the bottom.</p>"
                    ),
                },
            ],
        },
        {
            "kind": "List it",
            "when": (
                "State, mention or list a fixed number of things, and the number is in the ask. "
                "Where the ask is for differences, each line has to contrast both sides on one "
                "property: four statements about RISC alone are not four differences."
            ),
            "asks": [
                {
                    "id": "risc-cisc-differences",
                    "topic": "RISC and CISC",
                    "papers": [
                        src("2024/2025", "Q4(a)(ii)", 4, "2024/2025, Question 4(a)",
                            "ii) Mention any four (4) clear differences"),
                        src("2020/2021", "Q4(b)(i)", 4, "2020/2021, Question 4(b)",
                            "i) State Four (4) clear differences"),
                        src("2023/2024", "Q5(c)", 3, "2023/2024, Question 5(c)",
                            "Mention any 3 clear differences"),
                    ],
                    "answer": (
                        "<table>"
                        "<tr><th></th><th>RISC</th><th>CISC</th></tr>"
                        "<tr><td>Instruction set</td><td>Small and simple, each instruction doing "
                        "one thing</td><td>Large and complex, one instruction doing multi step "
                        "work</td></tr>"
                        "<tr><td>Instruction length</td><td>Fixed, so decoding and pipelining are "
                        "simple</td><td>Variable, so decoding is harder and pipelining "
                        "awkward</td></tr>"
                        "<tr><td>Memory access</td><td>Load and store only, arithmetic works on "
                        "registers</td><td>Instructions may operate directly on memory "
                        "operands</td></tr>"
                        "<tr><td>Cycles per instruction</td><td>Typically one, from a hardwired "
                        "control unit</td><td>Many, from a microcoded control unit</td></tr>"
                        "<tr><td>Registers</td><td>Many general purpose registers</td>"
                        "<td>Fewer registers, more addressing modes instead</td></tr>"
                        "</table>"
                        "<p><b>Two example processors each.</b> RISC: ARM and MIPS (SPARC and "
                        "PowerPC also count). CISC: the Intel x86 family, 8086 and Pentium, and "
                        "the Motorola 68000 (the DEC VAX also counts).</p>"
                    ),
                },
                {
                    "id": "von-neumann-aspects",
                    "topic": "Von Neumann",
                    "papers": [
                        src("2024/2025", "Q3(a)(ii)", 2, "2024/2025, Question 3(a)",
                            "ii) Mention any 2 significant aspects", "iii) Describe the Von Neumann")
                    ],
                    "answer": (
                        "<ul>"
                        "<li><b>A single shared memory.</b> Instructions and data are held in the "
                        "same memory and travel over the same bus, so nothing but the way the "
                        "machine uses a word tells an instruction from a datum.</li>"
                        "<li><b>Sequential execution of a stored program.</b> The program counter "
                        "holds the address of the next instruction, and instructions are fetched "
                        "and obeyed one at a time, in order, until a branch changes the "
                        "counter.</li>"
                        "</ul>"
                    ),
                },
                {
                    "id": "dram-sram",
                    "topic": "Memory technology",
                    "papers": [
                        src("2020/2021", "Q5(b)(i)", 4, "2020/2021, Question 5(b)",
                            "i) List four (4) differences between DRAM")
                    ],
                    "answer": (
                        "<table>"
                        "<tr><th></th><th>DRAM</th><th>SRAM</th></tr>"
                        "<tr><td>Storage cell</td><td>A charge held on a capacitor</td>"
                        "<td>A latch of transistors, typically six</td></tr>"
                        "<tr><td>Refresh</td><td>Must be refreshed every few milliseconds or the "
                        "charge leaks away</td><td>Needs no refresh while the power is on</td></tr>"
                        "<tr><td>Speed</td><td>Slower access</td><td>Faster access</td></tr>"
                        "<tr><td>Density and cost</td><td>High density, cheap per bit</td>"
                        "<td>Low density, dear per bit</td></tr>"
                        "<tr><td>Where it is used</td><td>Main memory</td>"
                        "<td>Cache and registers</td></tr>"
                        "</table>"
                    ),
                },
                {
                    "id": "mapping-advantages",
                    "topic": "Cache mapping",
                    "papers": [
                        src("2024/2025", "Q2(a)(iii)", None, "2024/2025, Question 2(a)",
                            "iii) State one advantage", "specifications:",
                            note="the 8 marks cover (ii) and (iii) together")
                    ],
                    "answer": (
                        "<table>"
                        "<tr><th>Mapping</th><th>Advantage</th><th>Disadvantage</th></tr>"
                        "<tr><td>Direct</td><td>Simplest and fastest lookup: a block can be in "
                        "exactly one line, so one tag comparison decides the hit</td>"
                        "<td>Two blocks that map to the same line evict each other however empty "
                        "the rest of the cache is, which is a conflict miss</td></tr>"
                        "<tr><td>Fully associative</td><td>A block may sit in any line, so there "
                        "are no conflict misses at all</td>"
                        "<td>Every line's tag must be compared at once, needing a comparator per "
                        "line and a replacement policy, so it is costly and the hit time grows "
                        "with the cache</td></tr>"
                        "<tr><td>Set associative, k way</td><td>The compromise: nearly all conflict "
                        "misses go for only k comparisons per access</td>"
                        "<td>More complex than direct mapping, and blocks competing for one set "
                        "can still evict one another</td></tr>"
                        "</table>"
                    ),
                },
            ],
        },
        {
            "kind": "Explain it, describe it, discuss it",
            "when": (
                "A name on its own is not an explanation. Say what the thing is, then why it holds "
                "or what the machine does about it, and where the ask says illustrate, the "
                "illustration carries its own marks."
            ),
            "asks": [
                {
                    "id": "locality",
                    "topic": "Memory and cache",
                    "papers": [
                        src("2025/2026", "Q5(c)", 3, "2025/2026, Question 5(c)",
                            "Explain the following terms 3mks"),
                        src("2024/2025", "Q2(b)(i)", 4.5, "2024/2025, Question 2(b)",
                            "i) Explain the following terms:", "ii) What happens"),
                        src("2023/2024", "Q3(c)", 4.5, "2023/2024, Question 3(c)",
                            "Explain the following 4"),
                    ],
                    "answer": (
                        "<p><b>Locality of reference</b> is the tendency of a program to use a "
                        "small and predictable set of memory locations during any short period, a "
                        "consequence of loops, of arrays and of subroutines. It is the reason a "
                        "small fast cache can satisfy most accesses, and so the reason a memory "
                        "hierarchy works at all.</p>"
                        "<p><b>Temporal locality</b>, locality in time: a location used now is "
                        "likely to be used again soon, as with a loop counter or the instructions "
                        "of the loop body. The machine exploits it by <b>keeping</b> recently used "
                        "blocks in the cache.</p>"
                        "<p><b>Spatial locality</b>, locality in space: locations near one just "
                        "used are likely to be used next, as when stepping through an array or "
                        "running straight line code. The machine exploits it by fetching a "
                        "<b>whole block</b> of neighbouring words on every miss.</p>"
                        "<p>Where the paper prints \"Special Locality\" or \"Spacial Locality\", the "
                        "term meant is spatial locality.</p>"
                    ),
                },
                {
                    "id": "cache-improves-performance",
                    "topic": "Memory and cache",
                    "papers": [
                        src("2024/2025", "Q2(a)(i)", 2, "2024/2025, Question 2(a)",
                            "i) Describe how cache memory improves", "ii) Using the specifications")
                    ],
                    "answer": (
                        "<p>Cache is a small, very fast memory between the CPU and main memory, "
                        "holding copies of the blocks in current use. Because programs show "
                        "locality of reference most requests are found there and are served at "
                        "cache speed instead of main memory speed, so the processor spends far "
                        "less time stalled waiting on memory.</p>"
                        "<p>The gain is in the <b>average</b> access time, "
                        "AMAT = T<sub>c</sub> + (1 &#8722; h) &#215; T<sub>m</sub>. With a hit rate "
                        "h = 0.96, a 2 ns cache and an 80 ns memory, the average access is "
                        "2 + 0.04 &#215; 80 = 5.2 ns rather than 80 ns, about fifteen times faster, "
                        "and no program had to be rewritten to get it.</p>"
                    ),
                },
                {
                    "id": "von-neumann-bottleneck",
                    "topic": "Von Neumann",
                    "papers": [
                        src("2024/2025", "Q3(a)(iii)", 2, "2024/2025, Question 3(a)",
                            "iii) Describe the Von Neumann architecture bottleneck")
                    ],
                    "answer": (
                        "<p>In the Von Neumann design instructions and data share one memory and "
                        "one bus, so only one of them can be in transit at a time: the processor "
                        "cannot fetch an instruction and read or write that instruction's data in "
                        "the same instant, and the two must take turns on the single path.</p>"
                        "<p>That shared path, not the processor, then sets the speed of the "
                        "machine. However fast the CPU is made it spends its time waiting on the "
                        "one bus, and that gap between processor speed and memory bandwidth is the "
                        "<b>Von Neumann bottleneck</b>. It is why the Harvard design separates the "
                        "two memories, and why caches exist.</p>"
                    ),
                },
                {
                    "id": "instruction-categories",
                    "topic": "Instruction sets",
                    "papers": [
                        src("2024/2025", "Q5(a)(i)", 4.5, "2024/2025, Question 5(a)",
                            "i) Describe three (3) categories", "ii) Discuss the characteristics")
                    ],
                    "answer": (
                        "<ul>"
                        "<li><b>Data transfer.</b> Move a value between registers, memory and "
                        "input or output without changing it. Examples: LOAD and STORE (also MOVE, "
                        "PUSH, POP).</li>"
                        "<li><b>Arithmetic and logic, also called data processing.</b> Compute a "
                        "new value from operands held in registers or memory, setting the "
                        "condition flags. Examples: ADD and AND (also SUB, MUL, OR, NOT and the "
                        "shifts).</li>"
                        "<li><b>Control transfer, also called program control.</b> Change which "
                        "instruction runs next, conditionally or not, so a program can test and "
                        "repeat. Examples: JUMP and BEQ (also CALL and RETURN).</li>"
                        "</ul>"
                    ),
                },
                {
                    "id": "memory-access-methods",
                    "topic": "Memory technology",
                    "papers": [
                        src("2024/2025", "Q5(a)(ii)", 4, "2024/2025, Question 5(a)",
                            "ii) Discuss the characteristics of computer memory")
                    ],
                    "answer": (
                        "<ul>"
                        "<li><b>Sequential access.</b> Records are read in the order they were "
                        "written, passing over everything in between, so the access time depends "
                        "on where the item sits and where the mechanism is now. Example: magnetic "
                        "tape.</li>"
                        "<li><b>Direct access.</b> Each block has its own address that the "
                        "mechanism moves to, then a short sequential search finds the item within "
                        "the block, so access times vary but only a little. Example: a magnetic "
                        "disk.</li>"
                        "<li><b>Random access.</b> Every location has its own addressing "
                        "circuitry and is reached in the same time as any other, whatever the "
                        "order of access. Example: semiconductor main memory, RAM.</li>"
                        "<li><b>Associative access.</b> A word is found by its contents rather "
                        "than by its address: a pattern is presented and every location compares "
                        "itself with it at once. Example: the tag memory of a cache.</li>"
                        "</ul>"
                    ),
                },
                {
                    "id": "end-around-carry",
                    "topic": "Signed numbers",
                    "papers": [
                        src("2024/2025", "Q4(b)(i)", 4, "2024/2025, Question 4(b)",
                            "i) Describe End-Around Carry", "ii) What do you understand by Overflow"),
                        src("2020/2021", "Q5(a)(ii)", 4, "2020/2021, Question 5(a)",
                            "ii) Describe End-Around Carry"),
                    ],
                    "answer": (
                        "<p><b>What it is.</b> In one's complement arithmetic a &#8722; b is done as "
                        "a + (&#8722;b), where &#8722;b is b with every bit inverted. If that addition "
                        "produces a carry out of the most significant bit the carry is not thrown "
                        "away: it is brought round and added into the least significant bit, and "
                        "that step is the <b>end around carry</b>. It is needed because one's "
                        "complement has two representations of zero, so without it every such sum "
                        "comes out one short. The carry out also tells you the result is positive; "
                        "no carry out means the result is negative and already in one's complement "
                        "form.</p>"
                        "<p><b>153 &#8722; 142 in a 10 bit register.</b></p>"
                        "<p>153 = 00 1001 1001<br>"
                        "142 = 00 1000 1110, so &#8722;142 = 11 0111 0001 (every bit inverted)</p>"
                        "<p>Add them:<br>"
                        "&nbsp;&nbsp;00 1001 1001<br>"
                        "+ 11 0111 0001<br>"
                        "= 1 00 0000 1010, with a carry out of the tenth bit</p>"
                        "<p>End around carry: 00 0000 1010 + 1 = <b>00 0000 1011</b> = 11, "
                        "leading bit 0 so positive, and 153 &#8722; 142 = 11. Correct.</p>"
                    ),
                },
                {
                    "id": "data-hazard-types",
                    "topic": "Pipelining",
                    "papers": [
                        src("2020/2021", "Q1(c)(i)", 1.5, "2020/2021, Question 1(c)",
                            "i) Describe the three types of data hazards",
                            "ii) What type of data hazards")
                    ],
                    "answer": (
                        "<ul>"
                        "<li><b>RAW, read after write</b>, a true dependency: an instruction needs "
                        "an operand an earlier instruction has not yet written, so it waits or is "
                        "handed the value by forwarding. MUL R2,R0,R1 then ADD R4,R2,R3 is RAW on "
                        "R2.</li>"
                        "<li><b>WAR, write after read</b>, an anti dependency: a later instruction "
                        "would write a register an earlier one has not yet read, so reordering "
                        "them would make the earlier one read the wrong value.</li>"
                        "<li><b>WAW, write after write</b>, an output dependency: two instructions "
                        "write the same register, and completing out of order would leave the "
                        "wrong value behind.</li>"
                        "</ul>"
                        "<p>RAW is a genuine flow of data and can only be hidden, by forwarding. "
                        "WAR and WAW are name dependencies and disappear altogether if the "
                        "registers are renamed.</p>"
                    ),
                },
                {
                    "id": "identify-hazards",
                    "topic": "Pipelining",
                    "context": (
                        "on the segment printed with the question: LW R1,0(R2) then ADD R3,R1,R4, "
                        "SUB R5,R3,R6, SW R5,8(R2), BEQ R5,R0,LABEL and MUL R7,R5,R8, with "
                        "forwarding available, the branch resolved in EX, one stall per load use, "
                        "a three cycle multiply and separate instruction and data caches"
                    ),
                    "papers": [
                        src("2025/2026", "Q2(b)(i)", 5, "2025/2026, Question 2(b)",
                            "i) Identify and explain every pipeline hazard",
                            "ii) Draw the pipeline timing")
                    ],
                    "answer": (
                        "<p>Take each instruction's destination register and look for it among the "
                        "source registers of those behind it. That, not the mnemonic, is what "
                        "finds every hazard.</p>"
                        "<p><b>Data hazards, all of them RAW:</b></p>"
                        "<ul>"
                        "<li><b>I1 to I2, a load use hazard.</b> I2 needs R1, which the load only "
                        "has after its MEM stage, so even with forwarding I2 must stall one cycle. "
                        "This is the one RAW that forwarding cannot remove.</li>"
                        "<li><b>I2 to I3</b> on R3, and <b>I3 to I4, I3 to I5 and I3 to I6</b> on "
                        "R5, are ordinary RAW hazards between arithmetic instructions, and "
                        "forwarding from EX to EX hides every one of them at no cost.</li>"
                        "</ul>"
                        "<p><b>Control hazard.</b> I5, the BEQ, is not resolved until its EX stage, "
                        "so whatever is fetched behind it is fetched before the outcome is known. "
                        "Without prediction a taken branch costs two cycles; the segment as "
                        "printed is counted as falling through.</p>"
                        "<p><b>Structural hazards.</b> The usual one, an instruction fetch clashing "
                        "with a data access in the same cycle, is removed by the separate "
                        "instruction and data caches the question grants. The multiplier is the "
                        "one that remains: I6 holds the single execute unit for three cycles, so "
                        "anything behind it would have to wait for the unit rather than for "
                        "data.</p>"
                        "<p>No WAR or WAW hazard arises here, because this pipeline writes back in "
                        "order and each of R1, R3, R5 and R7 is written by exactly one "
                        "instruction.</p>"
                    ),
                },
            ],
        },
        {
            "kind": "Compare it",
            "when": (
                "Differentiate or compare. Two columns and one property a row, so the contrast is "
                "visible without being read, and where a diagram is asked for it carries marks of "
                "its own."
            ),
            "asks": [
                {
                    "id": "architecture-vs-organization",
                    "topic": "Architecture and organization",
                    "papers": [
                        src("2025/2026", "Q1(a)(i)", 2, "2025/2026, Question 1(a)",
                            "i) Computer Systems are designed", "ii) Compare Von Neumann")
                    ],
                    "answer": (
                        "<p><b>Computer architecture</b> is the functional design and logical "
                        "structure of the system as the programmer sees it: the instruction set, "
                        "the data types, the addressing modes and the register organization. It "
                        "answers <b>what the computer does</b>, and is the specification a machine "
                        "is built to.</p>"
                        "<p><b>Computer organization</b> is the operational units and their "
                        "interconnection that realise that architecture: the control signals, the "
                        "buses and their widths, the memory technology, the caches and how the "
                        "units are pipelined. It answers <b>how the computer does it</b>.</p>"
                        "<table>"
                        "<tr><th></th><th>Architecture</th><th>Organization</th></tr>"
                        "<tr><td>Question it answers</td><td>What does it do</td>"
                        "<td>How is it done</td></tr>"
                        "<tr><td>Who sees it</td><td>The programmer, through the instruction "
                        "set</td><td>The hardware designer, and it is hidden from the "
                        "program</td></tr>"
                        "<tr><td>How often it changes</td><td>Rarely, because software depends on "
                        "it</td><td>Freely, between models of one family</td></tr>"
                        "<tr><td>A likeness</td><td>The architect's drawing of a building</td>"
                        "<td>The materials and methods it is actually built with</td></tr>"
                        "</table>"
                        "<p>One architecture can have many organizations: every x86 processor from "
                        "the 8086 onwards runs the same instruction set with an entirely different "
                        "internal design.</p>"
                    ),
                },
                {
                    "id": "von-neumann-vs-harvard",
                    "topic": "Von Neumann",
                    "papers": [
                        src("2025/2026", "Q1(a)(ii)", 3, "2025/2026, Question 1(a)",
                            "ii) Compare Von Neumann Architecture"),
                        src("2024/2025", "Q4(a)(i)", 3, "2024/2025, Question 4(a)",
                            "i) Compare Von Neumann Architecture", "ii) Mention any four"),
                    ],
                    "answer": (
                        "<table>"
                        "<tr><th></th><th>Von Neumann</th><th>Harvard</th></tr>"
                        "<tr><td>Memory</td><td>One memory holds instructions and data "
                        "together</td><td>Separate instruction memory and data memory</td></tr>"
                        "<tr><td>Buses</td><td>One shared bus, so a fetch and a data access take "
                        "turns</td><td>Separate buses, so a fetch and a data access happen at "
                        "once</td></tr>"
                        "<tr><td>Speed</td><td>Capped by that shared path, the Von Neumann "
                        "bottleneck</td><td>Higher throughput, and it suits pipelining</td></tr>"
                        "<tr><td>Cost and flexibility</td><td>Simpler and cheaper, and memory can "
                        "be divided between code and data as a program needs</td><td>More "
                        "hardware, and the split between code and data is fixed</td></tr>"
                        "<tr><td>Where it is used</td><td>General purpose computers</td>"
                        "<td>Digital signal processors, microcontrollers, and the split level 1 "
                        "caches inside modern CPUs</td></tr>"
                        "</table>"
                        "<p>Both diagrams carry marks of their own, so draw them:</p>" + figs
                    ),
                },
            ],
        },
        {
            "kind": "Explain why",
            "when": (
                "One line asks tacked onto the end of a calculation, worth a mark or so each. Each "
                "one wants the reason, not the arithmetic again."
            ),
            "asks": [
                {
                    "id": "speedup-below-maximum",
                    "topic": "Pipelining",
                    "papers": [
                        src("2025/2026", "Q1(b)(v)", 1, "2025/2026, Question 1(b)",
                            "v) Explain why the speedup differs")
                    ],
                    "answer": (
                        "<p>The theoretical maximum for a five stage pipeline is 5, and it assumes "
                        "perfectly balanced stages, no overhead between them, and one instruction "
                        "completing every cycle. This processor meets none of those: the stages are "
                        "5, 4, 6, 5 and 4 ns so the clock is set by the slowest, the pipeline "
                        "register overhead adds 1 ns to every cycle, and branches (two extra "
                        "cycles), floating point (three cycles in EX) and the 10% of memory "
                        "accesses that miss (four extra cycles) lift the actual CPI to 2.44 instead "
                        "of 1. The speedup comes out near 1.46, not 5.</p>"
                    ),
                },
                {
                    "id": "associativity-beyond-four",
                    "topic": "Cache mapping",
                    "papers": [
                        src("2025/2026", "Q2(c)(v)", 2, "2025/2026, Question 2(c)",
                            "v) Discuss how increasing associativity")
                    ],
                    "answer": (
                        "<p>Raising the associativity removes conflict misses, because more blocks "
                        "that map to the same set can be held at once. The gain falls away "
                        "quickly, though: most conflicts have already gone by four ways, so eight "
                        "or sixteen buys very little further hit rate.</p>"
                        "<p>The costs keep rising in a straight line. Every extra way is another "
                        "tag comparator working in parallel and a wider multiplexer on the data "
                        "path, so the hit time and the power both grow; LRU replacement over more "
                        "ways is harder to implement; and each doubling of the ways halves the "
                        "number of sets, so a set index bit moves into the tag and the tag "
                        "directory grows. Past four ways the added hit time can cost more than the "
                        "misses it saves, and the average access time gets worse rather than "
                        "better. A fully associative cache is the limit of this, which is why only "
                        "small structures such as a TLB are built that way.</p>"
                    ),
                },
                {
                    "id": "fully-associative-cost",
                    "topic": "Cache mapping",
                    "papers": [
                        src("2025/2026", "Q3(a)(iv)", 1.5, "2025/2026, Question 3(a)",
                            "iv) Explain why fully associative")
                    ],
                    "answer": (
                        "<p>A block may be placed in <b>any</b> line, so no two addresses are ever "
                        "forced to compete for one line: conflict misses vanish and only "
                        "compulsory and capacity misses remain.</p>"
                        "<p>The cost is the <b>search</b>. With no index field to point at one "
                        "line, the address tag must be compared against every line's tag, and "
                        "doing that in one cycle needs a comparator per line, that is content "
                        "addressable memory. So the hardware and the power grow with the cache, "
                        "the hit time grows with it, the tag field itself is longer because the "
                        "index bits are gone, and a replacement policy such as LRU must now be "
                        "implemented and updated on every access. That is why real caches are set "
                        "associative: nearly all of the gain for a small fraction of the cost.</p>"
                    ),
                },
                {
                    "id": "reduce-stalls",
                    "topic": "Pipelining",
                    "papers": [
                        src("2025/2026", "Q2(b)(iv)", 1, "2025/2026, Question 2(b)",
                            "iv) Suggest any two hardware improvements")
                    ],
                    "answer": (
                        "<ul>"
                        "<li><b>Fuller forwarding, or bypass, paths</b>, including MEM to EX, so a "
                        "value reaches the instruction behind it in the cycle it is produced "
                        "instead of after write back.</li>"
                        "<li><b>Pipeline or duplicate the multiplier</b>, so a three cycle multiply "
                        "no longer holds the single execute unit and the instructions behind it do "
                        "not wait for it.</li>"
                        "</ul>"
                        "<p>Branch prediction with a branch target buffer, which removes the "
                        "control stall on the BEQ, and separate instruction and data caches, which "
                        "this question already grants, are the other two that earn the mark.</p>"
                    ),
                },
            ],
        },
    ]


def main():
    book = {"lead": LEAD, "groups": groups(architecture_figures())}
    OUT.write_text(json.dumps(book, indent=1, ensure_ascii=False) + chr(10), encoding="utf-8")

    asks = [a for g in book["groups"] for a in g["asks"]]
    per_paper = {}
    for a in asks:
        for s in a["papers"]:
            hit = per_paper.setdefault(s["paper"], [0, 0.0, False])
            hit[0] += 1
            if s["marks"] is None:
                hit[2] = True
            else:
                hit[1] += s["marks"]
    print(f"  {len(asks)} theory asks in {len(book['groups'])} groups")
    for g in book["groups"]:
        print(f"    {g['kind']}: {len(g['asks'])}")
    for paper in sorted(per_paper, reverse=True):
        n, marks, shared = per_paper[paper]
        print(f"    {paper}: {n} asks, {marks:g} marks{' and a shared block' if shared else ''}")
    print(f"  written to {OUT.relative_to(WEBAPP)}")


if __name__ == "__main__":
    main()
