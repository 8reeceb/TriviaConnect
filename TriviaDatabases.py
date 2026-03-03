import sqlite3

#Establishes a connection and a cursor for the 'TriviaApp' database, 
#If such a database doesn't exist then this code creates one.
connection = sqlite3.connect('TriviaApp.db')
cursor = connection.cursor()




cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        
tables = cursor.fetchall()
        
if tables:
    print(f"Tables in TriviaApp:")
    # Iterate and print each table name
    for table in tables:
        print(f"- {table[0]}")
else:
    print(f"No tables found in TriviaApp.")


#----------------------------------
#
#   Creating tables
#
#----------------------------------


#Creates the accounts table with 4 collumns: ID, Username, and Password.
#When adding an entry, ID is automatically attributed but the others can be any 
#string consisting of 40 or less characters, they cannot be empty and both Email
#and Username must be unique entries to the table. IF a non unique entry is added
#the code will throw an error, making "Try Exept" statements very encouraged.
accountTableSetup = """CREATE TABLE IF NOT EXISTS accounts (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Username VARCHAR(40) NOT NULL UNIQUE,
Password VARCHAR(40) NOT NULL)"""
cursor.execute(accountTableSetup)


#Similar to the account table but with collumns: ID, Topic, Question, and Answers.
#All are self explanatory but Answers need to be formatted very particularly.
#I'm thinking a format where 4 answers are split by ;'s, code can then break the
#one string down into four, one for each answer, and the first can always be the correct
#one with code randomizing where it goes.

#Answers EX: "Correct answer;Trick Answer;False Answer;Wrong Answer"
#And then split(';') can be used.
TriviaTableSetup = """CREATE TABLE IF NOT EXISTS trivia (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
Topic VARCHAR(40) NOT NULL,
Question VARCHAR(100) NOT NULL,
Answers VARCHAR(200) NOT NULL)"""
cursor.execute(TriviaTableSetup)


#Creates a temporary table consisting of a number of topics, can be used to isolate
#desired questions from undesired questions and is formatted to allow gamemodes where
#more than one topic exists at a time.
def create_questions_table(topics):
    cursor.execute('DROP TABLE IF EXISTS tempTopics')

    query_parameter = ''
    i = 1
    for topic in topics:
        if i == 1:
            query_parameter += f"Topic = '{topic}'"
        else:
            query_parameter += f" OR Topic = '{topic}'"
        i += 1
    
    
    TempTableSetup = """CREATE TABLE IF NOT EXISTS tempTopics (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Topic VARCHAR(40) NOT NULL,
    Question VARCHAR(100) NOT NULL,
    Answers VARCHAR(200) NOT NULL)"""

    cursor.execute(TempTableSetup)

    TempTableInsertion = f"""INSERT INTO tempTopics (
    Topic, Question, Answers)
    SELECT Topic, Question, Answers
    FROM trivia
    WHERE {query_parameter}"""

    cursor.execute(TempTableInsertion)
    connection.commit()

    #cursor.execute(f'SELECT * FROM tempTopics')
    #rows = cursor.fetchall()
    #for row in rows:
    #    print(row)

#----------------------------------
#
#   Inserting and removing rows
#
#----------------------------------

#Calling this with the desired table's name and a valid row will add the row into the target table
#while returning the ID of the new row.
def insert_row(table,entry):
    if table == 'accounts':
        Username = entry[0]
        Password = entry[1]

        try:
            cursor.execute('INSERT INTO accounts (Username, Password) VALUES (?, ?)' ,(Username, Password))
            connection.commit()
            cursor.execute('SELECT last_insert_rowid()')
            result = cursor.fetchall()
            returnVal = result[0][0]
        except:
            print('an error occured while attempting to register this account.\n')
            returnVal = None
    


    elif table == 'trivia':
        Topic = entry[0]
        Question = entry[1]
        Answers = entry[2]

        try:
            cursor.execute('INSERT INTO trivia (Topic, Question, Answers) VALUES (?, ?, ?)' ,(Topic, Question, Answers))
            connection.commit()
            cursor.execute('SELECT last_insert_rowid()')
            result = cursor.fetchall()
            returnVal = result[0][0]
        except Exception as e:
            print(e)
            returnVal = None

    #return returnVal


#Removes all data from a table
def clear_table(table):
    try:
        cursor.execute(f'DELETE FROM {table}')
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table}';")
    except Exception as e:
        print(e)


#Removes a row from a targeted table using a targeted ID. Will probably
#be mostly used for removing accounts from the accounts table.
def remove_row(table,id):
    try:
        cursor.execute(f'DELETE FROM {table} WHERE ID = {id}')
        connection.commit()
    except:
        print('an error occured while attempting to add this question.\n')
            

            
#----------------------------------
#   Termination Function
#----------------------------------

#Removes the program's open connection to the database and cursor.
#This should ALWAYS be called before the program terminates.
def end_connection():
    connection.close()
    cursor.close()