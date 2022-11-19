#Jonathan Chi
#Created 9/20/2022
#Last updated 11/19/2022
#CS 457 PA1

import os

#This function is responsible for creating the tables and directories 9/20
def create(com):
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  #Checks if creating a database or a table 9/20
  if com[0].upper() == "DATABASE":
    #Checks for a directory with the same name 9/20
    try:
        os.mkdir(com[1])
        print("Database %s created." %com[1])
    except:
      print("!Failed to create database %s because it already exists." %com[1])
  elif com[0].upper() == "TABLE":

    #Checks for a table with same name 9/20
    if os.path.exists(com[1]): 
      print("!Failed to create table %s because it already exists." %com[1])
    else:
      print("Table %s created." %com[1])
      com.pop(0)
      location = com.pop(0)
      vars = (' '.join(str(words) for words in com)[1:-1]).replace(",", " |")
      with open(location, "w") as f:
        f.write(vars + "\n")
  else:
    print("Error: invalid argument.")
      
#This function is responsible for deleting the tables and directories 9/20
def drop(com):
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  #Checks if removing database or table 9/20
  if com[0] == "DATABASE":
    #Checks for a directory with the same name 9/20
    try:
      os.rmdir(com[1])
      print("Database %s deleted." %com[1])
    except:
      print("!Failed to delete %s because it does not exist." %com[1])
  elif com[0] == "TABLE":

    #Checks for a table with matching name 9/20
    try:
      os.remove(com[1])
      print("Table %s deleted." %com[1])
    except:
      print("!Failed to delete %s because it does not exist." %com[1])
  else:
    print("Error: invalid argument.")

#This function is responsible for changing the current directory 9/20
def use(com, cwd):
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  #Checks if we are in the original directory or in a database 9/20
  if cwd == os.getcwd:
    try:
      os.chdir(com[0])
      print("Using database %s." %com[0])
    except:
      print("!Failed to use %s because it does not exist." %com[0])
  else:
    #If not in the original directory, goes back into the original then into the called database 9/20
    try:
      os.chdir(cwd)
      os.chdir(com[0])
      print("Using database %s." %com[0])
    except:
      print("!Failed to use %s because it does not exist." %com[0])


#This function is responsible for displaying a table 10/28
def select(com):
  if com[0] == "*":
    com = semicolon(com)
    if com == 'Error':
      com = takeInput()
      if com == 'Error':
        return None
      
      #Gets a dictionary of name to the table and the join types 11/16
      nameTable, joinType = selectFrom(com)
      if nameTable == -1:
        return None
      com = takeInput()
      if com == 'Error':
        return None
      arg1 = com.pop(0)
      com = semicolon(com)
      if com == 'Error':
        return None

      #Checks for where vs on 11/16
      if arg1 == 'where':
        rowsToDisplay = selectWhere(com, nameTable)
        print(reformat(rowsToDisplay))
      elif arg1 == 'on':
        rowsToDisplay = selectOn(com, nameTable, joinType)
        print(reformat(rowsToDisplay))
      else:
        print("Error: invalid argument.")
        return None

    else:  
      com.pop(0)
      isFrom = com.pop(0)
      location = com.pop(0)
      if isFrom.upper() != "FROM":
        print("Error: invalid argument.")
        return None
      try:
        #reads the table 9/20
        with open(location, "r") as f:
          print(f.read())
      except:
        print("!Failed to use %s because it does not exist." %location)

  #Added functionality to select to allow from specifications for selection 10/28
  else:
    cols = com.copy()
    for i in range(len(cols)):
      cols[i] = cols[i].replace(",", "")
    com = takeInput()
    if com == 'Error':
      return None
    isFrom = com.pop(0)
    location = com.pop(0)
    com = takeInput()
    if com == 'Error':
      return None
    com = semicolon(com)
    if com == 'Error':
      print("!Error: missing semicolon.")
      return None
    isWhere = com.pop(0)
    colToCheck = com.pop(0)
    sign = com.pop(0)
    row = com.pop(0)
    if isFrom.upper() != "FROM" or isWhere.upper() != 'WHERE':
      print("Error: invalid argument.")
      return None

    #Checks if file exists and reads in info
    if os.path.exists(location):
      tableContents = open(location).read()

      #Turns the table into a 2d array this allows for having columns and rows and easily modifying data
      arr = toArray(tableContents)
      colIndexesToDisplay = []
      for col in cols:
        colIndexesToDisplay.append(getColumn(arr, col))
      if -1 in colIndexesToDisplay:
        print("Select parameters incorrect.")
        return None
      colToCheckIndex = getColumn(arr, colToCheck)

      rowIndexes  = getRows(arr, row, colToCheckIndex, sign)
      temp = []
      for i in range(len(rowIndexes)-1, -1, -1):
        temp.append(arr.pop(rowIndexes[i]))
      temp.append(arr[0])
      temp.reverse()
      output = []
      for rowToDisplay in temp:
        singleRowToDisplay = []
        for colToDisplay in colIndexesToDisplay:
          singleRowToDisplay.append(rowToDisplay[colToDisplay])
        output.append(singleRowToDisplay)
      output.append([""])
      print(reformat(output))
    else:
      print("!Failed to use %s because it does not exist." %location)
    
    
#This function is responsible for from argruments in select 11/16
def selectFrom(com):
  isFrom = com.pop(0)
  nameTable = {}
  joinType = []
  arg = ""
  if isFrom.upper() != "FROM":
    print("Error: invalid argument.")
    return (-1, -1)
  while com:
    table = com.pop(0)
    name = com.pop(0)
    #checks for a comma
    if name[-1] == ',':
      name = name[:-1]
    elif com:
      while arg.upper() != 'JOIN':
        arg = com.pop(0)
        joinType.append(arg)
    nameTable[name] = table
  return (nameTable, joinType)
    
#This function is responsible for where argruments in select 11/16    
def selectWhere(com, nameTable):
  section1 = com.pop(0).split('.')
  op = com.pop(0)
  section2 = com.pop(0).split('.')

  #Checks is the tables exist from the name 11/16
  if os.path.exists(nameTable[section1[0]]):
    t1 = open(nameTable[section1[0]]).read()
  else:
    print("!Failed to use %s because it does not exist." %nameTable[section1[0]])
    return -1
  if os.path.exists(nameTable[section2[0]]):
    t2 = open(nameTable[section2[0]]).read()
  else:
    print("!Failed to use %s because it does not exist." %nameTable[section2[0]])
    return -1
  if op == '=':

    #Gets the tables as 2d arrays 11/16
    t1 = toArray(t1)
    t2 = toArray(t2)
    t1.pop()
    t2.pop()
    col1 = getColumn(t1, section1[1])
    col2 = getColumn(t2, section2[1])
    if col1 == -1 or col2 == -1:
      print("Error: Not a column")
      return -1
    vars = t1.pop(0) + t2.pop(0)

    #Finds where the keys match and combine the rows into one row then returns the inner joined table 11/16
    rowsToDisplay = [vars]
    for row1 in t1:
      for row2 in t2:
        if row1[col1] == row2[col2]:
          rowsToDisplay.append(row1+row2)
    rowsToDisplay.append([""])
    return rowsToDisplay
  else:
    print("Error: invalid operation")
    return -1



#This function is responsible for on argruments in select 11/16
def selectOn(com, nameTable, joinType):
  section1 = com.pop(0).split('.')
  op = com.pop(0)
  section2 = com.pop(0).split('.')

  #Checks is the tables exist from the name 11/16
  if os.path.exists(nameTable[section1[0]]):
    t1 = open(nameTable[section1[0]]).read()
  else:
    print("!Failed to use %s because it does not exist." %nameTable[section1[0]])
    return -1
  if os.path.exists(nameTable[section2[0]]):
    t2 = open(nameTable[section2[0]]).read()
  else:
    print("!Failed to use %s because it does not exist." %nameTable[section2[0]])
    return -1
  if op == '=':

    #Gets the tables as 2d arrays 11/16
    t1 = toArray(t1)
    t2 = toArray(t2)
    t1.pop()
    t2.pop()
    col1 = getColumn(t1, section1[1])
    col2 = getColumn(t2, section2[1])
    if col1 == -1 or col2 == -1:
      print("Error: Not a column")
      return -1
    vars = t1.pop(0) + t2.pop(0)
    rowsToDisplay = [vars]

    #Checks for inner join or outer join 11/16
    if joinType[0].upper() == 'INNER' or joinType[1].upper() == 'INNER':
    
      #Finds where the keys match and combine the rows into one row then returns the inner joined table, same as where because inner join is the default 11/16
      for row1 in t1:
        for row2 in t2:
          if row1[col1] == row2[col2]:
            rowsToDisplay.append(row1+row2)
      rowsToDisplay.append([""])
    elif joinType[0].upper() == 'LEFT':
      #Finds where the keys match and combine the rows into one row then adds in the additional rows for the outer join 11/19
      inRowsToDisplay = []
      emptyCols = [''] * len(t2[0])
      for row1 in t1:
        for row2 in t2:
          if row1[col1] == row2[col2]:
            rowsToDisplay.append(row1+row2)
            inRowsToDisplay.append(row1)
      for row1 in t1:
        if row1 not in inRowsToDisplay:
          rowsToDisplay.append(row1 + emptyCols)
      rowsToDisplay.append([""])

    #Returns the rows that are to be shown 11/19
    return rowsToDisplay
  else:
    print("Error: invalid operation")
    return -1


#This function is responsible for changing a table 9/20
def alter(com):
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  if com[0] != "TABLE":
    print("Error: invalid argument.")
  else:
    if com[2] == "ADD":
      if os.path.exists(com[1]):
        com.pop(0)
        location = com.pop(0)
        com.pop(0)
        vars = (' '.join(str(words) for words in com))

        string = open(location).read()
        vars = string[:string.find('\n')] + " | " + vars + string[string.find('\n')+1:]
        with open(location, 'w') as f:
          f.write(vars)
        print("Table %s modified." %location)
      else:
        print("!Failed to use %s because it does not exist." %com[1])

#This function is responsible for inserting data into the table 10/26
def insert(com):
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  if com[0].upper() != 'INTO':
    print("Error: invalid argument.")
  else:
    #Gets command line and checks if the commands are valid
    if os.path.exists(com[1]):
      com.pop(0)
      location = com.pop(0)
      toString = ''.join(com)
      containsValues = toString[:toString.find('(')]
      if containsValues.upper() != 'VALUES':
        print("Error: invalid argument.")
      else:
        #Gets the row of data, formats it, then inputs it into the table
        values = toString[toString.find('(')+1:toString.rfind(')')].replace(',',' | ').replace("'","")
        with open(location, 'a') as f:
          f.write(values + "\n")
        print('1 new record inserted.')

#This function is responsible for updating data in a table 10/27
def update(com):
  
  #Parsing all of the commands input
  location = com.pop(0)

  #Takes in the second line of commands
  com = takeInput()
  if com == 'Error':
    return None
  setter = com.pop(0)
  colToChange = com.pop(0)
  sign1 = com.pop(0)
  nameToChange = com.pop(0).replace("'","")

  #takes in the third line and checks for a semicolon
  com = takeInput()
  if com == 'Error':
    return None
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  where = com.pop(0)
  colToSearch = com.pop(0)
  sign2 = com.pop(0)
  rowName = com.pop(0).replace("'","")
  if sign1 != '=':
    print("Error: need equals.")
    return None
  if setter.upper() == 'SET' and where.upper() == 'WHERE':
    if os.path.exists(location):
      tableContents = open(location).read()

      #Turns the table into a 2d array this allows for having columns and rows and easily modifying data
      arr = toArray(tableContents)

      #Finds the column to change's index
      colIndexChange = getColumn(arr, colToChange)
      if colIndexChange==-1:
        print("Error: not a real column.")
        return None
      colIndexSearch = getColumn(arr, colToSearch)
      if colIndexSearch==-1:
        print("Error: not a real column.")
        return None

      #Gets the indexes of all the rows that need to be changed 
      rowIndexes = getRows(arr, rowName, colIndexSearch, sign2)

      #Iterates through the rows and changes each column that needs to be changed
      for i in rowIndexes:
        arr[i][colIndexChange] = nameToChange

      #Reformats the table's contents to a string
      tableContents = reformat(arr)
      with open(location, 'w') as f:
        f.write(tableContents)
      if len(rowIndexes)==1:
        print("1 record modified.")
      else:
        print("%d records modified." %len(rowIndexes))
    else:
      print("!Failed to use %s because it does not exist." %location)
  else:
    print("Error: invalid argument(s).")

#This function is responsible for deleting data in a table 10/27
def delete(com):

  #Parsing all of the command inputs
  isFrom = com.pop(0)
  location = com.pop(0)

  #Taking more inputs
  com = takeInput()
  if com == 'Error':
    return None
  com = semicolon(com)
  if com == 'Error':
    print("!Error: missing semicolon.")
    return None
  isWhere = com.pop(0)
  colToSearch = com.pop(0)
  sign = com.pop(0)
  row = com.pop(0).replace("'","")
  if isFrom.upper() == 'FROM' and isWhere.upper() == 'WHERE':
    if os.path.exists(location):
      tableContents = open(location).read()

      #Turns the table into a 2d array this allows for having columns and rows and easily modifying data
      arr = toArray(tableContents)
      colIndex = getColumn(arr, colToSearch)

      #Gets the indexes of all the rows that need to be changed 
      rowIndexes = getRows(arr, row, colIndex, sign)

      #Deletes all of the rows
      for i in range(len(rowIndexes)-1, -1, -1):
        arr.pop(rowIndexes[i])

      #Reformats the table's contents to a string
      tableContents = reformat(arr)
      with open(location, 'w') as f:
        f.write(tableContents)
      if len(rowIndexes)==1:
        print("1 record deleted.")
      else:
        print("%d records deleted." %len(rowIndexes))
    else:
      print("!Failed to use %s because it does not exist." %location)
  else:
    print("Error: invalid argument(s).")

  




###################################################################################################################################################
#These are the helper functions

#Takes the input and removes the \r and checks for validity
def takeInput():
  command = input()
  command = command.split()

  if(len(command)==0):
    print("Error: invalid command.")
    return 'Error'
  else:
    if(command[len(command)-1][-1] == '\r'):
      command[len(command)-1] = command[len(command)-1][0:-1]
    return command

#Turns the table into a 2d list 10/26
def toArray(contents):
  newList = []
  temp = [col for col in contents.split('\n')]
  for string in temp:
    newList.append(string.split(' | '))
  return newList

#Turns 2d list into table format 10/26
def reformat(arr):
  newArray = []
  for col in arr:
    newArray.append(' | '.join(col))
  newArray = '\n'.join(newArray)
  return newArray

#Gets the rows that need to be updated in the table 10/26
def getRows(arr, rowName, colIndex, sign):
  rows = []
  count = 1
  temp = arr.pop(0)
  arr.pop()
  if sign == '=':
    for row in arr:
      if row[colIndex]==rowName:
        rows.append(count)
      count+=1
  elif sign == '>':
    for row in arr:
      if float(row[colIndex])>float(rowName):
        rows.append(count)
      count+=1
  elif sign == '<':
    for row in arr:
      if float(row[colIndex])>float(rowName):
        rows.append(count)
      count+=1
  elif sign == '!=':
    for row in arr:
      if row[colIndex]!=rowName:
        rows.append(count)
      count+=1
  
  else:
    print('Error: not a valid sign')
    return 'Error'
  arr.insert(0, temp)
  arr.append([''])
  return rows


#Gets the column that needs to be updated in the table 10/26
def getColumn(arr, argToChange):
  count = -1
  for arg in arr[0]:
    count+=1
    if argToChange == arg.split()[0]:
      break
  return count
  




#Checks for semicolon 9/21
def semicolon(command):
  if(command[len(command)-1][-1] != ';'):
    return 'Error'
  else:
    command[len(command)-1] = command[len(command)-1][0:-1]
    return command
    


def main():
  running = True
  cwd = os.getcwd()
  #Makes it run continuously checking the commands, specifically the first argument. 9/20
  while(running):
    command = input()
    command = command.split()

    if(len(command)==0):
      print("Error: invalid command.")
    else:
      if(command[len(command)-1][-1] == '\r'):
        command[len(command)-1] = command[len(command)-1][0:-1]
      if command[0].upper() == ".EXIT":
        running = False
        print("All done!")
      elif command[0].upper() == "CREATE":
        command.pop(0)
        create(command)
      elif command[0].upper() == "DROP":
        command.pop(0)
        drop(command)
      elif command[0].upper() == "USE":
        command.pop(0)
        use(command, cwd)
      elif command[0].upper() == "SELECT":
        command.pop(0)
        select(command)
      elif command[0].upper() == "ALTER":
        command.pop(0)
        alter(command)
      elif command[0].upper() == "INSERT":
        command.pop(0)
        insert(command)
      elif command[0].upper() == "UPDATE":
        command.pop(0)
        update(command)
      elif command[0].upper() == "DELETE":
        command.pop(0)
        delete(command)
      else:
        print("Error: invalid command.")

if __name__ == "__main__":
  main()