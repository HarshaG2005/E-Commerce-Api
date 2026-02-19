from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class TokenData(BaseModel):
    id: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class CreateUser(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    id: int
    email: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CreateProduct(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal=Field( gt=0)  # Ensure price is greater than 0
    stock: int=Field(ge=0)  # Ensure stock is non-negative

class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: Decimal=Field( gt=0)  # Ensure price is greater than 0
    stock: int=Field(ge=0)  # Ensure stock is non-negative
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class UpdateProduct(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[Decimal] = None
    stock: Optional[int] = None

