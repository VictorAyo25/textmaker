# Source survey: 13 decks vs the course manual

Read from the decks' own title slides and the course manual's table of contents, not
from filenames.

## Alignment: exact, one-to-one, in order

| # | Deck | Slides | Course manual unit |
|---|------|--------|--------------------|
| 1 | M1 U1 Overview of Computer Programming | 20 | Module One, Unit 1 |
| 2 | M2 U1 Introduction to Java and Java Development Environment | 16 | Module Two, Unit 1 |
| 3 | M3 U1 Java Basics: Data Types, Variables and Operators Part I | 39 | Module Three, Unit 1 |
| 4 | M3 U2 Java Basics: Data Types, Variables and Operators Part II | 27 | Module Three, Unit 2 |
| 5 | M4 U1 Conditional Statements and Decision Making | 30 | Module Four, Unit 1 |
| 6 | M4 U2 Loops and Branching | 30 | Module Four, Unit 2 |
| 7 | M5 U1 Methods and Parameter Passing | 45 | Module Five, Unit 1 |
| 8 | M6 U1 Object-Oriented Programming Part I | 45 | Module Six, Unit 1 |
| 9 | M6 U2 Object-Oriented Programming Part II | 38 | Module Six, Unit 2 |
| 10 | M7 U1 Strings and String Processing | 24 | Module Seven, Unit 1 |
| 11 | M8 U1 Arrays and Arrays Manipulation | 25 | Module Eight, Unit 1 |
| 12 | M9 U1 Introduction to Recursion | 30 | Module Nine, Unit 1 |
| 13 | M10 U1 Exception Handling and File I/O | 39 | Module Ten, Unit 1 |
|   | **Total** | **408** | |

**No numbering quirk.** Unlike PHY121 (where the lecturer's "Module 6" was the manual's
Module 5), deck numbering here matches the course manual exactly. The manual keeps
Modules 1 to 10 as the lecturer numbers them.

## Title drifts (deck vs course manual)

Minor, but record them so the manual does not repeat a typo:

| Deck says | Course manual says | Take |
|---|---|---|
| Data Types, Variables and **Operators** | ... and **Operations** | "Operators" is the real topic (`+`, `%`, `&&`). Deck wins. |
| Methods and Parameter **Passing** | Methods and Parameter **Testing** | "Parameter passing" is the actual concept. The manual's "Testing" looks like a slip. Deck wins. |
| **Strings and String Processing** | **Data Structures** and String Handling | Deck wins; the unit is strings, not data structures generally. |

The course manual's own TOC also contains a broken cross-reference
("Unit 2 - Loops and Branches ..... Error! Bookmark not defined."), which is a good
reminder that this source is not authoritative and must be checked against the decks.

## The teaching-order problem (a real decision, not a detail)

The lecturer's module order is **not** a valid teach-from-zero order:

- **Arrays are Module 8**, but the exam's Section A questions (both of them) are array
  problems, and the array is the natural vehicle for teaching loops in Module 4.
- **OOP is Module 6 and Strings Module 7**, both before arrays.
- **JOptionPane** is demanded for I/O from Section B onward, but it is an object method
  call on a library class, which a true novice cannot understand before Module 6.

Under the zero-external-sources rule, nothing may be used before it is taught, so this
has to be resolved deliberately rather than drifted into. The options:

1. **Keep the lecturer's module numbers** (so the manual maps onto the course and the
   exam) and let the **Foundations part** carry any concept a module needs early,
   introducing it properly there with a forward reference to its home module. This is
   what PHY121 did with its Foundations part.
2. Reorder the modules pedagogically. Rejected: it breaks the mapping to the course,
   the decks, and the reader's mental model of "Module 8 is arrays".

**Decision: option 1.** Modules stay numbered as the lecturer numbers them. Foundations
teaches, from zero and in the right order, whatever the early modules need: what a
program is, what a compiler is, variables, types, and a first honest introduction to
arrays and to the JOptionPane pattern. Each such box states plainly where the idea is
developed in full ("you will meet this properly in Module 8"). Module 8 then does not
repeat Foundations; it deepens it.

The JOptionPane tension specifically: teach it in Foundations as an explicit
copy-this-pattern box, honest that `JOptionPane.showMessageDialog(null, x)` is a method
call on a class from a library and that both words are fully explained in Module 6.
Never pretend it is magic, and never use it unexplained.
