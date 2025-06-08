from starlette.testclient import TestClient


def test_report_summary(client: TestClient, seed_data_extended):
    response = client.get("/api/reports/summary")
    assert response.status_code == 200
    data = response.json()
    assert data["total_farms"] == 7
    assert data["total_area"] == 870.0

def test_report_farms_by_crop(client: TestClient, seed_data_extended):
    response = client.get("/api/reports/farms-by-crop")
    assert response.status_code == 200

def test_report_farms_by_state(client: TestClient, seed_data_extended):
    response = client.get("/api/reports/farms-by-state")
    assert response.status_code == 200
    data = response.json()
