import pytest
from run import app
import sqlite3
from app import db
from app.models import Task, User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def test_user():
    return {
        "username": "test",
        "correctPassword": "test",
        "wrongPassword": "123"
    }

@pytest.fixture
def cleanup_users():
    users_to_delete = []

    yield users_to_delete

    for username in users_to_delete:
        user = User.query.filter_by(
        username=username
    ).first()

    if user:
        db.session.delete(user)
        db.session.commit()


     




@pytest.fixture
def cleanup_tasks():
    tasks_to_delete = []

    yield tasks_to_delete

    for task in tasks_to_delete:
        task = Task.query.filter_by(
        title=task["title"],
        description=task["description"]
    ).first()

    if task:
        db.session.delete(task)
        db.session.commit()

    