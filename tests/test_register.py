def test_register_page_opens(client):
    response = client.get("/register")

    assert response.status_code == 200

def test_register_creates_user(client, cleanup_users):
    username = "testRegister"
    password = "testRegisterPassword"

    response = client.post(
        "/register",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=True,
    )

    cleanup_users.append(username)
    text = response.get_data(as_text=True).lower()    

    assert len(response.history) >= 1
    assert response.history[0].status_code in (302, 303)    
    assert response.history[0].headers["Location"].endswith("/login")
    assert response.request.path == "/login"    
    assert response.status_code == 200
    assert "account created. you can log in now." in text

def test_register_creates_user_with_existing_username(client, test_user):
    username = test_user["username"]
    password = test_user["correctPassword"]

    response = client.post(
        "/register",
        data={
            "username": username,
            "password": password,
        },
        follow_redirects=True,

    )

    text = response.get_data(as_text=True).lower()

    assert response.status_code == 200    
    assert ("username already exists." in text)
    
    

