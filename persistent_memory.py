import sqlite3
import json
import threading
from datetime import datetime

class PersistentMemory:
    def __init__(self, db_path='chat_memory.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    user_id TEXT,
                    role TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def append(self, user_id, role, message):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO chat_history (user_id, role, message)
                VALUES (?, ?, ?)
            ''', (user_id, role, message))
            conn.commit()

    def get(self, user_id, limit=20):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT role, message FROM chat_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (user_id, limit))
            rows = cursor.fetchall()
            return [{"role": row[0], "content": row[1]} for row in reversed(rows)]

    def clear(self, user_id):
        with self.lock, sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
            conn.commit()

    def build_chat_context(self, user_id, system_prompt):
        history = self.get(user_id)
        context = [{"role": "system", "content": system_prompt}]
        context.extend(history)
        return context
