import random
from datetime import datetime, timedelta
import sqlite3


class GameLogic:
  def __init__(self, connection):
    self.connection = connection
    self.cursor = self.connection.cursor()
    self.create_used_questions_table()

  def create_used_questions_table(self):
    """Create the used_questions table if it doesn't exist."""
    self.cursor.execute("""
      CREATE TABLE IF NOT EXISTS used_questions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id INTEGER NOT NULL,
                category VARCHAR(40) NOT NULL,
                date_used DATE NOT NULL,
                UNIQUE(question_id, date_used)
            )
        """)
    self.connection.commit()

  def reset_weekly_questions(self):
    prev_week = datetime.now().date() - timedelta(days=7)
    self.cursor.execute("DELETE FROM used_questions WHERE date_used <= ?", (prev_week,))
    self.connection.commit()

  def get_all_categories(self):
    """Get all unique categories from the trivia table."""
    self.cursor.execute("SELECT DISTINCT Topic FROM trivia")
    categories = [row[0] for row in self.cursor.fetchall()]
    return categories

  def get_unused_questions(self, category, date):
    """Get unused questions for a category within the last 7 days."""
    seven_days_ago = date - timedelta(days=7)
    self.cursor.execute("""
            SELECT question_id FROM used_questions
            WHERE category = ? AND date_used > ?
        """, (category, seven_days_ago))
    used_questions_ids = {row[0] for row in self.cursor.fetchall()}

    self.cursor.execute("""
            SELECT ID, Question, Answers FROM trivia WHERE Topic = ?
        """, (category,))
    all_questions = self.cursor.fetchall()
    unused_questions = [
    {"id": q[0], "question": q[1], "answers": q[2].split(';')}
    for q in all_questions if q[0] not in used_questions_ids]

    return unused_questions
  
  def mark_question_as_used(self, question_id, category, date):
        """Mark a question as used."""
        self.cursor.execute("""
            INSERT OR IGNORE INTO used_questions (question_id, category, date_used)
            VALUES (?, ?, ?)
        """, (question_id, category, date))
        self.connection.commit()

  def select_daily_questions(self, questions_per_category=10):
    today = datetime.now().date().isoformat()
    daily_questions = []
    categories = self.get_all_categories()
    for category in categories:
        unused_questions = self.get_unused_questions(category, today)
        if len(unused_questions) < questions_per_category:
            self.cursor.execute("DELETE FROM used_questions WHERE category = ?", (category,))
            self.connection.commit()
            unused_questions = self.get_unused_questions(category, today)
        selected = random.sample(unused_questions, min(len(unused_questions), questions_per_category))
        for question in selected:
            question_id, question_text, answers_str = question
            answers = answers_str.split(';')
            daily_questions.append({
                'category': category,
                'question_id': question_id,
                'question': question_text,
                'answers': answers
            })
            self.cursor.execute("""
                INSERT OR IGNORE INTO used_questions (question_id, category, date_used)
                VALUES (?, ?, ?)
            """, (question_id, category, today))
            self.connection.commit()

    return daily_questions


