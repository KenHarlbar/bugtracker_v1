from . import model, schemas, enumerations
from sql_app import users


def get_project(db, project_id: str):
    ''' Get project by id '''
    return db.query(model.Project).filter(model.Project.id == project_id).first()


def get_projects(db, skip: int = 0, limit: int = 100):
    ''' Get all projects '''
    return db.query(model.Project).offset(skip).limit(limit).all()


def get_projects_by_user(db, user_id: str, skip: int = 0, limit: int = 100):
    ''' Get all projects '''
    db_user = get_project(db, user_id)
    if not db_user:
        return 'user_not_found'
    return db.query(model.Project).where(db_user.in_(list(model.Project.users))).offset(skip).limit(limit).all()


def create_project(db, project: schemas.ProjectIn, username: str):
    ''' Create new project '''
    db_user = users.crud.get_user_by_username(db, username)
    db_project = model.Project(
        name=project.name,
        description=project.description,
        status=enumerations.Status.__dict__.get(project.status, 'ongoing'),
        created_by = db_user.id
        )
    db_project.contributors.append(db_user)
    if not db_project.managed_by:
        db_project.managed_by = []
    db_project.managed_by += [db_user.id]
    db_project.save(db)
    return db_project


def update_project(db, project: schemas.ProjectUpdate):
    ''' Update db project '''
    db_project = get_project(db, project.project_id)
    db_project.name = project.name if project.name != '' else db_project.name
    db_project.description = project.description if project.description != '' else db_project.description
    db_project.status = enumerations.Status.__dict__.get(project.status,
        'ongoing') if project.status != '' or not project.status else db_project.status
    db_project.save(db)
    return db_project


def delete_project(db, project_id: str,):
    ''' Delete a project '''
    db_project = get_project(db, id)
    db_project.delete(db)
