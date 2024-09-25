import sqlite3

class MemoryManager:
    def __init__(self, db_name="assistant_memory.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversation_history
            (id INTEGER PRIMARY KEY AUTOINCREMENT,
             user_input TEXT,
             assistant_response TEXT,
             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
        ''')
        self.conn.commit()

    def update_conversation_history(self, user_input, assistant_response):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO conversation_history (user_input, assistant_response)
            VALUES (?, ?)
        ''', (user_input, assistant_response))
        self.conn.commit()

    def get_conversation_history(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT user_input, assistant_response
            FROM conversation_history
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        return cursor.fetchall()

    def close(self):
        self.conn.close()