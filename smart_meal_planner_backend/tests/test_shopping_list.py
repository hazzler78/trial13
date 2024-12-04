import pytest
from fastapi.testclient import TestClient
from datetime import date

@pytest.fixture
def sample_shopping_item():
    return {
        "name": "Test Item",
        "quantity": 2.5,
        "unit": "kg",
        "recipe_id": None,
        "purchased": False
    }

def test_create_shopping_item(client, sample_shopping_item):
    response = client.post("/api/v1/shopping-list/", json=sample_shopping_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_shopping_item["name"]
    assert data["quantity"] == sample_shopping_item["quantity"]
    assert data["unit"] == sample_shopping_item["unit"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_shopping_list(client, sample_shopping_item):
    # Create an item first
    client.post("/api/v1/shopping-list/", json=sample_shopping_item)
    
    response = client.get("/api/v1/shopping-list/")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert "purchased_items" in data
    assert "pending_items" in data
    assert "items" in data
    assert len(data["items"]) > 0
    assert data["total_items"] == len(data["items"])
    assert data["pending_items"] == data["total_items"] - data["purchased_items"]

def test_update_shopping_item(client, sample_shopping_item):
    # Create an item first
    create_response = client.post("/api/v1/shopping-list/", json=sample_shopping_item)
    item_id = create_response.json()["id"]
    
    # Update the item
    updated_data = sample_shopping_item.copy()
    updated_data["quantity"] = 3.5
    
    response = client.put(f"/api/v1/shopping-list/{item_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["quantity"] == 3.5

def test_delete_shopping_item(client, sample_shopping_item):
    # Create an item first
    create_response = client.post("/api/v1/shopping-list/", json=sample_shopping_item)
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/v1/shopping-list/{item_id}")
    assert response.status_code == 200

def test_mark_item_as_purchased(client, sample_shopping_item):
    # Create an item first
    create_response = client.post("/api/v1/shopping-list/", json=sample_shopping_item)
    item_id = create_response.json()["id"]
    
    # Mark as purchased
    response = client.post(f"/api/v1/shopping-list/{item_id}/purchase")
    assert response.status_code == 200
    data = response.json()
    assert data["purchased"] == True

def test_generate_shopping_list_from_recipe(client, sample_recipe):
    # Create a recipe first
    recipe_response = client.post("/api/v1/recipes/", json=sample_recipe)
    recipe_id = recipe_response.json()["id"]
    
    # Generate shopping list
    response = client.post("/api/v1/shopping-list/recipe/", json={
        "recipe_id": recipe_id,
        "servings": 2.0
    })
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(sample_recipe["ingredients"])
    
    # Check quantities are doubled
    for item, original in zip(data, sample_recipe["ingredients"]):
        assert item["quantity"] == original["quantity"] * 2.0

def test_mark_purchased_updates_inventory(client, sample_shopping_item):
    # Create a shopping list item
    create_response = client.post("/api/v1/shopping-list/", json=sample_shopping_item)
    item_id = create_response.json()["id"]
    
    # Mark as purchased with inventory update
    response = client.post(f"/api/v1/shopping-list/{item_id}/purchase", params={"update_inventory": True})
    assert response.status_code == 200
    
    # Check inventory
    inventory_response = client.get("/api/v1/inventory/")
    inventory_data = inventory_response.json()
    assert len(inventory_data) > 0
    
    # Find matching inventory item
    matching_item = next(
        (item for item in inventory_data if item["name"] == sample_shopping_item["name"]),
        None
    )
    assert matching_item is not None
    assert matching_item["quantity"] == sample_shopping_item["quantity"]
    assert matching_item["unit"] == sample_shopping_item["unit"] 