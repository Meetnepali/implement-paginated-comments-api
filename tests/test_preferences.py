import pytest
from fastapi.testclient import TestClient
from app.main import app, get_store

@pytest.fixture
def client():
    def override_store():
        # Returns a fresh dict for each test
        return {}
    app.dependency_overrides[get_store] = override_store
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def valid_prefs():
    return {
        "language": "en",
        "notifications_enabled": True,
        "theme": "light"
    }

def test_create_preferences_success(client):
    resp = client.post("/preferences/johndoe", json=valid_prefs())
    assert resp.status_code == 201
    data = resp.json()
    assert data["user_id"] == "johndoe"
    assert data["language"] == "en"
    assert data["notifications_enabled"] is True
    assert data["theme"] == "light"

def test_create_preferences_duplicate(client):
    url = "/preferences/janedoe"
    client.post(url, json=valid_prefs())
    resp = client.post(url, json=valid_prefs())
    assert resp.status_code == 409
    assert "already exist" in resp.json()["detail"]

def test_create_preferences_invalid_data(client):
    data = valid_prefs()
    data["language"] = "xx"
    resp = client.post("/preferences/doe", json=data)
    assert resp.status_code == 422
    assert "Unsupported language" in resp.json()["detail"]

def test_read_preferences_success(client):
    url = "/preferences/alice"
    prefs = valid_prefs()
    client.post(url, json=prefs)
    resp = client.get(url)
    assert resp.status_code == 200
    data = resp.json()
    assert data["user_id"] == "alice"
    assert data["language"] == prefs["language"]

def test_read_preferences_not_found(client):
    resp = client.get("/preferences/unknown")
    assert resp.status_code == 404
    assert "not found" in resp.json()["detail"]
