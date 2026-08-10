/**
 * The 25/26 paper answered end to end, as a student would write it.
 *
 * Deliberately plain: the question, then the answer, nothing else. No teaching,
 * no memory hooks, no commentary on where the marks are. Everything explanatory
 * lives in the question pages; this is what you would actually hand in.
 */
export interface ScriptItem {
  n: string;
  title: string;
  question: string;
  answer: string;
}

export const SCRIPT_2526: ScriptItem[] = [
  {
    n: 'One',
    title: 'Question One',
    question: `<p><b>a.</b> Briefly explain the following with symbolic examples: (i) Super type (ii) Specialisation (iii) Total specialisation (iv) Disjoint rule <i>(4 mks)</i></p>
<p><b>b.</b> Use Figure 1 to explain the concept of determinant in the context of normalization. Show all possible determinants, the corresponding attributes and the type of functional dependency involved. <i>(2&frac12; mks)</i></p>
<p><b>c.</b> Consider the relational schema and write the SQL queries to answer the business questions (i-vi) with standard SQL syntax. <i>(9 mks)</i></p>
<pre>BRANCH          (branch_no, street, city, postcode)
STAFF           (staff_no, fName, lName, position, sex, DOB, salary, branch_no)
PROPERTYFORRENT (property_no, street, city, postcode, type, rooms, rent,
                 staff_no, branch_no)</pre>
<p>(i) List all staff members whose salary is greater than &#8358;100,000, ordered from highest salary to lowest.<br>
(ii) Display the total number of staff working in each branch. Include the branch number and total staff count.<br>
(iii) Find the average salary of staff in each branch. Display branch number and average salary.<br>
(iv) Display the details of all properties having more than 3 rooms and a monthly rent above &#8358;80,000.<br>
(v) Show the property number, property type, rent, and the full name of the staff member responsible for each property.<br>
(vi) Display all branches that currently have no staff assigned to them.</p>`,
    answer: `<p><b>1a.</b></p>
<p><b>(i) Super type.</b> A super type is the generic entity type that holds the attributes common to a group of related entity types, which inherit them.<br>
<i>Example:</i> STAFF (staffNo, name, address) is the super type of LECTURER and DRIVER.</p>
<p><b>(ii) Specialisation.</b> Specialisation is the top-down process of identifying subgroups within a general entity type, each subgroup having attributes the others do not share.<br>
<i>Example:</i> STAFF specialises into LECTURER (rank, department) and DRIVER (licenceClass).</p>
<p><b>(iii) Total specialisation.</b> Total specialisation is the constraint that every instance of the super type must be a member of at least one subtype. It is shown by a double line from the super type to the circle.<br>
<i>Example:</i> every STAFF member must be either a LECTURER or a DRIVER; no staff member is neither.</p>
<p><b>(iv) Disjoint rule.</b> The disjoint rule is the constraint that an instance of the super type may be a member of at most one subtype. It is shown by the letter <b>d</b> in the circle.<br>
<i>Example:</i> a VEHICLE is either a CAR or a TRUCK, never both at the same time. Its opposite is the overlap rule, shown by <b>o</b>.</p>

<p><b>1b.</b> A determinant is the attribute, or group of attributes, on the left-hand side of a functional dependency, that is the attribute whose value determines the value of one or more other attributes.</p>
<table><tr><th>Determinant</th><th>Attributes determined</th><th>Type of functional dependency</th></tr>
<tr><td>(propertyNo, iDate) &mdash; the whole primary key</td><td>iTime, comments, staffNo, staffName, carReg</td><td>Full functional dependency</td></tr>
<tr><td>propertyNo &mdash; part of the primary key</td><td>pAddress</td><td>Partial dependency</td></tr>
<tr><td>staffNo &mdash; a non-key attribute</td><td>staffName</td><td>Transitive dependency</td></tr>
<tr><td>(staffNo, iDate) &mdash; non-key attributes</td><td>carReg</td><td>Transitive dependency</td></tr></table>
<p>A partial dependency is a determinant that is only part of a composite key; it violates 2NF. A transitive dependency is a determinant that is not a key attribute; it violates 3NF.</p>

<p><b>1c.</b></p>
<pre>-- (i)
SELECT   staff_no, fName, lName, position, salary
FROM     STAFF
WHERE    salary &gt; 100000
ORDER BY salary DESC;

-- (ii)
SELECT   branch_no, COUNT(*) AS total_staff
FROM     STAFF
GROUP BY branch_no;

-- (iii)
SELECT   branch_no, AVG(salary) AS average_salary
FROM     STAFF
GROUP BY branch_no;

-- (iv)
SELECT *
FROM   PROPERTYFORRENT
WHERE  rooms &gt; 3
  AND  rent &gt; 80000;

-- (v)
SELECT p.property_no, p.type, p.rent, s.fName, s.lName
FROM   PROPERTYFORRENT p
JOIN   STAFF s ON p.staff_no = s.staff_no;

-- (vi)
SELECT b.branch_no, b.street, b.city
FROM   BRANCH b
WHERE  b.branch_no NOT IN (SELECT branch_no
                           FROM   STAFF
                           WHERE  branch_no IS NOT NULL);</pre>`,
  },
  {
    n: 'Two',
    title: 'Question Two',
    question: `<p><b>a.</b> Explain two (2) limitations of the file-based approach to data processing. <i>(2 mks)</i></p>
<p><b>b.</b> What is a Database Management System (DBMS)? <i>(2 mks)</i></p>
<p><b>c.</b> What is meant by data abstraction? Explain the three (3) levels of data abstraction with examples. <i>(5&frac12; mks)</i></p>
<p><b>d.</b> Transform the EER diagram given into relations. <i>(8 mks)</i></p>`,
    answer: `<p><b>2a.</b></p>
<p><b>(i) Data redundancy and inconsistency.</b> In a file-based system each application keeps its own file, so the same data is duplicated in several places. When one copy is updated and the others are not, the copies disagree and the organisation holds two different versions of the same fact.</p>
<p><b>(ii) Program-data dependence.</b> Each application program contains the description of the file it accesses, so any change to the structure of that file requires every program that uses it to be modified and recompiled.</p>

<p><b>2b.</b> A Database Management System is the software that enables users to define, create, maintain and control access to a database. It provides a data definition language to define the structure, a data manipulation language to insert, update, delete and retrieve data, and controlled access including security, integrity, concurrency control, backup and recovery.</p>

<p><b>2c.</b> Data abstraction is the hiding of the complex details of how data is stored and maintained, presenting each user with only the data they need in a form they can understand.</p>
<p>There are three levels:</p>
<p><b>(i) External level (view level).</b> The users' view of the database. It describes that part of the database relevant to a particular user, and there may be many different external views of the same database.<br>
<i>Example:</i> a lecturer's view shows studentNo, name and grade, while the bursary's view of the same database shows studentNo, name and fees payable.</p>
<p><b>(ii) Conceptual level (logical level).</b> The community view of the database. It describes what data is stored and the relationships among the data, for all users taken together, without any concern for physical storage.<br>
<i>Example:</i> STUDENT(studentNo, name, level), COURSE(courseCode, title), and the enrolment relationship between them.</p>
<p><b>(iii) Internal level (physical level).</b> The physical representation of the database on the computer. It describes how the data is stored: file organisation, indexes, record placement and data compression.<br>
<i>Example:</i> STUDENT records stored as fixed-length records in a B-tree indexed on studentNo.</p>
<p>Separating these levels provides data independence: logical data independence allows the conceptual schema to change without altering external views, and physical data independence allows the internal schema to change without altering the conceptual schema.</p>

<p><b>2d.</b> The EER diagram is transformed into relations using the following rules:</p>
<p>1. Each regular entity type becomes a relation; its attributes become the columns and its identifier becomes the primary key.<br>
2. For a one-to-many relationship, the primary key of the entity on the "one" side is placed in the relation on the "many" side as a foreign key.<br>
3. For a many-to-many relationship, a new relation is created containing the primary keys of both participating entities as a composite primary key, together with any attributes of the relationship itself.<br>
4. For a one-to-one relationship, the primary key of one entity is placed in the other as a foreign key, preferably in the relation with mandatory participation.<br>
5. Each multivalued attribute becomes a new relation containing the primary key of its owner entity together with the attribute; both form the composite primary key.<br>
6. For a super type and its subtypes, one relation is created for the super type holding the common attributes, and one relation for each subtype holding its own attributes plus the primary key of the super type, which serves as both the primary key and a foreign key of the subtype relation.</p>
<p><i>For example, for a super type VEHICLE with subtypes CAR and TRUCK:</i></p>
<pre>VEHICLE (vehicleId, make, year)          PK vehicleId
CAR     (vehicleId, bootCapacity)        PK vehicleId, FK vehicleId -&gt; VEHICLE
TRUCK   (vehicleId, payload)             PK vehicleId, FK vehicleId -&gt; VEHICLE</pre>`,
  },
  {
    n: 'Three',
    title: 'Question Three',
    question: `<p><b>a. (i)</b> Would you choose a database system instead of simply storing data in operating system files? Justify your answer with two points. <i>(5 marks)</i><br>
<b>(ii)</b> When would it make sense not to use a database system? <i>(2&frac12; marks)</i></p>
<p><b>b.</b> Draw an EER diagram for the following description of a law firm: each case handled by the firm has a unique case number; a date opened, date closed and judgment description are also kept on each case. A case is brought by one or more plaintiffs, and the same plaintiff may be involved in many cases. A plaintiff has a requested judgment characteristic. A case is against one or more defendants, and the same defendant may be involved in many cases. A plaintiff or defendant may be a person or an organisation. Over time, the same person or organisation may be a defendant or a plaintiff in cases. In either situation, such legal entities are identified by an entity number, and other attributes are name and address. <i>(10 mks)</i></p>`,
    answer: `<p><b>3a(i).</b> Yes, I would choose a database system. My justification is as follows.</p>
<p><b>(1) Control of redundancy and inconsistency.</b> With operating system files, each application maintains its own copy of the data, so the same fact is stored several times. When one copy is updated and the others are not, the copies disagree. A database system stores each fact once and shares it among all applications, so there is a single version of the truth and integrity constraints can be enforced centrally.</p>
<p><b>(2) Data independence and shared, controlled access.</b> File-based programs embed the structure of their files, so a structural change forces every program to be rewritten. A database system separates the logical structure from the physical storage, so either may change without disturbing the other. It also provides concurrent access by many users, security and authorisation, backup and recovery, and a standard query language, none of which an operating system file provides.</p>

<p><b>3a(ii).</b> It would make sense not to use a database system in the following circumstances:</p>
<p>(1) When the data and the application are simple, small, well defined and not expected to change, so the cost and complexity of a DBMS are not justified.<br>
(2) When there is a single user and no requirement for concurrent access, security or recovery, so the services of a DBMS would not be used.<br>
(3) When the overhead of a general purpose DBMS would prevent strict real-time requirements from being met, as in some embedded systems.<br>
(4) When the organisation cannot meet the cost of the software, the hardware needed to run it, and the expertise required to administer it.</p>

<p><b>3b.</b> The EER diagram consists of the following.</p>
<p><b>Entities and attributes</b></p>
<pre>CASE          caseNumber (PK), dateOpened, dateClosed, judgmentDescription
LEGAL ENTITY  entityNumber (PK), name, address        [super type]
PERSON        entityNumber (PK)                        [subtype]
ORGANISATION  entityNumber (PK)                        [subtype]</pre>
<figure class="eerfig"><svg viewBox="0 0 660 330" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="11" role="img" aria-label="EER diagram for the law firm"><defs><marker id="tri" markerWidth="12" markerHeight="12" refX="11" refY="5" orient="auto"><path d="M0,0 L11,5 L0,10 z" fill="none" stroke="currentColor" stroke-width="1.2"/></marker></defs><rect x="255" y="10" width="150" height="46" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="330" y="27" text-anchor="middle" font-weight="bold">CASE</text><text x="330" y="43" text-anchor="middle" font-size="10">caseNumber (PK)</text><path d="M62,110 L120,86 L178,110 L120,134 Z" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="120" y="114" text-anchor="middle" font-size="10">BRINGS  M:N</text><path d="M482,110 L540,86 L598,110 L540,134 Z" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="540" y="114" text-anchor="middle" font-size="10">IS AGAINST  M:N</text><line x1="255" y1="40" x2="178" y2="100" stroke="currentColor" stroke-width="1.4"/><line x1="405" y1="40" x2="482" y2="100" stroke="currentColor" stroke-width="1.4"/><text x="150" y="78" font-size="10" >plaintiff</text><text x="470" y="78" font-size="10" >defendant</text><rect x="230" y="160" width="200" height="46" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="330" y="177" text-anchor="middle" font-weight="bold">LEGAL ENTITY</text><text x="330" y="193" text-anchor="middle" font-size="10">entityNumber (PK), name, address</text><line x1="120" y1="134" x2="120" y2="183" stroke="currentColor" stroke-width="1.4"/><line x1="120" y1="183" x2="230" y2="183" stroke="currentColor" stroke-width="1.4"/><line x1="540" y1="134" x2="540" y2="183" stroke="currentColor" stroke-width="1.4"/><line x1="540" y1="183" x2="430" y2="183" stroke="currentColor" stroke-width="1.4"/><text x="96" y="128" font-size="10" font-style="italic">requestedJudgment</text><line x1="330" y1="206" x2="330" y2="234" stroke="currentColor" stroke-width="1.4"/><line x1="334" y1="206" x2="334" y2="234" stroke="currentColor" stroke-width="1.4"/><circle cx="330" cy="248" r="14" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="326" y="252" font-size="10" font-weight="bold">d</text><line x1="330" y1="262" x2="330" y2="276" stroke="currentColor" stroke-width="1.4"/><line x1="240" y1="276" x2="420" y2="276" stroke="currentColor" stroke-width="1.4"/><line x1="240" y1="276" x2="240" y2="290" stroke="currentColor" stroke-width="1.4"/><line x1="420" y1="276" x2="420" y2="290" stroke="currentColor" stroke-width="1.4"/><rect x="160" y="290" width="160" height="34" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="240" y="311" text-anchor="middle" font-weight="bold">PERSON</text><rect x="340" y="290" width="180" height="34" fill="none" stroke="currentColor" stroke-width="1.4"/><text x="430" y="311" text-anchor="middle" font-weight="bold">ORGANISATION</text><text x="360" y="246" font-size="10" font-style="italic">total (double line) and disjoint (d)</text></svg><figcaption>Q3(b). Plaintiff and defendant are roles in two M:N relationships from LEGAL ENTITY to CASE, not subtypes, because the same legal entity may be either across different cases.</figcaption></figure><p><b>Specialisation.</b> LEGAL ENTITY is the super type; PERSON and ORGANISATION are its subtypes. The specialisation is <b>total</b>, since every legal entity is either a person or an organisation, shown by a double line, and <b>disjoint</b>, since no legal entity is both, shown by <b>d</b> in the circle.</p>
<p><b>Relationships</b></p>
<pre>BRINGS       LEGAL ENTITY (as plaintiff)  M : N  CASE
             attribute of the relationship: requestedJudgment

IS AGAINST   LEGAL ENTITY (as defendant)  M : N  CASE</pre>
<p>Both relationships are many-to-many, because a case has one or more plaintiffs and one or more defendants, and the same legal entity may be involved in many cases. Participation of CASE in both relationships is mandatory, since a case must have at least one plaintiff and at least one defendant.</p>
<p>Plaintiff and defendant are drawn as two separate relationships between LEGAL ENTITY and CASE, with the roles labelled on the relationship lines, rather than as subtypes, because the same legal entity may be a plaintiff in one case and a defendant in another.</p>
<p>When mapped to relations this gives:</p>
<pre>CASE          (caseNumber, dateOpened, dateClosed, judgmentDescription)
LEGAL_ENTITY  (entityNumber, name, address)
PERSON        (entityNumber)
ORGANISATION  (entityNumber)
PLAINTIFF_IN  (entityNumber, caseNumber, requestedJudgment)
DEFENDANT_IN  (entityNumber, caseNumber)</pre>`,
  },
  {
    n: 'Four',
    title: 'Question Four',
    question: `<p><b>a.</b> Describe the relational data model. <i>(2&frac12; mks)</i></p>
<p><b>b.</b> Explain six (6) Relational Algebra operations with examples. <i>(6 mks)</i></p>
<p><b>c.</b> Consider the following relational schemas and write the relational algebra for the tasks (i-iii). <i>(9 mks)</i></p>
<pre>Emp      (Fname, Lname, SSN, Dno)
Dept     (DName, DNum, Mgr_SSN)
D_Loc    (DNo, Location)
Project  (PName, PNo, DNo, P_Loc)
Works_on (ESSN, PNo, Hours)</pre>
<p>(i) Retrieve the names of all employees who work for the 'Headquarters' department.<br>
(ii) For every project located in 'Abuja', list the project number, controlling department and the manager's name.<br>
(iii) Find the names of the employees who work on all the projects controlled by DNo = A314.</p>`,
    answer: `<p><b>4a.</b> The relational data model is a logical data model in which all data is represented as a collection of relations, that is two-dimensional tables of rows and columns. Each row is a tuple and each column is an attribute, whose permitted values are drawn from a domain. The number of attributes is the degree of the relation and the number of tuples is its cardinality. Rows and columns are unordered, so each tuple is identified by the value of its primary key rather than by its position. Relationships between relations are represented by foreign keys rather than by physical pointers, and integrity is enforced by entity integrity, which requires that no part of a primary key is null, and referential integrity, which requires that every foreign key value matches an existing primary key value or is null. The model is manipulated by relational algebra and relational calculus, and was proposed by E. F. Codd in 1970.</p>

<p><b>4b.</b></p>
<p><b>(i) Selection (&sigma;).</b> Returns the tuples of a relation that satisfy a given condition. The result has the same attributes but fewer tuples.<br>
<i>Example:</i> &sigma;<sub>Dno=5</sub>(Emp) returns all employees in department 5.</p>
<p><b>(ii) Projection (&pi;).</b> Returns the specified attributes of a relation, with duplicate tuples removed. The result has fewer attributes.<br>
<i>Example:</i> &pi;<sub>Fname, Lname</sub>(Emp) returns only the first and last names of all employees.</p>
<p><b>(iii) Cartesian product (&times;).</b> Combines every tuple of one relation with every tuple of another.<br>
<i>Example:</i> Emp &times; Dept pairs each employee with every department.</p>
<p><b>(iv) Join (&#8904;).</b> Combines tuples from two relations that satisfy a given condition on their attributes. It is equivalent to a Cartesian product followed by a selection.<br>
<i>Example:</i> Emp &#8904;<sub>Dno=DNum</sub> Dept joins each employee to their own department.</p>
<p><b>(v) Union (&cup;).</b> Returns all tuples appearing in either of two union-compatible relations, with duplicates removed.<br>
<i>Example:</i> Managers &cup; Technicians returns all employees who are in either group.</p>
<p><b>(vi) Difference (&minus;).</b> Returns the tuples that appear in the first relation but not in the second. Both relations must be union compatible.<br>
<i>Example:</i> &pi;<sub>SSN</sub>(Emp) &minus; &pi;<sub>Mgr_SSN</sub>(Dept) returns the employees who are not managers.</p>
<p>Two relations are union compatible when they have the same number of attributes and corresponding attributes are drawn from the same domains.</p>

<p><b>4c.</b></p>
<pre>(i)   HQ     &#8592; &sigma; DName='Headquarters' (Dept)
      RESULT &#8592; &pi; Fname, Lname ( Emp &#8904; Dno=DNum HQ )

(ii)  ABUJA  &#8592; &sigma; P_Loc='Abuja' (Project)
      R1     &#8592; ABUJA &#8904; DNo=DNum Dept
      R2     &#8592; R1 &#8904; Mgr_SSN=SSN Emp
      RESULT &#8592; &pi; PNo, DNum, Fname, Lname (R2)

(iii) A314   &#8592; &pi; PNo ( &sigma; DNo='A314' (Project) )
      EMP_P  &#8592; &pi; ESSN, PNo (Works_on)
      ALL    &#8592; EMP_P &divide; A314
      RESULT &#8592; &pi; Fname, Lname ( ALL &#8904; ESSN=SSN Emp )</pre>
<p>In (iii) the division operator is used because the question asks for employees who work on <i>all</i> the projects controlled by that department.</p>`,
  },
  {
    n: 'Five',
    title: 'Question Five',
    question: `<p><b>a.</b> Given the following database concepts: <b>I.</b> the data definition language, <b>II.</b> the data manipulation language, <b>III.</b> the data model.<br>
<b>(i)</b> Which of the enumerations (I) to (III) plays an important role in representing information about the real world in a database? <i>(&frac12; mk)</i><br>
<b>(ii)</b> Explain each concept briefly; your explanation should reflect the difference between them.</p>
<p><b>b.</b> Draw an EER diagram for a company that provides offerings to its customers. Offerings are of two types: products and services, identified by an offering ID with an attribute of description. Products are described by product name, standard price and date of first release; services by the name of the unit responsible and conditions of service. There are repair, maintenance and other types of service. A repair service has a cost and is the repair of some product; a maintenance service has an hourly rate. Some products never require repair, and there are many potential repair services for a product. A customer may purchase an offering, and the company keeps the date purchased and the contact person; not all offerings are purchased. Customers are identified by customer ID with name, address and phone number. When a service is performed it is billed to some customer, who may be billed for services they did not purchase. For a billed service, the company keeps the date performed, the date the bill is due and the amount due.</p>`,
    answer: `<p><b>5a(i).</b> III, the data model.</p>

<p><b>5a(ii).</b></p>
<p><b>The data model</b> is a collection of concepts used to describe data, the relationships between the data, and the constraints on it. It provides the means of representing information about the real world, independent of any particular database or software product. The relational model, for example, provides relations, tuples, attributes, domains and keys. It is not a language and cannot be executed.</p>
<p><b>The data definition language (DDL)</b> is the part of a database language used to define and change the structure of the database: creating, altering and dropping tables, and stating the constraints on them. Its statements are CREATE, ALTER and DROP, and their result is recorded in the data dictionary. It does not operate on the data values themselves.</p>
<p><b>The data manipulation language (DML)</b> is the part of a database language used to work with the data held within that structure: inserting, updating, deleting and retrieving tuples. Its statements are INSERT, UPDATE, DELETE and SELECT. It cannot alter the structure of the database.</p>
<p><b>The difference.</b> The data model supplies the concepts used to represent the real world; the DDL records a particular design built from those concepts into the database; and the DML operates on the data held inside that design. That is, model, then structure, then contents. As an illustration, DELETE is DML and removes tuples from a table, whereas DROP is DDL and removes the table itself.</p>

<p><b>5b.</b> The EER diagram consists of the following.</p>
<p><b>Entities and attributes</b></p>
<pre>OFFERING      offeringID (PK), description             [super type]
PRODUCT       offeringID (PK), productName, standardPrice,
              dateOfFirstRelease                        [subtype]
SERVICE       offeringID (PK), unitName, conditionsOfService
                                                        [subtype]
REPAIR        offeringID (PK), cost                     [subtype of SERVICE]
MAINTENANCE   offeringID (PK), hourlyRate               [subtype of SERVICE]
CUSTOMER      customerID (PK), name, address, phoneNumber</pre>
<p><b>Specialisations.</b> OFFERING specialises into PRODUCT and SERVICE: total, since every offering is one or the other, and disjoint, since none is both. SERVICE specialises further into REPAIR, MAINTENANCE and other services: this specialisation is <b>partial</b>, because the description states there are other types of service, and disjoint.</p>
<p><b>Relationships</b></p>
<pre>PURCHASES    CUSTOMER  M : N  OFFERING
             attributes: datePurchased, contactPerson
             OFFERING participation optional, since not all
             offerings are purchased

REPAIR_OF    REPAIR    M : 1  PRODUCT
             PRODUCT participation optional, since some products
             never require repair, and a product may have many
             potential repair services

BILLED_FOR   CUSTOMER  M : N  SERVICE
             attributes: datePerformed, dateDue, amountDue
             optional on both sides, since a customer may never
             require a service, and a customer may be billed for
             a service they did not purchase</pre>
<p>BILLED_FOR is kept separate from PURCHASES because a customer may be billed for a service that they did not purchase.</p>`,
  },
  {
    n: 'Six',
    title: 'Question Six',
    question: `<p><b>a.</b> Explain the following relational terms briefly: (i) Schema (ii) Alternate key (iii) Tuple <i>(3 mks)</i></p>
<p><b>b.</b> Given the StaffPropertyInspection relation, answer the following:<br>
(i) Draw the functional dependency diagram for the relation. <i>(2&frac12; mks)</i><br>
(ii) Briefly explain the concept of transitive functional dependency. <i>(2 mks)</i><br>
(iii) Normalise the relation to third normal form. The primary key is (propertyNo, iDate). All actions involved in the normalization process should be well stated, and the output relations and tables presented clearly with identified primary key. <i>(10 mks)</i></p>`,
    answer: `<p><b>6a.</b></p>
<p><b>(i) Schema.</b> A schema is the overall structure or design of a database: the relations it contains, the attributes of each, their data types and the constraints upon them. It is distinct from an instance, which is the data held in the database at a particular moment.</p>
<p><b>(ii) Alternate key.</b> An alternate key is a candidate key that has not been selected as the primary key. A relation may have several candidate keys, each of which uniquely identifies a tuple; one is chosen as the primary key and the remainder are alternate keys.</p>
<p><b>(iii) Tuple.</b> A tuple is a single row of a relation, that is one complete record, consisting of one value for each attribute of the relation.</p>

<p><b>6b(i).</b> Functional dependency diagram for StaffPropertyInspection (propertyNo, pAddress, iDate, iTime, comments, staffNo, staffName, carReg), primary key (propertyNo, iDate):</p>
<pre>fd1  propertyNo, iDate  &rarr;  iTime, comments, staffNo, staffName, carReg
                             (full functional dependency on the whole key)

fd2  propertyNo         &rarr;  pAddress
                             (partial dependency on part of the key)

fd3  staffNo            &rarr;  staffName
                             (transitive dependency)

fd4  staffNo, iDate     &rarr;  carReg
                             (transitive dependency)</pre>
<p>In the diagram the attributes are listed in a row with the primary key attributes underlined. An arc is drawn above the row from (propertyNo, iDate) to each attribute of fd1, and arcs are drawn below the row for fd2 and fd3, each labelled with the type of dependency.</p>

<p><b>6b(ii).</b> A transitive functional dependency is a dependency in which a non-key attribute depends upon another non-key attribute rather than directly upon the primary key. That is, if A &rarr; B and B &rarr; C, where B and C are not key attributes, then C is transitively dependent on A through B.<br>
<i>Example from this relation:</i> (propertyNo, iDate) &rarr; staffNo and staffNo &rarr; staffName, so staffName is transitively dependent on the primary key through staffNo. Removing transitive dependencies takes a relation from second to third normal form.</p>

<p><b>6b(iii).</b></p>
<p><b>Step 1: the unnormalised relation and its key.</b></p>
<pre>StaffPropertyInspection (propertyNo, iDate, pAddress, iTime,
                         comments, staffNo, staffName, carReg)
Primary key: (propertyNo, iDate)</pre>
<p><b>Step 2: first normal form.</b> Every attribute of the relation holds a single atomic value and there are no repeating groups, therefore the relation is already in 1NF.</p>
<p><b>Step 3: second normal form. Remove partial dependencies.</b> A relation is in 2NF if it is in 1NF and every non-key attribute is fully functionally dependent on the whole primary key. Examining each non-key attribute, pAddress is determined by propertyNo alone, which is only part of the composite primary key, and is therefore partially dependent. It is removed into a new relation together with its determinant, which becomes the primary key of that relation. All other non-key attributes require both propertyNo and iDate and therefore remain.</p>
<pre>Property (propertyNo, pAddress)
Primary key: propertyNo

PropertyInspection (propertyNo, iDate, iTime, comments,
                    staffNo, staffName, carReg)
Primary key: (propertyNo, iDate)
Foreign key: propertyNo references Property(propertyNo)</pre>
<p>Both relations are now in 2NF.</p>
<p><b>Step 4: third normal form. Remove transitive dependencies.</b> A relation is in 3NF if it is in 2NF and no non-key attribute is transitively dependent on the primary key. In PropertyInspection, staffName is determined by staffNo, which is itself a non-key attribute, and is therefore transitively dependent on the primary key. It is removed into a new relation together with its determinant, which becomes the primary key of that relation, and staffNo remains in PropertyInspection as a foreign key.</p>
<pre>Property (propertyNo, pAddress)
Primary key: propertyNo

Staff (staffNo, staffName)
Primary key: staffNo

PropertyInspection (propertyNo, iDate, iTime, comments,
                    staffNo, carReg)
Primary key: (propertyNo, iDate)
Foreign keys: propertyNo references Property(propertyNo)
              staffNo    references Staff(staffNo)</pre>
<p><b>Step 5: conclusion.</b> All three relations are now in third normal form, since every attribute holds a single atomic value, every non-key attribute is fully functionally dependent on the whole primary key of its relation, and no non-key attribute is transitively dependent upon the primary key.</p>`,
  },
];
