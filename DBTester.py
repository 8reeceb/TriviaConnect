import TriviaDatabases
import sqlite3
import time

connection = sqlite3.connect('TriviaApp.db')
cursor = connection.cursor()

#This program should use a proper test case library and will probably get updated to do so but I don't have 
#the time for that at the moment so this will instead be a crude testing program.

#The following lines of code allow the tester to reset the trivia table and test that the insert row, remove row, and create questions table functions are working.


choice = input('\nreset trivia table and test insert? (Y/N)\n')
if choice == 'y':
    TriviaDatabases.clear_table('trivia')

    TriviaDatabases.insert_row('trivia',['test0','This is a question','ans;anw;asw;ane'])
    TriviaDatabases.insert_row('trivia',['test0','This is another question','ans;anw;asw;ane'])

    TriviaDatabases.insert_row('trivia',['test1','This is a prompt','ans;anw;asw;ane'])
    TriviaDatabases.insert_row('trivia',['test1','This is another prompt','ans;anw;asw;ane'])

    TriviaDatabases.insert_row('trivia',['test2','This is a query','ans;anw;asw;ane'])
    TriviaDatabases.insert_row('trivia',['test2','This is another query','ans;anw;asw;ane'])

print('\n    Trivia Table contents:')

cursor.execute('SELECT * FROM trivia')
rows = cursor.fetchall()
for row in rows:
    print(row)

print('\n     Test remove rows:\n')
TriviaDatabases.remove_row('trivia','3')

cursor.execute('SELECT * FROM trivia')
rows = cursor.fetchall()
for row in rows:
    print(row)

print('\n     Test Temp Table creation:\n')
TriviaDatabases.create_questions_table(['test0','test1'])

cursor.execute('SELECT * FROM tempTopics')
rows = cursor.fetchall()
for row in rows:
    print(row)
