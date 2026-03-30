import TriviaDatabases

TriviaDatabases.delete_table('Sports')

# Step 1: Create the trivia table
TriviaDatabases.create_trivia_table()

# Step 2: Populate the table with questions from a text file
TriviaDatabases.populate_trivia('data/QAsports.txt', 'Sports')

'''# Step 3: Verify the data
TriviaDatabases.cursor.execute('SELECT * FROM trivia')
rows = TriviaDatabases.cursor.fetchall()
for row in rows:
    print(row)'''

TriviaDatabases.delete_table('History')

# Step 1: Create the trivia table
TriviaDatabases.create_trivia_table()

# Step 2: Populate the table with questions from a text file
TriviaDatabases.populate_trivia('data/QAHistory.txt', 'History')

TriviaDatabases.delete_table('Movies')

# Step 1: Create the trivia table
TriviaDatabases.create_trivia_table()

# Step 2: Populate the table with questions from a text file
TriviaDatabases.populate_trivia('data/QAMovies.txt', 'Movies')

TriviaDatabases.delete_table('Music')

# Step 1: Create the trivia table
TriviaDatabases.create_trivia_table()

# Step 2: Populate the table with questions from a text file
TriviaDatabases.populate_trivia('data/QAmusic.txt', 'Music')

TriviaDatabases.delete_table('Science')

# Step 1: Create the trivia table
TriviaDatabases.create_trivia_table()

# Step 2: Populate the table with questions from a text file
TriviaDatabases.populate_trivia('data/QAscience.txt', 'Science')

TriviaDatabases.delete_table('TV')  

# Step 1: Create the trivia table
TriviaDatabases.create_trivia_table()

# Step 2: Populate the table with questions from a text file
TriviaDatabases.populate_trivia('data/QAtv.txt', 'TV')

# Step 4: End the connection
TriviaDatabases.end_connection()