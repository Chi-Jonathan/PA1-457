# PA1-457
Database

The program organizes multiple databases by making them into directories. 
These databases can be created and named using the CREATE DATABASE function and it will give a warning if you try to create another database that has the same name as a database already in your current database. 
Tables are made using text files and can be created using the CREATE TABLE function and it will create a table with the given name. Tables in the same database will be unable to have the same name and the program will give a warning if you attempt to do so. 
The program also allows for you to delete databases and tables using the DROP DATABASE/DROP TABLE commands, and will give a warning if the database or table doesn't exist.
These databases can be accessed using the USE command and tables can be updated using the ALTER command. Tables can be read using the SELECT command. Tables' contents are organized by using a | between rows.
I implemented the required functionality by turning each command into a function and help from the OS library. I created directories for each database and .txt files for each table and opened the directory to access the contents and read/write to the text files when needed.

To run use the command:
python3 database.py < PA1_test.sql

PA1_t.sql is the test file with the comments.
