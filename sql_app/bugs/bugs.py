from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from . import crud, schemas
from sql_app.dependencies import get_db
from sql_app import users, projects
from sql_app import security


router = APIRouter()


@router.get('/', response_model=schemas.BugOut)
def get_bugs(db: Session = Depends(get_db), current_user = Depends(security.get_current_user)):
    ''' Route for getting all bugs '''
    if current_user:
        return crud.get_bugs(db)


@router.get('/{bug_id}', response_model=schemas.BugOut)
def get_bug(bug_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for getting a bug by id '''
    if current_user:
        db_bug = crud.get_bug(db, bug_id)
        if not db_bug:
            raise HTTPException(status_code=404, detail='Bug not found')
        return db_bug


@router.post('/', response_model=schemas.BugOut)
def create_bug(bug: schemas.BugIn, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for creating a bug '''
    if current_user:
        db_project = projects.crud.get_project(db, bug.project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail='Project not found')
        if current_user not in db_project.contributors:
            raise HTTPException(status_code=403, detail='Access denied')
        return crud.create_bug(db, bug, current_user.username)


@router.put('/', response_model=schemas.BugOut)
def update_bug(bug: schemas.BugUpdate, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for updating a bug '''
    if current_user:
        db_bug = crud.get_bug(db, bug.bug_id)
        if not db_bug:
            raise HTTPException(status_code=404, detail='Bug not found')
        if current_user not in db_bug.project.contributors:
            raise HTTPException(status_code=403, detail='Access denied')
        return crud.update_bug(db, bug)


@router.delete('/{bug_id}')
def delete_bug(bug_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for deleting a bug '''
    db_bug = crud.get_bug(db, bug_id)
    if not db_bug:
        raise HTTPException(status_code=404, detail='Bug not found')
    if current_user == db_bug.user:
        return crud.delete_bug(db, bug_id)
