from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, g
import sqlite3
import random
import os
from game_logic import GameLogic

app = Flask(__name__)   #app object is created

DATABASE = 'TriviaApp.db'

def get_db_connection():
    """Create a new database connection for this request"""
    if 'db_conn' not in g:
        g.db_conn = sqlite3.connect(DATABASE)
        g.db_conn.row_factory = sqlite3.Row
    return g.db_conn

@app.teardown_appcontext
def close_db_connection(exception):
    """Close the database connection after the request is complete."""
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()

@app.route("/")
def index(): #route for the home page, renders the index.html template
    return render_template("index.html")

@app.route("/api/question/<topic>") #API endpoint to get a random question for a given topic, returns JSON response with question and answers
def get_question(topic):
    conn = get_db_connection()
    game_logic = GameLogic(conn)  # Pass the connection to GameLogic

    try:

        today = datetime.now().date()
        
        # Create temporary table with questions from the topic
        unused_questions = game_logic.get_unused_questions(topic, today)
        
        if not unused_questions:
            return jsonify({"error": f"No unused questions found for topic: {topic}"}), 404
        
        # Select a random question from unused questions
        question = random.choice(unused_questions)
        question_id = question["id"]
        question_text = question["question"]
        answers = question["answers"]


        # Mark the question as used
        game_logic.cursor.execute("""
            INSERT OR IGNORE INTO used_questions (question_id, category, date_used)
            VALUES (?, ?, ?)
        """, (question_id, topic, today))
        game_logic.connection.commit()
        
        return jsonify({
            "id": question_id,
            "question": question_text,
            "answers": answers
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/daily_questions")
def daily_questions():
    """API endpoint to get daily questions."""
    conn = get_db_connection()
    game_logic = GameLogic(conn)  # Pass the connection to GameLogic

    try:
        questions = game_logic.select_daily_questions()
        return jsonify(questions) 
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        pass  # Connection will be closed by the teardown function
    

if __name__ == "__main__": #runs the Flask app on localhost at port 5000 with debug mode enabled
    app.run(host="127.0.0.1", port=5000, debug=True)
