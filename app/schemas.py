from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Optional
from datetime import datetime

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
class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
