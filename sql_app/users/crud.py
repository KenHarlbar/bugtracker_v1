from . import model, schemas
from sql_app import security


def get_user(db, user_id: str):
    ''' Get user by id '''
    return db.query(model.User).filter(model.User.id == user_id).first()


def get_user_by_username(db, username: str):
    ''' Get user by username '''
    return db.query(model.User).filter(model.User.username == username).first()


def get_user_by_email(db, email: str):
    ''' Get user by email '''
    return db.query(model.User).filter(model.User.email == email).first()


def get_users(db, skip: int = 0, limit: int = 100):
    ''' Get all users '''
    return db.query(model.User).offset(skip).limit(limit).all()


def create_user(db, user: schemas.UserIn):
    ''' Create new user '''
    db_user = model.User(
        email=user.email,
        username=user.username,
        hashed_password=security.get_password_hash(user.password)
        )
    db_user.save(db)
    return db_user


def update_user_username(db, user: schemas.UserUpdateUsername):
    ''' Update db user '''
    db_user = get_user_by_username(db, user.old_username)
    db_user.username = user.new_username if user.new_username != '' else db_user.username
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_email(db, user: schemas.UserUpdateEmail):
    ''' Update db user '''
    db_user = get_user_by_email(db, user.old_email)
    db_user.email = user.new_email if user.new_email != '' else db_user.email
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db, user: schemas.UserDelete):
    ''' Delete user by id '''
    db_user = get_user_by_email(db, user.email)
    db_user.delete(db)
