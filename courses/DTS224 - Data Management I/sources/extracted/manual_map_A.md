# DTS224 Data Management I — Manual Map A (Modules One & Two, PDF pp. 3-71)

Source: `map_chunkA_mod12.txt`. Page numbers below are PDF page markers from the extract.

Question ID scheme: `M<module>U<unit>-SA#` (Self-Assessment), `-ACT#` (Unit Activity / Class Activity), `-TMA#` (Tutor-Marked Assignment). All questions quoted verbatim.

---

# MODULE ONE — Information Management Concept and Introduction to Database Systems

## M1U1 — Foundations of Data Storage and Management (pp. 4-9)

### 1. Learning outcomes
- Explain purpose and scope of information storage and retrieval in database systems.
- Identify real-world information management applications and their use cases.
- Understand how information is captured and represented in digital form.
- Describe techniques for indexing, searching, and ensuring information privacy.
- Define the importance of data integrity and security.
- Assess a system based on scalability, efficiency, and effectiveness.

### 2. Key concepts / terms (in order)
- **Information storage** — persistently storing data via digital structures (files, tables, documents) on physical/cloud systems (p.5).
- **Retrieval** — locating and accessing stored data via queries or indexing (p.5).
- Storage in relations (tables) vs documents (NoSQL); structured data has a schema; unstructured/semi-structured (logs, XML, JSON) use flexible models; query languages (SQL); indexing/normalisation/metadata (p.5).
- **Information management applications** — library systems, healthcare info systems, ERP, CRM, content management systems (p.5).
- **Information capture** — collecting data from real-world sources: manual entry, sensors/IoT, scanners/OCR, APIs (pp.5-6).
- **Data representation** — how captured data is formatted/stored: text/numbers/images/binary; schemas; data types (INT, VARCHAR, DATE) (p.6).
- **Analysis and Indexing** — indexing builds lookup structures (B-trees, hash indexes); search; full-text search & NLP for unstructured data; analysis via aggregation (SUM, COUNT, AVG), filtering/sorting, query optimisation (p.6).
- **Privacy** — protecting sensitive data via access control (role-based), anonymisation, legal compliance (GDPR, HIPAA) (p.6).
- **Integrity** — accuracy/consistency via constraints (NOT NULL, UNIQUE, CHECK), referential integrity (foreign keys), transaction management (ACID properties) (pp.6-7).
- **Security** — authentication & encryption, firewalls & DB hardening, backups & disaster recovery (p.7).
- **Scalability** — handle increasing data/users: vertical scaling (stronger hardware), horizontal scaling (replication, sharding) (p.7).
- **Efficiency** — resource use (CPU/memory/storage); query performance, indexing strategies, storage optimisation (p.7).
- **Effectiveness** — meets user needs: accuracy of results, reliability/uptime, user satisfaction (p.7).
- Note (exam-relevant): the three-way distinction **privacy vs integrity vs security** is explicitly taught and tested.

### 3. Worked / illustrative examples
- Example data types (INT, VARCHAR, DATE) as representation (p.6).
- Aggregation function examples (SUM, COUNT, AVG) for analysis (p.6).
- No fully worked numeric example; conceptual only.

### 4. Figures / diagrams / tables
- None in this unit.

### 5. VERBATIM questions

**Self-Assessment Questions**
- **M1U1-SA1.** "What is the purpose of indexing in a database, and how does it improve performance?"
- **M1U1-SA2.** "Explain the differences between data privacy, data integrity, and data security."
- **M1U1-SA3.** "List and describe three real-world applications of information management systems."

**Tutor-Marked Assignment**
- **M1U1-TMA1.** "Define the term "information storage and retrieval." Explain its relevance in managing a large-scale data system"
- **M1U1-TMA2.** "Identify any two security features implemented in modern database systems and explain their role."
- **M1U1-TMA3.** "Using a hospital management system as an example, describe how information is captured, stored, and retrieved, ensuring both security and efficiency."
- **M1U1-TMA4.** "Discuss what is meant by scalability and explain one strategy used to achieve it in enterprise databases"

---

## M1U2 — Introduction to Database Systems and Architecture (pp. 10-23)

### 1. Learning outcomes
- Define what a database is and identify its key components.
- Explain the concepts of data abstraction and data independence in database design.
- Describe the role and functions of a DBMS.
- Differentiate between various types of database systems (hierarchical, relational, NoSQL).
- Understand principles of database security and how data is protected.

### 2. Key concepts / terms (in order)
- **Database** — "an extensive collection of data organised especially for rapid search and retrieval"; also "a shared collection of logically related data (and a description of this data), designed to meet the information needs of an organisation." System catalogue (metadata) enables program-data independence (p.11).
- **Data model** — a collection of concepts used to describe data (p.12).
- **Schema** — a description of a particular collection of data using a given data model. Example: `Student {matricNo, name, Address, programme, age}` (p.12).
- **Database instance** — the information in a database at a particular point in time (p.12).
- **DBMS** — software system enabling users to define, create, and maintain the database and provide controlled access (p.12).
- **DDL (Data Definition Language)** — descriptive language to describe/name entities and relationships; compiled into tables stored in a **data dictionary / data directory** (aka system catalogue, catalogue tables, information schema) holding metadata (data about data) (p.13).
- **DML (Data Manipulation Language)** — operations for basic data manipulation; a **query language** is the portion of DML for retrieval only; DML/query language often used synonymously. Four operations: retrieval, insertion, deletion, modification (p.13).
- **Database application** — one or more programs/websites acting as intermediary between user and DBMS (p.13).
- **Database manager** — program module interfacing between low-level stored data and application programs/queries; DBs need gigabytes on disk; data moved between disk and main memory (p.13).
- **Database Administrator (DBA)** — person with central control over data and programs. Duties: schema definition, granting authorisation for data access, integrity constraint specification, storage structure & access method definition, schema & physical organisation modification (pp.14-15).
- **Database users** — application programs; **DML pre-compiler** converts DML calls (prefaced by special char like $, #) into host-language procedure calls; host compiler generates object code; **fourth-generation languages** combine Pascal-like control structures with DB manipulation; **query processor** breaks DML into instructions for database manager (pp.15-16).
- **Database Abstraction** — data stored as bits on disk/tape; users need only a subset (p.16).
- **Levels of Abstraction** (pp.16-18):
  - **External level** — highest; users see rows/columns; different views per access rights (e.g. student can't see lecturer salary); can perform calculations (tax, CGPA, age) without altering lower levels.
  - **Logical/Conceptual level** — next level; describes actual data as tables + mapping; holds all data; changes here don't affect external/physical.
  - **Internal level** — intermediary; often omitted (hence "three levels"); depends on DBMS software; can be combined with logical.
  - **Physical level** — lowest; how data actually stored in physical memory (tapes, hard disks); file organisation (hashing, sequential, B+ tree).
  - Note (exam-relevant): text says usually **three levels** but names four (internal is the extra intermediary).
- **Data Independence** — ability to modify schema at one level without affecting the next higher level; immunity of user apps to changes in data definition/organisation; data independence + operation independence = data abstraction (p.19).
  - **Physical data independence** — modify physical schema without rewriting application programs (pp.19-20).
  - **Logical data independence** — modify logical schema without rewriting programs; harder to achieve than physical (programs depend heavily on logical structure) (pp.19-20).
- **Types of Database** (p.20): **Personal database system** (one app, few tables, simple, one computer, one user) vs **Enterprise-level database system** (several simultaneous users, multiple apps, multiple computers, complex, many tables, many databases).
- **Database security** — protective measures against unauthorised access/misuse/breaches; ensures confidentiality, integrity, availability (p.21).

### 3. Worked / illustrative examples
- Student schema example `Student {matricNo, name, Address, programme, age}` (p.12).
- External-level calculation examples: tax from salary, CGPA of student, age from DOB (pp.16-17).
- Logical independence example: adding a 'skills' column doesn't change external view of student Ages (pp.17-18).
- Logical data independence example: users A & B selecting EmployeeNumber/EmployeeName; B adds salary column, A's view unaffected (p.20).

### 4. Figures / diagrams / tables (to redraw)
- **Figure 1.1: Components of a database system** (p.11) — depicts the components making up a DB system.
- **Figure 1.2: Components of the database** (p.11) — depicts internal components of the database.
- **Figure 1.3: Components of DBMS** (p.12) — depicts the functional components of a DBMS.
- **Figure 1.4: Data Abstraction Levels** (p.16) — depicts the abstraction-level hierarchy.
- **Figure 1.5: Data Abstraction Levels Example** (p.18) — worked example of the abstraction levels.
- **Figure 1.6: Data Independence** (p.19) — depicts types of data independence.
- **Figure 1.7: Enterprise-Level database systems** (p.19) — depicts an enterprise DB system.
- (Note: "Key Aspects of Database Security" heading on p.21 has no figure/list content rendered.)

### 5. VERBATIM questions

**Self-Assessment Questions**
- **M1U2-SA1.** "Define a database and list at least three of its key components."
- **M1U2-SA2.** "What is data abstraction, and what are the three levels involved in it?"
- **M1U2-SA3.** "Differentiate between physical data independence and logical data independence with examples."
- **M1U2-SA4.** "What are the primary functions of a Database Management System (DBMS)?"
- **M1U2-SA5.** "Describe two types of database systems and their typical use cases."
- **M1U2-SA6.** "Explain the role of the database administrator and list three key responsibilities."
- **M1U2-SA7.** "What is the purpose of a Data Manipulation Language (DML)? List four common operations"

**Tutor-Marked Assignment**
- **M1U2-TMA1.** "What does the term data independence mean, and why is it an important goal?"
- **M1U2-TMA2.** "Perform a search on the Internet of relational DBMS vendors. Pick two competing products and discuss whether each is scalable and if it can be used for a personal, workshop, departmental, enterprise, or Internet database."
- **M1U2-TMA3.** "One of the biggest challenges of building e-commerce sites has been the ability to deliver merchandise ordered by customers over the web quickly. Why do you think companies turned to database solutions to help them improve their supply chain management and expedite the filling and delivery of orders?"
- **M1U2-TMA4.** "Explain the difference between user views, a conceptual schema, and an internal schema as different perspectives of the same database"

---

# MODULE TWO — Introduction to Conceptual Models

## M2U1 — Introduction to Conceptual Models: ER Diagram (pp. 25-46)

### 1. Learning outcomes
- Understand the basic concept and purpose of data and conceptual modelling.
- Explain the structure and use of the Entity-Relationship (ER) model.
- Identify and define business rules that influence data models.
- Model entities and their attributes in an ER diagram.
- Model relationships between entities using appropriate notation.
- Understand and apply cardinality constraints to describe relationship rules accurately.

### 2. Key concepts / terms (in order)
- **Data modelling** — documentation of rules/policies governing an organisation's data (p.26). Role of database analyst: identify rules, represent unambiguously, implement in DB tech.
  - Note (odd/likely OCR intrusion): p.26 contains stray text about "a branch of mathematics… verification of truth/falsity", "valid arguments, inference, proofs… paradoxes, and fallacies" and an Einstein quote — appears to be spurious content bleeding from a discrete-math source; not core DB material.
- **Importance (system developers' view)** — data characteristics crucial to design; data more complex/stable than processes (p.26).
- **Benefits of data modelling** — communication, understanding of org rules, saves cost, improves data quality, reduces migration cost (pp.26-27).
- **Conceptual model** — high-level representation of an org's data and relationships (p.27).
- **Entity-Relationship (E-R) model** — detailed conceptual representation of entities, relationships, and attributes of both; expressed as an ERD (p.27).
- **ERD** — graphical representation of an E-R model; independent of the DBMS (p.27).
- **Entity metadata** — descriptive details (names, definitions, attributes, identifiers) (p.28).
- **Data names** — must relate to business (not technical), be meaningful, unique, repeatable, follow standard syntax, from an approved word list (pp.28-29).
- **Business rule** — foundation of data models, derived from policies/procedures/events; asserts/controls business structure/behaviour; also known as an **integrity constraint** in the DB context; not universal (pp.29-30).
- **Gathering business rules** — from interview notes, org documents; ask who/what/when/where/why/how (pp.30). Note (odd intrusion p.30): stray "truth set of a predicate" discrete-math sentence.
- **Characteristics of a good business rule** — Declarative, Precise, Atomic, Consistent, Expressible, Distinct, Business-oriented (pp.30-31).
- **E-R model notation** — no industry-standard notation; course combines common features (p.31).
- **Entity** — person, place, object, event, or concept about which the org keeps data; has a noun name. Examples: Person (EMPLOYEE), Place (STORE), Object (MACHINE), Event (SALE), Concept (ACCOUNT) (p.31).
- **Entity type vs entity instance** — entity type = collection sharing common properties (named, described once via metadata); entity instance = single occurrence (p.31-32).
- **Strong entity** — exists independently; has a unique identifier; aka independent entity (p.32).
- **Weak entity** — existence depends on another entity type; aka dependent entity; no business meaning without owner; the entity it depends on = **identifying owner**; typically no own identifier, has a **partial identifier** (pp.32-33).
- **Attribute** — property/characteristic of an entity type; has a noun name (p.33).
- **Required vs optional attribute** — required must be present; optional may lack a value (p.33).
- **Simple vs composite attribute** (p.34).
- **Multi-valued attribute** — may take more than one value per instance (e.g. EMPLOYEE Skill); shown with **curly brackets** (pp.34-35).
- **Derived attribute** — value calculated from related attributes (plus data like today's date); shown with **square brackets** (p.35).
- **Identifier attribute** — attribute(s) whose value distinguishes instances; no two instances share it; **composite identifier** consists of a composite attribute (p.35).
- **Relationship** — association among instances of one or more entity types; has a verb phrase name; relationships (degree + cardinality) represent business rules (p.36).
- **Relationship type** — meaningful association among entity types; line labelled with verb phrase (p.36).
- **Relationship instance** — association among entity instances, exactly one from each participating type (p.36).
- **Attribute on relationship** — attributes may attach to many-to-many or one-to-one relationships; e.g. Date Completed. Note (exam-relevant): "an attribute cannot be associated with a one-to-many relationship" (p.37).
- **Associative entity** — entity type associating instances of one/more entity types with attributes peculiar to the relationship; shown as rectangle with rounded corners (e.g. CERTIFICATE) (p.38).
- **Degree of relationship** — number of entity types participating: **unary** (deg 1), **binary** (deg 2), **ternary** (deg 3) (p.38).
- **Unary relationship** — between instances of a single entity type; aka **recursive** (p.38).
- **Binary relationship** — between two entity types; most common (pp.38-39).
- **Ternary relationship** — simultaneous relationship among three entity types (p.39).
- **Cardinality constraint** — rule specifying number of instances of one entity that can/must associate with each instance of another (p.39). Note (odd intrusion p.39): stray "Predicates represent properties… P(x) assigns true or false" discrete-math text.
- **Minimum cardinality** — min instances; zero = optional participation, else mandatory (pp.39-40).
- **Maximum cardinality** — max instances; often indicated by **crow's foot** symbol (p.40).
- Note (exam-relevant): "If minimum cardinality is zero, participation is optional; if one, mandatory" (p.40).

### 3. Worked / illustrative examples
- **Pine Valley Furniture** sample ERD — suppliers ship items assembled into products sold to customers who order products; orders have lines (p.27, and business-rule example p.41).
- **Completes** relationship (EMPLOYEE-COURSE, many-to-many): Melton completed 3 courses (C++, COBOL, Perl); SQL completed by Celko & Gosling; Visual Basic by no one (p.37).
- **Date Completed** attribute on the Completes relationship (p.37).
- **CERTIFICATE** associative entity example (p.38).
- **Cardinality examples** (pp.39-41): (1) PATIENT has Recorded PATIENT HISTORY; (2) EMPLOYEE is Assigned to PROJECT (employee Pete optional); (3) PERSON is Married to PERSON (optional zero-or-one both directions).
- **Business rule for the ERD** — full SUPPLIER/ITEM/PRODUCT/SHIPMENT/CUSTOMER/ORDER ruleset (pp.41-42).

### 4. Figures / diagrams / tables (to redraw)
- **Figure 2.1: E-R Diagram** (p.26) — the Pine Valley Furniture sample ERD (suppliers, items, products, customers, orders).
- **Table 2.1: Meta-Data of E-R Diagram** (p.28) — table of entity metadata for Figure 2.1.
- **Figure 2.2: Basic E-R Notations** (p.31) — symbol legend for E-R notation.
- **Figure 2.3: Entity Type Versus Entity Instance** (p.32) — one EMPLOYEE type vs many instances.
- **Figure 2.4: Strong, Weak Entity and Identifying Relationship Example** (p.33).
- **Figure 2.5: Required and Optional Attribute(s)** (p.32/34) — two STUDENT instances; optional attribute Major#.
- **Figure 2.6: Composite Attributes** (p.34).
- **Figure 2.7: Multivalued and Derived Attributes** (p.35) — EMPLOYEE Skill (multivalued), derived attribute.
- **Figure 2.8: Simple & Composite Identifier Attributes** (p.36).
- **Figure 2.9: Relationship Type and Instances** (p.37) — EMPLOYEE Completes COURSE many-to-many.
- **Figure 2.10: Attribute on Relationship** (p.37) — Date Completed on Completes.
- **Figure 2.11: Associative Entity** (p.38) — CERTIFICATE as rounded rectangle.
- **Figure 2.12: Unary Relationship** (p.38).
- **Figure 2.13: Binary Relationships** (p.39).
- **Figure 2.14: Ternary Relationship** (p.39).
- **Figure 2.15: Cardinality Constraint** (p.40) — MOVIE/DVD crow's-foot bidirectional example.
- **Figure 2.16: PATIENT Has Recorded PATIENT HISTORY** (p.41).
- **Figure 2.17: EMPLOYEE Is Assigned To PROJECT** (p.41).
- **Figure 2.18: PERSON Is Married to PERSON** (p.41).
- **Figure 2.19: Example of a Business Rule for the ERD** (p.42) — full SUPPLIER/ITEM/PRODUCT/SHIPMENT/CUSTOMER/ORDER ERD.
- **Figure 2.20: Class Activity E-R Diagram** (p.44) — cellular operator: customers, plans, handsets, manufacturer, OS.

### 5. VERBATIM questions

**Class Activities** (section 2.1.7, pp.42-45) — intro: "For each of the descriptions below, perform the following tasks: Identify the degree and cardinalities of the relationship. Express the relationships in each description graphically with an E-R diagram."
- **M2U1-ACT1 (1a).** "A book is identified by its ISBN, and it has a title, a price, and a date of publication. It is published by a publisher that has its own ID number and name. Each book has exactly one publisher, but one publisher typically publishes multiple books over time."
- **M2U1-ACT2 (1b).** "A book (see 1a) is written by one or multiple authors. Each author is identified by an author number and has a name and date of birth. Each author has either one or multiple books; in addition, data are occasionally needed on prospective authors who have not yet published any books."
- **M2U1-ACT3.** "In the context specified in 1a and 1b, better information is needed regarding the relationship between a book and its authors. Specifically, it is essential to record the percentage of the royalties that belongs to a specific author, whether or not a specific author is a lead author of the book, and each author's position in the sequence of the book's authors."
- **M2U1-ACT4.** "A book (see 1a) can be part of a series, which is also identified as a book and has its own ISBN. One book can belong to several sets, and a set consists of at least one but potentially many books."
- **M2U1-ACT5 (2).** "Look at this E-R Diagram: [Figure 2.20]. A cellular operator needs a database to track its customers, their subscription plans, and the handsets (mobile phones) they use. The E-R diagram in Figure 2.20 illustrates the key entities of interest to the operator and their relationships. Based on the figure, answer the following questions and explain the rationale for your response. For each question, identify the element(s) in the E-R diagram that you used to determine your answer."
  - a. "Can a customer have an unlimited number of plans?"
  - b. "Can a customer exist without a plan?"
  - c. "Is it possible to create a plan without knowing who the customer is?"
  - d. "Does the operator want to limit the types of handsets that can be linked to a specific plan type?"
  - e. "Is it possible to maintain data regarding a handset without connecting it to a plan?"
  - f. "Can a handset be associated with multiple plans?"
  - g. "Assume a handset type exists that can utilise multiple operating systems. Could this situation be accommodated within the model included in Figure 2-1?"
  - h. "Is the company able to track a manufacturer without maintaining information about its handsets?"
  - i. "Can the same operating system be used on multiple handset types?"

**Self-Assessment Questions**
- **M2U1-SA1.** "Is there a difference between data modelling and conceptual modelling? Justify your answer."
- **M2U1-SA2.** "What determines how data are handled?"
- **M2U1-SA3.** "Relationship instance and Associative entity are similar but different. Explain their similarities and differences"

**Unit Activities**
- **M2U1-ACT6.** "Read the content of Module 2, Unit 1 in the study guide. Consult the recommended texts and attempt the class activity and self-assessment questions. (90 minutes)"
- **M2U1-ACT7.** "TUTOR MARKED ASSIGNMENT: Complete the following and submit for grading. (60 minutes)"

**Tutor-Marked Assignment**
- **M2U1-TMA1.** "Give four reasons why many system designers believe that data modelling is important and arguably the most essential part of the systems development process."
- **M2U1-TMA2.** "Discuss why the ER model is a popular modelling tool."
- **M2U1-TMA3.** "Consider the situation: Faculty at a university (FACULTY entity) can also be part of the Board of Studies (BOARD entity). Is there a weak entity here? How?"
- **M2U1-TMA4.** "The entity type TEACHER has the following attributes: Teacher Name, Email, Phone, Age, Trainer, and Training Count. Trainer represents a workshop organised by the teacher, and Training Count represents the number of times the teacher has organised such workshops. This implies a teacher may organise more than one workshop. Draw an ERD for this situation. What attribute or attributes did you designate as the identifier for the TEACHER entity? Why?"

---

## M2U2 — Enhanced E-R Model (pp. 47-58)

### 1. Learning outcomes
- Understand the concept of Enhanced E-R modelling and its purpose in advanced database design.
- Identify and explain the use of supertypes and subtypes in representing entity hierarchies.
- Distinguish between specialisation and generalisation.
- Apply completeness and disjointness constraints in subtype/supertype relationships.
- Understand the role of subtype discriminators in determining entity categorisation.
- Interpret and construct supertype/subtype hierarchies in an E-R diagram.

### 2. Key concepts / terms (in order)
- **Enhanced Entity-Relationship (EER) model** — extends original E-R with new constructs; semantically similar to object-oriented modelling; key construct = supertype/subtype relationships (e.g. CAR supertype with SEDAN, SPORTS CAR, COUPE subtypes) (p.48).
- **Subtype** — a meaningful subgrouping of entities within an entity type (e.g. GRADUATE / UNDERGRADUATE STUDENT) (p.48).
- **Supertype** — a generic entity type with a relationship to one or more subtypes (e.g. STUDENT) (p.48).
- **Employee example** — hourly, salaried, contract-consultant employees; common attributes Employee Number/Name/Address/Date Hired (pp.48-49).
- **Attribute inheritance** — subtype entities inherit all attribute values and relationship instances of the supertype; avoids redundancy (p.50).
- **When to use supertype/subtype** — some attributes apply to only some instances; or subtype instances participate in a relationship unique to that subtype (p.50).
- **Generalisation** — defining a more general entity type from specialised ones; **bottom-up** process (p.51). Example note: MOTORCYCLE excluded because it has only common attributes and no unique relationship, so no subtype needed (pp.51-52).
- **Specialisation** — defining subtypes of a supertype; **top-down**, reverse of generalisation (p.52).
- **Completeness constraint** — whether a supertype instance must be a member of at least one subtype (pp.53). Rules:
  - **Total specialisation** — each supertype instance must be a member of some subtype.
  - **Partial specialisation** — a supertype instance is not required to belong to any subtype. (Note: text phrases it as "not allowed to belong to any subtype" — a wording quirk; standard meaning is "need not belong.")
- **Disjointness constraint** — whether a supertype instance may simultaneously belong to two+ subtypes (p.54). Rules:
  - **Disjoint rule** — a member of one subtype cannot simultaneously be in another.
  - **Overlap rule** — an instance can be in two+ subtypes simultaneously.
- **Subtype discriminator** — an attribute of the supertype whose values determine the target subtype (p.53).
- **Supertype/subtype hierarchy** — hierarchical arrangement where each subtype has only one supertype (p.53).
- **Summary of hierarchies** — attributes assigned at highest logical level (e.g. SSN at root PERSON; Date Hired at EMPLOYEE); subtypes inherit from all supertypes up to root; a FACULTY instance has SSN/Name/Address/Gender/DOB (from PERSON), Date Hired/Salary (from EMPLOYEE), Rank (from FACULTY) (pp.56-57).

### 3. Worked / illustrative examples
- **CAR** supertype with SEDAN/SPORTS CAR/COUPE subtypes (p.48).
- **STUDENT** supertype with GRADUATE/UNDERGRADUATE subtypes (p.48).
- **EMPLOYEE** hourly/salaried/contract-consultant with attribute lists (pp.48-49).
- **MOTORCYCLE not a subtype** reasoning under generalisation (pp.51-52).
- **PERSON → EMPLOYEE → FACULTY** attribute inheritance chain (pp.56-57).

### 4. Figures / diagrams / tables (to redraw)
- **Figure 2.21: Basic Supertypes and Subtypes Notations** (p.47) — notation legend.
- **Figure 2.22: Example of Supertypes and Subtypes** (p.47) — EMPLOYEE supertype with three subtypes.
- **Figure 2.23: Supertype and Subtype Relationships** (p.48) — subtype participating in a unique relationship.
- **Figure 2.24: Sample of Generalisation 1** (p.51) and **Figure 2.24: Sample of Generalisation 2** (p.51) — two parts (duplicate number in source), vehicle generalisation (incl. MOTORCYCLE discussion).
- **Figure 2.25: Sample of Specialisation 1** (p.52) and **Figure 2.26: Sample of Specialisation 2** (p.52).
- **Figure 2.27: Completeness Constraints Total Specialisation Rule** (p.53).
- **Figure 2.28: Completeness Constraints Partial Specialisation Rule** (p.54).
- **Figure 2.29: Disjointness Constraints Disjoint Rule** (p.54) and **Figure 2.29: Disjointness Constraints Overlap Rule** (p.55) — duplicate number in source.
- **Figure 2.30: Subtype Discriminator; Disjoint** (p.56) and **Figure 2.30: Subtype Discriminator; Overlap** (p.56) — duplicate number in source.
- Note: source reuses figure numbers 2.24, 2.29, 2.30 for two diagrams each; treat as parts a/b when redrawing.

### 5. VERBATIM questions

**Self-Assessment Questions**
- **M2U2-SA1.** "The two most important types of constraints in Supertype/Subtype Relationships are?"
- **M2U2-SA2.** "What does the partial specialisation rule specify? How is this different from the total specialisation rule?"
- **M2U2-SA3.** "What are the processes that serve as the mental models in developing supertype/subtype relationships? Is there a difference between data modelling and conceptual modelling? Justify your answer."

**Unit Activities**
- **M2U2-ACT1.** "Read the content of Module 2, Unit 2 in the study guide. Consult the recommended texts and attempt the In-text and self-assessment questions. (90 minutes)."
- **M2U2-ACT2.** "TUTOR MARKED ASSIGNMENT: Complete the following and submit for grading. (60 minutes)"

**Tutor-Marked Assignment**
- **M2U2-TMA1.** "Differentiate between supertype and subtype. Using a real-life example, explain in detail the operations of each in an organisation's database system."
- **M2U2-TMA2.** "When can each of these supertype and subtype Relationships be used? What is their attribute inheritance?"

---

## M2U3 — Introduction to Semi-Structured Models (XML Model) (pp. 59-67)

### 1. Learning outcomes
- Understand the concept of semi-structured data models and their purpose.
- Identify and differentiate between JSON and XML formats.
- Read, write, and interpret data using JSON and XML.

### 2. Key concepts / terms (in order)
- **Semi-structured data models** — flexible representation not conforming to rigid relational schema but retaining some structure; middle ground between structured and unstructured; schema changes often (p.60).
- **Flexible schema** — each tuple may have a different attribute set:
  - **Wide-column representation** — attribute set not fixed; new attributes added as needed (p.60).
  - **Sparse column representation** — fixed but huge number of attributes; each tuple uses only those it needs, rest null (p.60).
- **Multivalued data types** — attributes with non-atomic values (sets, multisets, arrays); e.g. topics of interest `{basketball, La Liga, cooking, anime, Jazz}` (p.60).
- **Nested data types** — structured attributes modelling composite attributes (e.g. name → firstname, lastname); two widely used flexible models: **JSON** and **XML** (pp.60-61).
- **JSON (JavaScript Object Notation)** — section 2.3.2 (p.59); note: body content for JSON is blank in the extract (heading only).
- **XML (eXtensible Markup Language)** — text-based scripting language describing data hierarchically with HTML-like tags; can be schemaless or schema-validated; tags in angle brackets `< >`, used in pairs `<tag>...</tag>`; e.g. `<title>Semi-Structured Data Models</title>`; can represent relational data and hierarchical structures (bills, purchase orders) (pp.61-62).
- **Storing XML documents** (pp.63): (1) **shredding** into a relational DB (each element in tables + relationship tables; SQL Server, Oracle); (2) **special XML columns** (can bind an XSD to validate); (3) **native XML database** (non-relational, purpose-built). Note: options 1-2 for XML as exchange format between browser/app server; option 1 when most info originally in XML.
- **Retrieving XML documents** — key technologies **XPath** and **XQuery** (pp.63-64):
  - **XPath** — XML technology supporting XQuery; expressions locate data in XML documents.
  - **XQuery** — XML transformation/query language over relational + XML data; built on XPath; supported by IBM, Oracle, Microsoft. "XQuery is to XML as SQL is to relational databases."
- **Displaying XML documents** — controlled by a stylesheet in **XSL (Extensible Stylesheet Language)**; browsers/languages support **XSLT**; transformation at web-server or app-server layer; handles varied devices (smartphones, tablets) (pp.64-65).
- **Summary of semi-structured models** — new tags added easily; data "self-documenting"; XQuery adoption limited; SQL extended for XML (XML data type; generate XML from relational via **XMLAGG** aggregate; extract via XPath path expressions) (pp.65-66).
- **Key features** — Schema Flexibility (no fixed schema, fields vary per record), Hierarchical Structure (nested trees/graphs), Self-Describing (metadata/tags describe data), Partial Organisation (tags/metadata make it more manageable than unstructured) (p.66).

### 3. Worked / illustrative examples
- Set-valued attribute `{basketball, La Liga, cooking, anime, Jazz}` (p.60).
- Composite name → firstname/lastname (pp.60-61).
- Tag example `<title>Semi-Structured Data Models</title>` (p.62).
- Purchase order in XML (nested representation) — Figure 2.32 (p.62).
- XQuery expression returning product elements with standard price > 300.00 (p.64).
- XSLT displaying Salesperson data as an HTML table — Figure 2.34 (p.65).

### 4. Figures / diagrams / tables (to redraw)
- **Figure 2.31: XML Tags** (p.62) — XML tags representing relational data (relation/attribute names as tags).
- **Figure 2.32: Realistic Use of XML** (p.62) — purchase order represented in nested XML.
- **Figure 2.33: Retrieval of XML Documents** (p.64) — XML document + XQuery expression (price > 300.00).
- **Figure 2.34: Sample XSLT specification** (p.65) — XSLT rendering Salesperson data as an HTML table.

### 5. VERBATIM questions

**Self-Assessment Questions**
- **M2U3-SA1.** "Is XML the same as HTML? Justify your answer."
- **M2U3-SA2.** "Explain the Semi-Structured Data types."

**Unit Activities**
- **M2U3-ACT1.** "Read the content of Unit 1 in the study guide. Consult the recommended texts and research more information on the internet. (90 minutes)"
- **M2U3-ACT2.** "Complete the self-introductory forum. Original post by Thursday. (10 minutes). Complete replies to 2 of your classmates by Sunday at 11:59 p.m. (10 minutes)"
- **M2U3-ACT3.** "TUTOR MARKED ASSIGNMENT: Complete the following and submit for grading. (60 minutes)"

**Tutor-Marked Assignment**
- **M2U3-TMA1.** "Identify and write out four (4) inconveniences of using semi-structured data models"
- **M2U3-TMA2.** "What advantage do semi-structured data models have over models with rigid organisation?"

---

## M2U4 — Examples of Conceptual Models (pp. 68-71)

### 1. Learning outcomes
- Read and create basic E-R diagrams based on everyday scenarios.
- Apply conceptual modelling techniques to real-world case studies.

### 2. Key concepts / terms (in order)
- **Worked conceptual-model scenarios** (p.67), each an E-R modelling case:
  - **University Database** — Student, Course, Lecturer, Department; students enrol in courses, lecturers teach courses, courses belong to departments.
  - **Hospital Management System** — Patient, Doctor, Appointment, Treatment; relationships "consults", "prescribes", "undergoes".
  - **Online Retail Store** — Customer, Product, Order, Payment; customers place orders, orders contain products, customers make payments.
  - **Library System** — Book, Member, Librarian, Loan; relationships "borrows", "returns".
  - **Hotel Reservation System** — Guest, Room, Staff, Reservation; bookings, check-ins, staff roles; rooms have type and rate.

### 3. Worked / illustrative examples
- The five scenarios above are themselves the illustrative examples (p.67). No fully drawn ERDs shown in the extract; students construct them.

### 4. Figures / diagrams / tables
- None rendered in the extract (this unit is prose scenarios; diagrams are for the student to draw).

### 5. VERBATIM questions

**Self-Assessment Questions**
- **M2U4-SA1.** "Draw a simple E-R diagram for a hospital with patients, doctors, and treatments."

**Unit Activities**
- **M2U4-ACT1.** "Read the content of Unit 1 in the study guide. Consult the recommended texts and research more information on the internet. (90 minutes)"
- **M2U4-ACT2.** "Complete the self-introductory forum. Original post by Thursday. (10 minutes). Complete replies to 2 of your classmates by Sunday at 11:59 p.m. (10 minutes)"
- **M2U4-ACT3.** "TUTOR MARKED ASSIGNMENT: Complete the following and submit for grading. (60 minutes)"

**Tutor-Marked Assignment**
- **M2U4-TMA1.** "Create a conceptual model for a hotel reservation system. Include guests, rooms, reservations, and staff."
- **M2U4-TMA2.** "List four attributes for each entity in a library management system."
- **M2U4-TMA3.** "Explain why creating a conceptual model is essential before building a database."

---

## Notes for rebuild
- Several OCR/source intrusions of discrete-mathematics text appear in M2U1 (logic, predicates, truth sets, Einstein quote) — clearly bleed from another course; exclude from the DB manual.
- Source duplicates figure numbers 2.24, 2.29, 2.30 (two diagrams each) and references "Figure 2-1" / "Figure 3-4" inconsistently — normalise when redrawing.
- JSON subsection (2.3.2) has a heading but no body text in the source; the manual will need JSON content authored to match the XML depth.
- Every unit ends with the same four-book References/Further Readings (Ramakrishnan & Gehrke; Elmasri & Navathe; Hoffer/Prescott/McFadden; Connolly & Begg) plus wisc.edu and unideb.hu links; M2U3 adds Rosen, Discrete Mathematics (2019).
