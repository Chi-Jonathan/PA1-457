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


PA3:
The program for first gets the from arguments and assigns each name to a table using a dictionary and gets puts the join arguments into a list.
It then checks the next line to see if it is where or on.
If it is where then it goes to the selectWhere function and passes it the name table dictionary and the final line of commands. This function does a default inner join by first getting the tables into a 2d array form and getting the columns we want to compare. It then checks the table arrays row by row for each specified column and if they match it takes those two rows, combines them and appends them to a new 2d array, that being the rows to display. It then returns that 2d array of rows to display.
If it is on then it goes to the selectOn function and passes it the name table dictionary, the final line of commands, and the join commands list. If it is an inner join then it does the exact same thing as the selectWhere function. If it is an outer join then it gets the tables as 2d arrays and the columns to compare. It then reads the join commands list to find what kind of join is needed. For the left outer join that is needed on this assignment it checks the table arrays row by row while comparing the specified columns and combines the matching ones, while having a separate list containing all of the rows that are going to be displayed for table 1 if it is a left outer join. It then appends the rest of the rows to the rows to display output from table 1 that didn't have a match and returns that 2d array of rows to display.
The select function then takes the rows to display and reformats the array then prints it.

To run use the command:
python3 database.py < PA3_test.sql

PA3_t.sql is the test file with the comments.