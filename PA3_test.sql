CREATE DATABASE CS457_PA3;
USE CS457_PA3;
create table Employee (id int, name varchar(10));
create table Sales (employeeID int, productID int);
insert into Employee values(1,'Joe');
insert into Employee values(2,'Jack');
insert into Employee values(3,'Gill');
insert into Sales values(1,344);
insert into Sales values(1,355);
insert into Sales values(2,544);
select * 
from Employee E, Sales S 
where E.id = S.employeeID;
select * 
from Employee E inner join Sales S 
on E.id = S.employeeID;
select * 
from Employee E left outer join Sales S 
on E.id = S.employeeID;
.exit
