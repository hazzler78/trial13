from sqlalchemy import Column, Integer, String, Float, Date, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, UTC

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(Date, default=lambda: datetime.now(UTC).date())
    updated_at = Column(Date, default=lambda: datetime.now(UTC).date(), onupdate=lambda: datetime.now(UTC).date())
    
    # Relationships
    inventory_items = relationship("InventoryItem", back_populates="user")
    recipes = relationship("Recipe", back_populates="user")
    shopping_list_items = relationship("ShoppingListItem", back_populates="user")

class InventoryItem(Base):
    __tablename__ = "inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float)
    unit = Column(String)
    expiry_date = Column(Date)
    created_at = Column(Date, default=lambda: datetime.now(UTC).date())
    updated_at = Column(Date, default=lambda: datetime.now(UTC).date(), onupdate=lambda: datetime.now(UTC).date())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship
    user = relationship("User", back_populates="inventory_items")

class Recipe(Base):
    __tablename__ = "recipes"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    ingredients = Column(JSON)  # List of ingredients with quantities
    instructions = Column(JSON)  # List of steps
    prep_time = Column(Integer)  # In minutes
    created_at = Column(Date, default=lambda: datetime.now(UTC).date())
    updated_at = Column(Date, default=lambda: datetime.now(UTC).date(), onupdate=lambda: datetime.now(UTC).date())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship
    user = relationship("User", back_populates="recipes")

class ShoppingListItem(Base):
    __tablename__ = "shopping_list"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float)
    unit = Column(String)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=True)
    purchased = Column(Boolean, default=False)
    created_at = Column(Date, default=lambda: datetime.now(UTC).date())
    updated_at = Column(Date, default=lambda: datetime.now(UTC).date(), onupdate=lambda: datetime.now(UTC).date())
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    recipe = relationship("Recipe")
    user = relationship("User", back_populates="shopping_list_items")