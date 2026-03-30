Steps to set up and run TriviaConnect

1. Clone the repo and ensure that the folder trivia_app exists (or your file name)
1a. Enter that directory by typing cd trivia_app into the terminal (or wherever you stored the files)

2. Create the virtual environment by putting python -m venv .venv into the terminal (skip this if there is already a venv created, go to 2a)
2a. Activate it using .venv\Scripts\activate.ps1 in the terminal 

3. Install Flask (SQLite is built into Python) 
3a. Flask can be installed with the command pip install flask

4. Make sure all the database files are actually there and have questions, answers, etc
4a. Run the databases using the command py populatingdatabase.py (make sure this is run before app.py)

5. Run the app using the command py app.py
5a. The default is host 127.0.0.1, port 5000, and debug = true

6. To stop the live server, hit Ctrl + C in the terminal
