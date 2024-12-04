from sqlalchemy.orm import Session
from . import schemas
from models import InventoryItem, Recipe, ShoppingListItem, User
from fastapi import HTTPException, status
from datetime import datetime, UTC
from typing import List, Optional

class InventoryService:
    @staticmethod
    def get_items(db: Session, user: User, skip: int = 0, limit: int = 100):
        return db.query(InventoryItem).filter(InventoryItem.user_id == user.id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_item(db: Session, item_id: int, user: User):
        item = db.query(InventoryItem).filter(
            InventoryItem.id == item_id,
            InventoryItem.user_id == user.id
        ).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    
    @staticmethod
    def create_item(db: Session, item: schemas.InventoryItemCreate, user: User):
        db_item = InventoryItem(**item.model_dump(), user_id=user.id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def update_item(db: Session, item_id: int, item: schemas.InventoryItemCreate, user: User):
        db_item = InventoryService.get_item(db, item_id, user)
        update_data = item.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.updated_at = datetime.now(UTC).date()
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete_item(db: Session, item_id: int, user: User):
        db_item = InventoryService.get_item(db, item_id, user)
        db.delete(db_item)
        db.commit()
        return {"message": "Item deleted successfully"}

class RecipeService:
    @staticmethod
    def get_recipes(db: Session, user: User, skip: int = 0, limit: int = 100):
        return db.query(Recipe).filter(Recipe.user_id == user.id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_recipe(db: Session, recipe_id: int, user: User):
        recipe = db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.user_id == user.id
        ).first()
        if recipe is None:
            raise HTTPException(status_code=404, detail="Recipe not found")
        return recipe
    
    @staticmethod
    def create_recipe(db: Session, recipe: schemas.RecipeCreate, user: User):
        db_recipe = Recipe(
            **recipe.model_dump(),
            user_id=user.id
        )
        db.add(db_recipe)
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    
    @staticmethod
    def update_recipe(db: Session, recipe_id: int, recipe: schemas.RecipeCreate, user: User):
        db_recipe = RecipeService.get_recipe(db, recipe_id, user)
        
        for field, value in recipe.model_dump().items():
            setattr(db_recipe, field, value)
        
        db_recipe.updated_at = datetime.now(UTC).date()
        db.commit()
        db.refresh(db_recipe)
        return db_recipe
    
    @staticmethod
    def delete_recipe(db: Session, recipe_id: int, user: User):
        db_recipe = RecipeService.get_recipe(db, recipe_id, user)
        db.delete(db_recipe)
        db.commit()
        return {"message": "Recipe deleted successfully"}
    
    @staticmethod
    def find_recipes_by_ingredients(db: Session, ingredients: List[str], user: User, limit: int = 10):
        """Find recipes that can be made with given ingredients"""
        recipes = db.query(Recipe).filter(Recipe.user_id == user.id).all()
        matching_recipes = []
        
        for recipe in recipes:
            recipe_ingredients = {ing["name"].lower() for ing in recipe.ingredients}
            available_ingredients = {ing.lower() for ing in ingredients}
            
            # Calculate how many ingredients match
            matching_count = len(recipe_ingredients.intersection(available_ingredients))
            total_ingredients = len(recipe_ingredients)
            
            if matching_count > 0:  # At least one ingredient matches
                match_percentage = (matching_count / total_ingredients) * 100
                matching_recipes.append({
                    "recipe": recipe,
                    "match_percentage": match_percentage
                })
        
        # Sort by match percentage and return top matches
        matching_recipes.sort(key=lambda x: x["match_percentage"], reverse=True)
        return matching_recipes[:limit]

class ShoppingListService:
    @staticmethod
    def get_items(db: Session, user: User, skip: int = 0, limit: int = 100):
        return db.query(ShoppingListItem).filter(ShoppingListItem.user_id == user.id).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_item(db: Session, item_id: int, user: User):
        item = db.query(ShoppingListItem).filter(
            ShoppingListItem.id == item_id,
            ShoppingListItem.user_id == user.id
        ).first()
        if item is None:
            raise HTTPException(status_code=404, detail="Shopping list item not found")
        return item
    
    @staticmethod
    def create_item(db: Session, item: schemas.ShoppingListItemCreate, user: User):
        db_item = ShoppingListItem(**item.model_dump(), user_id=user.id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def update_item(db: Session, item_id: int, item: schemas.ShoppingListItemCreate, user: User):
        db_item = ShoppingListService.get_item(db, item_id, user)
        update_data = item.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_item, field, value)
        
        db_item.updated_at = datetime.now(UTC).date()
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def delete_item(db: Session, item_id: int, user: User):
        db_item = ShoppingListService.get_item(db, item_id, user)
        db.delete(db_item)
        db.commit()
        return {"message": "Shopping list item deleted successfully"}
    
    @staticmethod
    def mark_as_purchased(db: Session, item_id: int, user: User, update_inventory: bool = True):
        db_item = ShoppingListService.get_item(db, item_id, user)
        db_item.purchased = True
        db_item.updated_at = datetime.now(UTC).date()
        
        if update_inventory:
            # Check if item exists in inventory
            inventory_item = db.query(InventoryItem).filter(
                InventoryItem.name == db_item.name,
                InventoryItem.unit == db_item.unit,
                InventoryItem.user_id == user.id
            ).first()
            
            if inventory_item:
                # Update existing inventory item
                inventory_item.quantity += db_item.quantity
                inventory_item.updated_at = datetime.now(UTC).date()
            else:
                # Create new inventory item
                inventory_item = InventoryItem(
                    name=db_item.name,
                    quantity=db_item.quantity,
                    unit=db_item.unit,
                    user_id=user.id
                )
                db.add(inventory_item)
        
        db.commit()
        db.refresh(db_item)
        return db_item
    
    @staticmethod
    def generate_from_recipe(db: Session, recipe_id: int, user: User, servings: float = 1.0):
        recipe = db.query(Recipe).filter(
            Recipe.id == recipe_id,
            Recipe.user_id == user.id
        ).first()
        if not recipe:
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        shopping_list_items = []
        for ingredient in recipe.ingredients:
            # Calculate quantity based on servings
            quantity = ingredient["quantity"] * servings
            
            # Check if item already exists in shopping list
            existing_item = db.query(ShoppingListItem).filter(
                ShoppingListItem.name == ingredient["name"],
                ShoppingListItem.unit == ingredient["unit"],
                ShoppingListItem.purchased == False,
                ShoppingListItem.user_id == user.id
            ).first()
            
            if existing_item:
                # Update quantity of existing item
                existing_item.quantity += quantity
                db.commit()
                db.refresh(existing_item)
                shopping_list_items.append(existing_item)
            else:
                # Create new shopping list item
                shopping_item = ShoppingListItem(
                    name=ingredient["name"],
                    quantity=quantity,
                    unit=ingredient["unit"],
                    recipe_id=recipe_id,
                    user_id=user.id
                )
                db.add(shopping_item)
                db.commit()
                db.refresh(shopping_item)
                shopping_list_items.append(shopping_item)
        
        return shopping_list_items
    
    @staticmethod
    def get_summary(db: Session, user: User):
        items = db.query(ShoppingListItem).filter(ShoppingListItem.user_id == user.id).all()
        total_items = len(items)
        purchased_items = sum(1 for item in items if item.purchased)
        pending_items = total_items - purchased_items
        
        return {
            "total_items": total_items,
            "purchased_items": purchased_items,
            "pending_items": pending_items,
            "items": items
        }