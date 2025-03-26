import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

    @classmethod
    def create_user(cls, username, password):
        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        conn.close()

    def verify_password(self, password):
        return check_password_hash(self.password, password)
