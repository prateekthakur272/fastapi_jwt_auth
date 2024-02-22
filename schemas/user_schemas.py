from pydantic import BaseModel, EmailStr
from database import Base
from sqlalchemy import (Column, String, Integer, Text, Boolean)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=True, default='')
    last_name = Column(String(100), nullable=True, default='')
    email = Column(String(200), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_staff = Column(Boolean, default=False)

class UserRegister(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str
    
