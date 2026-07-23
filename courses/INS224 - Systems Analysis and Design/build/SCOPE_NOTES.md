# INS224 Systems Analysis and Design — scope notes (intake complete)

## UPDATED COURSE TEXT (2026-07-23): sources/INS224 (updated).pdf, 117pp
The lecturer shipped an expanded text (was 86pp). It now covers almost the whole exam:
Module One (SAD/SDLC/methodology), Module Two (fact-gathering, use cases, process
modelling/DFD, ERD/data modelling), Module Three (ERD cont., structural UML/class,
behavioural UML/activity+sequence). So the topics previously marked "not in the course
text" (ERD, class, UML, activity, sequence, OOD) ARE NOW IN THE TEXT. The "Not in the
course text" chips were removed from Modules Four and Five accordingly.
- **Still NOT in the text (genuine gaps, Module Six keeps the chip):** client-server tiers,
  hardware architecture / architectural functions, system acquisition strategy (build/buy/
  outsource), interface design, relational database design. (Installation/conversion, help
  desk, maintenance ARE in the text via SDLC, so Module Six Unit 2 is covered.)
- **Notation mismatch (important):** the text draws ERDs in **Chen** style (diamonds for
  relationships, ovals for attributes, 1/M/N on the lines); the **exam asks for Information
  Engineering / crow's foot**. Manual teaches BOTH and flags which the paper wants. The text
  also teaches "reading an ERD left-to-right and right-to-left" = the forward/backward
  chaining the 25/26 paper asks for. Text's ERD example: Course Section / Enrollment /
  Student (M:N via a linking entity). Class relationships in the text use the SAME examples
  the manual chose (Department/Lecturer aggregation, Order/OrderLines composition).


Course lineage: **CSC317 -> INS224**. Old papers (2018-2022) and the 24/25 Alpha
paper are printed under **CSC317**; the course was renumbered to **INS224** and
the 24/25 Omega + 25/26 Omega papers carry **INS224**. Same examiner style, same
topic bank. Author footer: `INS224 · Systems Analysis and Design · Victor Ayodeji`.

## Exam format (weight toward the newest)
- **25/26 INS224 (Omega, the TARGET)**: 3 credit units, **3 HOURS**. Answer **ONE of two
  questions in Section A** and **ANY THREE of four questions in Section B** (Q3-Q6).
  Section A = broad scenario Qs (elicitation/SDLC/methodologies/requirements).
  Section B = the diagram-heavy Qs (ERD, DFD, use case, class, activity, OOD).
- **24/25 INS224 (Omega)**: same "one in A + three in B" split, 3 hours, 3 units.
- **24/25 CSC317 (Alpha)**: 2 units, 2 hours, answer ANY THREE of five (no sections).
- Older CSC317: ANY THREE of five (18/19, 22/23), or Section A all + Section B any-two
  (19/20, 2h30), or read-one-scenario-answer-three (21/22 video store).
- CBT tests: Test 1 (35 min, 6 short recall Qs), Test 2 INS224 (50 min, 2 scenario Qs).

## Full topic bank (union across ALL papers) — teach every one FROM ZERO
The official 86pp course text covers only ~40% of this (Modules 1-3: SAD intro,
SDLC, fact-gathering, use cases, DFD). Everything marked [gap] is NOT in the text
and must be taught from zero, tagged "not in the course text".

1. Analyst as problem solver; problem-solving sequence (research/understand ->
   verify benefits > costs -> define reqs -> alternatives -> recommend -> detail ->
   implement -> monitor); required skills (technical/business/people). [text]
2. Information system definition; subsystems; functional decomposition. [text]
3. SDLC 5 phases (planning, analysis, design, implementation, support) + activities
   + deliverables per phase (Table 2); principles of successful development. [text]
4. Approaches: predictive vs adaptive; methodologies — waterfall, prototyping, RAD,
   OOD, V-shape, spiral, incremental, Agile; when-to-use, adv/disadv, schematics;
   "compare 7 methodologies". [text partial; RAD/OOD/V/Agile/spiral = gap]
5. Feasibility: 5 types (technical, economic, operational, schedule, legal) + a risk
   each; 4 factors in confirming feasibility; "3 questions in feasibility". [text partial]
6. Requirements/fact-finding: elicitation (interview, questionnaire, observation,
   document review, JAD/JRP, prototyping, brainstorming) with why/what/how; functional
   vs non-functional; business/user/system requirements; requirement-analysis goals;
   overall fact-finding strategy; as-is vs to-be. [text partial]
7. Use cases: use-case diagram, actors, relationships (association, include, extend,
   generalization), narratives. [text]
8. DFD / process modelling: elements (external entity, process, data store, data flow);
   context / Process 0 (Level 0) / Level 1; mechanical errors; data balancing; illegal
   flows; naming a data store; common process-modelling mistakes. [text]
9. ERD / data modelling: entity, attribute, identifier/key, relationship; cardinality
   vs ordinality; cardinal relationships (1:1, 1:M, M:N, optional/mandatory); notation
   styles — Information Engineering (crow's foot) & Martin's & Chen; read/interpret an
   ERD; forward/backward chaining; data model vs process model differences;
   selecting an identifier; optional relationship. [GAP — biggest gap]
10. Class diagrams (UML): class, attributes, methods/operations, relationships &
    multiplicities; object vs class. [GAP]
11. OOD concepts: polymorphism, inheritance, multiple inheritance (+ drawbacks),
    composition, aggregation, association, generalization, encapsulation. [GAP]
12. Activity diagrams. [GAP]
13. Sequence diagrams. [GAP]
14. UML overview: definition, inventors (Booch, Rumbaugh, Jacobson) + uses; two
    diagram categories (structural vs behavioural) with 2 examples each + function. [GAP]
15. System architecture/design: client-server tiers; software architectural functions;
    hardware architecture nonfunctional reqs (operational, performance, security,
    cultural/political); interface design principles. [GAP]
16. System acquisition strategy: build vs buy vs outsource; supporting factors. [GAP]
17. Installation/conversion: direct cutover, parallel, phased, pilot. [text]
18. Relational database design: tables + primary keys, populate dummy rows. [GAP]
19. Project management: project-planning activities; scope/feature creep (refuse
    vs agree, reasons); reasons projects succeed/fail; stakeholders & their views;
    tools vs techniques vs models vs methodologies; job roles (project manager,
    software architect/tester, product designer). [text partial]
20. Support activities: maintain, enhance, support users / help desk. [text]
21. What is a model; explaining a model to stakeholders. [text partial]

## Recurring exam scenarios (quote verbatim when solved)
- Patient billing / hospital (24/25 & 25/26 Q2, Test 2): ERD + DFD context/L0/L1;
  also class + use case + activity + multiple-inheritance drawbacks.
- Sales management system (18/19, 22/23, Test 2): ERD + use case + sequence.
- Online university registration (24/25 CSC317 Q3/Q4): use case + class + activity + sequence.
- Landlord/estate agent (25/26 Q1): ERD + DFD + project success/fail + read ERD (fwd/bwd chaining).
- Video store (21/22): full scenario — methodology, use case, ERD, DFD, class, sequence.
- Jazzmatters festival (19/20): reqs + context diagram + class/use case.
- KHMS schools annexe/teacher/class (18/19, 22/23): ERD from narrative.
- Hospital ward/patient/nurse (18/19, 25/26 Q5): class diagram w/ multiplicities.
- Federal teaching hospital clinical workflow (25/26 Q5): 7 methodologies + planning + reqs.
- AI programming platform (25/26 Q6): as-is/to-be, elicitation plan, UML notes/categories/relationships.
- Tikki Tikka food/pastry (25/26 Q3): feasibility Qs, problem-solving steps, model, people skill, support, roles.
- Vought pharmaceutical (25/26 Q4): acquisition strategy, architectural functions, hardware, interface, DB.
- Warehouse stock/truck (25/26 Section B alt): ERD + Level 0 DFD.
- Nigerian airport food ordering (25/26 Q4a): DFD, why-DFD reasons.
- Quality Building Supply contractor sale (19/20): activity diagram.
- Elevator (19/20): sequence diagram.

## Papers to transcribe verbatim (sources/exams/transcripts/)
csc317_1819.txt, csc317_1920.txt, csc317_2122.txt, csc317_2223.txt (exam),
csc317_test1_2223.txt, csc317_2425.txt (Alpha), ins224_2425.txt (Omega, ins pg1-3),
ins224_2526.txt (Omega, 4pp photos — THE target), ins224_test2.txt.
All papers are .jpg/scanned-PDF; transcribe by eye per methodology 4c. The 24/25
Alpha PDF (2024-2025.pdf) HAS a text layer (2299 chars p1) usable as a locator only.

## Palette idea
Blueprint/architecture theme: deep blueprint indigo (TEACH/structure), drafting
cyan, amber (WORKED), crimson (TRAP), reserved violet/magenta for MUST-MEMORISE.
Subject = systems design/modelling -> blueprint metaphor fits.
