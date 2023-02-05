from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends
from jose import JWTError, jwt
from typing import Union
from datetime import timedelta, datetime
from os import getenv
from fastapi import HTTPException, status

from .dependencies import get_db, oauth2_scheme
from . import users, security_schemas
from .users.schemas import User


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
    ''' A function that generates a hashed password '''
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    ''' A function that checks password against the hashed password '''
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    ''' A function that authenticates a user '''
    user = users.crud.get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    ''' A function that creates an access token '''
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, getenv('SECRET_KEY'), algorithm=getenv('ALGORITHM'))
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    ''' A function to get the current user '''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        payload = jwt.decode(token, getenv('SECRET_KEY'), algorithms=[getenv('ALGORITHM')])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = security_schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = users.crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    ''' A function to get the current active user '''
    if current_user.disabled:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user
