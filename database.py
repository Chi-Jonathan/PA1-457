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
        f.write(vars)
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
  if com[1] != "FROM":
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
        with open(location, 'a') as f:
          f.write(" | " + vars)
        print("Table %s modified." %location)
      else:
        print("!Failed to use %s because it does not exist." %com[1])

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
    command = command.split(" ")

    

    if(command[len(command)-1][-1] == '\r'):
      command[len(command)-1] = command[len(command)-1][0:-1]
    if command[0] == ".EXIT":
      running = False
      print("All done!")
    elif command[0] == "CREATE":
      command.pop(0)
      create(command)
    elif command[0] == "DROP":
      command.pop(0)
      drop(command)
    elif command[0] == "USE":
      command.pop(0)
      use(command, cwd)
    elif command[0] == "SELECT":
      command.pop(0)
      select(command)
    elif command[0] == "ALTER":
      command.pop(0)
      alter(command)
    else:
      print("Error: invalid command.")

if __name__ == "__main__":
  main()