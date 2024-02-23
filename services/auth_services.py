from models import User
from fastapi.exceptions import HTTPException
from fastapi import Depends, status
from utils.auth_utils import create_access_token, create_refresh_token, get_payload
from schemas.responses import TokenResponse
from database import get_db_session
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer


oauth_scheme = OAuth2PasswordBearer(tokenUrl='auth/token')

def _check_account_access(user:User) -> bool:
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not active')
    if not user.is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='user not verified')
    return True

def generate_tokens(user:User, refresh_token:str|None=None) -> TokenResponse:
    payload = {'id':user.id, 'email':user.email}
    access_token = create_access_token(payload)
    if not refresh_token:
        refresh_token = create_refresh_token(payload)
    return TokenResponse(access_token=access_token,refresh_token=refresh_token)

def refresh_access_token(user:User, refresh_token:str):
    payload = get_payload(refresh_token)
    user_id = payload.get('id',None)
    if (not user_id) and (not user.id==user_id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid refresh token')
    return generate_tokens(user, refresh_token)

def get_current_user(token:TokenResponse = Depends(oauth_scheme), db:Session = Depends(get_db_session)):
    payload = get_payload(token)
    print(payload is dict)
    if payload:
        user_id = payload.get('id', None)
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid or expired token')
