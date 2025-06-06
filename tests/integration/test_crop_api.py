from starlette.testclient import TestClient


def test_create_crop(client: TestClient):
    response = client.post(
        "/api/crops",
        json={"name": "Maize"}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Maize"
    assert "id" in body


def test_list_crops(client: TestClient):
    response = client.get("/api/crops")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_crop_by_id(client: TestClient):
    create = client.post("/api/crops", json={"name": "Soybean"})
    crop_id = create.json()["id"]

    response = client.get(f"/api/crops/{crop_id}")
    assert response.status_code == 200
    assert response.json()["id"] == crop_id


def test_get_crop_not_found(client: TestClient):
    fake_id = "11111111-1111-1111-1111-111111111111"
    response = client.get(f"/api/crops/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Crop not found"


def test_update_crop(client: TestClient):
    create = client.post("/api/crops", json={"name": "Bean"})
    crop_id = create.json()["id"]

    response = client.put(
        f"/api/crops/{crop_id}",
        json={"name": "Bean Updated"}
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Bean Updated"


def test_update_crop_not_found(client: TestClient):
    fake_id = "22222222-2222-2222-2222-222222222222"
    response = client.put(
        f"/api/crops/{fake_id}",
        json={"name": "X"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Crop not found"


def test_delete_crop(client: TestClient):
    create = client.post("/api/crops", json={"name": "Wheat"})
    crop_id = create.json()["id"]

    response = client.delete(f"/api/crops/{crop_id}")
    assert response.status_code == 200
    assert response.json() is True

    get_deleted = client.get(f"/api/crops/{crop_id}")
    assert get_deleted.status_code == 404


def test_delete_crop_not_found(client: TestClient):
    fake_id = "33333333-3333-3333-3333-333333333333"
    response = client.delete(f"/api/crops/{fake_id}")
    assert response.status_code == 200
    assert response.json() is False
