import sqlite3

class Task:
    def __init__(self, id, title, description, user_id):
        self.id = id
        self.title = title
        self.description = description
        self.user_id = user_id

    @classmethod
    def create_task(cls, title, description, user_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (title, description, user_id) VALUES (?, ?, ?)", 
                       (title, description, user_id))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        return cls(task_id, title, description, user_id)

    @classmethod
    def get_tasks_by_user(cls, user_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [cls(*row) for row in rows]

    @classmethod
    def get_task_by_id(cls, task_id, user_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))
        row = cursor.fetchone()
        conn.close()
        if row:
            return cls(*row)
        return None

    def update_task(self, title, description):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET title = ?, description = ? WHERE id = ?", 
                       (title, description, self.id))
        conn.commit()
        conn.close()
        self.title = title
        self.description = description

    def delete_task(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (self.id,))
        conn.commit()
        conn.close()