from . import model, schemas, enumerations
from sql_app import users, projects



def get_bug(db, bug_id: str):
    ''' Get bug by id '''
    return db.query(model.Bug).filter(model.Bug.id == bug_id).first()


def get_bugs_by_project(db, project_id: str, skip: int = 0, limit: int = 100):
    ''' Get all bugs '''
    return db.query(model.Bug).filter(model.Bug.project_id == project_id).offset(skip).limit(limit).all()


def get_bugs(db, skip: int = 0, limit: int = 100):
    ''' Get all bugs '''
    return db.query(model.Bug).offset(skip).limit(limit).all()


def create_bug(db, bug: schemas.BugIn, username: str):
    ''' Create a bug '''
    db_user = users.crud.get_user_by_username(db, username)
    db_project = projects.crud.get_project(db, bug.project_id)
    db_bug = model.Bug(
        title = bug.title,
        description = bug.description,
        status = enumerations.Status.get('status', 'not_fixed'),
        priority = enumerations.Priority.get('priority', 'low'),
        user_id = db_user.id,
        project_id = db_project.id
        )
    db.add(db_bug)
    db.commit()
    db.refresh(db_bug)
    return db_bug


def update_bug(db, bug: schemas.BugUpdate):
    ''' Update a bug '''
    db_bug = get_bug(db, bug.id)
    # start update
    db_bug.title = bug.title if bug.title != '' else db_bug.title
    db_bug.description = bug.description if bug.description != '' else db_bug.description
    db_bug.status = enumerations.Status.__dict__.get(bug.status, 'not_fixed')
    db_bug.priority = enumerations.Priority.__dict__.get(bug.priority, 'low')
    db.add(db_bug)
    db.commit()
    db.refresh(db_bug)
    return db_bug


def delete_bug(db, bug_id: str):
    ''' Delete a bug '''
    db_bug = get_bug(db, bug_id)
    db_bug.delete(db)