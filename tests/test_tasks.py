import sqlite3

def login(client):
    return client.post(
        "/login",
        data={"username": "test", "password": "test"},
        follow_redirects=True,
    )

def test_add_note(client, cleanup_tasks):   
    login(client)
    title = "Shopping"
    description = "Buy milk"
    response = client.post(
        "/add",
        data={"title": title, "description": description},
        follow_redirects=True,
    )
    cleanup_tasks.append({"title":title, "description":description})
    text = response.get_data(as_text=True).lower()    

    assert response.status_code == 200
    assert "shopping" in text



         