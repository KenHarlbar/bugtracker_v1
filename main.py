from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from os import getenv

from sql_app.database import engine
from sql_app.users import users, model as user_model
from sql_app.projects import projects, model as project_model
from sql_app.bugs import bugs, model as bug_model
from sql_app.comments import comments, model as comment_model
from sql_app import security_schemas, security
from sql_app.dependencies import get_db


user_model.Base.metadata.create_all(bind=engine)
project_model.Base.metadata.create_all(bind=engine)
bug_model.Base.metadata.create_all(bind=engine)
comment_model.Base.metadata.create_all(bind=engine)


app = FastAPI()


app.include_router(
    users.router,
    prefix = '/api/v1/users',
    tags = ['Users']
    )
app.include_router(
    projects.router,
    prefix = '/api/v1/projects',
    tags = ['Projects']
    )
app.include_router(
    bugs.router,
    prefix = '/api/v1/bugs',
    tags = ['Bugs']
    )
app.include_router(
    comments.router,
    prefix = '/api/v1/comments',
    tags = ['Comments']
    )


@app.post('/api/v1/token', response_model=security_schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    ''' Route that generates a token for a user '''
    user = security.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'}
            )
    mins = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
    access_token_expires = timedelta(minutes=mins)
    access_token = security.create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}
