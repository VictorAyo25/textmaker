# What the COS221 exams actually test

Built from the full transcripts of both papers (`exam_2024_25_transcript.md`,
`exam_2025_26_transcript.md`). Every claimed output below was produced by a real JVM
(Temurin 17) and hand-checked independently.

## The format changed. The skills did not.

|              | 2024/25                          | 2025/26                                  |
|--------------|----------------------------------|------------------------------------------|
| Course title | Object-Oriented Programming (Java) | Computer Programming I (Java)           |
| Instruction  | Attempt any four (4) questions    | Attempt one question from each Section   |
| Structure    | 6 questions x 17.5 marks          | Section A 20, Section B 25, Section C 25 |
| Total / time | 70 marks / 3 hours                | 70 marks / 3 hours                       |

The paper was restructured, and the course was even retitled, but underneath, both
papers test the same four skills. Every single question on both papers is built from
them:

1. **Define / describe** a term precisely (method signature, encapsulation, checked vs
   unchecked, PrintWriter, try-with-resources, decision-making/looping/branching).
2. **Debug**: given broken code, list the errors and correct them. The 25/26 paper
   raises the stakes by also printing the correct output and making you work backwards
   to it.
3. **Dry run**: hand-trace code and state the output. The lecturer's own word is "dry
   run", which is why the manual's trace-table device is named DRY RUN.
4. **Write a program** to a spec, usually with methods, arrays, and a class.

**Consequence for the manual.** Teach to the four skills, not to a paper format. Then
the reader is safe whichever way the format lands next. Mocks must be written in both
shapes so neither is a surprise.

## The 25/26 Section A template is rigid

Question One and Question Two are the same question with different nouns:

| Part | Task                            | Marks | Q1 topic              | Q2 topic                |
|------|---------------------------------|-------|-----------------------|-------------------------|
| A    | Define                          | 2     | method overloading    | encapsulation           |
| B    | State three differences         | 3     | checked vs unchecked  | overloading vs overriding |
| C    | Find the errors, output given   | 5     | multiples of 4        | 10% discount            |
| D    | State output + convert loops    | 10    | Armstrong numbers     | perfect numbers         |

That is a gift: it is drillable. The manual should teach the template explicitly and
drill it, including "state three differences" as its own answerable form (a three-row
table beats a paragraph under time pressure).

## Recurring obsessions of this lecturer

These repeat across both papers and must be trained, not merely mentioned:

- **JOptionPane for all input and output.** Named in almost every write-a-program
  question, often "JOptionPane only".
- **Nested if-else, specifically.** 25/26 Q5 A(ii) and Q6 B(ii) both insist the logic be
  *nested*, "not independent/separate if checks", and Q5 spells out that days attending
  must be checked *within* each tier branch. Marks are for the shape of the control flow,
  not just the answer.
- **No collection classes.** ArrayList explicitly banned; parallel arrays required
  instead.
- **Loop conversion.** For to While and While to For, worth 10 marks in 25/26 Section A.
- **Validate input by re-prompting in a nested loop** until valid (Q5 B, Q6 B).
- **Own-method separation of concerns.** "Each task below must be its own method."
- **Exceptions and file I/O** with a restricted API list (only FileWriter, FileReader,
  BufferedReader, BufferedWriter, IOException).

## The planted errors, and what each one teaches

The debug questions are not random typos. They are a curriculum of the traps this
lecturer cares about. Verified list from 25/26 Q1 C (the same set recurs in Q2 C):

| Line | Planted error                                   | The idea it tests                        |
|------|-------------------------------------------------|------------------------------------------|
| 4    | `int[] arr = {24.0, ...}` — doubles in an int[] | type compatibility; the answer is 141.0, so it must be `double[]` |
| 5    | `int sum = 0` accumulating doubles              | the sum must be `double`                 |
| 8    | `i <= arr.length`                               | off-by-one, ArrayIndexOutOfBounds        |
| 10-12| `if (multiple of 4) continue;`                  | inverted condition: it skips exactly what it should keep |
| 13   | `sum += arr[j] - j`                             | should be `- 1`; wrong variable          |

Note how 10-12 and 13 are *logic* errors that still compile. That is the real lesson:
a program that compiles is not a program that is correct. This is the manual's central
theme for the debug skill.

## Verified outputs (from a real JVM, hand-checked)

- **25/26 Q1 D ArmstrongChecker** prints five lines:
  `370 -> ARMSTRONG`, `371 -> ARMSTRONG`, `372 -> NOT ARMSTRONG`, `407 -> ARMSTRONG`,
  `408 -> NOT ARMSTRONG`.
  (370 = 27+343+0; 371 = 27+343+1; 372 = 27+343+8 = 378 no; 407 = 64+0+343;
  408 = 64+0+512 = 576 no.)
- **25/26 Q2 D NumberClassifier** prints one line:
  `Perfect: 2, Abundant: 5, Deficient: 23`.
  (Perfect: 6, 28. Abundant: 12, 18, 20, 24, 30. 2+5+23 = 30 reconciles.)
- **24/25 Q1 C sumSeries(3,4,5,7)** returns **0 every time**. `sum += j / (j + 1)` is
  **integer division**, so every term is 0. This is the single best trap in either paper
  and deserves a prominent TRAP box: the reader who "does the maths" answers
  1/2 + 2/3 + ... and gets it wrong.
- **24/25 Q2 C** prints `-16` (2-4-6-8, not a sum).
- **24/25 Q4 C** prints `Sum = 7` (break at -1, so 2 is never added).
- **24/25 Q6 B compute(13)** returns **3** (13 is 1101 in binary; it counts set bits).
- **24/25 Q3 C** writes `Age: 25\nScore: 89.46` to data.txt (printf `%.2f` rounds
  89.456 to 89.46).

## Defect in the 24/25 paper (teach, do not silently fix)

Q6 D's example reads "1223 - true (pairs: 22). Only one pair - return false", which
contradicts itself in one line. Per the spec ("at least two pairs"), 1223 has one pair,
so the answer is **false** and the leading "true" is a slip. House rule: state what the
paper says and what is true.

## Implied weighting for the manual

Marks are dominated by write-a-program (7.5 of 17.5 in 24/25; 25 of every 25-mark
section in 25/26), so the manual's centre of gravity is **writing complete, compiling
programs to a spec**, with the debug and dry-run skills as the sharp instruments that
make that reliable. Definitions are cheap marks and should be drilled as flashcards
(MUST-MEMORISE), never as prose to be reread.
