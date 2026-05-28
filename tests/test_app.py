import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.monitor import load_endpoints


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_status_endpoint(client):
    response = client.get("/api/status")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_load_endpoints():
    config = {
        "endpoints": [
            {"name": "Example", "url": "https://example.com"}
        ]
    }
    endpoints = load_endpoints(config)
    assert len(endpoints) == 1
    assert endpoints[0].name == "Example"
