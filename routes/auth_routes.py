from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db_session
from schemas.user_schemas import UserRegister
from models import User
from utils.auth_utils import get_hashed_password, get_payload, verify_password
from services.auth_services import generate_tokens
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from schemas.responses import TokenResponse

router = APIRouter(prefix='/auth', tags=['Auth'], responses={404:{'description':'not found'}})
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')

@router.post('/register', status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
def create_user(user:UserRegister, db:Session = Depends(get_db_session)):
    if(db.query(User).filter(User.email==user.email).first()):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='user with same email already exists')
    new_user = User(**user.model_dump(exclude=['password']), password=get_hashed_password(user.password))
    db.add(new_user)
    db.commit()
    return {'message':'account created successfully'}


@router.post('/token', status_code=status.HTTP_200_OK, response_class=JSONResponse, response_model=TokenResponse)
def get_token(data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db_session)):
    user = db.query(User).filter(User.email==data.username).first()
    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='user not found')
    if not verify_password(data.password, user.password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid password')
    return generate_tokens(user)


@router.post('/refresh-token', status_code=status.HTTP_200_OK)
def refresh_access_token(refresh_token:str = Header(), db:Session = Depends(get_db_session)):
    payload = get_payload(refresh_token)
    user_id = payload.get('id',None)
    user = db.query(User).filter(User.id==1).first()
    if not user_id and not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid refresh token')
    return generate_tokens(user, refresh_token)