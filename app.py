from flask import Flask, render_template, jsonify
import sqlite3
import random
import os

app = Flask(__name__)   #app object is created

def get_db_connection():
    """Create a new database connection for this request"""
    conn = sqlite3.connect('TriviaApp.db')
    conn.row_factory = sqlite3.Row
    return conn

def create_temp_questions_table(conn, topics):
    """Create temp table with questions from specified topics"""
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS tempTopics')

    TempTableSetup = """CREATE TABLE IF NOT EXISTS tempTopics (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Topic VARCHAR(40) NOT NULL,
    Question VARCHAR(100) NOT NULL,
    Answers VARCHAR(200) NOT NULL)"""

    cursor.execute(TempTableSetup)

    # Build a case-insensitive WHERE clause using parameters to avoid SQL injection
    where_clauses = ' OR '.join(['LOWER(Topic) = LOWER(?)' for _ in topics])
    TempTableInsertion = f"""INSERT INTO tempTopics (Topic, Question, Answers)
    SELECT Topic, Question, Answers
    FROM trivia
    WHERE {where_clauses}"""

    cursor.execute(TempTableInsertion, topics)
    conn.commit()
    cursor.close()

def get_question_data(conn, question_id):
    """Get question and answers from temp table"""
    cursor = conn.cursor()
    
    cursor.execute(f'SELECT Question FROM tempTopics WHERE ID = ?', (question_id,))
    question = cursor.fetchone()[0]
    
    cursor.execute(f'SELECT Answers FROM tempTopics WHERE ID = ?', (question_id,))
    answers_str = cursor.fetchone()[0]
    answers = answers_str.split(';')
    
    cursor.close()
    return question, answers

@app.route("/")
def index(): #route for the home page, renders the index.html template
    return render_template("index.html")

@app.route("/api/question/<topic>") #API endpoint to get a random question for a given topic, returns JSON response with question and answers
def get_question(topic):
    conn = None
    try:
        conn = get_db_connection()
        
        # Create temporary table with questions from the topic
        create_temp_questions_table(conn, [topic])
        
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM tempTopics')
        count = cursor.fetchone()[0]
        cursor.close()
        
        if count == 0:
            return jsonify({"error": f"No questions found for topic: {topic}"}), 404
        
        # Get a random question ID
        random_id = random.randint(1, count)
        
        # Get the question data
        question, answers = get_question_data(conn, random_id)
        
        return jsonify({
            "id": random_id,
            "question": question,
            "answers": answers
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__": #runs the Flask app on localhost at port 5000 with debug mode enabled
    app.run(host="127.0.0.1", port=5000, debug=True)