def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_endpoint_with_data(client_with_data):
    response = client_with_data.get("/api/analysis")
    assert response.status_code == 200
    data = response.json()
    assert data["patient_name"] == "Jan"
    assert data["patient_surname"] == "Kowalski"
    assert "critical_issues" in data


def test_analysis_endpoint_without_data(client):
    response = client.get("/api/analysis")
    assert response.status_code == 404
