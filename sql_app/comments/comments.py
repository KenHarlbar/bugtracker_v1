from sqlalchemy.orm import Session
from sql_app import security
from fastapi import APIRouter, HTTPException, Depends
from . import crud, schemas
from sql_app.dependencies import get_db
from sql_app import bugs


router = APIRouter()


@router.post('/', response_model=schemas.CommentOut)
def create_comment(comment: schemas.CommentIn, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for creating a comment '''
    if current_user:
        db_bug = bugs.crud.get_bug(db, comment.bug_id)
        if not db_bug:
            raise HTTPException(status_code=404, detail='Bug not found')
        if current_user not in db_bug.project.contributors:
            raise HTTPException(status_code=403, detail='Access denied')
        return crud.create_comment(db, comment, current_user.username)


@router.get('/{comment_id}', response_model=schemas.CommentOut)
def get_comment(comment_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for getting a comment '''
    if current_user:
        db_comment = crud.get_comment(db, comment_id)
        if not db_comment:
            raise HTTPException(status_code=404, detail='Comment not found')
        return db_comment


@router.put('/', response_model=schemas.CommentOut)
def update_comment(comment: schemas.CommentUpdate, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for updating a comment '''
    db_comment = crud.get_comment(db, comment.comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    if current_user == db_comment.user:
        return crud.update_comment(db, comment)
    raise HTTPException(status_code=403, detail='Access denied')


@router.delete('/{comment_id}')
def delete_comment(comment_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for deleting a comment '''
    db_comment = crud.get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail='Comment not found')
    if current_user == db_comment.user:
        return crud.delete_comment(db, comment_id)
    raise HTTPException(status_code=403, detail='Access denied')
