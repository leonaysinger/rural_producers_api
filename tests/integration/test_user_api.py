import uuid

from starlette.testclient import TestClient


def test_create_user_route(client: TestClient) -> None:
    response = client.post(
        "/api/users",
        json={"name": "Maria", "email": "maria@mail.com", "password": "secret123"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "maria@mail.com"
    assert "id" in data


def test_create_user_duplicate_email(client: TestClient) -> None:
    client.post(
        "/api/users",
        json={"name": "João", "email": "joao@mail.com", "password": "abc123"},
    )

    response = client.post(
        "/api/users",
        json={"name": "João 2", "email": "joao@mail.com", "password": "def456"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_get_user_route(client: TestClient) -> None:
    create_response = client.post(
        "/api/users",
        json={"name": "Teste", "email": "teste@get.com", "password": "abc123"},
    )
    assert create_response.status_code == 200
    data = create_response.json()
    user_id = data["id"]

    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200

    user_data = get_response.json()
    assert user_data["id"] == user_id
    assert user_data["email"] == "teste@get.com"


def test_get_user_not_found(client: TestClient) -> None:
    fake_id = str(uuid.uuid4())

    response = client.get(f"/api/users/{fake_id}")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_route(client: TestClient) -> None:
    response = client.post(
        "/api/users",
        json={"name": "Lucia", "email": "lucia@mail.com", "password": "abc123"},
    )
    user_id = response.json()["id"]

    response = client.put(
        f"/api/users/{user_id}",
        json={
            "email": "lucia.new@mail.com",
            "name": "Lucia Silva",
            "password": "nova123",
        },
    )

    assert response.status_code == 200
    assert response.json()["email"] == "lucia.new@mail.com"
    assert response.json()["name"] == "Lucia Silva"


def test_delete_user_route(client: TestClient, db_session) -> None:
    response = client.post(
        "/api/users",
        json={"name": "Delete", "email": "delete@mail.com", "password": "abc123"},
    )
    assert response.status_code == 200
    user_id = response.json()["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code == 200
    assert response.json() is True

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 404

    from app.domain.models.user import User

    user = db_session.query(User).get(user_id)
    assert user is not None
    assert user.is_active is False
