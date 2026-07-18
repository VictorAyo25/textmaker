# DTS224 Data Management I — Manual Map B (Modules Three & Four, PDF pp. 72-122)

Source extract: `map_chunkB_mod34.txt`. Page markers refer to the PDF page numbers embedded in the extract.

Covers:
- Module Three (Logical Design): Unit 1 Introduction to Relational Model; Unit 2 Transforming Conceptual to Logical Design.
- Module Four (Functional Dependencies): Unit 1 Normalisation.

---

## MODULE THREE — Logical Design (cover PDF p.72)

---

### M3U1 — Introduction to Relational Model (PDF pp. 73-84)

**1. Unit title + range:** Module Three, Unit 1 — Introduction to Relational Model. PDF pp. 73-84.

**2. Learning outcomes (as printed — NOTE MISMATCH):**
The printed outcomes are copy-paste errors from a set-theory unit; they do NOT match the relational-model content. As printed:
- Define/identify types of sets (empty, singleton, finite, infinite, equal, equivalent).
- Apply set notation and membership (∈, ∉, ⊆, ⊂, P(A)).
- Perform set operations (union, intersection, difference, symmetric difference, complement) with Venn diagrams.
- Describe relationships between sets; determine subset, proper subset, disjoint conditions.
> FLAG: These outcomes are wrong for this unit. The actual taught content is: database design specifications, the relational data model, relational keys, integrity constraints, multivalued attribute removal, well-structured vs not-well-structured relations, anomalies. When redrawing/rewriting, the real intended outcomes should reflect the relational model.

**3. KEY CONCEPTS / terms (in order):**
- **Database design** (3.1.1) — transforming analysis requirements into specifications guiding implementation.
- **Logical specifications** — map conceptual requirements into the data model of a specific DBMS.
- **Physical specifications** — parameters for data storage, input to implementation; database defined using a DDL.
- **Logical database design** — process of transforming a conceptual data model into a logical data model consistent/compatible with a specific database technology.
- **Relational Data Model** (3.1.2) — introduced by E. F. Codd ~1970s. History: System R (IBM San Jose, late 1970s prototype RDBMS); Ingres (UC Berkeley, academic RDBMS); commercial RDBMS ~1980. Represents data as tables; based on mathematical theory.
- **Three components of relational model** — (a) Data structure (tables, rows/columns); (b) Data manipulation (operations, typically SQL); (c) Data integrity (business rules maintaining integrity). [EXAM-RELEVANT — asked in TMA]
- **Relation** — a named, two-dimensional table of data; set of named columns + arbitrary number of unnamed rows.
- **Attribute** — a named column of a relation.
- **Row/record** — corresponds to a record with attribute values for a single entity.
- **Shorthand notation** — relation name followed by attribute names in parentheses, e.g. EMPLOYEE1(EmpID, Name, DeptName, Salary).
- **Primary key** — attribute or combination of attributes that uniquely identifies each row; designated by underlining. E.g. EmpID for EMPLOYEE1.
- **Composite key** — primary key consisting of more than one attribute; e.g. DEPENDENT primary key = EmpID + DependentName.
- **Foreign key** — an attribute in a relation that serves as the primary key of another relation in the same database. E.g. DeptName is FK in EMPLOYEE1 referencing DEPARTMENT. [EXAM-RELEVANT definition]
- **Six Properties of a Relation** — (1) unique relation name; (2) each intersection entry is atomic/single-valued; (3) each row unique; (4) each attribute name unique; (5) column sequence insignificant; (6) row sequence insignificant. [EXAM-RELEVANT — the "six properties" are referenced again in Module Four]
- **Removing Multivalued Attributes** — CourseTitle and DateCompleted are multivalued (EmpID 100 has two courses SPSS & Surveys, dates 6/9/2015 & 10/7/2015); EmpID then no longer uniquely identifies rows; if no course taken, values are null (EmpID 190 example).
- **Schema** — description of the overall logical structure of the database.
- **Methods for expressing a schema** — (a) short text statements (relation named, attributes in parentheses); (b) graphical representation (rectangle per relation containing attributes). Text = simple; graphical = better for referential integrity constraints. [EXAM-RELEVANT — asked in TMA]
- **Integrity Constraint** (3.1.3) — rules limiting acceptable values/actions to maintain accuracy/integrity. Three major types: domain constraints, entity integrity, referential integrity.
- **Domain constraint** — a domain is the set of values assignable to an attribute; definition = domain name, meaning, data type, size/length, allowable values/range; all values in a column come from the same domain.
- **Entity integrity** — ensures every relation has a primary key and its values are valid; guarantees every primary key attribute is non-null.
- **Referential integrity constraint** — rule maintaining consistency between rows of two relations: an FK value must match a PK value in another relation OR be null. [EXAM-RELEVANT definition]
- **Null constraint / Null** — a value assigned when no other value applies or is unknown; not actually a value but the absence of one; not equal to zero or blanks; controversial (can give anomalous results).
- **Well-Structured Relation** (3.1.4) — contains minimal redundancy; allows insert/modify/delete without errors/inconsistencies. Example EMPLOYEE1 (Fig 3.7).
- **NOT-Well-Structured Relation** (3.1.5) — EMPLOYEE2 (Fig 3.8) has considerable redundancy (EmpID, Name, DeptName, Salary repeated for employees 100, 110, 150).
- **Anomaly** (3.1.6) — error/inconsistency when updating a table with redundant data. Three types: insertion, deletion, modification.
  - **Insertion anomaly** — cannot add employee without also supplying CourseTitle (PK = EmpID + CourseTitle; PK values cannot be null).
  - **Deletion anomaly** — deleting employee 140 loses the info that a course (Tax Acc, 12/8/2015) existed.
  - **Modification anomaly** — salary increase for employee 100 must be recorded in each of that employee's rows (two occurrences).

**4. WORKED / illustrative EXAMPLES:**
- EMPLOYEE1 relation — introduces attributes, PK, shorthand notation, FK (DeptName → DEPARTMENT).
- DEPENDENT — composite key example (EmpID + DependentName).
- Pine Valley Furniture schema — four relations CUSTOMER, ORDER, ORDERLINE, PRODUCT; ORDER LINE composite PK (OrderID + ProductID); CustomerID FK in ORDER; ORDER LINE has two FKs (OrderID, ProductID).
- EMPLOYEE1 extended with courses (Fig 3.2) — shows multivalued attribute problem.
- EMPLOYEE2 (Fig 3.8) — redundancy / anomaly demonstrations (insertion, deletion via Fig 3.9 Emp-Course, modification).

**5. FIGURES / DIAGRAMS / TABLES:**
- **Fig 3.1** (p.75) — Relation EMPLOYEE1 with four attributes (EmpID, Name, DeptName, Salary) and five tuples; EmpID underlined as PK.
- **Fig 3.2** (p.77) — EMPLOYEE1 extended with CourseTitle/DateCompleted showing multivalued attributes and nulls (EmpID 190).
- **Fig 3.3** (p.78) — Text description / schema for four Pine Valley relations (CUSTOMER, ORDER, ORDERLINE, PRODUCT).
- **Fig 3.4** (p.78) — Graphical representation of relations.
- **Fig 3.5** (p.79) — Domain definition.
- **Fig 3.6** (p.80) — Referential integrity constraint.
- **Fig 3.7** (p.81) — Well-structured relation (EMPLOYEE1).
- **Fig 3.8** (p.81) — NOT-well-structured relation (EMPLOYEE2).
- **Fig 3.9** (p.82) — Emp-Course relation (deletion anomaly illustration).

**6. VERBATIM QUESTIONS / ACTIVITIES:**

Self-Assessment Questions (p.83):
- **M3U1-SA1:** "What is the purpose of the relational keys?"
- **M3U1-SA2:** "What are integrity constraints? Explain them"

Tutor-Marked Assignment (p.83) — NOTE: printed numbering starts at 4:
- **M3U1-TMA1:** "Describe the primary differences between the conceptual and logical data models."
- **M3U1-TMA2:** "List the three components of the relational data model."
- **M3U1-TMA3:** "What is a schema? Discuss two common methods of expressing a schema"

---

### M3U2 — Transforming Conceptual to Logical Design (PDF pp. 85-98)

**1. Unit title + range:** Module Three, Unit 2 — Transforming Conceptual to Logical Design. PDF pp. 85-98.

**2. Learning outcomes:**
- Understand the purpose of transforming a conceptual model into a logical design.
- Convert regular entities from an ER diagram into relational tables.
- Assign appropriate primary keys and attributes during transformation.
- Ensure the logical design maintains integrity and structure of the original conceptual model.

**3. KEY CONCEPTS / terms (in order):**
- **Introduction to Transformation** (3.2.1) — during logical design, E-R/EER diagrams are transformed into relational schemas; inputs = ER/EER diagrams, outputs = relational schemas; well-defined rule set; CASE tools can automate.
- **Transforming Regular Entities** (3.2.2) — regular entities have independent existence (persons, products); represented by single-line rectangles.
  - *With composite attribute* — only the simple components of the composite attribute are included in the relation (e.g. Customer Address → Street, City, State in CUSTOMER, Fig 3.11).
  - *With multivalued attribute* — create TWO relations: first has all attributes except the multivalued; second has two attributes forming its PK (PK of first relation, now an FK, + the multivalued attribute); second relation name captures meaning of the multivalued attribute.
- **Transforming EER-D with weak entity** — create relation with simple attributes; include PK of identifying relation as FK; new relation PK = PK of identifying relation + partial identifier of weak entity. Alternative: surrogate key (DependentID) for DEPENDENT.
- **Transforming Binary 1:M relationships** — create a relation for each entity; include PK of the "one" side as FK in the "many" side relation. **Hint: the primary key migrates to the many side.** [EXAM-RELEVANT rule]
- **Transforming Binary M:N relationships** — for M:N between A and B, create a new relation C; include PKs of both entities as FKs in C; together they form C's composite PK; non-key attributes of the M:N relationship go in C.
- **Transforming Binary 1:1 relationships** (3.2.3) — special case of 1:M; two steps: create a relation per entity; include PK of one as FK in the other. Note: put the FK in the relation on the OPTIONAL side, referencing the PK of the entity with MANDATORY participation.
- **(3.2.4 — mislabeled "Binary one-to-one")** — actually covers associative entities: create three relations (one per participating entity + one associative relation); second step depends on whether an identifier was assigned to the associative entity.
- **Mapping Associative Entity Type** (3.2.5) — with no identifier (Fig 3.16) and with identifier (Fig 3.17).
- **Mapping Unary Relationships** (3.2.6) — relationship between instances of a single entity type; also called recursive; main cases are 1:M and M:N.
  - *Unary 1:M* — entity mapped to a relation; add an FK to the same relation referencing that relation's own PK (same domain). Called a **recursive foreign key** = FK referencing the PK of the same relation.
  - *Unary M:N* — two relations: one for the entity, one associative relation for the M:N; associative PK = two attributes both drawn from the other relation's PK; non-key attributes included. Example: ITEM + COMPONENT (PK = ItemNo, ComponentNo; Quantity non-key; both reference ItemNo). Surrogate key often used.
- **Map Ternary (and n-ary) Relationships** (3.2.7) — convert ternary to an associative entity; create an associative relation; default PK = three PKs of participating entities (may need extra attributes). Better: surrogate key (e.g. PTreatmentID).
- **Map Supertype/Subtype Relationships** — strategy: (1) separate relation for supertype and each subtype; (2) supertype gets attributes common to all members incl. PK; (3) each subtype gets supertype PK + attributes unique to that subtype; (4) assign supertype attribute(s) as the subtype discriminator. Example: supertype EMPLOYEE (PK Employee Number, discriminator Employee Type); subtypes HOURLY EMPLOYEE, SALARIED EMPLOYEE, CONSULTANT; each subtype PK = Employee Number with a prefix (e.g. SemployeeNumber for SALARIED), acting as FK to supertype.

**4. WORKED / illustrative EXAMPLES (ER-to-table mapping rules & examples):**
- Regular entity with simple attributes (Fig 3.10).
- Regular entity with composite attribute → CUSTOMER with Street/City/State (Fig 3.11).
- Regular entity with multivalued attribute → two relations (Fig 3.12).
- Weak entity → DEPENDENT with surrogate DependentID (Fig 3.13).
- 1:M binary relationship — PK migrates to many side (Fig 3.14).
- M:N binary relationship — new relation C with composite PK (Fig 3.14, duplicate label).
- 1:1 binary relationship (Fig 3.15).
- Associative entity mapping with/without identifier (Figs 3.16, 3.17).
- Unary 1:M — recursive FK (Fig 3.18).
- Unary M:N — ITEM/COMPONENT, ItemNo/ComponentNo/Quantity (Fig 3.19).
- Ternary — surrogate PTreatmentID (Fig 3.20).
- Supertype/subtype — EMPLOYEE + HOURLY/SALARIED/CONSULTANT (Figs 3.21, 3.22).

**5. FIGURES / DIAGRAMS / TABLES:**
- **Fig 3.10** (p.86) — Transforming regular entities (simple attributes).
- **Fig 3.11** (p.86/87, referenced) — CUSTOMER with composite Address (Street, City, State).
- **Fig 3.12** (p.87) — Transforming entity with multivalued attributes.
- **Fig 3.13** (p.88) — Transforming EER-D with a weak entity (DEPENDENT).
- **Fig 3.14** (p.89) — Transforming 1:M binary relationship. [label reused]
- **Fig 3.14** (p.89) — Transforming M:N binary relationship. [DUPLICATE label — two different figures both numbered 3.14]
- **Fig 3.15** (p.90) — Transforming binary 1:1 relationship.
- **Fig 3.16** (p.91) — Mapping associative entity type with NO identifier.
- **Fig 3.17** (p.91) — Mapping associative entity type WITH identifier.
- **Fig 3.18** (p.92) — Unary 1:M relationship (recursive FK).
- **Fig 3.19** (p.93) — Unary M:N relationship (ITEM/COMPONENT).
- **Fig 3.20** (p.94) — Mapping ternary relationships.
- **Fig 3.21** (p.95) — Subtype/supertype relationship (EMPLOYEE).
- **Fig 3.22** (p.95, then reused p.96) — Mapping supertype/subtype relationship. NOTE: Fig 3.22 label reused for the Class Activity EER diagram for bank cards.
- **Fig 3.22** (p.96) — EER diagram for bank cards (credit card environment) — DUPLICATE label.
- **Fig 3.23** (p.97) — EER diagram for Vacation Property Rental.

**6. VERBATIM QUESTIONS / ACTIVITIES:**

Class Activities (3.2.8, pp.96-97):
- **M3U2-ACT1:** "Figure 3.22 shows an EER diagram for a simplified credit card environment. There are two types of card accounts: debit cards and credit cards. Credit card accounts accumulate charges with merchants. Each charge is identified by the date and time of the charge, as well as the merchant and credit card primary keys.
  o Develop a relational schema."
- **M3U2-ACT2:** "Figure 3.23 shows an EER diagram for Vacation Property Rentals. This organisation rents preferred properties in several states. As shown in the figure, there are two basic types of properties: beach and mountain.
  - Transform the EER diagram to a set of relations and develop a relational schema."

Self-Assessment Questions (p.97):
- **M3U2-SA1:** "What is the difference between a conceptual model and a logical model in database design?"
- **M3U2-SA2:** "Explain how a regular entity with a composite attribute is transformed into a relational table."
- **M3U2-SA3:** "How are multivalued attributes handled during the transformation process?"
- **M3U2-SA4:** "What is the purpose of using a surrogate key in complex relationships?"
- **M3U2-SA5:** "Describe the steps involved in transforming a binary many-to-many (M:N) relationship."
- **M3U2-SA6:** "How is a unary one-to-many relationship represented in a relational schema?"
- **M3U2-SA7:** "Explain how to transform a supertype/subtype relationship into relational tables"

Tutor-Marked Assignment (p.98) — identical wording to SA1-SA7:
- **M3U2-TMA1:** "What is the difference between a conceptual model and a logical model in database design?"
- **M3U2-TMA2:** "Explain how a regular entity with a composite attribute is transformed into a relational table."
- **M3U2-TMA3:** "How are multivalued attributes handled during the transformation process?"
- **M3U2-TMA4:** "What is the purpose of using a surrogate key in complex relationships?"
- **M3U2-TMA5:** "Describe the steps involved in transforming a binary many-to-many (M:N) relationship."
- **M3U2-TMA6:** "How is a unary one-to-many relationship represented in a relational schema?"
- **M3U2-TMA7:** "Explain how to transform a supertype/subtype relationship into relational tables."

---

## MODULE FOUR — Functional Dependencies (cover PDF p.99)

---

### M4U1 — Normalisation (PDF pp. 100-122)

**1. Unit title + range:** Module Four, Unit 1 — Normalisation. PDF pp. 100-122.

**2. Learning outcomes:**
- Understand the purpose and importance of normalisation in database design.
- Identify and explain different normal forms (1NF, 2NF, 3NF, BCNF).
- Understand functional dependency and determinants.
- Recognise and apply different types of relational keys in normalisation.
- Use data models to guide the normalisation process.

**3. KEY CONCEPTS / terms + EXACT NORMALISATION RULES (in order):**

- **Normalisation** (4.1.1) — process of decomposing relations with anomalies to produce smaller, well-structured relations; a formal process deciding which attributes to group so all anomalies are removed; based on normal forms and functional dependencies (business rules, not data usage); a logical data-modelling technique. Two beneficial occasions: (a) during logical design to verify quality of relations from ER mapping; (b) when reverse-engineering older redundant systems.
- **Goals of Normalisation** — (1) minimise data redundancy to avoid anomalies and conserve storage; (2) simplify enforcement of referential integrity; (3) easier data maintenance (insert/update/delete); (4) better design / stronger basis for future growth.
- **Normal form** — a state of a relation requiring that certain rules about relationships between attributes (functional dependencies) are satisfied.

- **NORMAL FORMS — exact definitions as printed (p.101-102):**
  1. **First normal form:** "any multivalued attributes (also called repeating groups) have been removed, so there is a single value (possibly null) at the intersection of each row and column of the table."
  2. **Second normal form:** "any partial functional dependencies have been removed (i.e., nonkey attributes are identified by the whole primary key)."
  3. **Third normal form:** "any transitive dependencies have been removed (i.e., non-key attributes are identified by only the primary key)."
  4. **Boyce-Codd normal form:** "Any remaining anomalies that result from functional dependencies have been removed (because there was more than one possible primary key for the same non-keys)."

- **Functional Dependency (FD)** — a constraint between two attributes where the value of one is determined by another. For relation R, B is functionally dependent on A if for every valid instance of A, that value of A uniquely determines B. Notation: A → B. FD can be full, partial, or transitive.
- **Characteristics of FDs used in normalisation** — 1:1 relationship between LHS and RHS attributes; hold for all time; are nontrivial.
- **Determinant** — the attribute on the LEFT side of the arrow in an FD. (SSN, VIN, ISBN are determinants; in EMP COURSE, EmpID+CourseTitle is a determinant.)
- **FD examples given:** SSN → Name, Address, Birthdate; VIN → Make, Model, Colour; ISBN → Title, FirstAuthorName, Publisher.
- **EMPLOYEE2 FDs:** EmpID → Name, DeptName, Salary; and EmpID, CourseTitle → DateCompleted. Combination of EmpID + CourseTitle is the only candidate key (composite PK); neither alone identifies a row.

- **Relational Keys** (4.1.2) — attributes that determine other attributes = key attributes; single or composite. Listed types:
  1. Superkey / Primary Key
  2. Candidate Key / Composite Key — PK with >1 attribute of which no proper subset is a superkey; Uniqueness (values of K uniquely identify tuple); Irreducibility (no proper subset of K has uniqueness).
  3. Alternate Keys — candidate/composite keys not selected as PK.
  4. Foreign Key — attribute serving as PK of another relation in the same database.
- **Candidate Key** — attribute(s) uniquely identifying a row; must satisfy: Unique identification (each non-key attribute functionally dependent on the key) and Non-redundancy (no attribute can be deleted without destroying unique identification).
- **Candidate key vs determinant** — a candidate key is always a determinant, but a determinant may or may not be a candidate key. In EMPLOYEE2, EmpID is a determinant but NOT a candidate key. A determinant may be: a candidate key (EmpID in EMPLOYEE1), part of a composite candidate key (EmpID in EMPLOYEE2), or a nonkey attribute. [EXAM-RELEVANT distinction]

- **Data Models for Normalisation** (4.1.3) — normalise each relation from an EER transformation, or create+normalise relations per user interface (screens/forms/reports). Uses Pine Valley invoice.
- **Process of Normalisation** — formal technique analysing a relation via its PK and FDs; series of steps, each = a normal form; relations get progressively more restricted and less vulnerable to anomalies.
- **Unnormalised Form (UNF)** — a table containing one or more repeating groups; created by transforming data from an information source (e.g., a form) into table format.

- **Steps in Normalising a data model** (4.1.4):
  - **Step 0** — represent the user view (an invoice) as a single table with attributes as column headings; record sample data in rows including any repeating groups.
  - **Step 1 — Convert to 1NF:** A relation is in 1NF if both: no repeating groups; a single fact at each row/column intersection; and a primary key has been defined that uniquely identifies each row.
  - **Step 2 — Convert to 2NF:** A relation is in 2NF if it is in 1NF and contains no partial functional dependencies. A **partial functional dependency** exists when a non-key attribute is functionally dependent on part (but not all) of the PK. Conversion steps: (1) create a new relation for each PK attribute/combination that is a determinant in a partial dependency; (2) that attribute becomes the PK of the new relation; (3) move non-key attributes dependent only on that PK to the new relation. A 1NF relation is already in 2NF if: PK is a single attribute; OR no non-key attributes exist; OR every non-key attribute depends on the full PK.
  - **Step 3 — Convert to 3NF:** A relation is in 3NF if it is in 2NF and no transitive dependencies exist. A **transitive dependency** is an FD between the PK and one or more non-key attributes that depend on the PK via another non-key attribute. Removal procedure: for each non-key attribute (set) that is a determinant, create a new relation; that attribute becomes its PK; move attributes functionally dependent only on it; leave the determinant in the old relation as an FK.
- **Boyce-Codd Normal Form (BCNF)** — based on FDs accounting for ALL candidate keys; imposes additional constraints beyond 3NF. **A relation is in BCNF if and only if every determinant is a candidate key.** Difference between 3NF and BCNF for FD A→B: 3NF allows it if B is a primary-key attribute and A is not a candidate key; BCNF insists A must be a candidate key. Test: identify all determinants and ensure each is a candidate key.
- **Higher Order Normal Forms** — Fourth normal form: multivalued dependencies removed. Fifth normal form: any remaining anomalies removed.

**4. WORKED / illustrative EXAMPLES (full steps):**

**WORKED EXAMPLE A — Pine Valley Furniture INVOICE (main normalisation walkthrough, pp.106-114):**
- Base relation: **INVOICE** (user view = customer invoice).
- Attributes / determinants and FDs (from Step 1):
  - OrderID → OrderDate, CustomerID, CustomerName, CustomerAddress
  - CustomerID → CustomerName, CustomerAddress
  - ProductID → ProductDescription, ProductFinish, ProductStandardPrice
  - OrderID, ProductID → OrderedQuantity
- **1NF (Fig 4.6):** remove repeating groups (OrderID 1006 had three products = three repeating groups); PK selected = (OrderID, ProductID). Still has redundancy (Value Furniture customer data in 3+ rows) → insertion, deletion, update anomalies:
  - Insertion: cannot add a new product (Breakfast Table, ProductID 8) before it is ordered; adding a product to OrderID 1007 repeats order date + customer info.
  - Deletion: deleting Dining Table from OrderID 1006 loses item finish (Natural Ash) and price ($800.00).
  - Update: raising Entertainment Center (ProductID 4) price to $750.00 must change all rows.
- **2NF (Fig 4.7):** remove partial dependencies:
  - OrderID → OrderDate, CustomerID, CustomerName, CustomerAddress
  - ProductID → ProductDescription, ProductFinish, ProductStandardPrice
  - Results in **PRODUCT** and **CUSTOMER ORDER**; INVOICE left with (OrderID, ProductID) + OrderedQuantity, renamed **ORDER LINE**. ORDER LINE and PRODUCT are already in 3NF; CUSTOMER ORDER still has transitive dependencies.
- **3NF (Figs 4.8-4.10):** remove transitive dependencies in CUSTOMER ORDER:
  - OrderID → CustomerID → CustomerName
  - OrderID → CustomerID → CustomerAddress
  - Create **CUSTOMER** (PK CustomerID; CustomerName, CustomerAddress moved in). CUSTOMER ORDER renamed **ORDER**, CustomerID remains as FK.
- **Final result:** four 3NF relations — **CUSTOMER, PRODUCT, ORDER, ORDER LINE** (Fig 4.10 relational schema).

**WORKED EXAMPLE B — DreamHome Customer_Rental (2NF/3NF/BCNF, pp.115-119):**
- Base: **Unnormalised Customer Rental Relation** (Table 3.1) — multiple values at some row/column intersections (from DreamHome Customer Detail form, Fig 4.11).
- **1NF (Table 3.2):** single value at each intersection.
- Three candidate keys (all composite): (Customer_No, Property_No); (Customer_No, RentStart); (Property_No, RentStart). PK chosen = **(Customer_No, Property_No)**.
- Functional dependencies (Fig 4.11 dependency diagram):
  - fd1: Customer_No, Property_No → RentStart, RentFinish  (Pk / primary-key FD)
  - fd2: Customer_No → CName  (Pd / partial dependency)
  - fd3: Property_No → Paddress, Rent, Owner_No, OName  (Pd / partial dependency)
  - fd4: Owner_No → OName  (Td / transitive dependency)
  - fd5: Customer_No, RentStart → Property_No, Paddress, Rent, Owner_No, OName  (Ck / candidate key)
  - fd6: Property_No, RentStart → Customer_No, CName, RentFinish  (Ck / candidate key)
- **2NF (Table 4.3):** remove partial dependencies (fd2, fd3) into separate tables so every non-key attribute is fully dependent on its determinant.
- **3NF (Table 4.4):** all decomposed relations in 3NF except property_Owner, which has transitive dependency fd4 (Owner_No → OName). Decompose it; final relations:
  - Customer (Customer_No, Cname)
  - Rental (Customer_No, Property_No, RentStart, RentFinish)
  - Property_for_Rent (Property_No, Paddress, Rent, Owner_No)
  - Owner (Owner_No, Oname)
- **BCNF:** all decomposed relations already satisfy BCNF (no determinant that is not a candidate key). Rental's three determinants (fd1, fd5, fd6) are all candidate keys, so Rental is already in BCNF. "Violation of BCNF is quite rare."

**5. FIGURES / DIAGRAMS / TABLES:**
- **Fig 4.1** (p.103) — Functional dependency diagram for INVOICE.
- **Fig 4.1a** (p.104) — Functional dependencies sample1.
- **Fig 4.1b** (p.104) — Functional dependencies sample1 (EmpID → Name, DeptName, Salary).
- **Fig 4.2** (p.105) — EMP-COURSE relation.
- **Fig 4.3** (p.105) — Functional dependencies in EMPLOYEE2.
- **Fig 4.4** (p.106) — Customer invoice from Pine Valley Furniture Company.
- **Fig 4.5** (p.107) — Outcome of step 0 (Pine Valley invoice as single table with repeating groups).
- **Fig 4.6** (p.108) — Outcome of step 1 (INVOICE in 1NF).
- **Fig 4.7** (p.110) — Outcome of step 2 (INVOICE relations in 2NF/3NF: ORDER LINE, PRODUCT, CUSTOMER ORDER).
- **Fig 4.8** (p.114) — Customer Order relation in 2NF.
- **Fig 4.9** (p.114) — Customer Order relation in 2NF/3NF (CUSTOMER split out, ORDER with FK). [label near-duplicate of 4.8]
- **Fig 4.10** (p.115) — Relational schema for INVOICE data (CUSTOMER, PRODUCT, ORDER, ORDER LINE).
- **Fig 4.11** (p.116) — Dream Home Customer Detail form.
- **Fig 4.11** (p.117) — Dependency diagram for Customer_Rental relation. [DUPLICATE label — two figures numbered 4.11]
- **Table 3.1** (p.116) — Unnormalised Customer Rental relation.
- **Table 3.2** (p.117) — 1NF Customer Rental relation.
- **Table 4.3** (p.118) — 2NF Customer Rental relation.
- **Table 4.4** (p.119) — 3NF decomposed relations.
- (p.119) Property inspection report image for Class Activity (unlabeled figure).

**6. VERBATIM QUESTIONS / ACTIVITIES:**

Class Activities (4.1.5, pp.119-120):
- **M4U1-ACT1:** "Using the property inspection report below, generate the UNF, INF, 2NF and BCNF. requirements." (accompanied by a property inspection report image on p.120)

Self-Assessment Questions (p.120):
- **M4U1-SA1:** "What is normalisation, and why is it important in relational database design?"
- **M4U1-SA2:** "Differentiate between First Normal Form (1NF) and Third Normal Form (3NF)."
- **M4U1-SA3:** "Explain the concept of functional dependency and how it is used in the normalisation process"

Tutor-Marked Assignment (p.121):
- **M4U1-TMA1:** "For each of the following ER diagrams;
   - Transform the diagram to a relational schema that shows referential integrity constraints.
   - For each relation, diagram the functional dependencies.
   - If any of the relations are not in 3NF, transform them to 3NF. What is the difference between a conceptual model and a logical model in database design?"
   [NOTE: garbled — the ER diagrams are not present in the text, and a stray M3U2 question is appended.]
- **M4U1-TMA2:** "For each of the following relations, indicate the normal form for that relation. If the relation is not in third normal form, decompose it into 3NF relations. Functional dependencies (other than those implied by the primary key) are shown where appropriate.
   a. EMPLOYEE(EmployeeNo, ProjectNo)
   b. EMPLOYEE(EmployeeNo, ProjectNo, Location)
   c. EMPLOYEE(EmployeeNo, ProjectNo, Location, Allowance)
   d. [FD: Location → Allowance]
   e. EMPLOYEE(EmployeeNo, ProjectNo, Duration, Location, Allowance)
   f. [FD: Location → Allowance; FD: ProjectNo → Duration"
   [NOTE: as printed — sub-parts d and f are FD lines belonging to c and e respectively; closing bracket missing on f.]

---

## SUMMARY REPORT

**Units covered (3):**
- M3U1 Introduction to Relational Model (pp.73-84)
- M3U2 Transforming Conceptual to Logical Design (pp.85-98)
- M4U1 Normalisation (pp.100-122)

**Self-Assessment / Activity / TMA count (total 27 items):**
- M3U1: SA1, SA2; TMA1, TMA2, TMA3 (5)
- M3U2: ACT1, ACT2; SA1-SA7; TMA1-TMA7 (16)
- M4U1: ACT1; SA1, SA2, SA3; TMA1, TMA2 (6)
IDs: M3U1-SA1, M3U1-SA2, M3U1-TMA1, M3U1-TMA2, M3U1-TMA3, M3U2-ACT1, M3U2-ACT2, M3U2-SA1..SA7, M3U2-TMA1..TMA7, M4U1-ACT1, M4U1-SA1, M4U1-SA2, M4U1-SA3, M4U1-TMA1, M4U1-TMA2.

**Total figures/tables:** 34 labeled items —
- Module 3: Figs 3.1-3.23 (with duplicate labels: 3.14 used twice, 3.22 used twice) = ~23 figure labels.
- Module 4: Figs 4.1, 4.1a, 4.1b, 4.2-4.11 (4.11 used twice) + Tables 3.1, 3.2, 4.3, 4.4 + unlabeled property inspection report image.

**Normalisation worked-example tables used (two full walkthroughs):**
1. **Pine Valley Furniture INVOICE** — UNF → 1NF → 2NF → 3NF, yielding CUSTOMER, PRODUCT, ORDER, ORDER LINE (Figs 4.4-4.10).
2. **DreamHome Customer_Rental** — UNF → 1NF → 2NF → 3NF → BCNF, yielding Customer, Rental, Property_for_Rent, Owner (Tables 3.1, 3.2, 4.3, 4.4; Fig 4.11 dependency diagram; fd1-fd6).

**Flags for the author:**
- M3U1 learning outcomes are wrong (set-theory boilerplate) — replace with relational-model outcomes.
- M3U2 SA and TMA question sets are identical (verbatim duplicate).
- Duplicate figure numbers: 3.14 (1:M and M:N), 3.22 (supertype/subtype and bank-cards EER), 4.11 (DreamHome form and dependency diagram). Table numbering mixes "3.x" and "4.x" within Module 4.
- M4U1-TMA1 is garbled (missing ER diagrams; a stray M3U2 sentence appended). M4U1-TMA2 sub-parts d/f are FD annotations for c/e.
