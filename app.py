from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__, static_folder="assets")


def get_db_connection():
    conn = sqlite3.connect(".\\databases\\todo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    
    #DEBUG
    print("tasks")
    for task in tasks:
        print(type(task))

    conn.close()
    return render_template('index.html', tasks=tasks)
 

@app.route("/add", methods=["POST"])
def add_task():
    title = request.form.get("title")
    description = request.form.get("description")
    status = "todo"

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, description, status) VALUES (?, ?, ?)",
        (title, description, status)
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status = 'completed' WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)