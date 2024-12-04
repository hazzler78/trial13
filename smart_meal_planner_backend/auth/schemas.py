from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johndoe",
            "email": "john@example.com"
        }
    })

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johndoe",
            "email": "john@example.com",
            "password": "secretpassword123"
        }
    })

class User(UserBase):
    id: int
    is_active: bool
    created_at: date
    updated_at: date

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer"
        }
    })

class TokenData(BaseModel):
    username: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "username": "johndoe",
            "password": "secretpassword123"
        }
    }) 