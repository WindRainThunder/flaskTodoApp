def test_login_page_opens(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_login_with_bad_password_shows_error(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["username"], "password": test_user["wrongPassword"]},
        follow_redirects=True,
    )
    assert response.status_code == 200
    text = response.get_data(as_text=True).lower()
    assert ("invalid username or password." in text
    )

def test_login_with_good_data_redirects_to_index(client, test_user):
    response = client.post(
        "/login",
        data={"username": test_user["username"], "password": test_user["correctPassword"]},
        follow_redirects=False,
    )
    
    assert response.status_code in (302, 303)
    assert response.headers["Location"].endswith("/")