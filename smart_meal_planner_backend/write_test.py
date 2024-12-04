test_content = '''import pytest
from unittest.mock import patch, AsyncMock
import json
from fastapi.testclient import TestClient
from main import app
import openai
from fastapi import HTTPException

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }

@pytest.mark.asyncio
async def test_optimize_meal_plan(client, test_user):
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    response = client.post(
        "/api/v1/ai/meal-plans/optimize",
        json={
            "goal": "weight_loss",
            "days": 7,
            "dietary_restrictions": ["vegetarian"],
            "target_calories": 2000
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "optimized_meal_plan" in data
    assert "goal" in data["optimized_meal_plan"]
    assert "daily_targets" in data["optimized_meal_plan"]'''

with open('tests/test_ai.py', 'w', encoding='utf-8') as f:
    f.write(test_content) 