from pydantic import BaseModel


class CommentIn(BaseModel):
    ''' Schema for comment input '''
    bug_id: str
    content: str


class CommentUpdate(CommentIn):
    ''' Schema for comment update '''
    comment_id: str
    content: str


class CommentOut(BaseModel):
    ''' Schema for comment output '''
    id: str
    content: str

    class Config:
        orm_mode = True
