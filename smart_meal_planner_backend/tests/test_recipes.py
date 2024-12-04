import pytest
from fastapi.testclient import TestClient
from datetime import date

@pytest.fixture
def sample_recipe():
    return {
        "name": "Test Spaghetti",
        "description": "A simple pasta dish",
        "ingredients": [
            {"name": "Spaghetti", "quantity": 500, "unit": "g"},
            {"name": "Tomato Sauce", "quantity": 300, "unit": "ml"}
        ],
        "instructions": [
            "Boil water",
            "Cook pasta",
            "Add sauce"
        ],
        "prep_time": 20
    }

def test_create_recipe(client, sample_recipe):
    response = client.post("/api/v1/recipes/", json=sample_recipe)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_recipe["name"]
    assert data["description"] == sample_recipe["description"]
    assert len(data["ingredients"]) == len(sample_recipe["ingredients"])
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_recipes(client, sample_recipe):
    # Create a recipe first
    client.post("/api/v1/recipes/", json=sample_recipe)
    
    response = client.get("/api/v1/recipes/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    assert data[0]["name"] == sample_recipe["name"]

def test_get_recipe(client, sample_recipe):
    # Create a recipe first
    create_response = client.post("/api/v1/recipes/", json=sample_recipe)
    recipe_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/recipes/{recipe_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["name"] == sample_recipe["name"]
    assert len(data["ingredients"]) == len(sample_recipe["ingredients"])

def test_update_recipe(client, sample_recipe):
    # Create a recipe first
    create_response = client.post("/api/v1/recipes/", json=sample_recipe)
    recipe_id = create_response.json()["id"]
    
    # Update the recipe
    updated_data = sample_recipe.copy()
    updated_data["prep_time"] = 25
    updated_data["description"] = "Updated description"
    
    response = client.put(f"/api/v1/recipes/{recipe_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == recipe_id
    assert data["prep_time"] == 25
    assert data["description"] == "Updated description"

def test_delete_recipe(client, sample_recipe):
    # Create a recipe first
    create_response = client.post("/api/v1/recipes/", json=sample_recipe)
    recipe_id = create_response.json()["id"]
    
    # Delete the recipe
    response = client.delete(f"/api/v1/recipes/{recipe_id}")
    assert response.status_code == 200
    
    # Verify recipe is deleted
    get_response = client.get(f"/api/v1/recipes/{recipe_id}")
    assert get_response.status_code == 404

def test_find_recipes_by_ingredients(client, sample_recipe):
    # Create a recipe first
    client.post("/api/v1/recipes/", json=sample_recipe)
    
    # Search for recipes with matching ingredients
    response = client.get("/api/v1/recipes/by-ingredients/", params={
        "ingredients": ["Spaghetti", "Tomato Sauce"]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "recipe" in data[0]
    assert "match_percentage" in data[0]
    assert data[0]["match_percentage"] == 100.0  # Should be perfect match

def test_find_recipes_partial_match(client, sample_recipe):
    # Create a recipe first
    client.post("/api/v1/recipes/", json=sample_recipe)
    
    # Search with only one matching ingredient
    response = client.get("/api/v1/recipes/by-ingredients/", params={
        "ingredients": ["Spaghetti"]
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["match_percentage"] == 50.0  # Should be 50% match 