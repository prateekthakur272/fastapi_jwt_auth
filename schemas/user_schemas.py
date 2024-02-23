from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    first_name:str
    last_name:str
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    first_name:str
    last_name:str
    email:EmailStr
    is_active:bool
    is_verified:bool
    is_staff:bool