# CSC242 Discrete Structures: question inventory and coverage gate

Every question in every source must be solved somewhere in the manual.
Tick only when a WORKED EXAMPLE or solved-paper item carries a provenance chip.

## Course identity / lineage (CONFIRMED from banners)

| Session | Code printed | Title | Instruction | Time | CU |
|---|---|---|---|---|---|
| 2020/2021 | CSC311 | Discrete Structures | attempt any THREE | 2h | 2 |
| 2021/2022 | CSC416 | Discrete Structures | attempt any THREE | 2h | 2 |
| 2023/2024 | CSC 242 | Discrete Structure | (partial scan, Q3 on) | - | - |
| 2024/2025 | CSC416 | Discrete Structures | attempt any FOUR | 3h | 3 |
| 2025/2026 | CSC 242 | Discrete Structure | answer any FOUR | 3h | 3 |

Same course, renamed across sessions (CSC311 -> CSC416 -> CSC242). All papers are
valid practice. **Current format = 2025/26: answer any FOUR of six, each 17.5 marks
(total 70), 3 hours.** Weight the manual and mocks to 2024/25 + 2025/26.

## THE DEFINING FACT: the 161-page course text does NOT cover the exam

Probed the full text (184k chars). Occurrence counts:
reflexive 0, antisymmetric 0, vertex 0, vertices 0, adjacency 0, Handshaking 0,
Euler 0, planar 0, Kuratowski 0, poset 0, Hasse 0, isomorph 0, preorder 0,
postfix 0, Cartesian 0, bit string 0. "graph" x5 (all = plotting a function),
"tree" x12 (all = a Venn-diagram example about trees on a street), "matrix" x2
(two-line function notation, explicitly NOT a linear-algebra matrix).

Meanwhile EVERY paper leans on exactly those topics. On the 2025/26 paper the
graph, tree and relation material is roughly 40% of the available marks and 0% of
the course text. Therefore the manual must TEACH the gap topics from zero, not
merely drill them. Flag them clearly as examinable-but-not-in-the-course-text.

Course text modules (the half that IS covered): 1 Descriptive Statistics,
2 Predicate Logic, 3 Set, 4 Function, 5 Sequences and Summations, 6 Proof
Techniques, 7 Mathematical Induction, 8 Inclusion-Exclusion (+ Pigeonhole),
9 Permutations and Combinations, 10 Binomial Theorem, 11 Discrete Probability,
12 Recurrence Relations.

Also note: the course text running header says "CSC 242 | Elementary Differential
Equations" on every page. That is a copy-paste error in the source (the body is
genuinely discrete maths). Do not reproduce it.

## Coverage table

Legend: [ ] not yet covered, [x] solved in manual with provenance chip.

### 2025/2026 (PRIMARY TEMPLATE, 6 questions x 17.5, answer any 4)
- [ ] Q1a differentiate with 2 examples each: (i) degree vs valency of a node
      (ii) predicate vs propositional logic (iii) universal vs existential
      quantifier (iv) adjacency vs path matrix (v) logical matrix vs relation matrix (10)
- [ ] Q1b(i) discuss NINE types of sets with an example of each (3)
- [ ] Q1b(ii) two mathematical ways to describe a set (2)
- [ ] Q1c A={11,12,13,14} B={13,14,15,16}: intersection, A-B, B-A (2.5)
- [ ] Q2a five justifications for including Discrete Structures in the CS curriculum (5)
- [ ] Q2b S={John,Mary,Peter}, C={CSC701,CSC702}: Cartesian product S x C (2)
- [ ] Q2c R={(1,1),(2,2),(3,3),(4,4),(1,2),(2,3)}: is R reflexive? justify (2)
- [ ] Q2d A={1,2,3,4}, R={(1,1),(2,2),(3,3),(4,4),(1,3),(3,1),(2,4),(4,2)}:
      is R an equivalence relation? detailed explanation (4)
- [ ] Q2e partially ordered vs totally ordered set; classify the CGPA table
      A 4.80 / B 4.50 / C 4.10 with proof (4.5)
- [ ] Q3a 100 students, 72 Ibibio, 43 Efik: (i) both (ii) Ibibio only (iii) Efik only (7)
- [ ] Q3b 6 boys 4 girls, choose 4 with at least one boy (5)
- [ ] Q3c 10 male + 10 female pray one-male-one-female: (i) sessions
      (ii) prayer units (iii) choice of prayer partners (5.5)
- [ ] Q4a short notes with examples: (i) size of a graph (ii) valency of a vertex
      (iii) in-degree and out-degree (iv) graph isomorphism (v) Eulerian graph (10)
- [ ] Q4b the place of Logic in Computer Science, practical areas of relevance (2)
- [ ] Q4c three good examples of acceptable logic statements leading to a conclusion (3)
- [ ] Q4d number of ways the letters of "SCHOOL" can be arranged (2.5)
- [ ] Q5a(i) secure door opens on valid ID card A AND fingerprint B: Boolean
      algebra, when the door opens, Boolean table (4.5)
- [ ] Q5a(ii) alarm on fire sensor F OR smoke sensor S; output when only smoke (3)
- [ ] Q5b(i) briefly state and explain Kuratowski's Theorem (2)
- [ ] Q5b(ii) why are K5 and K3,3 important in graph theory (2)
- [ ] Q5b(iii) show K5 is non-planar using Euler (e <= 3v-6), and K3,3 (e <= 2v-4) (6)
- [ ] Q6a(i) clearly explain the adjacency matrix (2.5)
- [ ] Q6a(ii) discuss memory management in an adjacency matrix (4)
- [ ] Q6b ATM PIN, digits 0-9, repeats allowed: how many 4 to 6 digit codes (5)
- [ ] Q6c(i) how many three-digit natural numbers from digits 0..9 (1)
- [ ] Q6c(ii) number of parts in the task and their type (compulsory or alternative) (4)
- [ ] Q6c(iii) which rule applies here (1)

### 2024/2025 (CSC416, answer any FOUR, 3h)
- [ ] Q1a converse, contrapositive, inverse of 3 conditionals (snows tonight;
      beach whenever sunny; stay up late -> necessary that I sleep until noon) (4.5)
- [ ] Q1b truth tables for 4 compound propositions (4)
- [ ] Q1c "the home team wins whenever it is raining": contrapositive, converse,
      inverse with p = it is raining, q = the home team wins (3)
- [ ] Q1d prove only the contrapositive of p->q has the same truth value (6)
- [ ] Q2a C(x)/D(x)/F(x) cat-dog-ferret: 5 quantified translations (7.5)
- [ ] Q2b(i) f=ax+b, g=cx+d: necessary and sufficient conditions for fog = gof (2)
- [ ] Q2b(ii) if f and fog are one-to-one, does g follow? justify (2)
- [ ] Q2b(iii) fog and gof where f(x)=x^2+1, g(x)=x+2, R to R (2)
- [ ] Q2c "if a person is female and a parent, then this person is someone's
      mother" as a quantified logical expression (4)
- [ ] Q3a explain why (AxB)x(CxD) and Ax(BxC)xD are not the same (3.5)
- [ ] Q3b C++ program generating the power set of a given set of integers (6)
- [ ] Q3c set-builder notation and logical equivalences for the first De Morgan law (3)
- [ ] Q3d bit string for the complement of {1,3,5,7,9} in U={1..10} (2.5)
- [ ] Q4a(i) bit strings: union and intersection of {1,2,3,4,5} and {1,3,5,7,9} (2.5)
- [ ] Q4a(ii) truth values over the reals of 4 quantified statements (4)
- [ ] Q4b R1..R6 on {1,2,3,4}: reflexive, symmetric, antisymmetric, transitive (7.5)
- [ ] Q4c C++ isPerfectSquare by binary search, plus a main that prompts and reports (6)
- [ ] Q5 graph, 24 vertices, 30 edges, five of degree 4, seven pendant, seven of
      degree 2, the rest degree 3 or 4: (a) how many of degree 4 (b) degree-4 count
      in the corresponding complete graph (c) Handshaking proof (d) C++ snippet for
      the remaining degree-3-or-4 vertices (e) Handshaking applied in Data
      Communication (f) prove n vertices n edges and no vertex of degree 0 or 1
      implies every vertex has degree 2 (g) what it means for G and H to be
      isomorphic (17.5 total)
- [ ] Q6a tree traversals of the given tree: preorder, inorder, postorder (6)
- [ ] Q6b (3-4*2)-(5+(5-2)): rooted tree, prefix notation, postfix notation (6)
- [ ] Q6b(vi) a quinary tree of height 3: total number of leaves (2.5)
- [ ] Q6b(vii) prove an m-ary tree of height h has at most m^h leaves (3)

### 2023/2024 (CSC242, partial scan: Q3 onward)
- [ ] Q3a bit strings for {3,4,5}, {1,3,6,10}, {2,3,4,7,8,9} in U={1..10} (3)
- [ ] Q3b C++ program reading those sets dynamically and printing bit strings (7)
- [ ] Q3c fog and gof for f=x^2+1, g=x+2; state whether fog = gof (3.5)
- [ ] Q3d R1..R6 on A={1,2,3,4}: the divides relation, reflexive, symmetric,
      antisymmetric, transitive (10)
- [ ] Q4a types of undirected graph, in detail, with diagrams
- [ ] Q4b Detroit travelling-missionary minimum-distance tour (10)
- [ ] Q4c three application domains of tree models in computing, with examples (4.5)
- [ ] Q5a define the Handshaking Theorem (3)
- [ ] Q5b pilot, 5 cities, direct travel: can he visit exactly 3 from each?
      compute, and support with a diagram (5)
- [ ] Q5c directed graph: vertices, edges, in-degree, out-degree in tabular form (6)
- [ ] Q5d convocation chain letter, 4 each, ends after 100 read but did not send:
      (i) how many have seen it (ii) how many sent it out (9.5)

### 2021/2022 (CSC416, attempt any THREE, 2h)
- [ ] Q1a list the members of 5 set-builder sets (x^2=1 real; positive primes < 20;
      perfect square and x < 100; integer with x^2=2; integer with 2x=x) (5)
- [ ] Q1b digraph a,b,c,d in tabular form: vertices, edges, total in- and out-degree (6.5)
- [ ] Q1c types of undirected graph with diagrammatical illustrations (12)
- [ ] Q2a chairs labelled with an uppercase letter followed by a positive integer
      not exceeding 100: largest number labelled differently (6)
- [ ] Q2b simple communication links between 4 buildings, how many, plus diagram (7.5)
- [ ] Q2c five function correspondence types with a diagram (10)
- [ ] Q3a convocation chain letter (i) how many seen (ii) how many sent (10)
- [ ] Q3b four real-life scenarios where graph models apply, 2 examples each (6)
- [ ] Q3c key terminologies of a rooted tree, with a diagram (7.5)
- [ ] Q4a briefly explain the Handshaking Theorem (5.5)
- [ ] Q4b balanced m-ary tree, explained with examples (8.5)
- [ ] Q4c Detroit minimum-distance tour (10)
- [ ] Q5a four computing domains where graph models apply, with an example each (6)
- [ ] Q5b 25 major in Computer Science, 13 in Maths, 8 in both: size of the class (4)
- [ ] Q5c when is a vertex said to be incident to an edge, with an example (3.5)
- [ ] Q5d truth tables for (p<->q) XOR (p<->~q) and (q->~p)<->(p<->q) (10)

### 2020/2021 (CSC311, attempt any THREE, 2h)
- [ ] Q1a types of undirected graph, with relevant examples (12)
- [ ] Q1b simple communication links between 5 buildings, plus diagram (6.5)
- [ ] Q1c when is a vertex incident to an edge; identify every edge each vertex is
      incident to, in the e1..e6 diagram (5)
- [ ] Q2a Detroit travelling-missionary minimum-distance tour (10)
- [ ] Q2b four real-life scenarios where graph models apply, 2 examples each (6)
- [ ] Q2c key terminologies of a rooted tree, with a diagram (7.5)
- [ ] Q3a balanced m-ary tree, with examples (7.5)
- [ ] Q3b chain letter: how many seen, how many sent (8)
- [ ] Q3c four application areas in computing where graph models apply (8)
- [ ] Q4a playoff, best of five, first to three wins: (i) tree diagram
      (ii) in how many different ways can the playoff occur (7.5)
- [ ] Q4b five function correspondence types with a diagram (10)
- [ ] Q4c logical equivalences: (p->q)^(p->r) = p->(q^r);
      p<->q = (p^q)v(~p^~q) (6)
- [ ] Q5a define and draw the truth table for negation, conjunction, exclusive or,
      implication, tautology, contingency (6)
- [ ] Q5b passwords 6 to 8 characters, uppercase letter or digit, at least one
      digit: how many possible (5)
- [ ] Q5c R1..R6 on the integers given by rules (a<=b, a>b, a=b or a=-b, a=b,
      a=b+1, a+b<=3): (i) list 5 ordered pairs in each (ii) which are reflexive,
      symmetric, transitive (11.5)

## Repeat-offender list (the drills the exam hammers)
1. Types of undirected graph, with diagrams (2020/21, 2021/22, 2023/24: every year it appears)
2. Detroit travelling-missionary minimum tour (2020/21, 2021/22, 2023/24)
3. Chain letter / m-ary tree counting (2020/21, 2021/22, 2023/24)
4. Handshaking Theorem: statement, proof, application (2021/22, 2023/24, 2024/25)
5. R1..R6 relation-property classification (2020/21, 2023/24, 2024/25)
6. Five function correspondence types (2020/21, 2021/22)
7. Rooted-tree terminology, traversals, prefix/postfix (2020/21, 2021/22, 2024/25)
8. Truth tables, converse/contrapositive/inverse (every year)
9. Bit-string set representation (2023/24, 2024/25)
10. fog and gof for f=x^2+1, g=x+2 (2023/24 AND 2024/25, identical)
11. In-degree / out-degree tabulation of a digraph (2021/22, 2023/24, 2025/26)
12. Counting: passwords, chairs, PIN codes, SCHOOL arrangements (most years)
13. Inclusion-exclusion word problems (2021/22, 2025/26)
14. Balanced m-ary tree, leaves at height h (2020/21, 2021/22, 2024/25)

## C++ note
2023/24 and 2024/25 both demand written C++ (power set, bit strings,
isPerfectSquare by binary search, degree counting). The 2025/26 paper has none, but
the manual must still teach and provide these, compiled and run, since papers
recur. Cap code lines to the measured panel column limit (Chromium shrink, §2b).
