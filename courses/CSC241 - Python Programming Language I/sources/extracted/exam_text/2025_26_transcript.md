# CSC241 2025/2026 Exam Transcript

Transcribed by reading the page images (the source is seven phone photos, no text
layer). Source: `sources/exams/exam_2025_26.pdf` (built from the seven JPGs the
student supplied), 7 photographed sheets.

This is the newest paper on hand and the first from the 2025/2026 session. It prints
CSC241 / Python I cleanly (no CSC213 lineage question here). Stamped by the Head of
Department 10/07/2026.

## Header

```
COVENANT UNIVERSITY
CANAANLAND, KM 10, IDIROKO ROAD
P.M.B 1023, OTA, OGUN STATE, NIGERIA.
B.Sc. EXAMINATION

COLLEGE: Science and Technology        DEPARTMENT: Computer & Info. Sciences
SESSION: 2025/2026                     SEMESTER: OMEGA
COURSE CODE: CSC241                    CREDIT UNIT: 3
COURSE TITLE: Python I
INSTRUCTION: Answer any Four (4) Questions.    Time Allowed: 3 Hours
```

## THE TEMPLATE SHIFTED FROM 2024/25

This paper breaks three things the 2024/25 template held rigid, and the manual's
framing (built around "five subparts at 3.5 marks each") must absorb the change:

1. **Marks vary per subpart.** Seen this paper: 1, 2, 2.5, 3, 3.5, 4.5, 5, 6, 6.5,
   7, 7.5, 10.5. Not a uniform 3.5. Each question still totals 17.5 (70 over four).
2. **Subpart count varies.** Q1 has (a) to (e); Q2, Q3, Q5 have (a) to (d); Q4 and
   Q6 have (a) to (c). Not always five.
3. **Topics mix inside one question.** Q1 = strings + dict + two math programs. Q4 =
   immutability + a function + a full SQLite program. The clean one-module-per-
   question mapping of 2024/25 is gone.

What held: six questions offered, attempt any four; and the four underlying task
types (define/describe, find-and-fix errors, trace/state-output, write-a-program)
are still the whole exam.

## Question One

**(a)** Briefly describe how the `and` operator works in Python (use examples). [2.5 marks]

**(b)** What is a string in Python? List and briefly explain four common string
methods used in Python. Provide an example for each method. [5 marks]

**(c)** Identify the Errors in the following code segment: [3 marks]

```
1  person = { 'name': 'John Doe', 'age': 30, 'city':
2     'New York', 'Email': 'john.doe@example.com' }
3
4  print("Name:", person['Name'])
5  print("Age:", person['Age'])
6  print("City:", person['City'])
7  print("Email:", person['email'])
8
9  person['Age'] = "35"
10 person['phone'] = '123-456-7890'
11 del person['email']
12
13 print("Updated Person Dictionary:")
14 print(person)
15
```

Keys as defined: `'name'`, `'age'`, `'city'`, `'Email'`. Every access uses the wrong
case, so each is a `KeyError` on the FIRST one reached: `person['Name']` (line 4).
Also lines 5, 6 (`'Age'`, `'City'`), line 7 and line 11 (`'email'` vs `'Email'`),
and line 9 writes to `'Age'` which creates a NEW key rather than updating age. A
case-sensitivity lesson end to end.

**(d)** Write a Python program that implements a mathematical model to calculate Body
Mass Index (BMI). Use the formula: BMI = W / H^2, where W = weight in kilograms,
H = height in meters. [3.5 marks]

```
Requirements:
1. Classify the BMI:
   - BMI < 18.5            -> Underweight
   - 18.5 <= BMI < 25      -> Normal weight
   - 25 <= BMI < 30        -> Overweight
   - BMI >= 30             -> Obese
2. Display the BMI value with the BMI class.
```

**(e)** Write a Python program that calculates the future value of an investment
using compound interest. The program should display A and the interest earned
(A - P) to two decimal places. [3.5 marks]

```
Use the formula: A = P(1 + r/n)^(nt) where:
   - P = principal
   - r = annual interest rate (decimal)
   - n = number of times interest is compounded per year
   - t = time in years
```

## Question Two

**(a)** What is a count-controlled loop in Python? [3.5 marks]

**(b)** Explain the differences among the main types of control structures in Python.
Give one example of each. [4.5 marks]

**(c)** Identify the Errors in this code segment and write the corrected version. [3 marks]

```
1  my_string = "Serve Jesus Now"
2  print("Original String:", mystring)
3
4  first_character = my_string[1]
5  last_character = my_string[-0]
6  print("First Character:", first_character)
7  print("Last Character:", last_character)
8
9  substring = my_string[17:1]
10 print("Substring:", substring)
11
12 greeting = "Hi"
13 name = "Alice"
14 message = greeting + " , " + name + " ! "
15 print("Message:", message)
16
17 length = len(mystring)
18 print("Length of the String:", length)
19
20 count_e = my_string.count('e')
21 print("Count of 'e':", count_e)
22
```

Errors: line 2 and line 17 use `mystring` (undefined) not `my_string` -> `NameError`
(line 2 raises first). Logic: line 4 `my_string[1]` is the SECOND char not the first
(should be `[0]`); line 5 `my_string[-0]` is `-0 == 0`, the FIRST char, not the last
(should be `[-1]`); line 9 `my_string[17:1]` is out of range and empty (should be a
valid slice). Line 14 spacing is stylistic, not an error.

**(d)** Given that the correct password for accessing the system is `admin123`, write
a Python program that uses appropriate control structures to perform the required
tasks. Grading scheme: 70-100 A, 60-69 B, 50-59 C, 45-49 D, 0-44 F. [6.5 marks]

```
Requirements:
i.    Prompt for a password and keep requesting until 'admin123' is entered.
      Print "Access Denied" for every wrong attempt and "Access Granted" on success.
ii.   Prompt the user to enter a student's examination score.
iii.  Validate that the score is between 0 and 100; print an error if outside range.
iv.   If valid, determine and display the grade using the scheme above.
v.    Prompt for a positive integer and use a for loop to print its multiplication
      table from 1 to 12 in a neatly formatted manner.
vi.   Using a while loop, repeatedly prompt for numbers until 0 is entered. After 0,
      display the total sum of all numbers entered (excluding 0) and the count of
      valid numbers entered.
```

## Question Three

**(a)** Mention five (5) benefits of modularizing a program with functions. [2.5 marks]

**(b)** What is a function in Python? Why are functions important in programming?
Differentiate between built-in functions and user-defined functions (with examples). [6 marks]

**(c)** What will list1 and list2 contain after the following statements are executed? [3 marks]

```
i.   list1 = [1, 2] * 2
ii.  list2 = [3]
iii. list2 += list1
```

Answers (verify by run): list1 = `[1, 2, 1, 2]`; after `list2 += list1`,
list2 = `[3, 1, 2, 1, 2]`.

**(d)** The Computer Science Department organized a beginner Python Programming
Workshop. Write a program that uses the most suitable Python collection for each type
of data. [6 marks stem; the requirement list below is marked 5 marks]

```
Records provided:
  - Registered Students: Esther, John, Paula, Paul, Peter, Ada, John, Mary
  - Workshop Details: "Python Programming Workshop", "Room 204", "Monday", 30
  - Students Who Attended: Esther, John, Mercy, Paul, Esther, John, Paula

Requirements:
  i.    Store the registered students using the best collection.
  ii.   Store the workshop details using the best collection.
  iii.  Remove duplicate names from the attendance record.
  iv.   Store each student's score using the best collection.
  v.    Display the workshop details.
  vi.   Display the unique list of registered students.
  vii.  Display the unique list of students who attended.
  viii. Display students who registered but did not attend.
  ix.   Display students who attended but were not registered.
  x.    Display students who scored 60 and above.
```

Needs set difference both ways (registered - attended, attended - registered), a
tuple for the fixed workshop details, a dict for scores.

## Question Four

**(a)** Strings are Immutable. Explain, with reasons. [marks not legible on photo;
the two (b) parts are 1 mark each]

**(b)** A program contains the following function definition:

```
def cube(num):
    return num * num * num
```

  i.  Write a statement that passes the value 4 to this function and assigns its
      return value to the variable `result`. [1 mark]  ->  `result = cube(4)`
  ii. What will be the value in `result`? [1 mark]  ->  `64`

**(c)** A secondary school has decided to computerize the management of students'
academic records using an SQLite database. Store records in a database named
`school.db`, in a table named `student`, with fields StudentID (INTEGER),
StudentName (TEXT), Class (TEXT), and Score (REAL). [10.5 marks]

```
Records provided:
  101  David James    SS1  78
  102  Mary Johnson   SS2  85
  103  Peter Okoro    SS1  67
  104  Grace Bello    SS3  92
  105  Esther Ade     SS2  74

Requirements:
  i.   Create the database and table if they do not already exist.
  ii.  Insert the given records into the student table.
  iii. Retrieve and display all student records.
  iv.  Retrieve and display only the records of students in SS2.
  v.   Display statistics: total number of students, highest score, average score.
  vi.  Update the score of Peter Okoro from 67 to 75.
  vii. Delete the record of the student whose StudentID is 105.
```

## Question Five

**(a)** What is file handling in Python? [2 marks]

**(b)** List and explain four (4) file access modes used in the `open()` function. [6 marks]

**(c)** Mention the difference between reading from a file and appending to a file. [2 marks]

**(d)** The Computer Science Department conducted a Continuous Assessment (CA) for
CSC241 students. The file created at the beginning of the program must be used for
all subsequent operations. Each record holds Name, Matric Number, Department, Score,
stored in a text file named `your_matric_number_CSC241.txt` (e.g.
`23CG012345_CSC241.txt`). [7.5 marks]

```
Sample records:
  Name: John Doe, Matric No: 23CG012345, Department: Computer Science, Score: 78
  Name: Mary James, Matric No: 23CG012346, Department: MIS, Score: 85

Requirements:
  i.   Prompt for 10 student records and save them to the specified text file.
  ii.  Prompt for 5 more records and APPEND them without deleting existing ones.
  iii. Read and display all student records stored in the file.
  iv.  Read and display only the first five student records stored in the file.
```

## Question Six

**(a)** Given the following code segment: [3 marks]

```
nested_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
    [10, 11, 12, 13],
    [14, [15, 16, 17], 18],
    [19, [20, [21, 22, 23], 24]]
]
```

  i.   What is the value at index `[3][2]`?              -> `12`
  ii.  `print(len(nested_list[4]))`                       -> `3`
  iii. What is the value at index `[5][1][1][0]`?         -> `21`

(Deeply nested indexing; verify each by run.)

**(b)** A fitness club organized a Weekly Step Challenge. Write a program that uses a
VOID function named `display_achievement_summary(user_name, actual_total,
target_total)` to evaluate and display a participant's fitness achievement. [7 marks]

```
Requirements:
  i.   Prompt for name, number of days to track, and daily step goal.
  ii.  Use a loop to prompt for the steps taken each day.
  iii. Calculate the total steps taken.
  iv.  Calculate the overall target = daily goal * number of days.
  v.   Create a void function display_achievement_summary(user_name, actual_total, target_total).
  vi.  Pass name, total steps, and overall target to the function.
  vii. Inside, display the name, total steps, and whether the milestone was achieved.

Sample Interaction:
  Enter your name: Alice
  Enter the number of days to track: 3
  Enter your daily step goal: 10000
  Enter steps for day 1: 12000
  Enter steps for day 2: 9000
  Enter steps for day 3: 11000
  --- Progress Report for Alice ---
  Total Steps: 32000
  Milestone Achieved!!
```

(Target = 10000 * 3 = 30000; actual 32000 >= 30000, so achieved.)

**(c)** A commercial renovation company installs flooring in CIRCULAR meeting rooms.
Write a program that uses VALUE-RETURNING functions to estimate the project cost.
Area = pi * r^2 (pi from the math module). Total Cost = (Area * Flooring Price) +
Labor Fee. [7 marks]

```
Requirements:
  i.   Value-returning function get_data() prompts for room radius, flooring price
       per square meter, and labor fee.
  ii.  Return the three input values from get_data() to the main program.
  iii. Value-returning function calculate_area(radius) returns area using math.pi.
  iv.  Value-returning function calculate_total(area, material_price, labor_fee)
       returns the total project cost.
  v.   In main, call the three functions and compute the final estimate.
  vi.  Display the total calculated project cost.
  vii. If the total exceeds $10,000, print "Requires Senior Management Approval",
       otherwise print that approval is not required.

Sample Interaction:
  Enter room radius (meters): 12
  Enter flooring price per square meter: 20
  Enter labor fee: 1500
  --- Project Estimate ---
  Total Calculated Cost: 10546.90
  Status: Requires Senior Management Approval.
```

CANDIDATE DEFECT (verify by run): with radius 12, price 20, labor 1500 and
`math.pi`, Area = pi*144 = 452.3893..., cost = 452.3893*20 + 1500 = 10547.79, NOT the
printed 10546.90. The paper's own sample output looks wrong by about 0.89. Treat like
the other course-material defects: show the true run, note the paper's figure.

## Topic coverage (maps onto the manual's five modules)

| Q | Parts | Manual home |
| --- | --- | --- |
| 1 | and-operator, strings, dict errors, BMI, compound interest | M2 (operators, strings), M3 (dict), M1/M2 (arithmetic, **) |
| 2 | count loop, control structures, string errors, grading program | M3 (control flow) |
| 3 | modularization, functions, list ops, collections choice | M4 (functions), M3 (lists/sets/tuples/dicts) |
| 4 | immutability, cube function, SQLite | M2/M3, M4, M5 (databases) |
| 5 | file handling, modes, read vs append, CA file program | M4 Unit 3 (file handling) |
| 6 | nested list indexing, void function, value-returning + math.pi | M3 (lists), M4 (functions) |

Every question has a home. The blend question is what the manual does NOT yet teach
explicitly: see the gap audit alongside this file.
