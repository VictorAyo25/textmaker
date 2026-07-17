# CSC241 2018/2019 Exam Transcript

> **[sic]** This paper was filed under CSC241 (Python Programming Language I), but the printed header reads **COURSE CODE: CSC 213** and **COURSE TITLE: STRUCTURED PROGRAMMING**. The course code and title are transcribed exactly as printed below. The paper's content is entirely Python.

## Header

```
COVENANT UNIVERSITY
CANAANLAND, KM 10, IDIROKO ROAD
P.M.B 1023, OTA, OGUN STATE, NIGERIA.

TITLE OF EXAMINATION: ALPHA SEMESTER EXAMINATION
COLLEGE: SCIENCE AND TECHNOLOGY
DEPARTMENT: COMPUTER AND INFORMATION SCIENCES
SESSION: 2018/2019
COURSE CODE: CSC 213
COURSE TITLE: STRUCTURED PROGRAMMING
INSTRUCTION: ANSWER ANY FOUR QUESTIONS

SEMESTER: ALPHA
CREDIT UNIT: 3

Time: 2½ Hours
```

> **[handwritten]** Top-left corner, in blue ink, written diagonally: `[illegible: "MCGO2" or "17CG02..."]` — a partially cut-off word or matriculation-number fragment.

> **[handwritten]** Top-right corner, in blue ink, written vertically in large capitals: `DAMMIE`, with a small heart drawn above the final letter.

---

## Question One

**1. a)** With a given integer number n (user supplied), write a python program to generate a dictionary that contains {i : i*i} such that i is an integer number between 1 and n (both included). Then the program should print the dictionary. **(3.5 marks)**

**b)** Given the following dictionary:

```python
inventory = {

            'gold' : 500,
            'pouch' : ['flint', 'twine', 'gemstone'],
            'backpack' : ['xylophone', 'dagger', 'bedroll', 'bread loaf']
}
```

Write a python statement do the following:

> **[sic]** "Write a python statement do the following" — the word "to" is missing; it should read "to do the following". Also "statement" is singular although five separate statements are requested.

- Add a key to inventory called 'pocket' and set the value of 'pocket' to be a list consisting of the string values 'seashell', 'strange berry', and 'lint'.
- Sort the items in the list stored under the 'backpack' key.
- Remove 'dagger' from the list of items stored under the 'backpack' key.
- Add 50 to the number stored under the 'gold' key.
- Print the resulting dictionary

**(4 marks)**

**c)** Study the following dictionaries for an online grocery store:

```python
stock = {"banana": 6, "apple": 0, "orange": 32, "pear": 15, “avocado”: 1, “strawberry”: 4}
prices = {"banana": 4, "apple": 2, "orange": 1.5, "pear": 3, “avocado”: 5, “strawberry”: 8}
```

> **[sic]** Both dictionary literals mix straight double quotes (around "banana", "apple", "orange", "pear") with curly/smart typographic quotes (around “avocado” and “strawberry”). As printed, the smart quotes are not valid Python and would raise a SyntaxError.

Using the dictionaries,

**(i)** Write a function **compute_bill** that takes one argument (which is a list of shopping items) as input. The function should return the total price of the all items in the shopping list. While you loop through each item of the list, only add the price of the item to the total price if the item's stock count is greater than zero. If the item is in stock, after adding the price to the total, subtract one from the item's stock count.

> **[sic]** "the total price of the all items" — reads "the all items"; should be "all the items".

**(ii)** Your program should create a shopping list with any number of the items in the stock dictionary and then calculate the bill for the items in the shopping list. **(5 marks)**

**d)** The following are names of participants in a swimming and bowling event:

```
Swimming – Eric, Chioma, Bayo, Ekaete, Bridget, Hassan, Amina, Jumoke
Bowling – Hassan, Ngozi, Chris, Jide, Tosin, Eric, Zoe, Halima, Bayo, Ebuka
```

Write a python program to create a set for each event. Your program should;

- Print out list of participants who attended both events.
- Print out list of participants who attended only one of the events.
- Print out list of participants who attended only the swimming event but not the bowling event.
- Print out list of participants who attended only the bowling event but not the swimming event.
- Print out list of all participants.

**(5 marks)**

---

## Question Two

**2. a)** Mention and briefly describe the two types of files **(6marks)**

**b)** Write a function called **middle** that takes a list as parameter and returns a new list that contains all but the first and last elements. **(3.5marks)**

**c)** Suppose a file named **ChapelServiceAttendance.txt** contains the headers FName, LName, student number and four chapel attendance records for each student in the month of November. “1” signifies presence while “0” means the student was absent. A tab ('\t') delimits the data:

```
FName      LName     Student number      3Nov   10Nov   17Nov   24Nov
Nnamdi     Chukwu    12CF1122            1      1       0       1
Aderopo    Ude       12CF2233            0      0       1       1
Shina      Kudi      11CA4431            1      1       1       1
Helen      Mike      12CD8877            0      1       1       1
Kyle       Tunde     12CV7766            0      0       0       1
```

> **[sic]** The table is misprinted on the page. In the scan, the `10Nov`, `17Nov` and `24Nov` columns are typeset **one line higher** than the `3Nov` column and the name/student-number columns, so that the first `1 1 0 1` triplet sits on the `FName`/header row and each subsequent student's 10/17/24-Nov values appear on the row above their name. The alignment shown above is the intended reading, reconstructed from the paper's own worked examples: Nnamdi Chukwu = 1,1,0,1 → 3/4 = 75% and Aderopo Ude = 0,0,1,1 → 2/4 = 50%, which match the "e.g." lines exactly. The `Student number` column is also printed with a slight upward baseline offset relative to the names, and the leading `1` of `12CF1122`, `12CF2233`, `11CA4431` and `12CD8877` is faint/clipped in the scan.

Write a python program to read the content of the file and display the attendance percentage for all students on the screen. (**Hint**: compute **Attendance percentage** as **No. of times present/4\* 100**)

e.g. **Nnamdi Chukwu  12CF1122  75%**
     **Aderopo Ude      12CF2233  50%**

**(8marks)**

---

## Question Three

**3. a)** Briefly describe the following terms and give suitable examples where applicable **(7.5marks)**

**(i)** Lists **(ii)** Tuples **(iii)** Dictionary **(iv)** Sets **(v)** File

> **[handwritten]** In the right margin beside this sub-question, in pencil/faint ink: `5` and what appears to be a fraction working, `1 . 5` over `5` — `[illegible: likely a marker's score, "1.5/5"]`.

**b)** Given

```python
tuple = ('abcd', 787, 2.24, 'john', 70.2)
tinytuple = ('abcd', 786, 2.23, 'john', 70.2)
```

> **[sic]** The variable is named `tuple`, which shadows the Python built-in type `tuple`. Transcribed as printed.

What is the output of:

| | | |
|---|---|---|
| i. | `print(tuple[0])` | **(1mark)** |
| ii. | `print(tuple[1:3])` | **(1mark)** |
| iii. | `print(tuple[2:])` | **(1mark)** |
| iv. | `print(tinytuple[-4])` | **(1mark)** |
| v. | `print(tinytuple[-3:])` | **(1mark)** |

**c)** Write a Boolean function named is_prime which takes an integer as an argument and returns True if the argument is a prime number, or False otherwise. Use the function in a program that prompts the user to enter a number and then displays a message indicating whether the number is prime. **(5marks)**

> **[sic]** The function name is printed as `is_prime`, but the underscore renders as a low connecting stroke ("is\_prime") in the scan; read as `is_prime`.

---

## Question Four

**4. a)** Mention and describe any three string testing methods you know **(6marks)**

**b)** A car's kilometer-per-gallon (KPG) can be calculated with the following formula:

**KPG = Kilometer driven / Gallons of gas used**

Write a program that asks the user for the number of kilometers driven and the gallons of gas used. It should calculate the car's KPG and display the result. **(4marks)**

**c)** Write a Python program to print the even numbers from a given list called **list1** to a new list called **list2**. **(4.5marks)**

```
Sample List : [1, 2, 3, 4, 5, 6, 7, 8, 9]
Expected Result : [2, 4, 6, 8]
```

**d)** Using **for loop** and **range()** in Python, write a program to print the following sequence:

```
3 6 9 12 15 18 21 24
```

**(3marks)**

> **[sic]** In the scan the leading `3` of the sequence is printed slightly raised and smaller than the following digits (it sits superscript-like against the `6`), and the line "d) Using for loop and range()..." overlaps the sequence line. The sequence reads `3 6 9 12 15 18 21 24`.

---

## Question Five

**5. a)** List three escape characters and then effects in Python **(4.5marks)**

> **[sic]** "and then effects" — should read "and their effects".

**b)** Mention and briefly describe the three steps to be taken when a file is used by a program **(9marks)**

**c)** Write a python program to calculate the sum of the first 20 terms of the series. **(4marks)**

```
1/1 + ¼ + 1/9 + 1/16.....................
```

> **[sic]** This line is heavily degraded in the scan. The separators between terms are printed as short strokes that read as `-` but are `+` given the sum requested; `[illegible: "1/1 + 1/4 + 1/9 + 1/16 ..."]` is the best reading. The second term is printed with the single-glyph vulgar fraction `¼` while the others use `1/n` form. The series is the reciprocals of the squares (1/n² for n = 1, 2, 3, 4, ...). The sentence also ends with a full stop before the series, reading "...the first 20 terms of the series." rather than "of the series:".

---

## Question Six

**6. a)** Given the list of some books of the Bible

```python
BibleBooks = ['Matthew', 'Mark', 'Luke', 'John', 'Psalms', 'Romans']
```

Use List methods to achieve the following:

| | | |
|---|---|---|
| i. | Remove **Psalms** from the list. | **(1mark)** |
| ii. | Get the index of **Luke**. | **(1mark)** |
| iii. | Insert **Acts** in the list after **John** | **(1mark)** |
| iv. | Expand the list by adding **Corinthians** to the List | **(1mark)** |
| v. | Sort the list | **(1mark)** |
| vi. | What will be the output of print (**BibleBooks**)? | **(1mark)** |

**b)** Write a Python program to accept a string as input and add **'ing'** at the end of the given string (length should be at least 3). If the given string already ends with 'ing' then add **'ly'** instead. If the length of the given string is less than 3, leave it unchanged. For example: **(6.5marks)**

| Sample String (Input) | Expected Result (Output) |
|---|---|
| 'ab' | 'ab' |
| 'abc' | 'abcing' |
| 'string' | 'stringly' |

**c)** Write a Python program that writes to file called **products.txt**. The following records should be written to the product file. **(5marks)**

```
PName            Price        Category         Manufacturer
Gizmo            N19.99       Gadgets          GizmoWorks
Powergizmo       N29.99       Gadgets          GizmoWorks
SingleTouch      N149.99      Photography      Canon
MultiTouch       N203.99      Household        Hitachi
```

---

## Transcription notes

**Total pages:** 3 (`2018_19_p1.png`, `2018_19_p2.png`, `2018_19_p3.png`). All three were read visually and each was re-read a second time to verify the transcript line by line.

**Paper structure:**
- 6 questions printed; candidates **answer any four**.
- Time allowed: 2½ hours. Credit unit: 3. Semester: Alpha.
- Every question totals **17.5 marks**, so a full script is 4 × 17.5 = **70 marks**. The internal split varies per question:
  - Q1: 3.5 + 4 + 5 + 5
  - Q2: 6 + 3.5 + 8
  - Q3: 7.5 + (5 × 1) + 5
  - Q4: 6 + 4 + 4.5 + 3
  - Q5: 4.5 + 9 + 4
  - Q6: (6 × 1) + 6.5 + 5
- **No repeating subpart template.** Subpart counts differ (Q2 and Q5 have three subparts; Q1 and Q4 have four; Q3 and Q6 have three with an enumerated roman-numeral list inside one of them). The only consistent pattern is that each question mixes one short "mention/describe" theory subpart with two or three "write a program/function" subparts, and each question sums to 17.5.

**Topics per question:**
- Q1 — dictionaries (comprehension/generation, mutation of nested lists and values) and sets (union, intersection, symmetric difference, set difference).
- Q2 — file types (theory), list slicing via a `middle` function, and reading a tab-delimited file to compute attendance percentages.
- Q3 — core data-structure theory (lists, tuples, dictionaries, sets, files), tuple indexing and slicing output tracing, and a Boolean `is_prime` function.
- Q4 — string testing methods (theory), a simple input/arithmetic/output program (KPG), filtering even numbers from a list, and `for`/`range()` sequence printing.
- Q5 — escape characters (theory), the three steps of file use (theory), and summing a 20-term series.
- Q6 — list methods (remove, index, insert, append, sort), string manipulation with suffix rules ('ing'/'ly'), and writing records to a file.

**Illegible items:**
1. **Page 1, top-left handwriting** — a diagonal blue-ink word/fragment, partly cut off by the page edge; `[illegible: "MCGO2" / "17CG02"]`.
2. **Page 3, Question 5(c) series** — the term separators and the first term are badly degraded; `[illegible: "1/1 + 1/4 + 1/9 + 1/16 ..."]`. The separators read as `-` on the page but must be `+` for a sum; the mathematical intent (Σ 1/n² for the first 20 terms) is unambiguous.
3. **Page 2, Question 3(a) margin handwriting** — a faint numeric working; `[illegible: likely "1.5/5"]`.

**[sic] defects found:**
1. **Header/course mismatch** — filed as CSC241 (Python Programming Language I) but printed as **CSC 213 / STRUCTURED PROGRAMMING**. Content is Python throughout.
2. **Q1(b)** — "Write a python statement do the following" (missing "to"; also singular "statement" for five statements).
3. **Q1(c)** — `stock` and `prices` dict literals mix straight quotes with curly typographic quotes around “avocado” and “strawberry”; not valid Python as printed.
4. **Q1(c)(i)** — "the total price of the all items".
5. **Q2(c)** — attendance table columns misaligned: `10Nov`/`17Nov`/`24Nov` are typeset one line above the `3Nov` column and the names. Corrected alignment inferred from and confirmed by the paper's own worked examples (75% and 50%).
6. **Q3(b)** — variable named `tuple`, shadowing the Python built-in.
7. **Q4(d)** — leading `3` of the sequence printed raised/superscript-like and the preceding line overlaps it.
8. **Q5(a)** — "List three escape characters and then effects" (should be "their effects").
9. **Q5(c)** — series separators printed as `-` where `+` is required for a sum; mixed `¼` and `1/n` notation.

**Handwriting found (all on page 1 unless noted):**
- Top-left, blue ink, diagonal: `[illegible: "MCGO2"]`.
- Top-right, blue ink, large vertical capitals: `DAMMIE`, with a small heart above the last letter.
- Page 2, right margin at Q3(a): faint numeric working, `[illegible: likely "1.5/5"]`.
- Page 2 also carries small ink tick marks in the left margin beside the "3." and "4." question numbers, and a small stroke at the top right of the page. No handwriting on page 3 other than scan artefacts.

**Other notes:**
- Page 1 is scanned at a noticeable skew (roughly 5–7° rotation), which is why the header block and the bulleted lists in Q1(b) and Q1(d) run diagonally. All header fields remain legible.
- Mark allocations are printed inconsistently across the paper: Question 1 uses a space, e.g. `(3.5 marks)` and `(4 marks)`, while Questions 2–6 are closed up, e.g. `(6marks)`, `(3.5marks)`, `(8marks)`, `(1mark)`. Both forms are transcribed exactly as printed. No allocation on this paper uses the `[3.5mks]` bracket style.
