import TriviaDatabases
import sqlite3

connection = sqlite3.connect('TriviaApp.db')
cursor = connection.cursor()

#This program should use a proper test case library and will probably get updated to do so but I don't have 
#the time for that at the moment so this will instead be a crude testing program.

#The following lines of code allow the tester to reset the trivia table and test that the insert row, remove row, and create questions table functions are working.

TriviaDatabases.get_answers('trivia','15')

choice = input('\nReset Trivia Table? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.clear_table('trivia')

choice = input('\nreset trivia table and test insert? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.clear_table('trivia')

    TriviaDatabases.insert_row('trivia',['test0','This is a question','ans;anw;asw;ane'])
    TriviaDatabases.insert_row('trivia',['test0','This is another question','ans;anw;asw;ane'])

    TriviaDatabases.insert_row('trivia',['test1','This is a prompt','ans;anw;asw;ane'])
    TriviaDatabases.insert_row('trivia',['test1','This is another prompt','ans;anw;asw;ane'])

    TriviaDatabases.insert_row('trivia',['test2','This is a query','ans;anw;asw;ane'])
    TriviaDatabases.insert_row('trivia',['test2','This is another query','ans;anw;asw;ane'])


choice = input('\nPrint Trivia Table? (Y/N)\n')
if choice == 'y':
    print('\n    Trivia Table contents:')

    cursor.execute('SELECT * FROM trivia')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

choice = input('\nTest removing rows? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.remove_row('trivia','3')

    cursor.execute('SELECT * FROM trivia')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

choice = input('\nTest temp table creation? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.create_questions_table(['test0','test1'])

    cursor.execute('SELECT * FROM tempTopics')
    rows = cursor.fetchall()
    for row in rows:
        print(row)

choice = input('\nTest trivia table population? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.populate_trivia('QAmusic.txt','music')


choice = input('\nPrint Trivia Table? (Y/N)\n')
if choice == 'y':
    print('\n    Trivia Table contents:')

    cursor.execute('SELECT * FROM trivia')
    rows = cursor.fetchall()
    for row in rows:
        print(row)


choice = input('\nTest data insertion and collection with accounts table? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.delete_table('accounts')
    TriviaDatabases.create_accounts_table()

    TriviaDatabases.insert_row('accounts',['user1','abcde'])
    TriviaDatabases.insert_row('accounts',['user2','rjust'])
    TriviaDatabases.insert_row_commited('accounts',['user3','eksmy'])

    print(f'ID:2 username: {TriviaDatabases.get_username('2')}\npassword: {TriviaDatabases.get_password('2')}\n ID of user1: {TriviaDatabases.get_ID('user1')}')

TriviaDatabases.end_connection()

