import pytest
from unittest.mock import patch, AsyncMock, Mock
import json
from fastapi.testclient import TestClient
from main import app
import openai
from fastapi import HTTPException
import logging
import httpx

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123"
    }

@pytest.fixture
def mock_openai_response():
    class MockResponse:
        def __init__(self):
            self.choices = [
                type('Choice', (), {
                    'message': type('Message', (), {
                        'content': json.dumps({
                            "optimized_meal_plan": {
                                "goal": "weight_loss",
                                "daily_targets": {
                                    "calories": 2000.0,
                                    "protein": 150.0,
                                    "carbs": 200.0,
                                    "fat": 67.0,
                                    "fiber": 30.0
                                },
                                "meals": [
                                    {
                                        "meal_type": "breakfast",
                                        "timing": "8:00 AM",
                                        "recipes": [
                                            {
                                                "recipe": {
                                                    "name": "Protein Oatmeal",
                                                    "description": "High protein breakfast",
                                                    "ingredients": [
                                                        {"name": "oats", "quantity": 100, "unit": "g"}
                                                    ],
                                                    "instructions": ["Step 1"],
                                                    "prep_time": 15,
                                                    "difficulty": "easy",
                                                    "nutrition": {
                                                        "calories": 300,
                                                        "protein": 15,
                                                        "carbs": 45,
                                                        "fat": 8
                                                    }
                                                },
                                                "portion_size": 1.0,
                                                "contribution_to_goals": {
                                                    "calories": 300.0,
                                                    "protein": 15.0,
                                                    "carbs": 45.0,
                                                    "fat": 8.0
                                                },
                                                "timing_notes": "Eat within 30 minutes of waking",
                                                "pre_post_workout": False
                                            }
                                        ],
                                        "nutritional_balance": "Good protein to carb ratio",
                                        "meal_synergy": "Complex carbs with protein"
                                    }
                                ],
                                "supplements": [
                                    {
                                        "name": "Multivitamin",
                                        "timing": "Morning",
                                        "dosage": "1 tablet",
                                        "purpose": "General health",
                                        "notes": "Take with food"
                                    }
                                ],
                                "hydration_plan": {
                                    "daily_water": 3.0,
                                    "electrolytes": False,
                                    "timing_guidelines": ["Drink 500ml upon waking"]
                                },
                                "progress_tracking": {
                                    "metrics": ["weight", "measurements"],
                                    "measurement_frequency": "weekly",
                                    "expected_progress": "0.5-1kg per week"
                                }
                            }
                        })
                    })
                })
            ]
    return MockResponse()

@pytest.mark.asyncio
async def test_optimize_meal_plan_success(client, test_user, mock_openai_response):
    """Test successful meal plan optimization"""
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Mock OpenAI API call
    with patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai:
        mock_openai.return_value = mock_openai_response
        
        response = client.post(
            "/api/v1/ai/meal-plan/optimize",
            json={
                "goal": "weight_loss",
                "user_stats": {
                    "age": 28,
                    "weight": 75,
                    "height": 180,
                    "body_fat": 15,
                    "target_weight": 70,
                    "fitness_level": "intermediate"
                },
                "activity_level": "moderate",
                "preferences": {
                    "meal_frequency": 3,
                    "protein_sources": ["chicken", "fish", "eggs"],
                    "preferred_cuisines": ["mediterranean", "asian"]
                },
                "restrictions": ["vegetarian"],
                "existing_recipes": []
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "optimized_meal_plan" in data
        assert "goal" in data["optimized_meal_plan"]
        assert "daily_targets" in data["optimized_meal_plan"]
        assert "meals" in data["optimized_meal_plan"]
        assert "supplements" in data["optimized_meal_plan"]
        assert "hydration_plan" in data["optimized_meal_plan"]
        assert "progress_tracking" in data["optimized_meal_plan"]

@pytest.mark.asyncio
async def test_optimize_meal_plan_invalid_stats(client, test_user):
    """Test meal plan optimization with invalid user stats"""
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Test with missing required fields
    response = client.post(
        "/api/v1/ai/meal-plan/optimize",
        json={
            "goal": "weight_loss",
            "user_stats": {},  # Missing required fields
            "activity_level": "invalid",
            "preferences": {},
            "restrictions": [],
            "existing_recipes": []
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

@pytest.mark.asyncio
async def test_optimize_meal_plan_unauthorized(client):
    """Test meal plan optimization without authentication"""
    response = client.post(
        "/api/v1/ai/meal-plan/optimize",
        json={
            "goal": "weight_loss",
            "user_stats": {
                "age": 28,
                "weight": 75,
                "height": 180,
                "body_fat": 15,
                "target_weight": 70,
                "fitness_level": "intermediate"
            },
            "activity_level": "moderate",
            "preferences": {},
            "restrictions": [],
            "existing_recipes": []
        }
    )
    
    assert response.status_code == 401
    data = response.json()
    assert "detail" in data

@pytest.mark.asyncio
async def test_optimize_meal_plan_rate_limit(client, test_user):
    """Test meal plan optimization with rate limit error"""
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Create mock request and response for rate limit error
    mock_request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    mock_response = httpx.Response(
        status_code=429,
        request=mock_request,
        headers={"x-request-id": "test-request-id"},
        json={"error": {"message": "Rate limit exceeded", "type": "rate_limit_error"}}
    )
    
    # Mock OpenAI API call with rate limit error
    with patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai:
        mock_openai.side_effect = openai.RateLimitError(
            message="Rate limit exceeded",
            response=mock_response,
            body={"error": {"message": "Rate limit exceeded", "type": "rate_limit_error"}}
        )
        
        response = client.post(
            "/api/v1/ai/meal-plan/optimize",
            json={
                "goal": "weight_loss",
                "user_stats": {
                    "age": 28,
                    "weight": 75,
                    "height": 180,
                    "body_fat": 15,
                    "target_weight": 70,
                    "fitness_level": "intermediate"
                },
                "activity_level": "moderate",
                "preferences": {},
                "restrictions": [],
                "existing_recipes": []
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 429
        data = response.json()
        assert "detail" in data
        assert "rate limit" in data["detail"].lower()

@pytest.mark.asyncio
async def test_optimize_meal_plan_api_error(client, test_user):
    """Test meal plan optimization with API error"""
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Create mock request for API error
    mock_request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    
    # Mock OpenAI API call with API error
    with patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai:
        mock_openai.side_effect = openai.APIError(
            message="API error",
            request=mock_request,
            body={"error": {"message": "Internal server error", "type": "api_error"}}
        )
        
        response = client.post(
            "/api/v1/ai/meal-plan/optimize",
            json={
                "goal": "weight_loss",
                "user_stats": {
                    "age": 28,
                    "weight": 75,
                    "height": 180,
                    "body_fat": 15,
                    "target_weight": 70,
                    "fitness_level": "intermediate"
                },
                "activity_level": "moderate",
                "preferences": {},
                "restrictions": [],
                "existing_recipes": []
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert "detail" in data
        assert "api" in data["detail"].lower()