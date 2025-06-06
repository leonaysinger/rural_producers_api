from starlette.testclient import TestClient


def test_create_rural_producer(client: TestClient):
    response = client.post(
        "/api/producers",
        json={"name": "Juca", "document_type": "CPF", "document": "429.102.020-11"}
    )
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Juca"
    assert body["document_type"] == "CPF"
    assert body["document"] == "42910202011"
    assert "id" in body

def test_create_rural_producer_with_invalid_cpf_should_return_error(client: TestClient):
    response = client.post(
        "/api/producers",
        json={"name": "Juca", "document_type": "CPF", "document": "429.102.333-11"}
    )
    assert response.status_code == 422

def test_list_rural_producers(client: TestClient):
    response = client.get("/api/producers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_producer_by_id(client: TestClient):
    create = client.post("/api/producers", json={"name": "Juca2", "document_type": "CPF",
                                                 "document": "002.602.160-97"})
    rural_producer_id = create.json()["id"]

    response = client.get(f"/api/producers/{rural_producer_id}")
    assert response.status_code == 200
    assert response.json()["id"] == rural_producer_id

def test_get_producer_not_found(client: TestClient):
    fake_id = "11111111-1111-1111-1111-111111111111"
    response = client.get(f"/api/producers/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Producer not found"


def test_update_rural_producer(client: TestClient):
    create = client.post("/api/producers", json={"name": "Juca3", "document_type": "CPF",
                                                 "document": "361.255.050-06"})
    crop_id = create.json()["id"]

    response = client.put(
        f"/api/producers/{crop_id}",
        json={"name": "Juca test"}
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Juca test"


def test_update_rural_producer_not_found(client: TestClient):
    fake_id = "22222222-2222-2222-2222-222222222222"
    response = client.put(
        f"/api/producers/{fake_id}",
        json={"name": "X"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Producer not found"


def test_delete_rural_producer(client: TestClient):
    create = client.post("/api/producers", json={"name": "Juca3", "document_type": "CPF",
                                                 "document": "934.406.000-25"})
    rural_producer_id = create.json()["id"]

    response = client.delete(f"/api/producers/{rural_producer_id}")
    assert response.status_code == 200
    assert response.json() is True

    get_deleted = client.get(f"/api/producers/{rural_producer_id}")
    assert get_deleted.status_code == 404


def test_delete_crop_not_found(client: TestClient):
    fake_id = "33333333-3333-3333-3333-333333333333"
    response = client.delete(f"/api/producers/{fake_id}")
    assert response.status_code == 200
    assert response.json() is False