# Manual Map C — DTS 224 Data Management I

Source: `map_chunkC_mod5_ans.txt` (PDF pages 123-182).
Covers **Module Five** (Unit 1 Relational Algebra; Unit 2 SQL + Query Processing/Optimisation) and the **Answers to Self-Assessment Questions** (Modules One to Five).

Module Five title page: PDF p.123 — "Module Five: Relational Theory and Query Languages".

---

# MODULE FIVE — Unit 1: Relational Algebra

**PDF page range:** 124-132 (Unit opener p.124; References p.132).

## 1. Learning Outcomes
At the end of this unit you should be able to:
- Understand the purpose and structure of the relational model in database systems.
- Identify the components of a relation, including attributes, tuples, and keys.
- Explain the basic principles of relational algebra as a query language.
- Apply key relational algebra operations such as selection, projection, union, and join.
- Use relational algebra to express and solve database queries.

## 2. Key Concepts / Terms Taught (in order)

**5.1.1 Relational Model (p.125)**
- Relational Model (RM) — primary data model for commercial data-processing.
- A collection of tables, each with a unique name.
- **relation** = table; **tuple** = row; **attribute** = column.
- Course table example: attributes course ID, title, department name, credits.

**5.1.2 Relational Algebra (p.125-131)**
- Definition: a set of operations taking one or two relations as input, producing a new relation.
- **Unary** operations: select, project, rename.
- **Binary** operations: union, Cartesian product, set difference.
- Described as a functional query language forming the theoretical basis of SQL.

Operations the manual actually defines, with symbols **as printed**:
1. **Select** — selects tuples (rows) satisfying a predicate. Symbol: **σ** (printed as `σsalary<50000 (instructor)`, p.127).
2. **Project** — unary; returns argument relation with some attributes left out; "works on attributes." Symbol: none printed in Unit 1 body (the answers section later prints **π**, e.g. `πcourseid, credits`).
3. **Cartesian-Product** — combines information from any two relations; steps: combine all attributes, multiply tuples forming all outcomes, represent each as a single tuple. Symbol: cross **×** (p.128). Needs relation-name qualification of attributes (e.g. `instructor.ID`).
4. **Assignment** — works like a programming assignment operator; assigns query parts to temporary relation variables for reuse; evaluation displays no relation. Symbol: **←** (p.130).
5. **Join** — combines a selection and a Cartesian product into one operation. Most common type = **Natural Join** (joins on equality of same-named attributes, duplicate attribute eliminated). Notation partly garbled in text (`nd S is`); answers section prints **⋈** for JOIN.

> Note on coverage: The learning outcomes name **union** (and the intro names **set difference**), but the Unit 1 body only fully develops Select, Project, Cartesian-Product, Assignment, and Join. Union, set difference, division, aggregation, and rename are named but NOT worked as separate defined operations in this chunk (rename mentioned only as a unary example).

## 3. Worked / Illustrative Examples
- **Select example** (p.126-127): instructor relation (Table 5.2; attributes lecturerID, lecturerName, lecturerDept, lecturerSalary) — find all lecturers with salary below 50,000: `σsalary<50000 (instructor)`.
- **Cartesian-Product example** (p.128-129): instructor × teaches, producing the combined schema (instructor.ID, instructor.name, instructor.deptname, instructor.salary, teaches.ID, teaches.courseid, teaches.secid, teaches.semester, teaches.year).
- (Select/Project also illustrated conceptually via the "CU course registration relation".)

## 4. Figures / Diagrams / Tables (with page)
- **Table 5.1** Course Table — p.125.
- **Table 5.2** Instructor relation — p.126.
- **Table 5.3** Teaches relation — p.129.
- **Table 5.4** Instructor × teaches relation schema — p.129.
- (No numbered Figures in Unit 1.)

## 5. VERBATIM — Self-Assessment Questions, Activities, In-text Exercises

**M5U1-QC1 — Quick Classwork (p.127):**
> 1. Write a select statement to find all courses taken by the Computer Science department
> 2. Write a select statement to find all instructors with a salary greater than 50,000 but less than 70,000.

**M5U1-QC2 — Quick Classwork (p.128):**
> 1. Write a projection statement to find the course codes and their corresponding units

**M5U1-SA1 — Self-Assessment Question (p.131):**
> 1. Explain how the select and project operations in relational algebra work, and provide an example of each.

**M5U1-SA2 — Self-Assessment Question (p.131):**
> 2. What is the purpose of the Cartesian product and join operations, and how do they differ in terms of output and use cases?

**M5U1-TMA1 — Tutor-Marked Assignment (p.131-132):**
> Create your own relation and perform the following RA operations on it:
> - Select Operation
> - Projection Operation
> - Cartesian-Product Operation

---

# MODULE FIVE — Unit 2: Introduction to Structured Query Language (SQL) and Introduction to Query Processing and Optimisation

**PDF page range:** 133-168 (Unit opener p.133; References p.166; "Extra" SQL Server data types p.166-168).

## 1. Learning Outcomes
At the end of this unit you should be able to:
- Understand DDL commands and use the CREATE, ALTER and DROP commands efficiently.
- Manipulate a given database practically using DML commands such as SELECT.

## 2. Key Concepts / Terms Taught (in order)

**5.2.1 DDL, DML, DCL and the database development process (p.134)** — three sub-languages introduced (Figure 5.1).

**5.2.2 Database creation in MySQL (p.134):**
- `CREATE DATABASE databasename;`
- `SHOW DATABASES;`
- `USE nameofdatabase;`

**5.2.3 Datatypes in MySQL (p.134-135):** ISO SQL data types (Figure 5.2). Relational-model term mapping: Table = Relation, Row = Tuple, Column = Attribute.

**5.2.4 Data Definition Language (DDL) (p.135-144):**
- CREATE statement — creates schemas, tables, domains, plus views, indexes, assertions, triggers.
- Main SQL DDL: `CREATE SCHEMA` / `DROP SCHEMA`; `CREATE/ALTER DOMAIN` / `DROP DOMAIN`; `CREATE/ALTER TABLE` / `DROP TABLE`; `CREATE VIEW` / `DROP VIEW`; `CREATE INDEX` / `DROP INDEX`.
- Environment terms: DBMS, Catalog (named collection of schemas), Schema, Domain; objects in a schema (Tables, Views, Domains, assertions) share one owner.
- CREATE SCHEMA: `CREATE SCHEMA Name_of_Schema;`; `DROP SCHEMA Name_of_schema [RESTRICT | CASCADE];` — Example: `CREATE SCHEMA COMPANY;`.
- CREATE TABLE — columns with datatypes; `NOT NULL`; `DEFAULT` value; primary keys NOT NULL; `FOREIGN KEY` clause with referential action.
- RENAME TABLE: `RENAME TABLE Old_Table_Name to New_Table_Name;` (example EMPLOYEE → WORKER).
- DROP TABLE: `DROP TABLE table_name;`.
- ALTER TABLE — add column: `ALTER TABLE table_name ADD name_of_newColumn DATATYPE(size);`.
- ALTER TABLE — modify datatype: `ALTER TABLE table_name MODIFY COLUMN column_name DATATYPE(size);`.
- ALTER TABLE — reposition column: `... MODIFY column_name DATATYPE(size) AFTER target_column;` and `... MODIFY COLUMN ssn char(9) FIRST;`.
- ALTER TABLE — drop column: `ALTER TABLE table_name DROP COLUMN name;`.
- **Constraints:** UNIQUE (`ADD CONSTRAINT UNIQUE(attribute)`), NOT NULL (via MODIFY), CHECK (allowable values; `ADD CONSTRAINT constraint_name CHECK(logical condition)`), DEFAULT (default column value), TIMESTAMP/default Now() (8-byte date-time YYYY-MM-DD HH:MM:SS), AUTO_INCREMENT (key attributes only), FOREIGN KEY (base table + child table; `ADD CONSTRAINT ... FOREIGN KEY (attr) REFERENCES basetable(attr)`; `DROP FOREIGN KEY name`).

**5.2.5 Data Manipulation Language (DML) (p.145-147):**
- INSERT: `INSERT into table_name VALUES (...);`.
- UPDATE: `UPDATE table_name SET column = newValue WHERE identifier = value;`.
- **JOIN** clause — combines rows from two+ tables on a related column. Types: **Inner join, Left join, Right join** (each worked on customer/transaction tables).
- DML goals: access and manipulate data, efficient human interaction, query language.

**5.2.6 Writing SQL commands (p.147):** reserved vs user-defined words; case-insensitivity (except literal character data); indentation/lineation rules.

**5.2.7 Literals (p.147):** constants; non-numeric in single quotes; numeric without quotes.

**SELECT statement (p.148-149):**
- All columns/all rows; `*` abbreviation.
- Specific columns/all rows.
- **DISTINCT** to eliminate duplicates.

**SELECT — Aggregates (p.148):** five ISO aggregate functions — **COUNT, SUM, AVG, MIN, MAX**; `COUNT(*)` counts all rows incl. nulls/duplicates; DISTINCT before column; DISTINCT has no effect with MIN/MAX but may with SUM/AVG.

**SELECT — Grouping (p.152):** `GROUP BY` for sub-totals; SELECT list may contain only column names, aggregate functions, constants, expressions; WHERE applied before grouping; `ORDER BY`.

**Restricted groupings — HAVING (p.153):** filters groups (vs WHERE which filters rows); HAVING columns must be in GROUP BY or an aggregate.

**Subqueries (p.153-156):** subselect in WHERE/HAVING (subquery/nested query); also in INSERT/UPDATE/DELETE. Subquery rules: no ORDER BY in subquery; single column/expression except with EXISTS; subquery on right-hand side of comparison. Uses shown: equality subquery, aggregate subquery, nested subquery with **IN**.

**Views (p.156):** `CREATE VIEW` — Horizontal view (row-restricted, WHERE) and Vertical view (column-restricted).

**5.2.8 More practice on SQL queries (p.155-160):** based on the DreamHome rental database (Table 5.19). Predicates/operators: calculated fields with `AS`, comparison (`>`), compound comparison (`OR`), range (`BETWEEN ... AND`, `NOT BETWEEN`), set membership (`IN`, `NOT IN`), pattern matching (`LIKE`, `%` wildcard).

**5.2.12 Extra (p.166-168):** SQL Server data types — String, Number, Date data types.

> Query Processing and Optimisation: named in the unit title, but this chunk contains **no substantive query-processing/optimisation content or terms** (no cost estimation, no query trees, no heuristics discussed). Effectively unaddressed in the text.

## 3. Worked / Illustrative Examples (topic + schema)
- CREATE SCHEMA COMPANY (p.135).
- CREATE/RENAME/DROP/ALTER TABLE — EMPLOYEE / WORKER table (p.136-139).
- DEFAULT constraint — SKILL table (skill_Id, ssn, Skill_Type default "Coding", Number_of_Skill) (p.140).
- INSERT with DEFAULT — Skill table (p.140).
- TIMESTAMP default Now() — transaction table (p.141).
- AUTO_INCREMENT — customer table (customer_Id PK, Fname, Lname, Address) (p.142-143).
- FOREIGN KEY — transaction table referencing customer_ID (p.143-144).
- INNER / LEFT / RIGHT JOIN — customer & transaction tables (p.145-147).
- SELECT all/specific columns, DISTINCT — customers table (customer_Id, Fname, Lname, Address) (p.148-149).
- COUNT(*) — PropertyForRent, rent > 350 (p.150).
- COUNT(DISTINCT) — Viewing, viewDate in May '04 (p.150-151).
- COUNT + SUM — Staff, position = 'Manager' (p.151).
- MIN/MAX/AVG — Staff salary (p.151).
- GROUP BY — Staff per branchNo (count + sum salaries) (p.152).
- HAVING — branches with >1 staff (p.153).
- Subquery equality — staff at '163 Main St' (Staff/Branch) (p.153-154).
- Subquery aggregate — staff salary > average (Staff) (p.154).
- Nested subquery IN — properties handled by staff at '163 Main St' (PropertyForRent/Staff/Branch) (p.155).
- Horizontal view Manager3Staff; Vertical view Staff3 — Staff, branchNo B003 (p.156).
- DreamHome practice: calculated field (monthly salary), comparison, compound comparison (London/Glasgow), range (BETWEEN 20000-30000), set membership (Manager/Supervisor), pattern matching (LIKE '%Glasgow%') — Staff/Branch/PrivateOwner (p.157-160).

## 4. Figures / Diagrams / Tables (with page)
- **Figure 5.1** DDL, DML, DCL and the database development process — p.134.
- **Figure 5.2** ISO SQL Data Types — p.134.
- **Table 5.5** Alter Table, repositioning SSN — p.137.
- **Table 5.6** Modified Table, repositioning SSN as first attribute — p.138.
- **Table 5.7** Dropping column — p.138.
- **Table 5.8** Dropped column Dno — p.139.
- **Table 5.9** Transaction Table showing default Timestamp — p.141.
- **Table 5.10** Result of Auto_Increment constraint query — p.143.
- **Table 5.11** Result of foreign key constraint query — p.144.
- **Table 5.12** Primary-foreign key relationship — p.144.
- **Table 5.13** Inner Join — p.145/146.
- **Table 5.14** Left Join — p.146.
- **Table 5.15** Right Join — p.147.
- **Table 5.16** All columns and all rows from customers — p.148.
- **Table 5.17** Specific column and all rows from customers — p.149.
- **Table 5.18a** Use of distinct — p.149.
- **Table 5.18b** Use of distinct — p.150.
- **Table 5.19** Instance of the DreamHome rental database — p.155.
- (Unnumbered figures p.166-168: SQL Server String / Number / Date data type tables.)

## 5. VERBATIM — Self-Assessment Questions, Activities, In-text Exercises

**M5U2-QT1 — Quick Task for You (p.137):**
> Add a new column /attribute to the WORKER TABLE.
> New attribute should be named email with datatype VARCHAR(50).

**M5U2-QT2 — Quick Task for You (p.137):**
> Modify the datatype of the column email from VARCHAR(50) TO VARCHAR(100).

**M5U2-QE1 — Quick Exercise (p.141):**
> 1. Insert a row into the skill table with the value of ssn as 3:
> a) query the table skill to display its content
> b) Apply the unique constraint on the column ssn (state your observation)
> c) delete the record where the skill_Id is 010 and repeat the step in (b)
> d) Try to insert a new record with ssn value of 3 again and interpret the outcome.

**M5U2-CA2 — Class Activity 2 (Database Tables) (5.2.9, p.160-164):** (12 questions)
> 1. Which products have a standard price of less than 275?
> 2. What is the address of the customer named Home Furnishings? Use an alias NAME for the customer.
> 3. List the unit price, product name and product ID for all products in the product table.
> 4. What is the average standard price for the product in inventory?
> 5. How many different items were ordered on order number 1004
> 6. Which orders have been placed since 10/24/2006
> 7. What furniture does Pine Valley carry that isn't made of cherry?
> 8. List products, finish, and unit price for all desks and all tables that cost more than 300 in the PRODUCT view.
> 9. Which products in the PRODUCT view have a standard price between 200 and 300?
> 10. Count the number of customers with an address in each state to which we ship
> 11. Find only states with more than one customer
> 12. List the product finish and average standard price for cherry, natural ash, natural maple and white ash, where the average standard price is less than 750.

**M5U2-EX1 — Exercises (5.2.10, p.164-165):**
> Write a database description for each of the relations given. Assume the following attribute data types.
> - StudentID(integer, primary key)
> - StudentName(25 characters)
> - FacultyID(integer, primary key)
> - FacultyName(25 characters)
> - CourseID(8 characters, primary key)
> - CourseName(15 characters)
> - DateQualified(date)
> - SectionNo(integer, primary key)
> - Semester(7 characters)

> Note: Unit 2 has **no "Self-Assessment Questions" heading** of its own in this chunk (its SA answers appear in Module Five answers, which actually re-answer Unit 1's two questions — see below). The graded/practice items are the Quick Tasks, Quick Exercise, Class Activity 2, and Exercises above.

---

# ANSWERS TO SELF-ASSESSMENT QUESTIONS (PDF p.169-182)

> Caution: answers transcribed as printed; not independently verified. Several question numbers are duplicated or headings mislabeled in the source (flagged below).

## Module One
**Unit 1 (6.1.1, p.168) — answers to Q1, Q2:**
- Q1 (purpose of indexing): indexing creates lookup structures (B-trees, hash indexes) to speed queries by avoiding full scans.
- Q2 (data privacy vs integrity vs security): privacy = protect sensitive data from unauthorised access (access control, anonymisation, GDPR/HIPAA); integrity = accuracy/consistency (constraints NOT NULL/UNIQUE/CHECK, referential integrity, ACID); security = protection against unauthorised access/tampering (authentication, encryption, firewalls, backups, recovery).

**Unit 2 (6.1.2, p.169-173) — answers to Q1-Q6 (with a duplicated Q6):**
- Q1 (define database + 3 components): database = organised shared collection of logically related data; components = tables/relations, metadata/system catalogue, application programs.
- Q2 (data abstraction + 3 levels): hiding representation complexity; levels = External (highest, tables/rows), Logical/Conceptual, Physical (lowest, hardware storage).
- Q3 (physical vs logical data independence): physical = change physical schema without affecting apps (sequential file → B+ tree); logical = change logical schema without affecting external schema/apps (add 'skills' column doesn't affect name/age views).
- Q4 (primary functions of DBMS): define structures (DDL), manipulate data (DML), manage storage/access paths, control concurrency, enforce integrity, ensure security/recovery.
- Q5 (two types of DB systems + use cases): Personal (single user/app, few tables, one computer — expense tracker); Enterprise-level (many users/apps, complex — company ERP).
- Q6 (role of DBA + 3 responsibilities): DBA has central control; schema definition/modification (DDL), granting authorisation, specifying integrity constraints. **[Duplicate Q6]** second Q6 (purpose of DML + four operations): DML enables accessing/manipulating data; operations = retrieval, insertion, deletion, modification. *(Note: the manual prints this second item also as "Q6" — likely a numbering error for Q7.)*

## Module Two
**Unit 1 (6.2.1, p.171-173) — answers to Q1, Q2, Q3:**
- Q1 (data modelling vs conceptual modelling): yes different; data modelling is broad (defining/analysing data requirements, incl. conceptual/logical/physical), conceptual modelling is the initial high-level phase using ERDs (entities/attributes/relationships, no physical concern).
- Q2 (what determines how data are handled): business rules, data-modelling decisions, system design; models represent org rules; ER diagrams reflect real-world logic (cardinality, constraints, integrity).
- Q3 (relationship instance vs associative entity): both represent associations and model M:N; relationship instance = a specific occurrence (EMPLOYEE completing a COURSE); associative entity = entity representing an M:N relationship with its own attributes (CERTIFICATE with DateCompleted).

**Unit 2 (6.2.2, p.174-175) — answers to Q1, Q2, Q3:**
- Q1 (two most important supertype/subtype constraints): completeness and disjointness constraints.
- Q2 (partial vs total specialisation rule): partial = a supertype instance need not belong to any subtype; total = each supertype instance must be a member of some subtype.
- Q3 (mental models for supertype/subtype): generalization and specialization.

**Unit 3 (6.2.3, p.175-176) — answers to Q1, Q2:**
- Q1 (is XML the same as HTML): no; XML describes/stores data (custom tags, structure/meaning, data transport); HTML displays data (predefined tags, presentation). *(Source has a stray fragment "What mass will remain after 10 hours?" — OCR bleed, ignore.)*
- Q2 (semi-structured data types): flexible schema (wide/sparse columns), multivalued types (sets/arrays), nested types (JSON/XML hierarchies); non-tabular, hierarchical, self-describing.

## Module Three
**Unit 1 (6.3.1, p.176-177) — answers to Q1, Q2:**
- Q1 (purpose of relational keys): ensure consistency/uniqueness; primary key (unique row identifier), composite key (multi-attribute PK), foreign key (PK of another relation); maintain connections, prevent duplicates.
- Q2 (integrity constraints): domain constraint (permissible values), entity integrity (PK not null), referential integrity (FK matches PK or null).

**Unit 2 (6.3.2, p.177-179) — answers to Q1-Q7:**
- Q1 (conceptual vs logical model): conceptual = high-level ER/EER, no storage concern; logical = translate to relational tables with PKs/FKs/constraints.
- Q2 (regular entity with composite attribute): include only the simple components as columns (Address → Street, City, State).
- Q3 (multivalued attributes): two relations — one without the multivalued attribute, one with it plus PK of first as FK; combination forms composite PK.
- Q4 (surrogate key purpose): system-generated unique identifier simplifying PKs when natural keys are long/composite; improves efficiency, reduces complexity in M:N/ternary.
- Q5 (transforming binary M:N): create new relation; include both entities' PKs as FKs forming composite PK; add relationship attributes.
- Q6 (unary one-to-many): add a recursive FK referencing the relation's own PK.
- Q7 (supertype/subtype transformation): supertype relation with common attributes + PK; each subtype relation with supertype PK (as PK+FK) plus subtype-specific attributes; optional discriminator attribute.

## Module Four
**Unit 1 (6.4.1, p.177-178) — answers to Q1, Q2, Q2 (duplicated):**
- Q1 (what is normalisation + importance): decomposing anomaly-prone relations into well-structured ones; reduces redundancy, eliminates update/insertion/deletion anomalies, aids referential integrity.
- Q2 (1NF vs 3NF): 1NF = no repeating groups, atomic values, PK identifies each row; 3NF = already in 2NF and no transitive dependencies (non-key attributes depend only on PK).
- **[Duplicate Q2]** (functional dependency + use in normalisation): FD is a constraint where A uniquely determines B (A → B); FDs underpin normal forms and help detect/eliminate partial and transitive dependencies. *(Manual prints this second item also as "Q2" — likely a numbering error for Q3.)*

## Module Five
**Unit 1 (6.5.1, p.178-179) — answers to Q1, Q2:**
- *(Heading text mislabeled: printed as "Explain the concept of functional dependency..." but the answer body actually answers M5U1-SA1 on select/project.)*
- Q1 (select and project): select (σ) retrieves rows satisfying a predicate — `σsalary < 50000 (instructor)`; project (π) retrieves specific columns — `πcourseid, credits (course)`; select filters rows, project filters columns.
- Q2 (Cartesian product vs join): Cartesian product (×) combines every tuple with every tuple (all combinations, precursor to join); JOIN (⋈) combines related tuples on a common attribute/condition, natural join merges same-named attributes and eliminates duplicate columns; differences in output size/relevance and use case.
- *(No printed answers for any Module Five Unit 2 items — Class Activity 2, Exercises, Quick Tasks/Exercise are unanswered at the back.)*

---

# REPORT SUMMARY

**Units covered:** Module Five Unit 1 (Relational Algebra, p.124-132) and Module Five Unit 2 (SQL + Query Processing/Optimisation, p.133-168); plus the Answers section (p.169-182).

**Self-assessment / activity / exercise count (11 items, all IDs):**
- M5U1-QC1 (Quick Classwork, 2 parts), M5U1-QC2 (Quick Classwork, 1 part), M5U1-SA1, M5U1-SA2, M5U1-TMA1 (Tutor-Marked Assignment, 3 tasks).
- M5U2-QT1, M5U2-QT2 (Quick Tasks), M5U2-QE1 (Quick Exercise, 4 sub-parts a-d), M5U2-CA2 (Class Activity 2, 12 questions), M5U2-EX1 (Exercises).

**Total figures:** 2 numbered Figures (5.1, 5.2). **Total numbered Tables:** 19 (5.1-5.19, counting 5.18a & 5.18b as two = 20 table objects). Plus 3 unnumbered SQL Server data-type tables (p.166-168).

**Relational-algebra operations list (as defined in Unit 1):** Select (σ), Project (π — symbol printed only in answers), Cartesian-Product (×), Assignment (←), Join / Natural Join (⋈ — printed in answers). Named but NOT worked as separate defined operations: union, set difference (named in intro/outcomes), rename (named as unary example). No division or aggregation in relational-algebra form.

**SQL features list (Unit 2):** DDL — CREATE DATABASE, SHOW DATABASES, USE, CREATE/DROP SCHEMA, CREATE/ALTER/DROP DOMAIN, CREATE/ALTER/DROP TABLE, CREATE/DROP VIEW, CREATE/DROP INDEX, RENAME TABLE; constraints NOT NULL, DEFAULT, PRIMARY KEY, FOREIGN KEY (+ADD/DROP), UNIQUE, CHECK, AUTO_INCREMENT, TIMESTAMP/Now(). DML — INSERT, UPDATE, (DELETE mentioned re subqueries), SELECT with `*`/specific columns, DISTINCT, WHERE, GROUP BY, HAVING, ORDER BY; JOINs (INNER, LEFT, RIGHT; natural join in RA); aggregates COUNT/SUM/AVG/MIN/MAX (+ COUNT(*), COUNT(DISTINCT)); operators/predicates AS (alias/calculated fields), comparison, AND/OR, BETWEEN/NOT BETWEEN, IN/NOT IN, LIKE (% wildcard); subqueries/nested queries (equality, aggregate, IN, EXISTS rule); views (horizontal/vertical). Query Processing & Optimisation: named in the title but **no actual content** in this chunk.

**Which units have answers provided at the back:** Module One U1 (Q1-Q2) & U2 (Q1-Q6 w/ duplicate Q6); Module Two U1 (Q1-Q3), U2 (Q1-Q3), U3 (Q1-Q2); Module Three U1 (Q1-Q2), U2 (Q1-Q7); Module Four U1 (Q1, Q2, duplicate Q2); Module Five U1 (Q1-Q2). **No answers** for Module Five Unit 2 or for any Modules One-Four units beyond those listed (e.g., Module Three has no Unit 3+ answers, Module Four only Unit 1).

**Data-quality flags:** duplicated Q6 (M1U2) and Q2 (M4U1) numbering; Module Five answer heading mislabeled; OCR bleed fragments ("What mass will remain after 10 hours?", garbled join notation on p.131); answers are as-printed and not independently verified.
