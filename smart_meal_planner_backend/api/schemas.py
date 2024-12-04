from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional, List, Dict

class InventoryItemBase(BaseModel):
    name: str = Field(description="Name of the item")
    quantity: float = Field(description="Quantity of the item")
    unit: str = Field(description="Unit of measurement")
    expiry_date: Optional[date] = Field(None, description="Expiry date of the item")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Tomatoes",
            "quantity": 1.5,
            "unit": "kg",
            "expiry_date": "2024-12-31"
        }
    })

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItem(InventoryItemBase):
    id: int
    created_at: date
    updated_at: date

    model_config = ConfigDict(from_attributes=True)

class RecipeIngredient(BaseModel):
    name: str = Field(description="Name of the ingredient")
    quantity: float = Field(description="Quantity needed")
    unit: str = Field(description="Unit of measurement")

class RecipeBase(BaseModel):
    name: str = Field(description="Name of the recipe")
    description: str = Field(description="Description of the recipe")
    ingredients: List[RecipeIngredient] = Field(description="List of ingredients with quantities")
    instructions: List[str] = Field(description="List of preparation steps")
    prep_time: int = Field(description="Preparation time in minutes")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Spaghetti Bolognese",
            "description": "Classic Italian pasta dish with meat sauce",
            "ingredients": [
                {"name": "Spaghetti", "quantity": 500, "unit": "g"},
                {"name": "Ground Beef", "quantity": 400, "unit": "g"},
                {"name": "Tomato Sauce", "quantity": 500, "unit": "ml"}
            ],
            "instructions": [
                "Boil the spaghetti according to package instructions",
                "Brown the ground beef in a large pan",
                "Add tomato sauce and simmer for 20 minutes"
            ],
            "prep_time": 45
        }
    })

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    created_at: date
    updated_at: date

    model_config = ConfigDict(from_attributes=True)

class RecipeMatch(BaseModel):
    recipe: Recipe
    match_percentage: float

    model_config = ConfigDict(from_attributes=True)

class ShoppingListItemBase(BaseModel):
    name: str = Field(description="Name of the item")
    quantity: float = Field(description="Quantity needed")
    unit: str = Field(description="Unit of measurement")
    recipe_id: Optional[int] = Field(None, description="ID of the recipe this item is for")
    purchased: bool = Field(default=False, description="Whether the item has been purchased")

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "name": "Tomatoes",
            "quantity": 1.5,
            "unit": "kg",
            "recipe_id": 1,
            "purchased": False
        }
    })

class ShoppingListItemCreate(ShoppingListItemBase):
    pass

class ShoppingListItem(ShoppingListItemBase):
    id: int
    created_at: date
    updated_at: date

    model_config = ConfigDict(from_attributes=True)

class ShoppingListFromRecipe(BaseModel):
    recipe_id: int = Field(description="ID of the recipe to generate shopping list from")
    servings: float = Field(default=1.0, description="Number of servings to calculate quantities for")

class ShoppingListSummary(BaseModel):
    total_items: int
    purchased_items: int
    pending_items: int
    items: List[ShoppingListItem]

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "total_items": 5,
            "purchased_items": 2,
            "pending_items": 3,
            "items": []
        }
    }) 