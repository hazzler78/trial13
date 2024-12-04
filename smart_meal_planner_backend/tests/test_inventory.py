from fastapi.testclient import TestClient
import pytest
from datetime import date

def test_create_inventory_item(client, sample_inventory_item):
    response = client.post("/api/v1/inventory/", json=sample_inventory_item)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == sample_inventory_item["name"]
    assert data["quantity"] == sample_inventory_item["quantity"]
    assert data["unit"] == sample_inventory_item["unit"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_get_inventory_items(client, sample_inventory_item):
    # Create an item first
    client.post("/api/v1/inventory/", json=sample_inventory_item)
    
    response = client.get("/api/v1/inventory/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    assert data[0]["name"] == sample_inventory_item["name"]

def test_get_inventory_item(client, sample_inventory_item):
    # Create an item first
    create_response = client.post("/api/v1/inventory/", json=sample_inventory_item)
    item_id = create_response.json()["id"]
    
    response = client.get(f"/api/v1/inventory/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == sample_inventory_item["name"]

def test_update_inventory_item(client, sample_inventory_item):
    # Create an item first
    create_response = client.post("/api/v1/inventory/", json=sample_inventory_item)
    item_id = create_response.json()["id"]
    
    # Update the item
    updated_data = sample_inventory_item.copy()
    updated_data["quantity"] = 3.5
    
    response = client.put(f"/api/v1/inventory/{item_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["quantity"] == 3.5

def test_delete_inventory_item(client, sample_inventory_item):
    # Create an item first
    create_response = client.post("/api/v1/inventory/", json=sample_inventory_item)
    item_id = create_response.json()["id"]
    
    # Delete the item
    response = client.delete(f"/api/v1/inventory/{item_id}")
    assert response.status_code == 200
    
    # Verify item is deleted
    get_response = client.get(f"/api/v1/inventory/{item_id}")
    assert get_response.status_code == 404

def test_get_nonexistent_item(client):
    response = client.get("/api/v1/inventory/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"

def test_create_invalid_inventory_item(client):
    invalid_item = {
        "name": "Test Item",
        "quantity": "invalid",  # should be a number
        "unit": "kg"
    }
    response = client.post("/api/v1/inventory/", json=invalid_item)
    assert response.status_code == 422  # Validation error 