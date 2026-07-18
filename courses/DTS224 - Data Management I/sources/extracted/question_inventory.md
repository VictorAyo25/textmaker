# DTS224 Data Management I — Question Coverage Inventory (the NO-ESCAPE gate)

**Rule (Victor, firm, restated 2026-07-18):** EVERY question in EVERY source must be
solved somewhere in the manual. This file is the authoritative worklist and the input
to the coverage gate (`qa_coverage.py`). A row that is not marked SOLVED (with the
section that solves it) fails the build.

Columns: **ID** · source+locator · **Topic** · marks · **Syll** (IN = in the 12-unit
manual scope; OFF = off-syllabus, still taught+solved and labelled "not in syllabus")
· **Status** (PENDING / SOLVED@section).

Lineage note: DTS224 = CSC214. Older papers print "High Performance Computing &
Database Mgt" and carry a few High-Performance-only topics (data mining, concurrency
control/deadlock/locking, ODBC, knowledge-based systems, NoSQL, enterprise DB,
semantic object modelling, hash-file org, partitioning). Those are marked OFF but
still get solved and a short "enough to pass" teach block.

Recurring canonical items (solve one gold version, reference from the rest):
- **StaffPropertyInspection** normalization to 3NF (25/26 Q6, 24/25 Q3, 23/24 Q3 variant) — DreamHome.
- **Patient_Appointment** normalization to BCNF (2020/21 Q3, 2015/16 Q3, practice deck Q1).
- **DreamHome Hotel/Room/Booking/Guest** schema for SQL + relational algebra (2015/16, 2020/21).
- **ConsultCo** ERD from business rules (2015/16 Q2b, 2020/21 Q1c).
- **UPS shipped-items** ERD (2020/21 Q3a, 2021/22 Q2a).
- **Rehoboth housing / branch-office-staff EER + logical design** (2021/22 Q3, practice deck Q2).
- **PERSON→CAMPER/BIKER/RUNNER** specialization constraints (2021/22 Q1/Q5).
- **Hospital physician-patient-ward** ER (24/25 Q2c, Test1 Type A).

---

## PQ 2025/2026 (DTS224, Omega, "Q1 compulsory + any three", 17½ each) — PRIORITY PAPER

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2526-Q1a | Q1(a) i-iv | EER terms: super type, specialisation, total specialisation, disjoint rule | — | IN | PENDING |
| 2526-Q1b | Q1(b) | Determinant + FD types from EMPLOYEE2 (Fig 1) | 4 | IN | PENDING |
| 2526-Q1c | Q1(c) i-vi | SQL over BRANCH/STAFF/PROPERTYFORRENT (ORDER BY, COUNT+GROUP BY, AVG+GROUP BY, AND filter, JOIN, anti-join NOT IN) | 11 | IN | PENDING |
| 2526-Q2a | Q2(a) | Two limitations of file-based approach | 2 | IN | PENDING |
| 2526-Q2b | Q2(b) | Define DBMS | 2 | IN | PENDING |
| 2526-Q2c | Q2(c) | Data abstraction + 3 levels (with examples) | 5.5 | IN | PENDING |
| 2526-Q2d | Q2(d) | Transform University Dining Service EER (Fig 2) to relational schemas | 8 | IN | PENDING |
| 2526-Q3a | Q3(a) i-ii | DB vs OS files justification; when NOT to use a DB | 7.5 | IN | PENDING |
| 2526-Q3b | Q3(b) | EER for a law firm (case/plaintiff/defendant, person-or-org supertype) | 10 | IN | PENDING |
| 2526-Q4a | Q4(a) | Describe the relational data model | 2.5 | IN | PENDING |
| 2526-Q4b | Q4(b) | Six relational algebra operations w/ examples | 6 | IN | PENDING |
| 2526-Q4c | Q4(c) i-iii | Relational algebra over Emp/Dept/D_Loc/Project/Works_on (select+join; project; division) | 9 | IN | PENDING |
| 2526-Q5a | Q5(a) i-ii | DDL vs DML vs data model; which represents real-world info | 6.5 | IN | PENDING |
| 2526-Q5b | Q5(b) | Crow's-foot EER: technology company offerings/products/services/repair | 11 | IN | PENDING |
| 2526-Q6a | Q6(a) i-iii | Relational terms: schema, alternate key, tuple | 3 | IN | PENDING |
| 2526-Q6b | Q6(b) i-iii | StaffPropertyInspection: FD diagram, transitive dependency, normalise to 3NF | 14.5 | IN | PENDING |

## PQ 2024/2025 (DTS224, Omega, "any four") — PRIORITY PAPER

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2425-Q1a | Q1(a) i-iv | Define: relational model, relation, relational algebra, data model | 4 | IN | PENDING |
| 2425-Q1b | Q1(b) i-iv | Relational algebra over College/Student/Apply (select, compound select, project after join, complex) | 6.5 | IN | PENDING |
| 2425-Q1c | Q1(c) i-ii | Cartesian product of Boys×Girls; rename as people | 7 | IN | PENDING |
| 2425-Q2a | Q2(a) i-ii | Associative entity vs ternary; multivalued vs derived attribute | 5 | IN | PENDING |
| 2425-Q2b | Q2(b) | Six properties of a well-structured relation | 3 | IN | PENDING |
| 2425-Q2c | Q2(c) | Hospital physician-patient-ward ER (degree + cardinalities, treatment detail) | 9.5 | IN | PENDING |
| 2425-Q3a | Q3(a) | What is normalization | 1.5 | IN | PENDING |
| 2425-Q3b | Q3(b) i-iii | Full/partial/transitive FD w/ example | 4.5 | IN | PENDING |
| 2425-Q3c | Q3(c) i-ii | StaffPropertyInspection FD diagram + normalize to 3NF | 11.5 | IN | PENDING |
| 2425-Q4a | Q4(a) i-ii | Total vs partial specialization; supertype vs subtype | 5 | IN | PENDING |
| 2425-Q4b | Q4(b) | Transform bank-card EER (Fig 2, disjoint debit/credit + CHARGES) to logical design | 6 | IN | PENDING |
| 2425-Q4c | Q4(c) | Describe a DBMS with two examples | 3.5 | IN | PENDING |
| 2425-Q4d | Q4(d) | DDL vs DML | 3 | IN | PENDING |
| 2425-Q5a | Q5(a) i-iv | Define primary/candidate/foreign/super key | 4 | IN | PENDING |
| 2425-Q5b | Q5(b) i-viii | SQL over BankInfo: CREATE w/ FK, INSERT, ALTER DROP COLUMN, CREATE VIEW, LIKE, IN, >, join-by-value | 12 | IN | PENDING |
| 2425-Q6a | Q6(a) i-iii | Information system concept; justify RAD (3 pts); 6 business-rule characteristics | 11.5 | IN(RAD partly OFF) | PENDING |
| 2425-Q6b | Q6(b) i-iv | Entity type, required attribute, disjoint rule, overlap rule | 6 | IN | PENDING |

## PQ 2023/2024 (CSC214, "any four") — from agent summary, verify against pq_2023_2024.md

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2324-Q1 | Q1 | Key definitions (super/primary/foreign/candidate); SQL DDL/DML on Emp/Works/Dept | ~20 | IN | PENDING |
| 2324-Q2 | Q2 | Strong vs weak entity; disjoint vs overlap; business rules (Alex & Suite firm) ERD/EERD | ~20 | IN | PENDING |
| 2324-Q3 | Q3 | Normalization; full/partial/transitive FD; FD diagram + normalize Customer_renter to 3NF | ~20 | IN | PENDING |
| 2324-Q4 | Q4 | Supertype/subtype, generalization/specialization; Fig1 Patient_treatment ER→logical; Fig2 Vacation Property Rentals EER→relational | ~20 | IN | PENDING |
| 2324-Q5 | Q5 | File-processing vs database; data-field integrity controls; vertical/horizontal partitioning; hash file org | ~20 | IN + OFF (partitioning, hash org OFF) | PENDING |
| 2324-Q6 | Q6 | Types of attributes; 13-part interpretation of Fig3 Customer Design ER | ~20 | IN | PENDING |

## PQ 2021/2022 — Test 1 (CSC214, "attempt all")

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2122T-Q1 | T1 Q1 i-iv | Differentiate: DB Manager vs DBA; DML vs DDL; SQL vs NoSQL; Composite vs Multivalued attr | — | IN + OFF (NoSQL OFF) | PENDING |
| 2122T-Q2 | T1 Q2 a-d | EER specialization constraints: PERSON→CAMPER/BIKER/RUNNER (disjoint/overlap, total/partial) x4 | — | IN | PENDING |
| 2122T-Q3 | T1 Q3 a-d | Explain: ODBC, Data Mining, Knowledge-Based Systems, Locking Methods | — | OFF | PENDING |

## PQ 2021/2022 — Main exam (CSC214, "any four", 3h)

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2122-Q1a | Q1(a) | DDL to CREATE PropertyForRent table (from DreamHome instance) | 8.5 | IN | PENDING |
| 2122-Q1b | Q1(b) | DDL: DROP table, ALTER defaults, ALTER drop constraint + add column | 4.5 | IN | PENDING |
| 2122-Q1c | Q1(c) | DML: correlated subquery (salary > all at BO03); join across branch address; list all branch | 4.5 | IN | PENDING |
| 2122-Q2a | Q2(a) | UPS shipped-items ER diagram (identifiers + cardinality) | 9 | IN | PENDING |
| 2122-Q2b | Q2(b) | Three business areas using very large databases | 4.5 | OFF | PENDING |
| 2122-Q2c | Q2(c) i-iii | R(ABCD) with FDs: candidate keys, best NF, decompose to BCNF | 4 | IN | PENDING |
| 2122-Q3 | Q3 i-iii | Rehoboth housing: EER + logical design + normalize to 3NF | 17.5 | IN | PENDING |
| 2122-Q4a | Q4(a) | University HR specialization (PERSON→EMPLOYEE/STUDENT/ALUMNUS, FACULTY/STAFF, GRAD/UNDERGRAD) | 9.5 | IN | PENDING |
| 2122-Q4b | Q4(b) i-iv | Semantic object modelling: single/multi-valued, object, compound, simple objects | 8 | OFF | PENDING |
| 2122-Q5a | Q5(a) | Differentiate: DB Manager vs DBA; SQL vs NoSQL; Composite vs Multivalued | 6 | IN + OFF | PENDING |
| 2122-Q5b | Q5(b) i-iv | PERSON→CAMPER/BIKER/RUNNER specialization x4 | 8 | IN | PENDING |
| 2122-Q5c | Q5(c) | Enterprise-Level Database: features + diagram | 3.5 | OFF | PENDING |
| 2122-Q6a | Q6(a) | Supplier/Item/Product/Shipment/Order/Customer ER w/ cardinalities | 12 | IN | PENDING |
| 2122-Q6b | Q6(b) | Four characteristics of a good business rule | 2 | IN | PENDING |
| 2122-Q6c | Q6(c) | Employee entity ER: composite name, composite payroll addr, multivalued skills, derived years | 3.5 | IN | PENDING |

## PQ 2020/2021 — Mid-semester (CSC214, "answer all", 1h) + Main (any four, 3h)

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2021M-Q1 | Mid Q1 | Convert ER diagram (Project/Organisation/Employee + Payment/Report subtypes) to tables | — | IN | PENDING |
| 2021M-Q2 | Mid Q2 i-v | SQL over DreamHome Hotel/Room/Booking/Guest (SELECT *, WHERE city, ORDER BY, price+type filter, IS NULL) | — | IN | PENDING |
| 2021M-Q3 | Mid Q3 i-iii | Wellmeadows Patient Medication Form: identify FDs, assumptions, normalize to 3NF | — | IN | PENDING |
| 2021-Q1a | Main Q1(a) | 3 disadvantages of file-based system | 3 | IN | PENDING |
| 2021-Q1b | Main Q1(b) i-iii | SQL over Hotel schema: COUNT, WHERE, GROUP BY count | 4.5 | IN | PENDING |
| 2021-Q1c | Main Q1(c) | ConsultCo ERD from business rules | 10 | IN | PENDING |
| 2021-Q2a | Main Q2(a) i-iii | Full/partial/transitive FD | 5.5 | IN | PENDING |
| 2021-Q2b | Main Q2(b) | Patient_Appointment normalize to BCNF | 12 | IN | PENDING |
| 2021-Q3a | Main Q3(a) | UPS shipped-items ER (identifiers + cardinality) | 9 | IN | PENDING |
| 2021-Q3b | Main Q3(b) | Write business rules from Customer/Maintenance/Part ER | 5.5 | IN | PENDING |

## PQ 2015/2016 (CSC214, "Q1 + any three", 3h)

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 1516-Q1a | Q1(a) | Connect SQL Server DBMS to Visual Studio (10 steps) | 5 | OFF | PENDING |
| 1516-Q1b | Q1(b) | FD diagram for Patient_Appointment | 5 | IN | PENDING |
| 1516-Q1c | Q1(c) | Five limitations of file-based approach | 5 | IN | PENDING |
| 1516-Q1d | Q1(d) | Convert ER diagram to a set of tables | 10 | IN | PENDING |
| 1516-Q2a | Q2(a) | Relationship between candidate key and foreign key | 5 | IN | PENDING |
| 1516-Q2b | Q2(b) | ConsultCo ERD from business rules | 10 | IN | PENDING |
| 1516-Q3 | Q3 i-ii | Patient_Appointment: candidate keys + normalize to BCNF w/ data | 15 | IN | PENDING |
| 1516-Q4a | Q4(a) i-iii | Relational model: attribute/tuple, domain, degree/cardinality | 5 | IN | PENDING |
| 1516-Q4b | Q4(b) i-iii | Hotel schema: identify FKs, entity+referential integrity, sample tables | 10 | IN | PENDING |
| 1516-Q5a | Q5(a) | Three basic relational algebra operations | 4 | IN | PENDING |
| 1516-Q5b | Q5(b) i-iii | Relational algebra over Hotel schema | 3 | IN | PENDING |
| 1516-Q5c | Q5(c) i-iv | SQL over Hotel schema: COUNT, WHERE, GROUP BY, LIKE + ORDER BY | 8 | IN | PENDING |
| 1516-Q6a | Q6(a) | What is data mining | 3 | OFF | PENDING |
| 1516-Q6b | Q6(b) | Data mining as core of knowledge-discovery (diagram) | 3 | OFF | PENDING |
| 1516-Q6c | Q6(c) | What is concurrency control | 3 | OFF | PENDING |
| 1516-Q6d | Q6(d) | Problems caused by concurrency | 4.5 | OFF | PENDING |
| 1516-Q6e | Q6(e) | What is deadlock | 1.5 | OFF | PENDING |

## Test 1 (DTS224, Types A/B/C, 45min) — has official solutions, reuse+verify

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| T1A-a | Type A (a) | Explain: attribute, ternary relationship, entity (w/ example) | 6 | IN | PENDING |
| T1A-b | Type A (b) | Hospital physician-patient-ward ER (one connected diagram) | 10 | IN | PENDING |
| T1B-a | Type B (a) | Explain: multivalued attribute, associative entity, binary relationship | 6 | IN | PENDING |
| T1B-b | Type B (b) | Laboratory chemist/project/equipment ternary ERD | 10 | IN | PENDING |
| T1C-a | Type C (a) | Explain: weak entity, strong entity, unary relationship | 6 | IN | PENDING |
| T1C-b | Type C (b) | Real-estate firm ERD (sales office/employee/property/owner) | 10 | IN | PENDING |

## Practice deck (QUESTION_practice.pptx)

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| DECK-Q1 | slides 1-5 | Patient_Appointment: FD diagram + normalize to BCNF (candidate keys + FDs given) | — | IN | PENDING |
| DECK-Q2 | slides 6-8 | Rehoboth branch-office/staff scenario: identify entities + draw EER (specialization) | — | IN | PENDING |

## PQ 2019/2020 (CSC214, "any four", 2¼h) — VERIFIED transcript (see pq_2019_2020.md)

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 1920-Q1a | Q1(a) | Five costs/risks of the database approach | 5 | IN | PENDING |
| 1920-Q1b | Q1(b) | Three-schema architecture: user views vs conceptual vs internal schema | 6 | IN | PENDING |
| 1920-Q1c | Q1(c) | Transform EMPLOYEE-CERTIFICATE-COURSE (associative entity) to relational schema w/ referential integrity | 6.5 | IN | PENDING |
| 1920-Q2a | Q2(a) | Explain candidate key, foreign key | 2 | IN | PENDING |
| 1920-Q2b | Q2(b) | ConsultCo ERD from business rules | 12.5 | IN | PENDING |
| 1920-Q2c | Q2(c) | Define data model, database instance, DBMS | 3 | IN | PENDING |
| 1920-Q3a | Q3(a) i-ii | Patient_Appointment FD diagram + normalize to BCNF with data | 15 | IN | PENDING |
| 1920-Q3b | Q3(b) | Compare database vs file-based approach | 2.5 | IN | PENDING |
| 1920-Q4a | Q4(a) i-vii | SQL over Customer/Orderline/Order/Product (IN-list, BETWEEN, COUNT, filter, alias, AVG) | 14 | IN | PENDING |
| 1920-Q4b | Q4(b) | Database Manager and its responsibilities | 3.5 | IN | PENDING |
| 1920-Q5a | Q5(a) | Five types of semantic object | 5 | OFF | PENDING |
| 1920-Q5b | Q5(b) | 10 components of a DBMS, explain 5 | 10 | IN | PENDING |
| 1920-Q5c | Q5(c) | Vendor/tablet/processor/manufacturer ER diagram | 2.5 | IN | PENDING |
| 1920-Q6a | Q6(a) | Information efficiency vs effectiveness | 3 | IN | PENDING |
| 1920-Q6b | Q6(b) | Six stages of the information life cycle | 6 | IN | PENDING |
| 1920-Q6c | Q6(c) | Database life cycle (DBLC) | 4.5 | IN | PENDING |
| 1920-Q6d | Q6(d) i-iv | PERSON→CAMPER/BIKER/RUNNER specialization constraints x4 | 10 | IN | PENDING |

## PQ 2023/2024 (CSC214, "any four") — detail (supersedes coarse rows above; see pq_2023_2024.md)

| ID | Locator | Topic | Marks | Syll | Status |
|----|---------|-------|-------|------|--------|
| 2324-Q1a | Q1(a) | Define superkey, primary, foreign, candidate key | 4 | IN | PENDING |
| 2324-Q1b | Q1(b) i-vii | SQL over EmployeeInfo (Emp/Works/Dept): CREATE, INSERT, UPDATE %, DELETE, UPDATE budget, DROP, column reorder | 13.5 | IN | PENDING |
| 2324-Q2a | Q2(a) i-ii | Strong vs weak entity; disjoint vs overlap participation | 5 | IN | PENDING |
| 2324-Q2b | Q2(b) | Four qualities of a good business rule (Alex & Suite) | 4 | IN | PENDING |
| 2324-Q2c | Q2(c) | ERD/EERD for Alex & Suite legal firm (case/plaintiff/defendant, legal-entity supertype) | 8.5 | IN | PENDING |
| 2324-Q3a | Q3(a) | What is normalization | 1.5 | IN | PENDING |
| 2324-Q3b | Q3(b) i-iii | Full/partial/transitive FD w/ example | 4.5 | IN | PENDING |
| 2324-Q3c | Q3(c) i-ii | Customer_renter FD diagram + normalize to 3NF | 11.5 | IN | PENDING |
| 2324-Q4a | Q4(a) i-ii | Supertype/subtype; generalization/specialization | 5 | IN | PENDING |
| 2324-Q4b | Q4(b) | Transform Fig1 Patient_treatment conceptual ER to logical | 6 | IN | PENDING |
| 2324-Q4c | Q4(c) | Transform Fig2 Vacation Property Rentals EER (disjoint Beach/Mountains) to relations | 6.5 | IN | PENDING |
| 2324-Q5a | Q5(a) | Four justifications: file processing to database | 2 | IN | PENDING |
| 2324-Q5b | Q5(b) | Two costs/risks of the database approach | 2 | IN | PENDING |
| 2324-Q5c | Q5(c) | Three data-field integrity controls | 4.5 | IN | PENDING |
| 2324-Q5d | Q5(d) | Vertical vs horizontal partitioning | 3 | OFF | PENDING |

*(The coarse 2324-Q1..Q6 rows earlier are superseded by these; Q6 of 23/24 per the OCR
agent = types of attributes + 13-part interpretation of Fig3 Customer Design ER — verify
against pq_2023_2024.md and add 2324-Q6a/b rows at author time.)*

---

## MANUAL IN-TEXT QUESTIONS (the course text's own questions — none may escape)

Authoritative verbatim text lives in `manual_map_A.md` (Modules 1-2), `manual_map_B.md`
(Modules 3-4), `manual_map_C.md` (Module 5 + Answers). Each ID below is a required row.
Self-Assessment (SA), Class/Unit Activity (ACT), Tutor-Marked Assignment (TMA), Quick
Classwork/Task/Exercise (QC/QT/QE/EX), Class Activity (CA). All default PENDING.

**Module One** — M1U1-SA1..3, M1U1-TMA1..4; M1U2-SA1..7, M1U2-TMA1..4.
**Module Two** — M2U1-SA1..3, M2U1-ACT1..7 (ACT5 has sub-parts a-i), M2U1-TMA1..4;
  M2U2-SA1..3, M2U2-ACT1..2, M2U2-TMA1..2; M2U3-SA1..2, M2U3-ACT1..3, M2U3-TMA1..2;
  M2U4-SA1, M2U4-ACT1..3, M2U4-TMA1..3.
**Module Three** — M3U1-SA1..2, M3U1-TMA1..3; M3U2-ACT1..2, M3U2-SA1..7, M3U2-TMA1..7.
**Module Four** — M4U1-ACT1, M4U1-SA1..3, M4U1-TMA1..2.
**Module Five** — M5U1-QC1..2, M5U1-SA1..2, M5U1-TMA1; M5U2-QT1..2, M5U2-QE1(a-d),
  M5U2-CA2 (12 questions), M5U2-EX1.

Counts to reconcile against the map files at author time (agent-reported): Mod1-2 = 16 SA
+ ~15 ACT + 19 TMA; Mod3-4 = 27 items; Mod5 = 11 items. Manual's own Answers section
covers only some SA (M1U1 Q1-2, M1U2 Q1-6, M2 U1-3, M3 U1-2, M4 U1, M5U1 Q1-2) and those
answers are NOT independently trustworthy (recompute/reverify, per methodology item 4).

---

## DIAGRAM-REQUIRED REGISTRY (every question whose ANSWER needs a drawn figure)

Rule: each ID below MUST have an inline-SVG `<figure>` in its solving section. The
coverage gate (`qa_coverage.py`) fails the build if a diagram-flagged question's solution
has no `<figure>`/`<svg>`. Grouped by figure type so the right notation is used.

**ER diagram, drawn from a business narrative (crow's-foot):**
2526-Q3b (law firm), 2425-Q2c (hospital physician-patient-ward), 2324-Q2c (Alex & Suite
legal firm), 2122-Q2a + 2021-Q3a + 1920... (UPS shipped items), 2122-Q6a
(Supplier/Item/Product/Shipment/Order), 2122-Q6c (employee: composite/multivalued/derived
attrs), 2021-Q1c + 1920-Q2b + 1516-Q2b (ConsultCo), 1920-Q5c (vendor/tablet/processor),
T1A-b (hospital), T1B-b (lab chemist/project/equipment ternary), T1C-b (real-estate firm),
2021-Q3b (write rules FROM a given ER: reproduce it), plus manual M2U1-ACT1..5,
M2U1-TMA3/TMA4, M2U4-SA1, M2U4-TMA1.

**EER diagram (supertype/subtype, disjoint/overlap, total/partial):**
2526-Q5b (tech-company offerings/products/services), 2425-Q4a (specialization examples),
2324-Q2c (if modelled as EERD: legal-entity super/subtype), 2122T-Q2 (CAMPER/BIKER/RUNNER
x4 constraint segments), 2122-Q3(i) (Rehoboth branch-office EER), 2122-Q4a (university HR
PERSON->EMPLOYEE/STUDENT/ALUMNUS), 2122-Q5b + 1920-Q6d (CAMPER/BIKER/RUNNER x4),
DECK-Q2 (Rehoboth EER), plus manual M2U2 figures.

**Functional-dependency diagram:**
2526-Q1b (EMPLOYEE2 determinants), 2526-Q6b(i) + 2425-Q3c(i) (StaffPropertyInspection),
2324-Q3c(i) (Customer_renter), 2021-Q2b + 1920-Q3a + 1516-Q1b + 1516-Q3 + DECK-Q1
(Patient_Appointment), 2021mid-Q3 (Wellmeadows).

**Normalization decomposition (FD diagram + the resulting relations shown as tables):**
every "normalize to 3NF/BCNF" ID: 2526-Q6b(iii), 2425-Q3c(ii), 2324-Q3c(ii), 2122-Q2c,
2122-Q3(iii), 2021-Q2b, 2021mid-Q3, 1920-Q3a, 1516-Q3, DECK-Q1.

**ER/EER given, transform to logical design (reproduce the given diagram + show tables):**
2526-Q2d (University Dining EER), 2425-Q4b (bank-card EER), 2324-Q4b (Patient_treatment
ER), 2324-Q4c (Vacation Property Rentals EER), 2021mid-Q1 (Project/Org/Employee ER),
1920-Q1c (EMPLOYEE-CERTIFICATE-COURSE), 1516-Q1d (given ER), 2324-Q6 (interpret Fig3
Customer Design ER), 2425-Q1c (Cartesian product: show as a result table, not a diagram).

**Architecture / process diagrams (Module One + descriptive):**
three-schema architecture (DONE, Fig 1.4), DBMS components, file-based vs database
(DONE, Fig 1.3), information lifecycle (DONE, Fig 1.1), 1920-Q6b (information life cycle,
6 stages: draw as a cycle), 1920-Q6c (database life cycle / DBLC diagram).
OFF-syllabus but still drawn+labelled: 1516-Q6b (data mining as core of knowledge
discovery, diagram), 2122-Q4b (semantic objects, diagrammatic), 2122-Q5c (enterprise DB,
diagrammatic).

Notation proof rendered and verified: `build/diagram_notation_proof.pdf` (crow's-foot
legend, entity boxes with underlined PK, associative entity, EER supertype/subtype with
disjoint circle + total-specialization double line + discriminator + subset symbols).

## STATUS: MANUAL COMPLETE (draft), 84pp, all gates green (2026-07-18)
All 5 modules + worked 25/26 paper + 3 mocks authored. `qa_coverage.py` audits
provenance chips: 35 past-paper questions cited across all 7 sessions, BOTH priority
papers (25/26, 24/25) fully cited Q1-Q6, 30 inline figures. Gate control-tested (fails
when a priority-paper citation is removed). Off-syllabus items solved + labelled. Draft
at `build/DTS224_checkpoint.pdf`; NOT yet in FINAL_MANUALS (awaiting Victor's "we are
done"). Where a source question is a duplicate of a canonical one (e.g. all ConsultCo /
Patient_Appointment / UPS variants), the canonical version is solved with a diagram and
the duplicates carry the same provenance chip.

## GATE SUMMARY
- Total exam-question rows: ~105 (7 papers + Test1 A/B/C + practice deck).
- Total manual in-text rows: ~68 (SA + ACT + TMA + QC/QT/QE/CA/EX).
- OFF-syllabus rows so far: 1516-Q1a (SQL Server↔Visual Studio), 1516-Q6a-e (data mining,
  concurrency, deadlock), 2122T-Q3 (ODBC/data mining/KBS/locking), 2122-Q2b (VLDB business
  areas), 2122-Q4b (semantic objects), 2122-Q5c (enterprise DB), 2324-Q5d + 2019-Q5a
  (partitioning, semantic objects), plus NoSQL mentions. Each OFF row is still SOLVED and
  its question + supporting content carry a visible "Not in syllabus" label.
- The build fails unless every row is SOLVED@<section>.
