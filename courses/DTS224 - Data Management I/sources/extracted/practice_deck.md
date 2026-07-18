
===== SLIDE 1 =====
QUESTION
NORMALIZATION

===== SLIDE 2 =====
What to do?
Show the Functional dependency diagram for the table below using the information	given.
Describe and illustrate the process of normalizing the table below to Boyce-Codd Normal form, giving the following information

===== SLIDE 3 =====
[1 image(s) on slide]

===== SLIDE 4 =====
The keys…
Candidate keys:
PNo, ADate			(Primary key)
ADate, Atime, SurgeonNo
StaffNo, ADate, Atime

===== SLIDE 5 =====
Functional Dependencies
PNo, ADate, → StaffNo ,ATime, DentistName, SurgeonNo
PNo → PName
StaffNo → DentistName
StaffNo, ADate → SurgeonNo
ADate, ATime, SurgeonNo → PNo, PName, StaffNo, DentistName
StaffNo, ADate, ATime → PNo, PName

===== SLIDE 6 =====
Question 2
Identify all the entities in the scenario
Draw the EER

===== SLIDE 7 =====
[1 image(s) on slide]

===== SLIDE 8 =====
Branch_office { branch number, address ,telephone number and manager name}
Staff{ staff no, name, address, telno, sex, date of  birth, position,salary and date-of-appointment}
Manager{ staff no, name, address, telno, sex, date of  birth, position,salary and date-of-appointment, bonus}
Secretary{ staff no, name, address, telno, sex, date of  birth, position,salary and date-of-appointment, typing speed}
sales rep{ staff no, name, address, telno, sex, date of  birth, position,salary and date-of-appointment, sales-area, car-allowance.
Full time staff{ staff no, name, address, telno, sex, date of  birth, position,salary and date-of-appointment, salary-scale and hourly-allowance
partime staff{ staff no, name, address, telno, sex, date of  birth, position,salary and date-of-appointment, rated-per-hour
next of kin{ staff no, name, relationship-to-the-member of staff, address and telephone-number}