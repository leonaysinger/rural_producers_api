from starlette.testclient import TestClient


def test_create_rural_property(client: TestClient):
    response = client.post(
        "/api/producers",
        json={"name": "Juca", "document_type": "CPF", "document": "060.616.300-00"}
    )
    body = response.json()

    response = client.post(
        "/api/properties",
        json={
          "producer_id": body['id'],
          "name": "Fazenda Boa Esperança",
          "city": "Uberlândia",
          "state": "MG",
          "cep": "38400-000",
          "number": "456",
          "description": "Propriedade voltada para cultivo de soja",
          "total_area": 100.0,
          "farming_area": 60.0,
          "vegetation_area": 40.0
        }
    )
    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Fazenda Boa Esperança"
    assert "id" in body

def test_create_rural_property_with_crops(client: TestClient):
    response = client.post(
        "/api/producers",
        json={"name": "Juca", "document_type": "CPF", "document": "261.787.640-30"}
    )
    producer = response.json()

    response = client.post(
        "/api/crops",
        json={"name": "Maize"}
    )
    crop = response.json()

    response = client.post(
        "/api/seasons",
        json={"name": "winter", "year": 2025}
    )
    season = response.json()

    response = client.post(
        "/api/properties",
        json={
            "producer_id": producer["id"],
            "name": "Fazenda Experimental",
            "city": "Luziânia",
            "state": "GO",
            "cep": "72800-000",
            "number": "999",
            "description": "Área de teste com plantio rotativo",
            "total_area": 150.0,
            "farming_area": 100.0,
            "vegetation_area": 50.0,
            "property_crops": [
                {
                    "season_id": season["id"],
                    "crop_id": crop["id"]
                }
            ]
        }
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Fazenda Experimental"
    assert "id" in body


def test_get_property_by_id(client: TestClient):
    response = client.post(
        "/api/producers",
        json={"name": "Juca", "document_type": "CPF", "document": "077.182.690-78"}
    )
    body = response.json()

    response = client.post(
        "/api/properties",
        json={
            "producer_id": body['id'],
            "name": "Fazenda Boa Esperança 2",
            "city": "Uberlândia",
            "state": "MG",
            "cep": "38400-000",
            "number": "456",
            "description": "Propriedade voltada para cultivo de soja",
            "total_area": 100.0,
            "farming_area": 60.0,
            "vegetation_area": 40.0
        }
    )

    rural_property_id = response.json()["id"]

    response = client.get(f"/api/properties/{rural_property_id}")
    assert response.status_code == 200
    assert response.json()["id"] == rural_property_id

def test_get_property_not_found(client: TestClient):
    fake_id = "11111111-1111-1111-1111-111111111111"
    response = client.get(f"/api/properties/{fake_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Property not found"


def test_update_rural_property(client: TestClient):
    create = client.post("/api/producers", json={"name": "Juca3", "document_type": "CPF",
                                                 "document": "370.342.510-53"})
    rural_producer_id = create.json()["id"]

    response = client.post(
        "/api/properties",
        json={
            "producer_id": rural_producer_id,
            "name": "Fazenda Boa Esperança 3",
            "city": "Uberlândia",
            "state": "MG",
            "cep": "38400-000",
            "number": "456",
            "description": "Propriedade voltada para cultivo de soja",
            "total_area": 100.0,
            "farming_area": 60.0,
            "vegetation_area": 40.0
        }
    )

    property_id = response.json()['id']
    response = client.put(
        f"/api/properties/{property_id}",
        json={"name": "Fazenda Nova"}
    )
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Fazenda Nova"

def test_update_rural_property_not_found(client: TestClient):
    fake_id = "22222222-2222-2222-2222-222222222222"
    response = client.put(
        f"/api/properties/{fake_id}",
        json={"name": "X"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Property not found"

def test_delete_rural_property(client: TestClient):
    create = client.post("/api/producers", json={"name": "Juca33", "document_type": "CPF",
                                                 "document": "179.665.400-06"})
    rural_producer_id = create.json()["id"]

    response = client.post(
        "/api/properties",
        json={
            "producer_id": rural_producer_id,
            "name": "Fazenda Boa Esperança 3",
            "city": "Uberlândia",
            "state": "MG",
            "cep": "38400-000",
            "number": "456",
            "description": "Propriedade voltada para cultivo de soja",
            "total_area": 100.0,
            "farming_area": 60.0,
            "vegetation_area": 40.0
        }
    )
    rural_property_id = response.json()["id"]

    response = client.delete(f"/api/properties/{rural_property_id}")
    assert response.status_code == 200
    assert response.json() is True

    get_deleted = client.get(f"/api/producers/{rural_property_id}")
    assert get_deleted.status_code == 404