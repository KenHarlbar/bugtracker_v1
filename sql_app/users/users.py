from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.orm import Session
from sql_app import security
from sql_app.dependencies import get_db

from . import crud, schemas


router = APIRouter()


@router.get('/me', response_model=schemas.UserOut)
def get_user(current_user = Depends(security.get_current_user)):
    return current_user


@router.post('/new', response_model=schemas.UserOut, status_code=201)
def create_user(user: schemas.UserIn, db: Session = Depends(get_db)):
    ''' Route for creating a new user '''
    if crud.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail='Username already exists, please choose another!')
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail='Email already exists, please login instead!')
    if len(user.password) < 8:
        raise HTTPException(status_code=400, detail='Password must be at least 8 characters long!')
    if ' ' in user.password:
        raise HTTPException(status_code=400, detail='Password cannot contain spaces!')
    return crud.create_user(db, user)


@router.put('/change_username', response_model=schemas.UserOut)
def change_username(user: schemas.UserUpdateUsername, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for editing username '''
    if current_user:
        db_user = crud.get_user_by_username(db, user.new_username)
        if db_user and db_user != current_user:
            raise HTTPException(status_code=400, detail='Username already exists, please choose another!')
        current_user.username = user.new_username
        current_user.save(db)
        return current_user
    raise HTTPException(status_code=401, detail='You must be logged in to change your username!')


@router.put('/change_email', response_model=schemas.UserOut)
def change_email(user: schemas.UserUpdateEmail, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for editing email '''
    if current_user:
        db_user = crud.get_user_by_email(db, user.new_email)
        if db_user and db_user != current_user:
            raise HTTPException(status_code=400, detail='email already exists, please choose another!')
        current_user.email = user.new_email
        current_user.save(db)
        return current_user
    raise HTTPException(status_code=401, detail='You must be logged in to change your email!')


@router.delete('/delete')
def delete_user(current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for deleting user '''
    if current_user:
        db.delete(current_user)
        db.commit()