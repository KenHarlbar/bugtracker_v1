from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from . import crud, schemas
from sql_app.dependencies import get_db
from sql_app import users, security


router = APIRouter()


@router.get('/', response_model=List[schemas.ProjectOut])
def get_projects(db: Session = Depends(get_db), current_user = Depends(security.get_current_user),):
    ''' Route for getting all projects '''
    if current_user:
        return crud.get_projects(db)


@router.get('/project', response_model=schemas.ProjectOut)
def get_project(project_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for getting a particular project by ID '''
    if current_user:
        if not crud.get_project(db, project_id):
            raise HTTPException(status_code=404, detail='Project not found')
        return crud.get_project(db, project_id)


@router.post('/new', response_model=schemas.ProjectOut)
def new_project(project: schemas.ProjectIn, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for creating project '''
    if current_user:
        return crud.create_project(db, project, current_user.username)


@router.put('/update', response_model=schemas.ProjectOut)
def update_project(project: schemas.ProjectUpdate, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for updating project '''
    if current_user:
        db_project = crud.get_project(db, project.project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail='Project not found')
        if current_user not in db_project.contributors:
            raise HTTPException(status_code=403, detail=f'You are not a contributor to this project')
        return crud.update_project(db, project)

@router.delete('/delete/{project_id}')
def delete_project(project_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for deleting a project '''
    if current_user:
        db_project = crud.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail='Project not found')
        if current_user.id not in db_project.managed_by:
            raise HTTPException(status_code=403, detail=f'You do not manage this project')
        crud.delete_project(db, project_id)


@router.put('/contributors/new', response_model=schemas.ProjectAddUsersOut)
def add_contributors(project: schemas.ProjectAddUsers, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for adding contributors to a project '''
    db_project = crud.get_project(db, project.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail='Project not found')
    if current_user and current_user.id in db_project.managed_by:
        scammers = []
        for username in project.usernames:
            db_project = crud.get_project(db, project.project_id)
            db_user = users.crud.get_user_by_username(db, username)
            if not db_user:
                scammers.append(username)
            elif db_user not in db_project.contributors:
                db_project.contributors.append(db_user)
                db_project.save(db)
        if not scammers:
            return crud.get_project(db, project.project_id)
        else:
            raise HTTPException(status_code=404, detail=f'{(", ").join(scammers)} do not exists')
    else:
        raise HTTPException(status_code=403, detail='You do not manage this project')


@router.put('/contributors/remove/', response_model=schemas.ProjectDeleteContributorsOut)
def delete_contributors(project: schemas.ProjectDeleteContributorsIn, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for deleting contributors from a project '''
    db_project = crud.get_project(db, project.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail='Project not found')
    if current_user and current_user.id in db_project.managed_by:
        scammers = []
        for username in project.users_to_remove_usernames:
            db_project = crud.get_project(db, project.project_id)
            db_user = users.crud.get_user_by_username(db, username)
            if not db_user:
                scammers.append(username)
            elif db_user in db_project.contributors:
                db_project.contributors.remove(db_user)
                db_project.save(db)
        if not scammers:
            return crud.get_project(db, project.project_id)
        else:
            raise HTTPException(status_code=404, detail=f'{(", ").join(scammers)} do not exists')
    else:
        raise HTTPException(status_code=403, detail='You do not manage this project')


@router.put('/managers/new', response_model=schemas.ProjectAddManagersOut)
def add_managers(project: schemas.ProjectAddManagersIn, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for adding managers to a project '''
    db_project = crud.get_project(db, project.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail='Project not found')
    if current_user and current_user.id in db_project.managed_by:
        scammers = []
        for username in project.managers_to_add_usernames:
            db_project = crud.get_project(db, project.project_id)
            db_user = users.crud.get_user_by_username(db, username)
            if not db_user:
                scammers.append(username)
            elif db_user not in db_project.managed_by:
                db_project.managed_by.append(db_user.id)
                db_project.save(db)
        if not scammers:
            return crud.get_project(db, project.project_id)
        else:
            raise HTTPException(status_code=404, detail=f'{(", ").join(scammers)} do not exists')
    else:
        raise HTTPException(status_code=403, detail='You do not manage this project')


@router.put('/managers/delete', response_model=schemas.ProjectDeleteManagersOut)
def delete_managers(project: schemas.ProjectDeleteManagersIn, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for deleting managers from a project '''
    db_project = crud.get_project(db, project.project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail='Project not found')
    if current_user and current_user.id in db_project.managed_by:
        scammers = []
        for username in project.managers_to_remove_usernames:
            db_project = crud.get_project(db, project.project_id)
            db_user = users.crud.get_user_by_username(db, username)
            if not db_user:
                scammers.append(username)
            elif db_user in db_project.managed_by:
                db_project.managed_by.remove(db_user.id)
                db_project.save(db)
        if not scammers:
            return crud.get_project(db, project.project_id)
        else:
            raise HTTPException(status_code=404, detail=f'{(", ").join(scammers)} do not exists')
    else:
        raise HTTPException(status_code=403, detail='You do not manage this project')


@router.get('{project_id}/contributors/', response_model=List[users.schemas.UserOutAsContributor])
def get_contributors(project_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for getting contributors of a project '''
    if current_user:
        db_project = crud.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail='Project not found')
        return db_project.contributors


@router.get('{project_id}/managers/', response_model=List[users.schemas.UserOutAsManager])
def get_managers(project_id: str, current_user = Depends(security.get_current_user), db: Session = Depends(get_db)):
    ''' Route for getting managers of a project '''
    if current_user:
        db_project = crud.get_project(db, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail='Project not found')
        return db_project.managed_by
