from starlette.testclient import TestClient


def test_login_success(client: TestClient):
    password_plain = "abc123"
    response = client.post(
        "/api/users",
        json={"name": "MariaTest", "email": "mariatest@mail.com", "password": password_plain},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/login",
        json={"email": "mariatest@mail.com", "password": password_plain}
    )

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert "refresh_token" in body



def test_login_invalid_password(client: TestClient):
    password_plain = "abc123"
    response = client.post(
        "/api/users",
        json={"name": "MariaTest2", "email": "mariatest2@mail.com", "password": password_plain},
    )
    assert response.status_code == 200

    response = client.post(
        "/api/login",
        json={"email": "mariatest2@mail.com", "password": "wrongpass"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
