from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from . import schemas, services
from auth.utils import get_current_active_user
from models import User

router = APIRouter(prefix="/api/v1")
inventory_service = services.InventoryService()
recipe_service = services.RecipeService()
shopping_list_service = services.ShoppingListService()

# Inventory routes
@router.get("/inventory/", response_model=List[schemas.InventoryItem])
def get_inventory_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all inventory items for the current user with pagination support.
    """
    return inventory_service.get_items(db, current_user, skip=skip, limit=limit)

@router.post("/inventory/", response_model=schemas.InventoryItem)
def create_inventory_item(
    item: schemas.InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new inventory item for the current user.
    """
    return inventory_service.create_item(db, item, current_user)

@router.get("/inventory/{item_id}", response_model=schemas.InventoryItem)
def get_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific inventory item by ID for the current user.
    """
    return inventory_service.get_item(db, item_id, current_user)

@router.put("/inventory/{item_id}", response_model=schemas.InventoryItem)
def update_inventory_item(
    item_id: int,
    item: schemas.InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing inventory item for the current user.
    """
    return inventory_service.update_item(db, item_id, item, current_user)

@router.delete("/inventory/{item_id}")
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete an inventory item for the current user.
    """
    return inventory_service.delete_item(db, item_id, current_user)

# Recipe routes
@router.get("/recipes/", response_model=List[schemas.Recipe])
def get_recipes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get all recipes for the current user with pagination support.
    """
    return recipe_service.get_recipes(db, current_user, skip=skip, limit=limit)

@router.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Create a new recipe for the current user.
    """
    return recipe_service.create_recipe(db, recipe, current_user)

@router.get("/recipes/{recipe_id}", response_model=schemas.Recipe)
def get_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get a specific recipe by ID for the current user.
    """
    return recipe_service.get_recipe(db, recipe_id, current_user)

@router.put("/recipes/{recipe_id}", response_model=schemas.Recipe)
def update_recipe(
    recipe_id: int,
    recipe: schemas.RecipeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update an existing recipe for the current user.
    """
    return recipe_service.update_recipe(db, recipe_id, recipe, current_user)

@router.delete("/recipes/{recipe_id}")
def delete_recipe(
    recipe_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a recipe for the current user.
    """
    return recipe_service.delete_recipe(db, recipe_id, current_user)

@router.get("/recipes/by-ingredients/", response_model=List[schemas.RecipeMatch])
def find_recipes_by_ingredients(
    ingredients: List[str] = Query(..., description="List of ingredients to search for"),
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Find recipes that can be made with the given ingredients for the current user.
    Returns recipes sorted by match percentage.
    Example: /recipes/by-ingredients/?ingredients=tomato&ingredients=pasta
    """
    return recipe_service.find_recipes_by_ingredients(db, ingredients, current_user, limit)

# Shopping List routes
@router.get("/shopping-list/", response_model=schemas.ShoppingListSummary)
def get_shopping_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Get the current shopping list with summary statistics for the current user.
    """
    return shopping_list_service.get_summary(db, current_user)

@router.post("/shopping-list/", response_model=schemas.ShoppingListItem)
def add_shopping_list_item(
    item: schemas.ShoppingListItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Add a new item to the shopping list for the current user.
    """
    return shopping_list_service.create_item(db, item, current_user)

@router.post("/shopping-list/recipe/", response_model=List[schemas.ShoppingListItem])
def generate_shopping_list_from_recipe(
    recipe_data: schemas.ShoppingListFromRecipe,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Generate shopping list items from a recipe for the current user.
    Optionally specify the number of servings to adjust quantities.
    """
    return shopping_list_service.generate_from_recipe(
        db,
        recipe_data.recipe_id,
        current_user,
        recipe_data.servings
    )

@router.put("/shopping-list/{item_id}", response_model=schemas.ShoppingListItem)
def update_shopping_list_item(
    item_id: int,
    item: schemas.ShoppingListItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Update a shopping list item for the current user.
    """
    return shopping_list_service.update_item(db, item_id, item, current_user)

@router.delete("/shopping-list/{item_id}")
def delete_shopping_list_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Delete a shopping list item for the current user.
    """
    return shopping_list_service.delete_item(db, item_id, current_user)

@router.post("/shopping-list/{item_id}/purchase")
def mark_item_as_purchased(
    item_id: int,
    update_inventory: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Mark a shopping list item as purchased for the current user.
    Optionally update the inventory with the purchased item.
    """
    return shopping_list_service.mark_as_purchased(db, item_id, current_user, update_inventory) 