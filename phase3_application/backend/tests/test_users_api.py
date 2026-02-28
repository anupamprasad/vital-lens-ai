import pytest
from fastapi.testclient import TestClient
import sys
import os

# ensure project root is on path so that 'main' can be imported
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root not in sys.path:
    sys.path.insert(0, root)

from main import app

client = TestClient(app)


def signup_and_login(email: str, password: str):
    # create user (ignore if exists)
    client.post("/api/v1/auth/signup", json={"name": "Test", "email": email, "password": password})
    resp = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert resp.status_code == 200
    token = resp.json().get("access_token")
    return token


def test_list_users_requires_auth():
    r = client.get("/api/v1/users/")
    assert r.status_code == 401  # unauthorized


def test_list_users_success():
    token = signup_and_login("apiuser@example.com", "secret123")
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/api/v1/users/", headers=headers)
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # check that returned objects have expected keys
    sample = data[0]
    assert "email" in sample and "id" in sample


def test_register_alias_works():
    """Ensure /register endpoint behaves identically to /signup."""
    # choose a random email to avoid conflicts
    email = f"alias{os.urandom(3).hex()}@example.com"
    resp = client.post("/api/v1/auth/register", json={"name": "Alias", "email": email, "password": "pw123456"})
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("access_token")
    assert data.get("user", {}).get("email") == email


if __name__ == "__main__":
    pytest.main([__file__, "-v"])