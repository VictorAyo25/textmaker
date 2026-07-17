# CSC241 2023/2024 Exam Transcript

## Header

COVENANT UNIVERSITY
CANAANLAND, KM 10, IDIROKO ROAD
P.M.B 1023, OTA, OGUN STATE, NIGERIA.
B.Sc. DEGREE EXAMINATION

- **COLLEGE:** Science and Technology
- **DEPARTMENT:** Computer & Info. Sciences
- **SESSION:** 2023/2024
- **SEMESTER:** ALPHA
- **COURSE CODE:** CSC213
- **CREDIT UNIT:** 3
- **COURSE TITLE:** Structured Programming
- **TIME:** 3 Hours
- **INSTRUCTION:** Answer any FOUR (4) Questions

> **[sic]** The printed header reads COURSE CODE: CSC213 / COURSE TITLE: Structured Programming, but this paper is filed as the CSC241 (Python Programming Language I) past paper. The paper's own content is entirely Python. Transcribed as printed; not corrected.

> **[sic]** "COURSE TTTLE" is printed for "COURSE TITLE" (three T's).

Stamp block, top right of page 1:

> **[handwritten]** Signature over the printed line "HEAD OF DEPARTMENT", inside a stamped box reading "COVENANT UNIVERSITY OTA / COMPUTER & INFO. SCIENCES". Beneath it: "Date: 20/2/24" (the day digit is unclear; `[illegible: 20]`).

Page footer, page 1:

> **[handwritten]** "1" written between the printed dashes at the foot of the page ("- 1 -").

---

## Question One

**a.** Briefly describe how the *and* operator works in Python (use examples)  **[2.5 Marks]**

**b.** Given `numbers = [1, 2, 3, 4, 5]`. What will be the output of `numbers*2`  **[3 Marks]**

**c.** Identify the Errors in the following code segment  **[4 Marks]**

```python
 1 person = { "name": 'John Doe', 'age': 30, 'city':
 2      'New York', 'Email': 'john.doe@example.com' }
 3
 4 print("Name:", person['Name'])
 5 print("Age:", person['Age'])
 6 Print("City:", person['City'])
 7 print("Email:", person['email'])
 8
 9 person['Age'] = "35"
10 person['phone'] = '123-456-7890
11 del person['email']
12
13 print("Updated Person Dictionary:")
14 print(person)
15
```

> **[sic]** The code is the subject of the "identify the errors" question, so its bugs are intentional. Reproduced verbatim, including: the dictionary keys being lower-case (`"name"`, `'age'`, `'city'`) while lines 4-6 index with capitalised keys (`'Name'`, `'Age'`, `'City'`); the key `'Email'` being capitalised while lines 7 and 11 use `'email'`; line 6's `Print` being capitalised (verified under magnification — lines 4, 5 and 7 are lower-case `print`); and line 10's string literal `'123-456-7890` having no closing quote. Note also the mixed quoting on line 1 (`"name"` in double quotes, `'John Doe'` in single). Line numbers 1-15 are printed in the paper's own gutter and are not part of the code. Line 1 carries a code-folding marker in the original.

**d.** In Nigeria, property taxes are calculated based on the assessment value of the property, which is typically 60 percent of its actual value. For instance, if a plot of land is valued at ₦100,000, its assessment value would be ₦60,000. The property tax rate varies depending on the assessed value. For properties with an assessment value of ₦10,000 or less, the tax rate is ₦0.72 for each ₦100 of the assessment value. However, for properties with an assessment value exceeding ₦10,000, the tax rate increases to ₦0.85 for each ₦100 of the assessment value. Write a Python program that prompts the user to input the actual value of a property and then calculates and displays the corresponding assessment value along with the property tax based on the applicable tax rates [Hint: Use Functions].  **[8 Marks]**

---

## QUESTION TWO

**a.** What is a count-controlled loop in Python?  **[2.5 Marks]**

**b.** Identify the Errors in this code segment and write the corrected version.  **[3 Marks]**

```python
 1 my_string = "Serve Jesus Now"
 2 print("Original String:", mystring)
 3
 4 first_character = my_string[1]
 5 last_character = my_string[-0]
 6 print("First Character:", first_character)
 7 print("Last Character:" last_character)
 8
 9 substring = my_string[17:]
10 print("Substring:", substring)
11
12 greeting = "Hi"
13 name = "Alice"
14 message = greeting + ", " + name + "!"
15 print("Message:", message)
16
17 length = len(mystring)
18 print("Length of the String:", length)
19
20 count_e = my_string.count('e')
21 print("Count of 'e':", count_e)
22
```

> **[sic]** Bugs are intentional (this is the "identify the errors" segment). Reproduced verbatim, including: `mystring` vs `my_string` (lines 2 and 17); `my_string[1]` for the first character; `my_string[-0]`; the missing comma on line 7; and the out-of-range slice start on line 9. Line numbers 1-22 are the paper's gutter numbers.

> **[handwritten]** Marginal annotations surround this code segment on page 2, mostly faint pencil. Legible fragments only: near line 1, `[illegible]`; beside line 4, `[illegible: index]` with a small `0` written above the `[1]`; beside line 5, `-1`; beside line 9, `12` written above the `17`; a bracketed note to the right reading `[illegible]`; and at right-hand margin a block including `value = d..[..+1]`, `d..[..] = value`, `the d..[..] = 4` and `print(...)` fragments. The right-margin block is too faint to read reliably and is not transcribed further. Also arrows drawn to lines 15, 17 and 20.

**c.** Write a Python program that generates 100 random numbers between 1 and 10. The program should then store the frequency of each number generated in a dictionary, where the number is the key and the frequency is the value. For example, if the program generates the number 6 a total of 11 times, the dictionary will contain a key of 6 with a value of 11. After storing the frequencies, the program should display information about the frequency of each number. Additionally, the program should calculate and display the sum of all the 100 random numbers generated using the formula Key*Value.  **[12 Marks]**

---

## Question Three

**a.** Mention five (5) benefits of modularizing a program with functions  **[2.5 Marks]**

**b.** Look at the following statement: levels = "Beginner, Average, Advanced, Expert". Write a statement that splits this string, creating a list of the competence levels.  **[2 Marks]**

**c.** What is are the outputs given the following code segment  **[3 Marks]**

> **[sic]** "What is are the outputs" is printed as shown.

```python
 1
 2 nested_list = [
 3     [1, 2, 3],
 4     [4, 5, 6],
 5     [7, 8, 9],
 6     [10, 11, 12, 13],
 7     [14, [15, 16, 17], 18],
 8     [19, [20, [21, 22], 23], 24]
 9 ]
10
```

> Line numbers 1-10 are the paper's gutter numbers. Line 2 carries a code-folding marker in the original.

  **i.** What is the value at index [3][2]?

  **ii.** print (len (nested_list[4]))

  **iii.** What is the value at index [5][1][1][0]?

**d.** Suppose there is a file named financial_data.txt stored on a computer's disk. This file contains financial records, each consisting of two fields: a company name followed by its yearly revenue (expressed in millions of Naira). Write a Python program to analyze the data in financial_data.txt and display the company with the highest revenue, along with its revenue value. Additionally, your program should report the total number of companies included in the file. [Hint: Utilize a variable and an "if" statement to track the highest revenue found while iterating through the records. Also, maintain a variable to count the total number of records in the file.]  **[10 Marks]**

---

## Question Four

**a.** Distinguish between a Void and Value-returning function in Python (with examples).  **[2.5 Marks]**

**b.** What will `list1` and `list2` contain after the following statements are executed?  **[2 Marks]**

  **i.** list1 = [1, 2] * 2

  **ii.** list2 = [3]

  **iii.** list2 += list1

> **[sic]** The assignment operators in b(i) and b(ii) are printed indistinctly and read as dashes/hyphens rather than clean `=` signs; b(iii) likewise reads as `+-` rather than `+=`. Rendered above as the intended `=` and `+=`. Best-guess reading: `list1 = [1, 2] * 2`, `list2 = [3]`, `list2 += list1`.

**c.** Identify the Error in this code Segment  **[3 Marks]**

```python
 1
 2 with open(example.txt, 'w') as file:
 3     file.write("Hello, World!\n")
 4     file.write("This is a sample file.\n")
 5     file.write("It contains some text.\n")
 6
 7 # Reading data from the file
 8 with open(example.txt, 'r') as file:
 9     # Read the entire content of the file
10     content = file.reading()
11
12 # Print the content read from the file
13 print(content)
14
```

> **[sic]** Bugs are intentional. Reproduced verbatim, including the unquoted filename `example.txt` on lines 2 and 8, and `file.reading()` on line 10. Line numbers 1-14 are the paper's gutter numbers. Lines 2 and 8 carry code-folding markers in the original.

**d.** Imagine you're using an application that converts your favorite 9-letter word into a unique numeric format. This application employs a special mapping where alphabetic characters correspond to numbers as shown below. Write a Python program that interacts with users, prompting them to input their favorite 9-letter word. Once entered, the program should convert the word into its unique numeric format based on the provided mapping and display the result. For example, if the user enters "HIGHLIGHT", the program should output the corresponding numeric format which is 444454448.  **[10 Marks]**

```
A, B, and C = 2
D, E, and F = 3
G, H, and I = 4
J, K, and L = 5
M, N, and O = 6
P, Q, R, and S = 7
T, U, and V = 8
W, X, Y, and Z = 9
```

> **[sic]** The worked example is inconsistent with the mapping. "HIGHLIGHT" is 9 letters mapping to H=4, I=4, G=4, H=4, L=5, I=4, G=4, H=4, T=8, i.e. 444454448 — this is correct. However the mapping omits any letter assigned to 1 and assigns four letters (P, Q, R, S) to 7 while all other groups have three; transcribed as printed.

---

## Question Five

**a.** Highlight the three (3) File Modes in Python  **[3 Marks]**

**b.** A program contains the following function definition:  **[2 Marks]**

```python
2
3 def cube(num):
4     return num * num * num
5
```

> Line numbers 2-5 are the paper's gutter numbers (the segment starts at 2 as printed). Line 3 carries a code-folding marker in the original.

  **i.** Write a statement that passes the value 4 to this function and assigns its return value to the variable result.

  **ii.** What will be the value in result

**c.** Design a Python program that interacts with users, prompting them to enter a series of 20 numbers. The program should store these numbers in a list and then display the following data:  **[12.5 Marks]**

  **i.** The lowest number in the list.

  **ii.** The highest number in the list.

  **iii.** The total sum of the numbers in the list.

  **iv.** After displaying the lowest, highest, and total sum of the numbers, the program should offer users the following choice to calculate the average of the numbers in the list Including or excluding the highest and lowest numbers.

  **v.** Note that if any of the entered numbers are negative, prompt the user to enter them again until all 20 numbers are non-negative. If after five attempts a non-negative number is not provided, terminate the program with an appropriate message.

---

## Question Six

**a.** Strings are *Immutable*. Explain and give reason why.  **[2.5 Marks]**

**b.** Write a function that accepts a string as an argument and returns true if the argument starts with the substring 'https'. Otherwise, the function should return false.  **[3 Marks]**

**c.** Given three Bible scriptures stored as strings:

```
Str1= "For God so loved the world that he gave his one and only Son, that whoever
believes in him shall not perish but have eternal life."

Str2 = "The Lord is my shepherd, I lack nothing."

Str3 = "For I know the plans I have for you, declares the Lord, plans to prosper you
and not to harm you, plans to give you hope and a future."
```

Write a Python program that performs the following Set operations on the words in these scriptures:  **[12 Marks]**

  **i.** Create a set containing all unique words found in the scriptures.

  **ii.** Display the set of unique words from the scriptures.

  **iii.** Calculate the intersection of the sets formed by the words in each scripture.

  **iv.** Calculate the union of the sets formed by the words in each scripture.

  **v.** Calculate the difference between the sets formed by the words in each scripture.

---

## Transcription notes

**Total pages:** 4 (2023_24_p1.png through 2023_24_p4.png). All four read and re-read for verification.

**Paper structure:**
- Six questions (One through Six). Instruction: "Answer any FOUR (4) Questions". Time: 3 Hours. Credit unit: 3.
- Every question totals 17.5 marks, so four questions total 70 marks:
  - Q1: 2.5 + 3 + 4 + 8
  - Q2: 2.5 + 3 + 12
  - Q3: 2.5 + 2 + 3 + 10
  - Q4: 2.5 + 2 + 3 + 10
  - Q5: 3 + 2 + 12.5
  - Q6: 2.5 + 3 + 12
- **Repeating subpart template:** yes, the questions follow a consistent shape — (a) a short definition/theory prompt worth 2-3 marks; (b) and/or (c) a short code-reading task (trace the output, split a string, or "Identify the Errors in this code segment") worth 2-4 marks; and a final long "Write a Python program that..." task worth 8-12.5 marks. Four of the six questions (Q1c, Q2b, Q4c, and by extension the trace in Q3c) hang on a deliberately buggy code segment printed with the paper's own gutter line numbers.
- Marks are printed as `[N Marks]` (spelled out), not `[Nmks]`. No `[3.5mks]`-style allocation appears anywhere in this paper.
- Mark allocations are right-aligned and frequently offset vertically from the subpart they belong to (most visibly on page 1, where the three Q1 allocations stack to the right of parts a-c, and on page 2, where the Q3 allocations trail their subparts by a line). Attribution above follows the paper's ordering.

**Illegible items:**
- The stamped date on page 1 reads as "20/2/24"; the day digit is smudged — recorded as `[illegible: 20]`.
- The right-margin handwriting on page 2 (beside Q2b) is faint pencil and largely unreadable. Only fragments were recoverable; noted inline as `[illegible]` rather than guessed.

**[sic] defects found:**
1. **Header course mismatch (most significant):** the paper is printed as **CSC213 / Structured Programming**, yet it is filed as the CSC241 (Python Programming Language I) past paper and its content is 100% Python. Either the paper was misprinted or the source file is mis-filed. Flagged, not corrected.
2. "COURSE TTTLE" printed for "COURSE TITLE" on page 1.
3. Q3c: "What is are the outputs" (grammatical error, printed as shown).
4. Q4b: the `=` and `+=` operators are printed indistinctly and read as dashes; best-guess reading recorded.
5. Q4d: the letter-to-number mapping has no letter assigned to 1, and the group P/Q/R/S has four letters while every other group has three. The worked example ("HIGHLIGHT" → 444454448) is itself internally correct.
6. Intentional bugs in Q1c, Q2b and Q4c code segments are the subject of those questions and were transcribed verbatim with explanatory notes (they are not paper defects).

**Handwriting found:**
- Page 1: HOD signature and date "20/2/24" in the stamp box; a handwritten "1" in the page-number footer.
- Page 2: extensive faint pencil annotations in both margins around the Q2b code segment (index corrections such as `0`, `-1`, `12`, plus a right-margin working block), and arrows pointing at lines 15, 17 and 20. Marked `[handwritten]`, never merged into printed text.
- Pages 2, 3: the "COVENANT UNIVERSITY OTA / COMPUTER & INFO. SCIENCES" stamp with signature recurs bottom-right.
- Page 3: scattered faint pencil marks in the right margin and around Q4d's mapping block, too light to read; not transcribed.
- Page 4: no handwriting.
