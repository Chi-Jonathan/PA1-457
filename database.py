#Jonathan Chi
#Created 9/20/2022
#CS 457 PA1

import os

#This function is responsible for creating the tables and directories 9/20
def create(com):
  com = semicolon(com)
  if com == 'Error':
    return None
  #Checks if creating a database or a table 9/20
  if com[0] == "DATABASE":
    #Checks for a directory with the same name 9/20
    try:
        os.mkdir(com[1])
        print("Database %s created." %com[1])
    except:
      print("!Failed to create database %s because it already exists." %com[1])
  elif com[0] == "TABLE":

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

#This function is responsible for allowing us to see a table 9/20
def select(com):
  com = semicolon(com)
  if com == 'Error':
    return None
  #Checks if arguments are valid 9/20
  if com[1].upper() != "FROM":
    print("Error: invalid argument.")
  else:
    if com[0] == "*":
      try:

        #reads the table 9/20
        with open(com[2], "r") as f:
          print(f.read())
      except:
        print("!Failed to use %s because it does not exist." %com[2])

#This function is responsible for changing a table 9/20
def alter(com):
  com = semicolon(com)
  if com == 'Error':
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
  setter = com.pop(0)
  colToChange = com.pop(0)
  sign1 = com.pop(0)
  nameToChange = com.pop(0).replace("'","")
  #takes in the third line and checks for a semicolon
  com = takeInput()
  com = semicolon(com)
  if com == 'Error':
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
      arr.append([''])

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
  isFrom = com.pop(0)
  location = com.pop(0)
  com = takeInput()
  com = semicolon(com)
  if com == 'Error':
    return None
  isWhere = com.pop(0)
  colToSearch = com.pop(0)
  sign = com.pop(0)
  row = com.pop(0).replace("'","")
  if isFrom.upper() == 'FROM' and isWhere == 'WHERE':
    tableContents = open(location).read()
    arr = toArray(tableContents)
    colIndex = getColumn(arr, colToSearch)

  




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
  count = 0
  arr.pop()
  print(rowName)
  if sign == '=':
    for row in arr:
      print(row)
      if row[colIndex]==rowName:
        rows.append(count)
      count+=1
  elif sign == '>':
    for row in arr:
      if int(row[colIndex])>int(rowName):
        rows.append(count)
      count+=1
  elif sign == '<':
    for row in arr:
      if int(row[colIndex])>int(rowName):
        rows.append(count)
      count+=1
  else:
    print('Error: not a valid sign')
    return 'Error'
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
    print("!Error: missing semicolon.")
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