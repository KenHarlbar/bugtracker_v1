from pydantic import BaseModel
from typing import List
from sql_app.comments.schemas import CommentOut


class BugIn(BaseModel):
    ''' Schema for bug input '''
    project_id: str
    title: str
    description: str = ''
    status: str
    priority: str


class BugUpdate(BaseModel):
    ''' Schema for bug update '''
    bug_id: str
    title: str
    description: str = ''
    status: str
    priority: str


class BugOut(BaseModel):
    ''' Schema for bug output '''
    id: str
    title: str
    description: str
    status: str
    priority: str
    user_id: str
    comments: List[CommentOut] = []

    class Config:
        orm_mode = True
