# PA-457
Database

PA1:
The program organizes multiple databases by making them into directories. 
These databases can be created and named using the CREATE DATABASE function and it will give a warning if you try to create another database that has the same name as a database already in your current database. 
Tables are made using text files and can be created using the CREATE TABLE function and it will create a table with the given name. Tables in the same database will be unable to have the same name and the program will give a warning if you attempt to do so. 
The program also allows for you to delete databases and tables using the DROP DATABASE/DROP TABLE commands, and will give a warning if the database or table doesn't exist.
These databases can be accessed using the USE command and tables can be updated using the ALTER command. Tables can be read using the SELECT command. Tables' contents are organized by using a | between rows.
I implemented the required functionality by turning each command into a function and help from the OS library. I created directories for each database and .txt files for each table and opened the directory to access the contents and read/write to the text files when needed.

To run use the command:
python3 database.py < PA1_test.sql

PA1_t.sql is the test file with the comments.

PA2:
The program stores tuples in the table as separate lines, or in the code, a string being separated by \n, \n representing the end of a tuple.
Each tuple has different columns, those columns being separated by a "|"
Insertion is handled by opening the table passed in, formatting the tuple with the \n at the end and "|" separating each column, then appends the tuple, that is now correctly formatted, to the table.
Deletion is handled by waiting until all the information is entered, then reformatting the table to a 2d array, then searching by row in the appropriate column for the row indexes to delete, then that tuple is removed from the 2d array, reformatted, and written to the table.
Modification is handled by waiting until all the information is entered, then reformatting the table to a 2d array, then searching by row in the appropriate column for the row indexes that needs to be updated. The 2d array at the specific row and column is then updated with the information. Then the 2d array is reformatted and written to the table.
Query is handled by waiting until all the information is entered, then, reformatting the table to a 2d array, then gets all of the columns that need to be queried, then searches for the rows that will be included in that query. It reformats the 2d array now having only the needed columns and rows, then queries the informamtion.

To run use the command:
python3 database.py < PA2_test.sql

PA2_t.sql is the test file with the comments.