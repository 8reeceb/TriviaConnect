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
#string consisting of 40 or less characters, they cannot be empty and the
#username must be a unique entry to the table. IF a non unique entry is added
#the code will throw an error, making "Try Exept" statements very encouraged.
def create_accounts_table():
    accountTableSetup = """CREATE TABLE IF NOT EXISTS accounts (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username VARCHAR(40) NOT NULL UNIQUE,
    Password VARCHAR(40) NOT NULL)"""
    cursor.execute(accountTableSetup)
    connection.commit()


#Similar to the account table but with collumns: ID, Topic, Question, and Answers.
#All are self explanatory but Answers need to be formatted very particularly.
#I'm thinking a format where 4 answers are split by ;'s, code can then break the
#one string down into four, one for each answer, and the first can always be the correct
#one with code randomizing where it goes.

#Answers EX: "Correct answer;Trick Answer;False Answer;Wrong Answer"
#And then split(';') can be used.
def create_trivia_table():
    TriviaTableSetup = """CREATE TABLE IF NOT EXISTS trivia (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Topic VARCHAR(40) NOT NULL,
    Question VARCHAR(100) NOT NULL,
    Answers VARCHAR(200) NOT NULL)"""
    cursor.execute(TriviaTableSetup)
    connection.commit()


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

    

#----------------------------------
#
#   Retrieving table data
#
#----------------------------------


#The following three functions return their respective column from the 
#target table and target ID. table can be either the main trivia table or
#the tempTopics table
def get_topic(table,ID):
    cursor.execute(f'SELECT Topic FROM {table} WHERE ID = (?)',(ID,))
    question = cursor.fetchall()
    return question[0][0]

def get_question(table,ID):
    cursor.execute(f'SELECT Question FROM {table} WHERE ID = (?)',(ID,))
    question = cursor.fetchall()
    return question[0][0]

#This specific function returns the answers as a 4 element array.
def get_answers(table,ID):
    cursor.execute(f'SELECT Answers FROM {table} WHERE ID = (?)',(ID,))
    answers = cursor.fetchall()[0][0]
    return answers.split(';')


#These functions are similar to the ones above but they get data from the
#accounts table instead of the trivia table. Since there is only one
#accounts table these only need an ID instead of that and the table name
def get_username(ID):
    cursor.execute(f'SELECT Username FROM accounts WHERE ID = (?)',(ID,))
    user = cursor.fetchall()
    return user[0][0]
    
def get_password(ID):
    cursor.execute(f'SELECT Password FROM accounts WHERE ID = (?)',(ID,))
    password = cursor.fetchall()
    return password[0][0]

#This function is the inverse of the get_username function, it can come
#in handy for finding the ID of a specific user for the purpose of finding
#their password.
def get_ID(User):
    cursor.execute(f'SELECT ID FROM accounts WHERE Username = (?)',(f"""{User}""",))
    ID = cursor.fetchall()
    return ID[0][0]
          

#----------------------------------
#
#   Inserting and removing rows
#
#----------------------------------

#Calling this with the desired table's name and a valid row will add the row into the target table
#while returning the ID of the new row. This function does not auto commit it's changes so connection.commit()
#needs to be called once all desired changes are made.
def insert_row(table,entry):
    if table == 'accounts':
        Username = entry[0]
        Password = entry[1]

        try:
            cursor.execute('INSERT INTO accounts (Username, Password) VALUES (?, ?)' ,(f"""{Username}""", f"""{Password}"""))
            cursor.execute('SELECT last_insert_rowid()')
            result = cursor.fetchall()
            returnVal = result[0][0]
        except Exception as e:
            print(e)
            #print('an error occured while attempting to register this account.\n')
            #returnVal = None
    
    elif table == 'trivia':
        Topic = entry[0]
        Question = entry[1]
        Answers = entry[2]

        try:
            cursor.execute('INSERT INTO trivia (Topic, Question, Answers) VALUES (?, ?, ?)' ,(f"""{Topic}""", f"""{Question}""", f"""{Answers}"""))
            connection.commit()
            cursor.execute('SELECT last_insert_rowid()')
            result = cursor.fetchall()
            returnVal = result[0][0]
        except Exception as e:
            print(e)
            returnVal = None

#This function does the same thing as the above one but it commits the change immediatly on being called.
#Since committing changes takes some resources, the above function should be used if you plan to add
#many entries, and this one should be used if you plan to add very few.
def insert_row_commited(table,entry):
    if table == 'accounts':
        Username = entry[0]
        Password = entry[1]

        try:
            cursor.execute('INSERT INTO accounts (Username, Password) VALUES (?, ?)' ,(f"""{Username}""", f"""{Password}"""))
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
            cursor.execute('INSERT INTO trivia (Topic, Question, Answers) VALUES (?, ?, ?)' ,(f"""{Topic}""", f"""{Question}""", f"""{Answers}"""))
            connection.commit()
            cursor.execute('SELECT last_insert_rowid()')
            result = cursor.fetchall()
            returnVal = result[0][0]
        except Exception as e:
            print(e)
            returnVal = None


#Removes all data from a table
def clear_table(table):
    try:
        cursor.execute(f'DELETE FROM {table}')
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name = '{table}';")
        connection.commit()
    except Exception as e:
        print(e)

def delete_table(table):
    try:
        cursor.execute(f'DROP TABLE {table}')
        connection.commit
    except Exception as e:
        print(f'Could not drop table with error:\n{e}')


#Removes a row from a targeted table using a targeted ID. Will probably
#be mostly used for removing accounts from the accounts table.
def remove_row(table,id):
    try:
        cursor.execute(f'DELETE FROM {table} WHERE ID = {id}')
        connection.commit()
    except:
        print('an error occured while attempting to add this question.\n')


#This function populates the trivia table with questions and answers from
#a provided txt document. the filename can only be the direct name of the file
#if the file is located in the same area as TriviaDatabases.py. If it's not then
#fileName has to be the path to the file instead. 
#Topic should be all lowercase.
def populate_trivia(fileName,topic):
    try:
        cursor.execute(f"DELETE FROM trivia WHERE Topic = '{topic}'")
        connection.commit()
    except Exception as e:
        print(e)

    with open(fileName, 'r', encoding='utf-8') as txt:
        i = 0
        question = ''
        answers = ''
        added = 0
        for line in txt:
            if i == 0:
                question = line[:-1]
                i += 1
            else:
                if i == 1:
                    answers += (line[:-1])
                    i += 1
                else:
                    answers += (';' + line[:-1])
                    i += 1
            if i == 5:
                try:
                    cursor.execute(f'INSERT INTO trivia (Topic, Question, Answers) VALUES (?,?,?)',(f"""{topic}""",f"""{question}""",f"""{answers}""",))
                    i = 0
                    added += 1
                    question = ''
                    answers = ''
                except Exception as e:
                    print(e)
        
        connection.commit()
        print(f'Added {added} entries to Trivia.')






            

            
#----------------------------------
#   Termination Function
#----------------------------------

#Removes the program's open connection to the database and cursor.
#This should ALWAYS be called before the program terminates.
def end_connection():
    connection.close()
