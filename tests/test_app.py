import pytest
from unittest.mock import patch

from app.app import app, init_db


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # Keep the database isolated for testing.
    monkeypatch.chdir(tmp_path)

    init_db()

    app.config.update(TESTING=True)

    with app.test_client() as test_client:
        yield test_client


def test_home_returns_welcome_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "Welcome to the vulnerable DevSecOps lab"
    }


def test_health_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_search_existing_user(client):
    response = client.get("/api/search?username=alex")

    assert response.status_code == 200
    assert response.get_json() == [
        {"id": 1, "username": "alex"}
    ]


def test_search_missing_user(client):
    response = client.get("/api/search?username=unknown")

    assert response.status_code == 200
    assert response.get_json() == []


@patch("app.app.subprocess.run")
def test_ping_endpoint(mock_run, client):
    mock_run.return_value.stdout = "Mock ping output"
    mock_run.return_value.stderr = ""
    mock_run.return_value.returncode = 0

    response = client.get("/api/ping?host=127.0.0.1")

    assert response.status_code == 200
    assert response.get_json() == {
        "output": "Mock ping output"
    }

    mock_run.assert_called_once()
