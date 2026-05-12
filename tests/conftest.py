import pytest
from app import app
import sqlite3

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

    conn = sqlite3.connect("databases/todo.db")
    cursor = conn.cursor()

    for username in users_to_delete:
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))

    conn.commit()
    conn.close()

@pytest.fixture
def cleanup_tasks():
    tasks_to_delete = []
    yield tasks_to_delete

    conn = sqlite3.connect("databases/todo.db")
    cursor = conn.cursor()

    for task in tasks_to_delete:
        cursor.execute("DELETE FROM tasks WHERE title = ? and description = ?", (task["title"],task["description"],))

    conn.commit()
    conn.close()