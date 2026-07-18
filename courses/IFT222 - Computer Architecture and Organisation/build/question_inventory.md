# IFT222 — Master Question Inventory (coverage gate)

> **SLIDE-COVERAGE BLEND (2026-07-18): after a four-deck audit, every substantive teaching
> item from the lecturer slides is now in the manual (77pp).** Added: bit-shift x2/div2;
> BCD weighted codes (8421/5421/4221) + Excess-3 both ways; character codes (Morse,
> Hollerith, ASCII table/ranges/DEL, EBCDIC, Unicode); bitmap-vs-vector graphics + the
> 4x6@300dpi worked example; double-precision floating point + IEEE operations; memory
> characteristics/vocabulary (nibble/cell/word/block) + memory-size calc; the two-level
> hierarchy average-access example (95% -> 0.015us); tag-directory size across all three
> mappings; cache read dataflow, physical/logical(virtual) addressing + MMU, cache-size
> trade-off; ISA binary-instruction decode drills, indirect ADD/STORE, backward relative
> branch, condition-code register, Boolean data type, load/store direction; computer
> definition + components/motherboard; Stack Pointer; I/O (programmed/interrupt/DMA);
> DDR/prefetch/PIM. Deliberately skipped: the Ariane-5/Vancouver anecdotes and
> processor-specific mnemonics (MC68000). Every new number is in the numeric gate (148
> checks); all five gates green.
>
> **COVERAGE STATUS (2026-07-18): the manual teaches every method and solves a
> representative instance of every question type across all papers, weighted to 24/25 +
> 25/26.** Descriptive staples (arch/org, VN vs Harvard, bottleneck, RISC/CISC, locality,
> DRAM/SRAM, access methods, instruction categories, addressing modes, data hazards,
> Flynn) all covered. Numeric types all worked with the real exam values: number-rep
> tables, IEEE both ways (incl. X/Y/Z, -1240.56, C4F2E000), 2's-comp range/arithmetic,
> end-around carry, overflow, image memory, CPI/addressing-CPI, Amdahl, pipeline
> speedup/throughput, RISC load-use hazard timing, instruction formats + byte counting,
> EA/operand, cache block lookup + address fields + AMAT, cache sizes. Boolean/K-map in
> the flagged Supplement. Both mocks fully solved with fresh recomputed numbers.
>
> **All question types now individually worked, including 25/26 Q3b** (multi-cycle EX
> MUL=3/DIV=6 pipeline): added to M2U3 as a full transposed cycle diagram under explicitly
> stated structural assumptions (single in-order EX unit; WB one cycle after EX; forwarding
> feeds EX the next cycle). Schedule verified by simulation: **15 cycles with forwarding,
> 17 without**. Both counts are in the numeric gate. Nothing is left method-only.


Every question in every source, organised by topic (the order teaching will follow so
each topic's questions are solved as it is taught). Requirement: **no question escapes**
the manual. `Covered:` is filled with the manual section that solves it as authoring
proceeds. Victor's emphasis: **24/25 (PQ2425) and 25/26 (PQ2526)** get the deepest
drilling; the mocks lean their way. Off-syllabus items are tagged [NOT-IN-SYLLABUS] and
still taught to a pass.

Source IDs:
- PQ2021 = exam 2020/2021 (printed CSC227)   | PQ2324 = exam 2023/2024
- PQ2425 = exam 2024/2025 [FAVE]             | PQ2526 = exam 2025/2026 [FAVE, newest, richest]
- T1a = test 1 2021-2022.jpg | T1b = test 1 question.jpg | T1mk = test question.jpg (makeup) | Tq2 = test question.jpg (2nd 25-min test)
- T2a = test 2 question1.jpg | T2b = test 2.jpg | T2mk = Test 2 Marking guide.pdf (solves T2b)
- CW = classwork docx | CH6 = ch6-examples.pdf | TUT = CSC227 tutorial sheet
- DECK-INTRO / DECK-DATA / DECK-ISA / DECK-MEM = slide quizzes/homework/worked examples

Legend for type: [NUM]=calculation, [DESC]=descriptive, [DESIGN]=logic/diagram design, [CODE]=assembly.

---

## MODULE ONE

### U1. Architecture vs Organization; Von Neumann vs Harvard; bottleneck  [DESC]
- [ ] PQ2021-Q2c(i): Von Neumann vs Harvard with diagrams (3). Covered:
- [ ] PQ2021-Q2c(ii): Von Neumann bottleneck + 3 mitigations (4). Covered:
- [ ] PQ2324-Q4a: VN concept (1) / 2 significant aspects (2) / bottleneck (2). Covered:
- [ ] PQ2324-Q5b: VN vs Harvard with diagrams (4). Covered:
- [ ] PQ2425-Q3a: VN concept (1) / 2 aspects (2) / bottleneck (2). Covered:
- [ ] PQ2425-Q4a(i): VN vs Harvard with diagrams (3). Covered:
- [ ] PQ2526-Q1a(i): differentiate Architecture vs Organization (2). Covered:
- [ ] PQ2526-Q1a(ii): compare VN vs Harvard, diagram each (3). Covered:
- [ ] T1a-Q1: arch vs org + example / VN vs Harvard / bottleneck+3 mitigations. Covered:
- [ ] T1b-Q1(i): VN bottleneck + 2 mitigations. Covered:
- [ ] T1mk-Q2: VN concept + 2 aspects / VN vs Harvard diagrams. Covered:
- [ ] DECK-INTRO: architecture vs organization component lists; VN vs Harvard. Covered:

### U2. Data Representation — number systems & base conversion  [NUM]
- [ ] TUT / PQ2324 test-block: express 111101111011110001110 in octal & hex. Covered:
- [ ] T1mk-Q1(ii): relate binary/octal/hex of 1044.125 (decimal). Covered:
- [ ] DECK-DATA worked: 13->1101; A34E16->41806; 110101101011101->6B5C16. Covered:

### U2. Data Representation — signed integers (Unsigned / S-M / 1's / 2's), ranges  [NUM]
- [ ] PQ2021-Q2a: -25 in 8-bit in the three signed modes (3). Covered:
- [ ] PQ2021-Q3b: table Unsigned/S-M/1's/2's for 234, -106, 1111011011 in 10 bits (6). Covered:
- [ ] PQ2021-Q4c: pos & neg ranges in a 16-bit register, S-M/1's/2's (6). Covered:
- [ ] PQ2324-Q4b(i): table for 204, -139, 1101001101 1 in 12 bits (6). Covered:
- [ ] PQ2425-Q3b(i): table for 204, -139, 1101 00110 11 in 12 bits (6). Covered:
- [ ] PQ2526-Q1c(i): range of 16-bit 2's comp; do -182/487/-1023 fit (2). Covered:
- [ ] PQ2526-Q1c(ii): -182, 487, -1023 each in binary and hex (3). Covered:
- [ ] T1a-Q2(i): 16-bit register range in S-M (2). Covered:
- [ ] T1a-Q2(ii): table for 234, -106, 1111 0110 11 in 10 bits (6). Covered:
- [ ] T1b-Q2(i): table for 204, -139 (10 bits). Covered:
- [ ] CW: interpret 11010 in S-M(-10)/1's(-5)/2's(-6). Covered:
- [ ] DECK-DATA: 74 & -43 S-M; 1's of 43; 2's of +24/+127/-39/-92/-128; 110011->-13. Covered:
- [ ] DECK-DATA quiz: S-M/1's/2's of 111100111; -82 in three modes; -89 8-bit three modes; 10111011 three modes; 16-bit S-M range. Covered:

### U2. Data Representation — binary arithmetic, overflow, end-around carry  [NUM]
- [ ] PQ2021-Q5a(ii): end-around carry, 153-142 in 10-bit register (4). Covered:
- [ ] PQ2021-Q5b(ii): 214+65 in 8-bit, binary & decimal, overflow (3). Covered:
- [ ] PQ2324-Q5d: end-around carry, 153-142 in 10-bit (4). Covered:
- [ ] PQ2425-Q4b(i): end-around carry, 153-142 in 10-bit (4). Covered:
- [ ] PQ2425-Q4b(ii): overflow vs underflow + one example each (3). Covered:
- [ ] PQ2526-Q1c(iii): compute (-182)+487 in 2's complement (2). Covered:
- [ ] PQ2324 test-block: overflow/underflow; end-around carry 125-123 8-bit. Covered:
- [ ] T1b-Q1(ii): end-around carry 153-142 10-bit. Covered:
- [ ] T1mk-Q1(i): end-around carry 15-13 8-bit. Covered:
- [ ] CW: end-around carry 23-20 in 6-bit. Covered:
- [ ] DECK-DATA: overflow & underflow (Ariane-5, Vancouver SE); 47+35 6-bit 2's-comp quiz. Covered:

### U2. Data Representation — BCD / Excess-3 / alphanumeric codes  [NUM/DESC, syllabus check]
- [ ] DECK-DATA: BCD 8421/5421/4221, Excess-3 self-complementing, conversions. Covered:
- [ ] DECK-DATA: Morse/Hollerith/ASCII-7/EBCDIC/Unicode. Covered:

### U2/graphics. Image memory sizing  [NUM]
- [ ] PQ2324-Q4b(ii): image 17.12x9.45 in @250 dpi in MB (3). Covered:
- [ ] PQ2425-Q3b(ii): image 17.12x9.45 in @250 dpi in MB (3). Covered:
- [ ] PQ2526-Q4c: image 17.12x9.45 in @250 dpi in MB (3). Covered:
- [ ] Tq2-Q3: image 13.45x9.62 in @300 dpi B/W in MB. Covered:
- [ ] DECK-DATA worked: 4x6 in @300 dpi B/W = 2,160,000 bits ~ 263.4 KB. Covered:

### U3. Floating Point — IEEE-754 single precision, decimal -> hex  [NUM]  (FAVE-heavy)
- [ ] PQ2021-Q2b(i): 4.75 -> IEEE-754 32-bit (4). Covered:
- [ ] PQ2324-Q4c: -1240.56 -> IEEE SP (6). Covered:
- [ ] PQ2425-Q3c: -1240.56 -> IEEE SP (6). Covered:
- [ ] PQ2425-Q5c: -421.55 -> IEEE SP, mantissa bits after first 12 = 0, all binary (5.5). Covered:
- [ ] PQ2526-Q5a: -1240.56 -> IEEE SP (6). Covered:
- [ ] T1a-Q2(iii): -452.25 -> IEEE SP hex (7). Covered:
- [ ] T1b-Q3: -1240.56 -> IEEE SP. Covered:
- [ ] T1mk-Q4: -1073.625 -> IEEE SP. Covered:
- [ ] Tq2-Q1: 1/16 and -1.05 -> IEEE 32-bit. Covered:
- [ ] CW: 20.25 -> 41A20000h (worked); task -423.35 -> IEEE. Covered:
- [ ] DECK-DATA worked: 64.2 -> 42806666h; homework 23.5 -> hex. Covered:

### U3. Floating Point — IEEE-754 single precision, hex -> decimal  [NUM]  (FAVE-heavy)
- [ ] PQ2021-Q2b(ii): 44FAC000h -> value (4). Covered:
- [ ] PQ2021-Q3c: BE7C2002H -> base-10 (5). Covered:
- [ ] PQ2324-Q1c / PQ2425-Q1a / PQ2526-Q4a: X=C1400000h, Y=42100000h, Z=41400000h -> decimals + test (Y-Z)>0, X+Z=0, Z=X+Y (9). Covered:
- [ ] PQ2425-Q4c: C4F2E000h -> base-10 (6). Covered:
- [ ] PQ2526-Q5d: C4F2E000h -> base-10 (6). Covered:
- [ ] T1b-Q3(reverse): C4240266H -> value. Covered:
- [ ] T1mk-Q3: 41242016H -> value. Covered:
- [ ] Tq2-Q2: decimal of three IEEE bit patterns (one = 0.8125). Covered:
- [ ] T2a-Q1: 48FAC000(H) -> value (5). Covered:
- [ ] CW: C2410001h -> ~-48.25 (worked); task 80220000h -> decimal. Covered:
- [ ] DECK-DATA quiz: BE7BAC10h -> decimal. Covered:

### U4. ISA — instruction set, formats, addressing modes (concepts)  [DESC]
- [ ] PQ2021-Q1f(i): what is ISA (1). Covered:
- [ ] PQ2021-Q2b(iii): Instruction Format vs Instruction Set (2). Covered:
- [ ] PQ2021-Q4a / PQ2425-Q5a(i): three categories of instructions + 2 examples each. Covered:
- [ ] T2b-Q5a: two instruction categories + examples (4). Covered:
- [ ] PQ2021-Q3a(i): describe Immediate/Register-Indirect/PC-Relative modes. Covered:
- [ ] T2b-Q3: addressing-mode definition (1). T2b-Q4: describe Immediate/Direct/Register (6). Covered:
- [ ] DECK-ISA: registers (GPR, PC/IR/MAR/MDR), instruction types, MC6809/68000 examples. Covered:

### U4. ISA — instruction formats 0/1/2/3-address + byte counting  [NUM/CODE]  (FAVE-heavy)
- [ ] PQ2021-Q1f(ii): 0/1/2-address for Z=V*((U+W)/(X*Y)), byte count (opcode 2B, mem 1B) (9). Covered:
- [ ] PQ2425-Q1d: 0/1/2/3-address for X=((A*B)+C/D)/(F*G+J*K), byte count (8). Covered:
- [ ] PQ2526-Q4b: 0/1/2/3-address Pentium-4 asm for X=((A*B)+C/D)/(F*G+J*K), byte count (8). Covered:
- [ ] T2b-Q5b: one- and two-address format for X=((A*B)+C/D)/(F*G+J*K) (5). Covered:
- [ ] T2mk: solves T2b-Q5b (reuse but recompute). Covered:
- [ ] PQ2425-Q2c: assembly program to add two numbers and store (4). Covered:
- [ ] DECK-ISA worked: 0/1/2/3-address for X=(A+B)*(C+D). Covered:

### U4. ISA — instruction format decode & addressing-mode EA/operand  [NUM]  (25/26 FAVE)
- [ ] PQ2021-Q3a(ii): represent instruction in memory segment (4.5); (iii) address & value of operand added to R1 (3) [0x017A, 0xC21A, R5=0xA75F->0x1BEC, PC-relative]. Covered:
- [ ] PQ2526-Q1e: EA + operand for Immediate/Direct/Indirect/Register-Indirect(R1)/Relative, given PC=7000, R1=1500, memory table, addr field 1200 (6). Covered:
- [ ] DECK-ISA worked: 16/32-bit format decode; 4 indirect LOAD/ADD/STORE; 2 relative branch. Covered:

---

## MODULE TWO — Processor Design & Performance

### U2. CPU performance — CPI from instruction/addressing mix, MIPS, improvement %  [NUM]  (25/26 FAVE, NEW emphasis)
- [ ] PQ2526-Q1b: pipelined clock cycle / actual CPI / exec time / speedup / why != theoretical (mix Arith40/Mem35/Br20/FP5, stages IF5 ID4 EX6 MEM5 WB4, overhead 1ns, branch 3-cyc EX, mem 2-cyc penalty, FP +4, 20M instr) (6). Covered:
- [ ] PQ2526-Q1d: average CPI / total clock cycles / new CPI if indirect->2 cyc / % improvement (1M instr, addressing-mode mix) (6). Covered:
- [ ] PQ2526-Q3c: Amdahl's law + speedup, cache 10x faster, 85% cache access (4). Covered:
- [ ] PQ2324-Q1b: Amdahl's law + speedup, cache 10x, 85% hit (4.5). Covered:
- [ ] TUT-Q(minicomputer): 18-bit address bus -> address space / largest memory bytes / PC length. Covered:
- [ ] PQ2021-Q1a: minicomputer 18 address signals -> space/bytes/PC length (3). Covered:
- [ ] PQ2021-Q5a(i): 4GB word-addressable, word=2B -> address bits (2). Covered:

### U3. Pipelining — speedup, throughput, Gantt, hazards  [NUM]  (25/26 FAVE, RISC hazards NEW)
- [ ] PQ2021-Q1b: pipelining def; non-pipelined vs pipelined exec, 4 ops x 5 stages 8/9/11/13/16ns, Gantt + speedup (8). Covered:
- [ ] PQ2021-Q1c: three data-hazard types (1.5) + classify 3 instruction pairs (1.5). Covered:
- [ ] PQ2021-Q5c: 4-stage pipeline cycle table; chart one loop iter (6); cycles for for(i=1..2) (1). Covered:
- [ ] PQ2324-Q1a: 5-stage (IF/ID/OF/EX/WB), EX 1/3/6 for ADD-SUB/MUL/DIV; cycles I1..I4 with forwarding (4.5) and without (5.5). Covered:
- [ ] PQ2425-Q5b: pipeline 4 phases 60/50/90/80ns, latch 10ns -> cycle time/non-pipe/speedup/500-task pipe/500-task seq/throughput (6). Covered:
- [ ] PQ2526-Q2b: 5-stage RISC I1 LW..I6 MUL; forwarding, branch in EX, load-use 1 stall, MUL 3-cyc EX; hazards(5)/timing diagram(2)/total cycles(1)/2 hw improvements(1). Covered:
- [ ] PQ2526-Q3b: 5-stage IF/ID/OF/EX/WB, EX 1/3/6 ADD-SUB/MUL/DIV; I1 MUL..I4 SUB with forwarding (4.5) and without (5.5). Covered:
- [ ] PQ2526-Q5b: pipeline 4 phases 60/50/90/80ns, latch 10ns -> cycle/non-pipe/speedup/500-task pipe/500-task seq (5). Covered:
- [ ] T2a-Q3: pipeline 4 phases 60/50/90/80ns, latch 10ns, 1000 tasks (6). Covered:

### [NOT-IN-SYLLABUS check] Boolean algebra / K-maps / logic circuit design  [DESIGN]
Not in the 186pp course manual's units; appears in older exams. Teach enough to pass.
- [ ] PQ2021-Q1d: minimum SOP from K-map with don't-cares (2). Covered:
- [ ] PQ2021-Q1e: Boolean simplification of gate circuit (4). Covered:
- [ ] PQ2324-Q2a: what is Boolean Algebra (2). Covered:
- [ ] PQ2324-Q2b: code converter 2->4 K-map + circuit; 3->3 in+1/-1 truth table+K-map+circuit (8). Covered:
- [ ] PQ2324-Q3d: simplify (AB'.(A+C))' + A'B.(A+B'+C')' = A+B (4.5). Covered:
- [ ] PQ2324-Q5a: combinational circuit T1-T4, F1/F2 expr (5) + 16-row truth table (4). Covered:
- [ ] T2a-Q2: X=AB+ABC+ABC'+AC logic diagram/minimize/reduced diagram + K-map SOP. Covered:

---

## MODULE THREE — Memory Organization

### U1. Memory overview — access methods, hierarchy, locality  [DESC]
- [ ] PQ2021-Q4b(ii): memory characteristics: access methods; memory hierarchy diagram (4). Covered:
- [ ] PQ2425-Q5a(ii): memory characteristics by access methods + example each (4). Covered:
- [ ] PQ2324-Q3c / PQ2425-Q2b(i): locality of reference / temporal / spatial (3-4.5). Covered:
- [ ] PQ2526-Q5c: locality of reference; temporal locality (3). Covered:
- [ ] PQ2425-Q2b(ii): what happens on a cache miss (1.5). Covered:
- [ ] DECK-MEM: access methods; 5-level hierarchy; two-level example L1/L2 95% hit -> 0.015us. Covered:

### U2. Semiconductor memory — DRAM vs SRAM  [DESC]
- [ ] PQ2021-Q5b(i): four differences DRAM vs SRAM (4). Covered:
- [ ] PQ2526-Q3a(iv): why fully associative eliminates conflict misses but adds a challenge (1.5). Covered:

### U3. Cache — mapping (direct/assoc/set-assoc), address fields, AMAT  [NUM]  (25/26 FAVE)
- [ ] PQ2324-Q1d: 8-way set-assoc, 32-bit words, 4 words/line, 4096 sets -> line/set/cache size (5). Covered:
- [ ] PQ2324-Q1e: how cache improves performance (2). Covered:
- [ ] PQ2324-Q3a / PQ2425-Q1b: AMAT simultaneous vs hierarchical, hit 80%, cache 5ns, MM 100ns + diagrams. Covered:
- [ ] PQ2324-Q3b: 16-bit addr, 2KB direct-mapped, 64B/block, word=1B -> Tag/Index/Offset. Covered:
- [ ] PQ2425-Q1c: 24-bit addr, 16 words/block, direct-mapped 256 blocks -> block for 1A2BC0/FFFF00/123456/C109D5 (6). Covered:
- [ ] PQ2425-Q2a: cache 1KB, block 16B, MM 64KB, 16-bit addr -> design Direct/Fully/2-way + adv/disadv (8). Covered:
- [ ] PQ2526-Q2a: 32-bit addr, 16 words/block, direct-mapped 256 blocks -> block for CA2DFC12/F24F25FF/24BBABCD/C1D9EEF2 (4). Covered:
- [ ] PQ2526-Q2c: MM 1GB, cache 512KB, 128B block, 4-way -> blocks/sets/address format/AMAT@96%,2ns,80ns/associativity effect (6). Covered:
- [ ] PQ2526-Q3a: MM 64MB, cache 128KB, 64B block -> lines / direct(index,tag,offset) / 4-way(sets,set-index,tag) / fully-assoc note (6). Covered:
- [ ] T2b-Q1: 32-bit addr, 16 words/block, direct-mapped 256 blocks -> line for 1A2BC012/FFFF00FF/12345678/C109D532 (6). Covered:
- [ ] T2b-Q2: 8GB, 64-bit words, 16 words/block, direct-mapped 128 blocks -> format + 4-way format, layouts (3). Covered:
- [ ] T2mk: solves T2b-Q1/Q2 (Tag20/Index8/Offset4; blocks 1,15,103,83; 19-7-4 and 21-5-4). Reuse, recompute. Covered:
- [ ] CH6: EAT off-chip cache 2ns/98% MM40ns->2.8ns; +on-chip 0.5ns/94%->0.668ns speedup 4.2; VM EAT solve X; 8GB/16w/128blk 19-7-4 & 4-way 21-5-4; direct map 1A2BC012.. blocks 1,15,103,83; paging 8pg/16fr. Covered:
- [ ] DECK-MEM: mapping worked, 16KB cache/256B block/128KB MM: direct tag=3, assoc tag=9/dir 72B, 16GB/4KB tag=22, 2-way 64 lines->32 sets->5 set bits. Covered:

---

## MODULE FOUR — Advanced Architectures

### U1. RISC vs CISC  [DESC]
- [ ] PQ2021-Q4b(i): four differences RISC vs CISC + two example processors each (4). Covered:
- [ ] PQ2324-Q5c: three differences RISC vs CISC + two examples each (3). Covered:
- [ ] PQ2425-Q4a(ii): four differences RISC vs CISC + two examples each (4). Covered:

### U2. Parallel architectures / interconnection networks  [DESC]
- [ ] (No direct PQ found; course-manual Module Four Unit 2 defines scope. Cover from manual.) Covered:

---

## SELF-ASSESSMENT (course manual, pp.170-177) + GLOSSARY (p.178)
- [ ] All self-assessment questions per unit must be answered in-manual. Covered: (to enumerate from manual_text.txt)

## MOCK EXAMS (to author) — 70 marks, Q1 compulsory 30 + any two of 20, 2h
- [ ] Mock A: weighted to 25/26 flavour (CPI/performance + RISC hazards + cache + IEEE). Fully solved.
- [ ] Mock B: weighted to 24/25 flavour. Fully solved.
- [ ] (Optional Mock C mixing older-paper Boolean/K-map + pipeline Gantt.) Fully solved.
