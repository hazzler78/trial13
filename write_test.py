import os

test_content = '''import pytest
from unittest.mock import patch, AsyncMock
import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def test_user():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }

@pytest.fixture
def test_recipe():
    return {
        "name": "Test Recipe",
        "description": "A test recipe",
        "ingredients": [
            {"name": "ingredient1", "quantity": 100, "unit": "g"}
        ],
        "instructions": ["Step 1"],
        "prep_time": 30,
        "difficulty": "medium",
        "nutrition": {
            "calories": 500,
            "protein": 20,
            "carbs": 50,
            "fat": 15
        }
    }

@pytest.fixture
def test_optimization_request():
    return {
        "goal": "muscle gain",
        "user_stats": {
            "age": 28,
            "weight": 75,
            "height": 180,
            "body_fat": 15,
            "target_weight": 80,
            "fitness_level": "intermediate"
        },
        "activity_level": "very active",
        "preferences": {
            "meal_frequency": 5,
            "protein_sources": ["chicken", "fish", "eggs"],
            "preferred_cuisines": ["mediterranean", "asian"]
        },
        "restrictions": ["no_dairy"],
        "existing_recipes": []
    }

@pytest.fixture
def test_adaptation_request(test_recipe):
    return {
        "recipe": test_recipe,
        "target_skill_level": "beginner",
        "user_equipment": ["oven", "skillet", "baking sheet"],
        "time_constraints": 60,
        "specific_techniques": ["searing", "baking"]
    }

@pytest.fixture
def mock_openai_optimization_response():
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "optimized_meal_plan": {
                        "goal": "muscle gain",
                        "daily_targets": {
                            "calories": 3000,
                            "protein": 180,
                            "carbs": 375,
                            "fat": 83,
                            "fiber": 35
                        },
                        "meals": [{
                            "meal_type": "breakfast",
                            "timing": "7:00 AM",
                            "recipes": [{
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
                                        "calories": 500,
                                        "protein": 30,
                                        "carbs": 60,
                                        "fat": 15
                                    }
                                },
                                "portion_size": 1,
                                "contribution_to_goals": {
                                    "calories": 500,
                                    "protein": 30,
                                    "carbs": 60,
                                    "fat": 15
                                },
                                "timing_notes": "Eat within 30 minutes of waking",
                                "pre_post_workout": False
                            }],
                            "nutritional_balance": "Good protein to carb ratio",
                            "meal_synergy": "Complex carbs with protein"
                        }],
                        "supplements": [{
                            "name": "Creatine",
                            "timing": "Post-workout",
                            "dosage": "5g",
                            "purpose": "Muscle recovery",
                            "notes": "Take with water"
                        }],
                        "hydration_plan": {
                            "daily_water": 4,
                            "electrolytes": True,
                            "timing_guidelines": ["Drink 500ml upon waking"]
                        },
                        "progress_tracking": {
                            "metrics": ["weight", "measurements", "strength"],
                            "measurement_frequency": "weekly",
                            "expected_progress": "0.5kg per week"
                        }
                    }
                })
            }
        }]
    }

@pytest.fixture
def mock_openai_adaptation_response():
    return {
        "choices": [{
            "message": {
                "content": json.dumps({
                    "adapted_recipe": {
                        "original_difficulty": "advanced",
                        "adapted_difficulty": "beginner",
                        "simplifications": [{
                            "original_step": "Sear the beef",
                            "simplified_step": "Cook the beef in a pan",
                            "reason": "More familiar terminology",
                            "tips": ["Use medium-high heat"]
                        }],
                        "equipment_substitutions": [{
                            "original_equipment": "Cast iron skillet",
                            "alternative": "Regular frying pan",
                            "usage_instructions": [
                                "Heat pan thoroughly before cooking"
                            ]
                        }],
                        "technique_breakdown": [{
                            "technique": "searing",
                            "difficulty_level": "beginner",
                            "detailed_steps": ["Heat pan", "Add oil"],
                            "practice_suggestions": ["Try with cheaper cuts first"]
                        }],
                        "timing_adjustments": {
                            "original_time": 120,
                            "adjusted_time": 60,
                            "explanation": "Simplified steps take less time"
                        },
                        "recipe": {
                            "name": "Simplified Test Recipe",
                            "description": "Beginner-friendly version",
                            "ingredients": [
                                {"name": "ingredient1", "quantity": 100, "unit": "g"}
                            ],
                            "instructions": ["Simplified Step 1"],
                            "prep_time": 60,
                            "difficulty": "beginner",
                            "nutrition": {
                                "calories": 500,
                                "protein": 20,
                                "carbs": 50,
                                "fat": 15
                            }
                        },
                        "confidence_building_steps": [
                            "Practice each step separately"
                        ],
                        "common_mistakes_prevention": [
                            "Don\'t skip preheating"
                        ]
                    }
                })
            }
        }]
    }

@pytest.mark.asyncio
async def test_optimize_meal_plan(
    client,
    test_user,
    test_optimization_request,
    mock_openai_optimization_response
):
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Mock OpenAI API call
    with patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai:
        mock_openai.return_value = mock_openai_optimization_response
        
        response = client.post(
            "/api/v1/ai/meal-plan/optimize",
            json=test_optimization_request,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "optimized_meal_plan" in data
        plan = data["optimized_meal_plan"]
        
        # Verify plan structure
        assert "goal" in plan
        assert "daily_targets" in plan
        assert "meals" in plan
        assert "supplements" in plan
        assert "hydration_plan" in plan
        assert "progress_tracking" in plan
        
        # Verify daily targets
        targets = plan["daily_targets"]
        assert "calories" in targets
        assert "protein" in targets
        assert "carbs" in targets
        assert "fat" in targets
        assert "fiber" in targets
        
        # Verify meal structure
        meal = plan["meals"][0]
        assert "meal_type" in meal
        assert "timing" in meal
        assert "recipes" in meal
        assert "nutritional_balance" in meal
        assert "meal_synergy" in meal
        
        # Verify recipe details
        recipe = meal["recipes"][0]
        assert "recipe" in recipe
        assert "portion_size" in recipe
        assert "contribution_to_goals" in recipe
        assert "timing_notes" in recipe
        assert "pre_post_workout" in recipe

@pytest.mark.asyncio
async def test_adapt_recipe_difficulty(
    client,
    test_user,
    test_adaptation_request,
    mock_openai_adaptation_response
):
    # Register and login user
    client.post("/api/v1/auth/register", json=test_user)
    login_response = client.post("/api/v1/auth/login", json={
        "username": test_user["username"],
        "password": test_user["password"]
    })
    token = login_response.json()["access_token"]
    
    # Mock OpenAI API call
    with patch("openai.ChatCompletion.acreate", new_callable=AsyncMock) as mock_openai:
        mock_openai.return_value = mock_openai_adaptation_response
        
        response = client.post(
            "/api/v1/ai/recipes/adapt",
            json=test_adaptation_request,
            headers={"Authorization": f"Bearer {token}"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "adapted_recipe" in data
        recipe = data["adapted_recipe"]
        
        # Verify adaptation structure
        assert "original_difficulty" in recipe
        assert "adapted_difficulty" in recipe
        assert "simplifications" in recipe
        assert "equipment_substitutions" in recipe
        assert "technique_breakdown" in recipe
        assert "timing_adjustments" in recipe
        assert "recipe" in recipe
        assert "confidence_building_steps" in recipe
        assert "common_mistakes_prevention" in recipe
        
        # Verify simplification details
        simplification = recipe["simplifications"][0]
        assert "original_step" in simplification
        assert "simplified_step" in simplification
        assert "reason" in simplification
        assert "tips" in simplification
        
        # Verify equipment substitution
        substitution = recipe["equipment_substitutions"][0]
        assert "original_equipment" in substitution
        assert "alternative" in substitution
        assert "usage_instructions" in substitution
        
        # Verify technique breakdown
        technique = recipe["technique_breakdown"][0]
        assert "technique" in technique
        assert "difficulty_level" in technique
        assert "detailed_steps" in technique
        assert "practice_suggestions" in technique
        
        # Verify timing adjustments
        timing = recipe["timing_adjustments"]
        assert "original_time" in timing
        assert "adjusted_time" in timing
        assert "explanation" in timing
        
        # Verify adapted recipe matches target skill level
        assert recipe["adapted_difficulty"] == test_adaptation_request["target_skill_level"]
'''

# Create tests directory if it doesn't exist
os.makedirs('smart_meal_planner_backend/tests', exist_ok=True)

# Write the test file
with open('smart_meal_planner_backend/tests/test_ai.py', 'w', encoding='utf-8') as f:
    f.write(test_content) 