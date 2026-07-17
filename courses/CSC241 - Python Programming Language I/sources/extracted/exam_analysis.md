# CSC241 exam analysis, nine sessions (2014/15 to 2024/25)

Built from the verified transcripts in `exam_text/`. Every claim about what a code
snippet does was checked by executing it, not by reading it.

## The headline finding: eight of the nine papers are a different course

Seven of the nine papers print **CSC213 / Structured Programming** in the header,
not CSC241 / Python Programming Language I:

| Session | Printed course code | Printed title | Python era |
| --- | --- | --- | --- |
| 2014/15 | CSC213 | Structured Programming | **Python 2** (2.7.3 banner in a screenshot) |
| 2015/16 | CSC 213 | STRUCTURED PROGRAMMING | Python 2 idiom |
| 2018/19 | CSC 213 | STRUCTURED PROGRAMMING | Python 3 |
| 2019/20 | CSC213 | Structured Programming | Python 3 |
| 2020/21 | CSC213 | Structured Programming | Python 3 |
| 2021/22 | CSc213 | Structured Programming | Python 3 |
| 2022/23 | **CSC 241** | PYTHON | Python 3 |
| 2023/24 | CSC213 | Structured Programming | Python 3 |
| 2024/25 | **CSC241** | Python Programming Language I | Python 3 |

This is not a filing mistake. It is the same course under its old identity: the
content of the CSC213 papers is Python throughout. The course was renumbered and
retitled, and only the two most recent papers carry the new identity. The
**2023/24 paper still prints CSC213 while the 2022/23 one prints CSC241**, so the
changeover was not clean and the header cannot be used to date a paper.

**Consequence for the manual:** the older papers are still legitimate practice for
the *skills*, but they are not a reliable guide to the *shape* of the exam Victor
will sit, and two of them test topics that no longer exist on the syllabus.

## Scope drift: what the old papers test that the manual does not cover

The 2014/15 and 2015/16 papers carry genuine Structured Programming theory that has
**no counterpart in the 224-page CSC241 manual's five modules**:

- What is Structured Programming; the three features (top-down analysis,
  modularization, structured code)
- Structured Programming versus Object Oriented Programming, three differences
- What is an Algorithm, properties of a good algorithm
- **Write the algorithm and draw the flow chart** (2015/16 Q1f, 7 marks)
- Python versus C-like syntax (semicolons, braces, indentation)

None of this is in Modules One to Five. Teaching it would pad the manual with
material the current course does not examine. **Recommendation: exclude the
2014/15 and 2015/16 papers from the drilled set**, and note them only as history.

There is a second reason to quarantine 2014/15: it is a **Python 2** paper. Its
marking scheme relies on `1/(i*i)` being integer division and uses `raw_input`.
Under Python 3 those answers are simply wrong. Mining it for content risks
importing Python 2 semantics into a Python 3 manual, which is exactly the class of
silent error the QA bar forbids.

## The 2024/25 paper is the template, and it is rigid

The most recent paper is the only one that matches the current course title, and it
is also the most regular paper of the nine. Six questions, attempt any four, every
question five subparts at [3.5mks], 17.5 per question, 70 total.

**Every one of the six questions follows the identical subpart template:**

| Part | Task |
| --- | --- |
| (a) | Define the concept, list N things, give an example of each |
| (b) | Identify and fix the errors in a broken snippet |
| (c) | State the output and explain execution line by line |
| (d) | Write a program to a numbered spec, fixed-size input |
| (e) | Extend (d) to arbitrary-size input |

Topic per question maps cleanly onto the manual:

| Q | Topic | Manual module |
| --- | --- | --- |
| One | Control structures, break/continue, for/else | Module Three, Units 1 to 2 |
| Two | Built-in data structures (list, dict, set, tuple) | Module Three, Units 3 to 4 |
| Three | Functions, default parameters | Module Four, Unit 1 |
| Four | Strings and string methods | Module Two, Unit 2 |
| Five | File handling, open() modes, with-statement | Module Four, Unit 3 |
| Six | Databases, sqlite3, SQL | Module Five, Unit 1 |

Module Five Unit 2 (GUI/tkinter) drew no question on this paper, **but it is not a
dead topic**: 2019/20 Q6 closes with a GUI Celsius-to-Fahrenheit converter. It must
be taught, just not weighted like the six topics above. Module One (overview/setup)
and Module Four Unit 4 (exception handling) drew no question on any paper, though
exception handling is implicitly needed for the robust-input requirements in the
(d)/(e) parts, and Module One is a prerequisite the zero-external-sources rule
forces us to teach regardless (installing Python, the REPL versus a script).

## What is invariant across every session

Regardless of the header, the same four tasks recur in all nine papers:

1. **Define/describe/list N things** with an example of each.
2. **Identify and fix the error(s)** in a printed code segment. Present in every
   paper; in 2019/20 it appears in all six questions, worth [3 Marks] each; in
   2023/24 the buggy segments are printed with gutter line numbers.
3. **What will this code display**, i.e. trace and state the output.
4. **Write a Python program that...**, the largest single allocation, 7 to 12.5
   marks in the older papers, restructured into the (d)+(e) pair in 2024/25.

**These four tasks are the whole exam.** The manual's practice apparatus should be
built from them directly: a DEFINE box, a FIND THE BUG box, a DRY RUN box (trace
tables), and a WRITE IT box.

## The 2024/25 signature: arbitrary-size input

Part (e) of every question extends part (d) from fixed-size to arbitrary-size
input, using one of exactly two idioms:

- **The `done` sentinel loop** (Q3(e), Q5(e), Q6(e)): loop until the user types
  `done`.
- **The split-and-convert loop** (Q1(e), Q2(e)): read one line of space-separated
  values, `split()`, convert each to `int`.

Whatever else the manual drills, it must drill these two to reflex. Together they
are worth 17.5 marks on the 2024/25 paper, a full quarter of the attemptable total.

## Defects to teach, not silently fix

The house rule is to teach a defective source, not paper over it. The serious ones:

**2024/25 question paper:**

1. **Q1(b) hangs.** The snippet's `continue` sits inside `if i % 2 == 0:` and
   *before* `i += 1`, so at `i == 6` it skips the increment and loops forever.
   Executed and confirmed: it prints `2`, `4`, then spins at `i = 6`. The question
   says the code "is intended to print all even numbers from 1 to 10, skipping
   number 6" and asks only to correct the error(s). A candidate who fixes only the
   skip logic has not fixed the hang. This is the best teaching snippet on the paper.
2. **Q1(c) tests `for`/`else`**, a niche construct. `break` at `i == 3` suppresses
   the `else`, so the output is `0 1 2` and "Loop finished" never prints. Executed
   and confirmed. The manual must introduce `for`/`else` before this is answerable.
3. **Q4(c) traps the casing.** `text.lower()` turns "Python!" into "python!", so
   `.replace("python", "world")` *does* match. Output is `  hello, world!  ` and
   `len(text)` is 18. Executed and confirmed. Evaluating `replace` against the
   original casing gives the wrong answer.
4. **Q4(b)** uses two invented methods: `.index()` called with no argument
   (TypeError, confirmed) and `.uppercase()`, which does not exist (the method is
   `.upper()`). Both intentional.
5. **Q5(b)** is a compound break: an unclosed parenthesis on the `write` line (a
   SyntaxError that masks everything after it, confirmed) plus `file.close` missing
   its parentheses. The interpreter never reaches the second bug. Good lesson about
   error ordering.
6. **Q2(b)'s `list(students)` is a no-op**, not an error. The code runs and prints
   5. There is no exception to spot; the defect is purely logical.
7. **The pass mark exists only in handwriting.** Q2(e) and Q5(e) both ask the
   candidate to count "passes and fails" while the printed paper never defines a
   pass mark. A handwritten annotation, "Pass mark is 45 and above", appears twice
   (pages 3 and 5). Without it both parts are unanswerable as printed.

**2014/15 marking scheme (substantially broken, 39 defects logged).** This paper
uniquely includes a **full marking scheme**, which is genuinely valuable as evidence
of what earns marks, but it cannot be trusted as a source of correct Python:

- **Q3(a) answers the wrong question**: asks for factorial, supplies Fibonacci.
- **Q5(a) is self-contradictory**: `def is divisible_by_3(n):` (space instead of
  underscore, a syntax error) and both the `if` and `else` branches print the same
  "not divisible" message, so it can never report success.
- **Q6(d) prints 0**: increments before adding, and relies on Python 2 integer
  division.
- **Q6(c) explains a program that is not the program asked about.**
- **Q6's subparts are mislabelled**: `c)` and `d)` each appear twice, no `(b)` at all.

**Other papers:** 2018/19 Q2(c)'s attendance table is misprinted with columns offset
by one line; the intended alignment was reconstructed and confirmed against the
paper's own worked percentages (75% and 50%). Several papers print string literals
with curly typographic quotes, so the snippets are not valid Python as printed
(2018/19 Q1(c), 2019/20 Q1(c) and Q2(b)).

## Recommended weighting for authoring

| Tier | Papers | Use |
| --- | --- | --- |
| **Primary** | 2024/25 | The template. Mock 1 mirrors it exactly, question for question. |
| **Secondary** | 2022/23, 2023/24, 2021/22, 2020/21, 2019/20, 2018/19 | Skill drilling. Python 3, on-syllabus, but older question shapes. Mine for FIND THE BUG and DRY RUN items. |
| **Quarantine** | 2015/16, 2014/15 | Off-syllabus (flowcharts, algorithms, SP vs OOP) and Python 2. Do not mine for content. 2014/15's marking scheme is useful only as evidence of marking style. |

## Reference-card inventory

Every idiom the exam actually requires, each needing an in-manual reference card
under the zero-external-sources rule:

`input()`, `int()`, `float()`, `str.split()` with and without a delimiter,
`str.strip()`, `str.lower()`, `str.upper()`, `str.replace()`, `str.index()`,
string slicing, `len()`, `max()`, `min()`, `sum()`, `sort()` and `sorted()`
ascending and descending (`reverse=True`), `list.append()`, `list.remove()`,
`list.insert()`, `set()` for dedup, set operations (union, intersection, symmetric
difference), dict literals, key access, nested mutation, `def`, default parameters,
`return`, `%` modulo, `range()`, `break`, `continue`, `for`/`else`, `open()` modes
`r`/`w`/`a`, `with ... as`, `file.write()`, `file.close()`, `sqlite3.connect()`,
`conn.cursor()`, `cursor.execute()`, `conn.commit()`, `conn.close()`, `fetchall()`,
and the SQL `CREATE TABLE` / `INSERT INTO` / `SELECT` trio.
