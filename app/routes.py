from flask import Blueprint, render_template, request, url_for, redirect, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import Task, User

bp = Blueprint("main", __name__)

@bp.route('/')
def index():
    if "user_id" not in session:
        return redirect(url_for(".login"))

    tasks = Task.query.filter_by(user_id=session["user_id"]).order_by(Task.id.desc()).all()

    print("tasks")
    for task in tasks:
        print(type(task))

    return render_template("index.html", tasks=tasks, username=session["username"])
 

@bp.route("/add", methods=["POST"])
def add_task():
    if "user_id" not in session:
        return redirect(url_for(".login"))

    title = request.form.get("title")
    description = request.form.get("description")
    status = "todo"

    task = Task(
        title=title,
        description=description,
        status=status,
        user_id=session["user_id"]
    )

    db.session.add(task)
    db.session.commit()

    return redirect(url_for(".index"))

@bp.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if "user_id" not in session:
        return redirect(url_for(".login"))

    task = Task.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    return redirect(url_for(".index"))

@bp.route("/update/<int:task_id>", methods=["POST"])
def update_task(task_id):
    if "user_id" not in session:
        return redirect(url_for(".login"))

    task = Task.query.filter_by(
        id=task_id,
        user_id=session["user_id"]
    ).first()

    if task:
        task.status = "completed"
        db.session.commit()

    return redirect(url_for(".index"))


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = user.username
            return redirect(url_for(".index"))

        flash("Invalid username or password.")
        return redirect(url_for(".login"))

    return render_template("login.html")

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        if not username or not password:
            flash("Fill in all fields.")
            return redirect(url_for(".register"))

        hashed_password = generate_password_hash(password)

        user = User(username=username, password=hashed_password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists.")
            return redirect(url_for(".register"))

        flash("Account created. You can log in now.")
        return redirect(url_for(".login"))

    return render_template("register.html")


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for(".login"))