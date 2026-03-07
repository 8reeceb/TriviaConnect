import random
from datetime import datetime, timedelta
import sqlite3

questions = "" #path to database

class GameLogic:
  def __init__(self):
    self.connection = sqlite3.connect(questions)
    self.cursor = self.connection.cursor()
    self.create_used_questions_table()

  def used_questions_table(self):
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
    self.cursor.execute("DELETE FROM used_questions WHERE date_used <= ?", (one_week_ago,))
    self.connection.commit()

  def get_all_categories(self):
    self.cursor.execute("SELECT DISTINCT Topic FROM trivia")
    categories = [row[0] for row in self.cursor.fetchall()]
    return categories

  def get_unused_questions(self, category, date):
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
    unused_questions = [q for q in all_questions if q[0] not in used_question_ids]
    return unused_questions

