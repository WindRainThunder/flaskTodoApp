import pytest
from app import app

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