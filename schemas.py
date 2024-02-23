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

class TokenResponse(BaseModel):
    access_token:str
    refresh_token:str
    token_type:str = 'Bearer'