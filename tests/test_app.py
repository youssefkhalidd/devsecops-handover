import pytest
from app.app import app


@pytest.fixture()
def client():
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_home_returns_welcome_message(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Welcome to the DevSecOps handover app"


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_existing_user_is_returned(client):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    assert response.get_json() == {"id": 1, "name": "Alex"}


def test_missing_user_returns_404(client):
    response = client.get("/api/users/999")
    assert response.status_code == 404
    assert response.get_json() == {"error": "User not found"}
