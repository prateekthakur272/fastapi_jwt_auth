from datetime import timedelta, datetime
from passlib.context import CryptContext
from config import get_settings
import jwt

settings = get_settings()
password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_hashed_password(plain_password:str) ->str :
    return password_context.hash(plain_password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return password_context.verify(plain_password, hashed_password)

def create_access_token(payload:dict) -> str:
    token_payload = payload.copy()
    expire_in = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_TIME)
    token_payload.update({'exp': expire_in})
    access_token = jwt.encode(token_payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return access_token


def create_refresh_token(payload:dict) -> str:
    refresh_token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return refresh_token

def get_payload(token:str)-> dict|None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        print(payload)
        return payload
    except jwt.PyJWTError:
        return None