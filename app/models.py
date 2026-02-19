from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime,Numeric
from sqlalchemy.sql.functions import func

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())