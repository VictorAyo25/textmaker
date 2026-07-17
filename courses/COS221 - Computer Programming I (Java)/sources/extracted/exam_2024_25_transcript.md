# COS221 exam 2024/2025 — transcript

Transcribed by eye from `sources/exams/exam_2024_25.pdf` (5 pages, scans embedded in a
Word document, no text layer). Verified in a second pass against the rendered images.

**Header.** B.Sc. Degree Examination. College: Science and Technology. Department:
Computer and Info. Science. Session 2024/2025. Semester: Omega. Course code: COS 221.
Course title: **Object-Oriented Programming (Java)**. Credit unit: 3. Time: 3 hours.
HOD stamp dated 4/7/25.

**Instructions.** Attempt any four (4) questions.

**Shape.** Six questions, 17.5 marks each, answer any four. Total 70 marks. There are
no sections. Each question follows a loose A/B/C/D template of
define (3), debug (3), dry run (4), write a program (7.5).

> Format note: the 25/26 paper replaced this with three sections and forced one
> question from each. Both papers total 70 marks over 3 hours, and both test the same
> four skills: define, debug, dry run, write.

---

## Question One (17.5 Marks)

**A.** Define Method signature, Method overloading and Void Method. **[3 marks]**

**B.** Debug this code snippet, list and correct the errors. **[3 marks]**

```java
public class SquareCalc {
    public static void main(String[] ) {
        int num = 5;
        double result = square(num)
        System.out.println("Square is: " + result);
    }

    public static int square(int) {
        return n * n;
```

**C.** Dry run this code snippet with the following values: 3,4,5,7. **[4 marks]**

```java
public static int sumSeries(int i) {
    int sum = 0;
    for (int j = 1; j <= i; j++) {
        sum += j / (j + 1);
    }
    return sum;
}
```

**D.** Write a program that *overloads* a method named area to compute: **[7.5 marks]**
  i. The area of a circle
  ii. The area of a rectangle
  iii. The area of a triangle.
  Call these methods and print out their values in the main method.

---

## Question Two (17.5 Marks)

**A.** Define the following: Dynamic array initialisation, the length property of
arrays, and the out-of-bounds exception in arrays. **[3 marks]**

**B.** Debug this code snippet, list and correct the errors. **[3 marks]**

```java
public class CopyArray {
    public static void main(String[] args) {
        int[] a = {2, 4, 6, 8};
        int b;
        System.arrayCopy(a, 0, b, 0, a.length);
        for(int i = 0; i <= b.length; i) {
            System.out.println(b[i]);
        }
    }
}
```

**C.** Dry run this code. State the output for each iteration and state the final output
**[4 marks]**

```java
public class Array {
    public static void main(String[] args) {
        int[] nums = {2, 4, 6, 8};
        int x = nums[0];
        for (int i = 1; i < nums.length; i++) {
            x = x - nums[i];
        }
        System.out.println(x);
    }
}
```

**D.** Write a program that does the following: **[7.5 marks]**
  i. *Prompts* the user to input 10 values into an array
  ii. Implement two methods
      a. A method to *find, count* and *display* the number of even
      b. Another method to *sum* and *display* the odd numbers.
  iii. In the main method, use a for loop to *find* and *display* the maximum number.

---

## Question Three (17.5 Marks)

**A.** Define the following: PrintWriter, Files.write() method and try-with-resources
block. **[3 marks]**

**B.** Debug this code snippet, list and correct the errors. **[3 marks]**

```java
java.io.FileWriter;

public class FileTest {
    public static void main(String[] args) {
        FileWriter writer = FileWriter("note.txt");
        writer.write("Hello from Java!");
        writer.close
    }
}
```

**C.** What is the output of the data.txt file? **[4 marks]**

```java
import java.io.*;

public class PrintWriterExample {
    public static void main(String[] args) throws IOException {
        PrintWriter pw = new PrintWriter("data.txt");
        pw.print("Age: ");
        pw.println(25);
        pw.printf("Score: %.2f", 89.456);
        pw.close();
    }
}
```

**D.** Write a program that does the following: **[7.5 marks]**
  i. *Create a file* named students.txt if it does not exist.
  ii. Uses PrintWriter to *write* the following student records to the file in a
      formatted table

      | Name   | Age | GPA  |
      |--------|-----|------|
      | John   | 20  | 3.75 |
      | Lilian | 21  | 3.95 |
      | Ken    | 19  | 3.65 |

  iii. Use printf() for proper column alignment
  iv. Ensure the file is appended to if it already exists.
  v. *Handle* possible exceptions properly

---

## Question Four (17.5 Marks)

**A.** Describe the following statements: Decision-making, Looping and Branching.
**[3 marks]**

**B.** Debug this code snippet, list and correct the errors. **[3 marks]**

```java
int count = 1
float output = "";

while(count <=5); {
    output = output + count + " ";
    Count
}

System.out.println(output);
```

**C.** State the output of each iteration and the final sum. **[4 marks]**

```java
int sum = 0;
int[] inputs = {3, 4, -1, 2};

for(int i = 0; i < inputs.length; i++) {
    if(inputs[i] < 0)
        break;
    sum += inputs[i];
}
System.out.println("Sum = " + sum);
```

**D.** Write a program to define a class called TemperatureCheck with the following
specifications: **[7.5 marks]**
  i. Data field (state): double temperature.
  ii. A constructor method to *set* the temperature
  iii. A method called evaluateTemperature() that *uses* if-else statements to output:
       a. "Too Cold" if temperature < 15
       b. "Normal" if the temperature is between 15 and 30 (inclusive)
       c. "Too Hot" if temperature > 30.
  iv. In your main method, *prompt* the user to enter a temperature value, *create* an
      object of the class, and *display* the evaluation result. Use JOptionPane to accept
      inputs.

---

## Question Five (17.5 Marks)

**A.** Describe the following statements: Inheritance, Polymorphism, and Method
Overriding. **[3 marks]**

**B.** *Write* a method called countNegatives that accepts a single-dimensional array of
integers and returns the number of negative values in the array. You do not need to write
the full class or main method, just the method definition. **[3 marks]**

**C.** Identify the errors in this code snippet and state the final output after
correction. **[4 marks]**

```java
public class Main {
    public static void main(String[] args) {
        int nums = {10, 20, 30};
        System.out.println("Middle value is: " + nums[3]);
        int sum = 0;
        for(int i = 0; i <= nums.length; i) {
            sum += nums[i];
        }
        System.out.println("Sum is: " + );
    }
}
```

**D.** Write a program using inheritance and method overriding as follows: **[7.5 marks]**
  i. *Create* a superclass called Vehicle with the following:
     a. An instance variable speed (int)
     b. A constructor that initialises speed
     c. A method displayInfo() that *prints* "Vehicle speed: <speed> km/h"
  ii. *Create* a subclass called Bicycle that *overrides* the displayInfo() method to
      print: "Bicycle speed: <speed> km/h. This is an eco-friendly ride."
  iii. In the main method:
       a. *Create* an object of class Vehicle with a speed of 80
       b. *Create* an object of class Bicycle with a speed of 25
       c. *Call* displayInfo() on both objects to demonstrate polymorphism.

---

## Question Six (17.5 Marks)

**A.** Write a code snippet to demonstrate the following loop types: **[3 marks]**
  i. A for loop that prints numbers 1 to 5
  ii. A while loop that prints numbers from 5 to 1
  iii. A do-while loop that prints only the number 10 once.

**B.** What will be the return value of compute(13)? Show the steps to explain your
answer. **[3 marks]**

```java
public static int compute(int x) {
    int count = 0;
    while (x > 0) {
        if (x % 2 == 1) count++;
        x = x / 2;
    }
    return count;
}
```

**C.** Debug this code snippet. List the errors and state the correct output.
**[4 marks]**

```java
public class EvenFinder {
    public static void main(String args) {
        printEven(10.0)
    }

    public static void printEven(int) {
        for (int i = 0; i <= n; i++);
            if (i % 2 == 0)
                System.out.print(i + " ");
    }
}
```

**D.** Write a program that includes a method called hasEqualAdjacentPairs(int n) which:
**[7.5 marks]**
  i. *Returns* true if the number n (a positive integer) contains at least two pairs of
     equal adjacent digits.
  ii. *Returns* false otherwise.
  iii. You must:
       a. *Write* the method hasEqualAdjacentPairs(int n)
       b. *Write* the main() method to *test* at least two cases

  Example
  - 112233 - true (pairs: 11, 22, 33). More than two adjacent pairs.
  - 1223 - true (pairs: 22). Only one pair - return false

  > **Defect in the paper, transcribed as printed.** The second bullet says "true"
  > and then "return false" in the same line. Given the spec ("at least two pairs")
  > and the worked meaning, 1223 has only one pair and the correct return is
  > **false**; the leading "true" is a slip. The manual must show what the paper says
  > and what is true, never silently correct it.
