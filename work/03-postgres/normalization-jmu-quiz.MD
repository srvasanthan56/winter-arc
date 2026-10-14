Question 1¶
Consider relation: R = (A, B, C, D, E)

with the set of functional dependencies: {CE → D, D → B, C → A}

Find all candidate keys.
Identify the best normal form that R satisfies (1NF, 2NF, 3NF).
If the relation is not in 3NF, decompose it until it becomes 3NF.
At each step, identify a new relation, decompose and re-compute the keys and the normal forms they satisfy.
Question 2¶
Consider relation: R = (A, B, C, D, E, F, G, H, I, J)

with the set of functional dependencies: {AB → C, A → DE, B → F, F → GH, D → IJ}

Find all candidate keys.
Identify the best normal form that R satisfies (1NF, 2NF, 3NF).
If the relation is not in 3NF, decompose it until it becomes 3NF.
At each step, identify a new relation, decompose and re-compute the keys and the normal forms they satisfy.
Question 3¶
Consider relation: R = {A, B, C, D, E, F, G, H, I, J}

and the set of functional dependencies: {AB → C, BD → EF, AD → GH, A → I, H → J}

Find all candidate keys.
Identify the best normal form that R satisfies (1NF, 2NF, 3NF).
If the relation is not in 3NF, decompose it until it becomes 3NF.
At each step, identify a new relation, decompose and re-compute the keys and the normal forms they satisfy.
Question 4¶
Given the sample order form and description below, create the un-normalized form of the data and transform through the steps needed to move into 3NF.

Gallery Customer History Form

Customer Name
    Jackson, Elizabeth        Phone  (555) 867-5309
    123 4th Avenue
    Fonthill, ON, L3J 4S4

Purchases Made
Artist                    Title                       Purchase Date     Sales Price
03 - Carol Channing       Laugh with Teeth            09/17/2000        7000.00
15 - Dennis Frings        South toward Emerald Sea    05/11/2000        1800.00
03 - Carol Channing       At the Movies               02/14/2002        5550.00
15 - Dennis Frings        South toward Emerald Sea    07/15/2003        2200.00
The Gill Art Gallery wishes to maintain data on their customers, artists and paintings. They may have several paintings by each artist in the gallery at one time. Paintings may be bought and sold several times. In other words, the gallery may sell a painting, then buy it back at a later date and sell it to another customer.

Question 5¶
Given the sample forms and description below, create the un-normalized form of the data and transform through the steps needed to move into 3NF. Finally, merge the two views into a unified schema.

View 1¶
Good News Grocers — Price Update List

This report is used by the department managers to update the prices that are displayed in the grocery store for these products.

Department	Product Code	Aisle	Price	Units
Produce	4081	1	0.35	lb
Produce	4027	1	0.90	ea
Produce	4108	1	1.99	lb
Butcher	331100	5	1.50	lb
Butcher	331105	5	2.40	lb
Butcher	332110	5	5.00	lb
Freezer	411100	6	1.00	ea
Freezer	521101	6	1.00	ea
Freezer	866503	6	5.00	ea
Freezer	866504	6	5.00	ea
View 2¶
Good News Grocers — Product Cost Report

This report is used by the grocery store manager to determine the final selling price of their products.

Supplier	Product	Cost	Markup	Price	Dept
21 – Very Veggie	4108 – tomatoes, plum	1.89	5%	1.99	PR
32 – Fab Fruits	4081 – bananas	0.20	75%	0.35	PR
32 – Fab Fruits	4027 – grapefruit	0.45	100%	0.90	PR
32 – Fab Fruits	4851 – celery	1.00	100%	2.00	PR
08 – Meats R Us	331100 – chicken wings	0.50	300%	1.50	BU
08 – Meats R Us	331105 – lean ground beef	0.60	400%	2.40	BU
08 – Meats R Us	332110 – boneless chicken breasts	2.50	100%	5.00	BU
10 – Jerry’s Juice	411100 – orange juice	0.25	400%	1.00	FR
10 – Jerry’s Juice	521101 – apple juice	0.25	400%	1.00	FR
45 – Icey Creams	866503 – vanilla ice cream	2.50	100%	5.00	FR
45 – Icey Creams	866504 – chocolate ice cream	2.50	100%	5.00	FR
Question 6¶
For the following tables, identify what normal form the table is in: 0NF, 1NF, 2NF or 3NF. If it’s not in 3NF, bring it up to 3NF.

Table 1¶
Ship(BoatId, NbrOfPools, YearMade, Tonnage, CompanyId, CompanyName)

The functional dependencies for this table are:

BoatId → NbrOfPools, YearMade, Tonnage, CompanyId, CompanyName
CompanyId → CompanyName
CompanyName → CompanyId
Table 2¶
Inventory(PartNbr, {Warehouse, Location}, QOH, Weight, PartColor)

The functional dependencies for this table are:

PartNbr → Weight, PartColor
PartNbr + Warehouse → QOH   QOH is Quantity On Hand
Warehouse → Location
Sample Data

PartNbr	Warehouse	Location	QOH	Weight	PartColor
01	500	NW	135	11.75	Blue
01	600	SW	210	11.75	Blue
01	800	East	192	11.75	Blue
02	500	NW	75	2.50	Red
02	800	East	45	2.50	Red
03	500	NW	290	21.35	Green
03	600	SW	83	21.35	Green
This format makes the repeating groups easier to see:

PartNbr	Weight	PartColor	Warehouse	Location	QOH
01	11.75	Blue	500	NW	135
600	SW	210
800	East	192
02	2.50	Red	500	NW	75
800	East	45
03	21.35	Green	500	NW	290
600	SW	83
Table 3¶
Hospital(Patient, Insurance, Doctor, {Test, Result})

The functional dependencies for this table are:

Patient → Insurance, Doctor
Patient + Test → Result
Sample Data

Patient	Insurance	Doctor	Test	Result
Tweety	Red Cross	Livingston	Brain Scan	Not Found
Tweety	Red Cross	Livingston	Blood work	Yes and red
Sylvester	Red Shield	Kildare	Cat Scan	Yes he is a Cat
Sylvester	Red Shield	Kildare	X Rays	No broken bones
Sylvester	Red Shield	Kildare	Flea check	None
Table 4¶
Cars(Vin, Make, Style, Price, Year, Color)

The functional dependencies for this table are:

Vin → Make, Style, Price, Year, Color
Sample Data

Vin	Make	Style	Price	Year	Color
1FD56GH8901X	Ford	SUV	55,000	1965	Red
1HC21KQ0733G	Chevy	Sports	18,200	1998	Green
3AS88JV9203K	Dodge	Truck	13,200	1997	Silver
4PL72XD5431M	Ford	Truck	5,500	1996	Blue
8BE24RU7385Y	Ford	Sedan	5,500	1996	Blue
7JU69TD2485R	Dodge	SUV	18,200	1998	Black
0LF83SA6540Z	Dodge	Sedan	500	1990	Rust

Answers:

1. {C,E} are composite candidate key

ii). Check all the NF one by one , 
    1NF - *assuming there are unqiue rows*
    2NF *(no parital dependency on non prime attributes on part of candidate key)*
    Here C, E are candidate keys, but when seeing the relation (C -> A), C a candidate keys determines A ( a non prime attribute)
    So it is not 2NF
    Therefore the given relation is in the 1NF only 

iii).Now decompose
    R1 = (C,E,D)    --> no partial dependency , only D is non key therefore there is no non key -> non key dependency so it is in 3NF
    R2 = (D,B)       --> since the key has one attribute so no partial dependency , 
    R3 = (C,A)      --> Same as R2



B -> F,G,H
A -> D,E
AB -> C,D,E,F,G,H

D -> I, j

So 
i )AB -> C,D,E,F,G,H,I,J
A,B are the candidate Key

ii) 1NF -> 2NF
No
R1 = (A,B,C) AB -> C
R2 = (A,D,E) A -> D,E
R3 = (D,I,J) D -> I, J 
R4 (B,F,G,H) B -> F,G,H

GPT Answer:
AB+ = A,B

AB -> C 
AB -> A,B,C

A -> D,E
AB -> A,B,C,D,E

B -> F
AB -> A,B,C,D,E,F

F -> G,H
A,B -> A,B,C,D,E,F,G,H

D -> I,J
A,B -> A,B,C,D,E,F,G,H,I,J

Therefore A,B is candidate key 

ii) Test to see non prime key attributes are dependent on any one of prime key attribute
Prime -> A,B
NP -> D,E,F,G,H,I,J

but see A -> D,E ( D and E which are non prime are dependent on a part of primary key A)
iii)R1 = (A,B,C) AB -> C
R2 = (A,D,E) A -> D,E
R3 = (D,I,J) D -> I, J 

previously I said , R4 = (B,F,G,H)
B->F ; F -> G,H  Here we have a transitive dependency so this is not in 3NF

R4 = (B,F)
R5 = (F,G,H)
3 ) 
R = a,b,c,d,e,f,g,h,i

a-> I

ab -> i,c
ad -> g,h,i

abd -> c,i,g,h

bd -> e,f
h -> J

abd -> c,e,f,g,h,j,i
i) {A,B,D} are candidate key of whole or primary key 
ii)1NF
iii) 

2NF - 
R1 -> 

a,i
a,b,c
ad,g,h,j
b,d,e,f

3NF

a,i
a,b,c
ad,g,h
b,d,e,f
h,j

ChatGPT: 
AB -> C

BD -> EF

AD -> GH

ABD -> A B C D E F G H
A -> I

ABD -> A B C D E F G H I
H -> J

ABD -> A B C D E F G H I J

i) So Candidate key is composite key of A,B,D

ii ) It is not 2NF, because, A ( part of candidate key) determines Non prime attribute which causes partial dependency

so it is 1NF

iii) R1(A,B,C)
R2(B,D,E,F)
R3(A,D,G,H)
R4(A,I)
R5(H,J)

4) 

Un Normalized Form
This is in 1NF
(Customer_Name, Title, Purchase_Date) -> Candidate KEY
| Customer_Name | Customer_Address | Customer_Phone | Artist | Title | Purchase_Date | Sales_Price |
|-----------------|----------------|----------------|---------|------|---------------|-------------|
| Jackson, Elizabeth | 123 4th Avenue | (555) 867-5309 | 03 - Carol Channing | Laugh with Teeth | 09/17/2000 | 7000.00 |
| Jackson, Elizabeth | 123 4th Avenue | (555) 867-5309 | 15 - Dennis Frings | South toward Emerald Sea | 05/11/2000 | 1800.00 |
| Jackson, Elizabeth | 123 4th Avenue | (555) 867-5309 | 03 - Carol Channing | At the movies | 02/14/2002 | 5550.00 |
| Jackson, Elizabeth | 123 4th Avenue | (555) 867-5309 | 15 - Dennis Frings | South toward Emerald Sea | 07/15/2000 | 2200.00 |

2NF
Customer Table
ID

|ID| Customer_Name | Customer_Address | Customer_Phone |
|--|-----------------|----------------|----------------|
|01| Jackson, Elizabeth | 123 4th Avenue | (555) 867-5309 |

Purchase Table


| Purchase_ID | Artist | Title | Purchase_Date | Sales_Price |Customer_ID|
|------------ |--------|-------|---------------|-------------|--|
| 01 | 03 - Carol Channing | Laugh with Teeth | 09/17/2000 | 7000.00 |01|
| 02 | 15 - Dennis Frings | South toward Emerald Sea | 05/11/2000 | 1800.00 |01|
| 03 | 03 - Carol Channing | At the Movies | 02/14/2002 | 5550.00 |01|
| 04 | 15 - Dennis Frings | South toward Emerald Sea | 07/15/2000 | 2200.00 |01|

3NF
On Checking Relation 1 it follows 3NF
On checking Relation 2 Purchase table it is not following 3NF because Title Determines Artist (Title a non prime attribute determines a another non prime attribute Artist)

So 3NF will be

| Purchase_ID | Title | Purchase_Date | Sales_Price |Customer_ID|
|------------|-------|---------------|-------------|--|
| 01  | Laugh with Teeth | 09/17/2000 | 7000.00 |01|
| 02  | South toward Emerald Sea | 05/11/2000 | 1800.00 |01|
| 03  | At the Movies | 02/14/2002 | 5550.00 |01|
| 04  | South toward Emerald Sea | 07/15/2000 | 2200.00 |01|

Art Table

Title | Artist
------|-------
Laugh with Teeth |03 - Carol Channing 
South toward Emerald Sea | 15 - Dennis Frings |
At the Movies |03 - Carol Channing 


So Resultant Normal Forms are 

Customer Table
ID

|ID| Customer_Name | Customer_Address | Customer_Phone |
|--|-----------------|----------------|----------------|
|01| Jackson, Elizabeth | 123 4th Avenue | (555) 867-5309 |


Purchase Table
| Purchase_ID | Title | Purchase_Date | Sales_Price |Customer_ID|
|------------|-------|---------------|-------------|--|
| 01  | Laugh with Teeth | 09/17/2000 | 7000.00 |01|
| 02  | South toward Emerald Sea | 05/11/2000 | 1800.00 |01|
| 03  | At the Movies | 02/14/2002 | 5550.00 |01|
| 04  | South toward Emerald Sea | 07/15/2000 | 2200.00 |01|

Art Table

Title | Artist
------|-------
Laugh with Teeth |03 - Carol Channing 
South toward Emerald Sea | 15 - Dennis Frings |
At the Movies |03 - Carol Channing 



GPT Answer:
1NF 
| Customer_Name | Customer_Address | Customer_Phone | Artist | Title | Purchase_Date | Sales_Price |
|---|---|---|---|---|---|---:|
| Jackson, Elizabeth | 123 4th Avenue, Fonthill, ON, L3J 4S4 | (555) 867-5309 | 03 - Carol Channing | Laugh with Teeth | 09/17/2000 | 7000.00 |
| Jackson, Elizabeth | 123 4th Avenue, Fonthill, ON, L3J 4S4 | (555) 867-5309 | 15 - Dennis Frings | South toward Emerald Sea | 05/11/2000 | 1800.00 |
| Jackson, Elizabeth | 123 4th Avenue, Fonthill, ON, L3J 4S4 | (555) 867-5309 | 03 - Carol Channing | At the Movies | 02/14/2002 | 5550.00 |
| Jackson, Elizabeth | 123 4th Avenue, Fonthill, ON, L3J 4S4 | (555) 867-5309 | 15 - Dennis Frings | South toward Emerald Sea | 07/15/2003 | 2200.00 |

2NF
The customer information depends only on the customer, rather than on the complete purchase.

| Customer_ID | Customer_Name | Customer_Address | Customer_Phone |
|---|---|---|---|
| C01 | Jackson, Elizabeth | 123 4th Avenue, Fonthill, ON, L3J 4S4 | (555) 867-5309 |


| Purchase_ID | Artist | Title | Purchase_Date | Sales_Price | Customer_ID |
|---|---|---|---|---:|---|
| P01 | 03 - Carol Channing | Laugh with Teeth | 09/17/2000 | 7000.00 | C01 |
| P02 | 15 - Dennis Frings | South toward Emerald Sea | 05/11/2000 | 1800.00 | C01 |
| P03 | 03 - Carol Channing | At the Movies | 02/14/2002 | 5550.00 | C01 |
| P04 | 15 - Dennis Frings | South toward Emerald Sea | 07/15/2003 | 2200.00 | C01 |

Here Purchase_ID is introduced as a surrogate key for the purchase transaction.


3NF
| Customer_ID | Customer_Name | Customer_Address | Customer_Phone |
|---|---|---|---|
| C01 | Jackson, Elizabeth | 123 4th Avenue, Fonthill, ON, L3J 4S4 | (555) 867-5309 |

| Artist_ID | Artist_Name |
|---|---|
| A03 | Carol Channing |
| A15 | Dennis Frings |

| Painting_ID | Artist_ID | Title |
|---|---|---|
| PT01 | A03 | Laugh with Teeth |
| PT02 | A15 | South toward Emerald Sea |
| PT03 | A03 | At the Movies |

| Purchase_ID | Customer_ID | Painting_ID | Purchase_Date | Sales_Price |
|---|---|---|---|---:|
| P01 | C01 | PT01 | 09/17/2000 | 7000.00 |
| P02 | C01 | PT02 | 05/11/2000 | 1800.00 |
| P03 | C01 | PT03 | 02/14/2002 | 5550.00 |
| P04 | C01 | PT02 | 07/15/2003 | 2200.00 |


