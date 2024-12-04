import pytest
from fastapi.testclient import TestClient
from datetime import date

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123"
    }

def test_register_user(client, test_user):
    response = client.post("/api/v1/auth/register", json=test_user)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_register_duplicate_username(client, test_user):
    # Register first user
    client.post("/api/v1/auth/register", json=test_user)
    
    # Try to register with same username
    duplicate_user = test_user.copy()
    duplicate_user["email"] = "another@example.com"
    response = client.post("/api/v1/auth/register", json=duplicate_user)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_register_duplicate_email(client, test_user):
    # Register first user
    client.post("/api/v1/auth/register", json=test_user)
    
    # Try to register with same email
    duplicate_user = test_user.copy()
    duplicate_user["username"] = "anotheruser"
    response = client.post("/api/v1/auth/register", json=duplicate_user)
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

def test_login_success(client, test_user):
    # Register user first
    client.post("/api/v1/auth/register", json=test_user)
    
    # Try to login
    response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client, test_user):
    # Register user first
    client.post("/api/v1/auth/register", json=test_user)
    
    # Try to login with wrong password
    response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": "wrongpassword"
    })
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]

def test_get_current_user(client, test_user):
    # Register user first
    client.post("/api/v1/auth/register", json=test_user)
    
    # Login to get token
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Get current user info
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user["username"]
    assert data["email"] == test_user["email"]

def test_get_current_user_invalid_token(client):
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"] 