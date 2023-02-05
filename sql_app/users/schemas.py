from pydantic import BaseModel, EmailStr
from typing import List
from sql_app.projects.schemas import ProjectOut


class User(BaseModel):
    ''' Schema for user '''
    email: EmailStr
    username: str


class UserUpdateUsername(BaseModel):
    ''' Schema for user update '''
    new_username: str


class UserUpdateEmail(BaseModel):
    ''' Schema for user update '''
    new_email: EmailStr


class UserIn(BaseModel):
    ''' Schema for user input '''
    email: EmailStr
    username: str
    password: str


class UserDelete(BaseModel):
    ''' Schema for deleting user '''
    email: EmailStr
    password: str


class UserOut(BaseModel):
    ''' Schema for user output '''
    id: str
    email: EmailStr
    username: str
    projects: List[ProjectOut] = []

    class Config:
        orm_mode = True


class UserOutAsContributor(BaseModel):
    ''' Schema for user output as contributor '''
    id: str
    username: str

    class Config:
        orm_mode = True


class UserOutAsManager(BaseModel):
    ''' Schema for user output as manager '''
    id: str
    username: str

    class Config:
        orm_mode = True