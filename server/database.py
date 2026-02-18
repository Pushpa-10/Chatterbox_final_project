import sqlite3
from contextlib import closing

DB_PATH = "chat.db"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()


def get_user(username):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("SELECT * FROM users WHERE username=?", (username,))
        return cursor.fetchone()


def add_user(username, password):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
        conn.commit()


def save_message(username, message):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        conn.execute("INSERT INTO messages (username,message) VALUES (?,?)", (username, message))
        conn.commit()


def get_recent_messages(limit=20):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        cursor = conn.execute("SELECT username, message, timestamp FROM messages ORDER BY id DESC LIMIT ?", (limit,))
        return cursor.fetchall()
