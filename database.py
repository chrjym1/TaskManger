import mysql.connector

class Database:
    def __init__(self, host="localhost", user="root", password="", database="task_manager"):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.create_table()

    def create_table(self):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    priority INT,
                    important BOOLEAN,
                    urgent BOOLEAN,
                    completed BOOLEAN DEFAULT FALSE
                )
            """)
        self.connection.commit()

    def add_task(self, task):
        with self.connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tasks (name, priority, important, urgent, completed)
                VALUES (%s, %s, %s, %s, %s)
            """, (task.name, task.priority, task.important, task.urgent, task.completed))
        self.connection.commit()

    def get_tasks(self):
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM tasks")
            return cursor.fetchall()

    def update_task(self, task_id, **kwargs):
        columns = ", ".join([f"{k} = %s" for k in kwargs.keys()])
        values = list(kwargs.values()) + [task_id]
        with self.connection.cursor() as cursor:
            cursor.execute(f"UPDATE tasks SET {columns} WHERE id = %s", values)
        self.connection.commit()

    def delete_task(self, task_id):
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        self.connection.commit()
