from flask import Flask, render_template, request, url_for, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__, static_folder="assets")
app.secret_key = "ptakiLatajaKluczem"


def get_db_connection():
    conn = sqlite3.connect(".\\databases\\todo.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    return conn

@app.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for("login"))    
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks where user_id = ? ORDER BY id DESC", (session["user_id"],)).fetchall()
    
    #DEBUG
    print("tasks")
    for task in tasks:
        print(type(task))

    conn.close()
    return render_template('index.html', tasks=tasks, username=session["username"])
 

@app.route("/add", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    title = request.form.get("title")
    description = request.form.get("description")
    status = "todo"

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, description, status, user_id) VALUES (?, ?, ?, ?)",
        (title, description, status, session["user_id"])
    )
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ? and user_id = ?", (task_id,session["user_id"],))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))

@app.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    conn = get_db_connection()
    conn.execute("UPDATE tasks SET status = 'completed' WHERE id = ? and user_id = ?", (task_id,session["user_id"],))
    conn.commit()
    conn.close()

    return redirect(url_for("index"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        connection = get_db_connection()
        user = connection.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        connection.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("index"))

        flash("Invalid username or password.")
        return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            flash("Fill in all fields.")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect(".\\databases\\todo.db")
        try:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            flash("Username already exists.")
            conn.close()
            return redirect(url_for("register"))

        conn.close()
        flash("Account created. You can log in now.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)