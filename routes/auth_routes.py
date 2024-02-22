from fastapi.routing import APIRouter
from fastapi import Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db_session
from schemas.user_schemas import UserRegister, User
from utils.auth_utils import get_hashed_password


router = APIRouter(prefix='/auth', tags=['Auth'], responses={404:{'description':'not found'}})

@router.post('/register', status_code=status.HTTP_201_CREATED, response_class=JSONResponse)
def create_user(user:UserRegister, db:Session = Depends(get_db_session)):
    if(db.query(User).filter(User.email==user.email).first()):
        return HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='user with same email already exists')
    new_user = User(**user.model_dump(exclude=['password']), password=get_hashed_password(user.password))
    db.add(new_user)
    db.commit()
    return {'message':'account created successfully'}