from fastapi.testclient import TestClient


def test_create_season(client: TestClient):
    response = client.post(
        "/api/seasons",
        json={"name": "winter", "year": 2025}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "winter"
    assert body["year"] == 2025
    assert "id" in body

def test_list_seasons(client: TestClient):
    response = client.get("/api/seasons")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_season_by_id(client: TestClient):
    create = client.post("/api/seasons", json={"name": "Winter", "year": 2025})
    season_id = create.json()["id"]

    response = client.get(f"/api/seasons/{season_id}")
    assert response.status_code == 200
    assert response.json()["id"] == season_id

def test_get_season_not_found(client: TestClient):
    fake_id = "11111111-1111-1111-1111-111111111111"
    response = client.get(f"/api/seasons/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Season not found"


def test_update_season(client: TestClient):
    create = client.post("/api/seasons", json={"name": "winter", "year": 2025})
    season_id = create.json()["id"]

    response = client.put(
        f"/api/seasons/{season_id}",
        json={"name": "Winter Updated"}
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Winter Updated"
