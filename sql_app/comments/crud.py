from . import model, schemas
from sql_app import users, projects, bugs


def get_comment(db, comment_id: str):
    ''' Get a comment by id '''
    return db.query(model.Comment).filter(model.Comment.id == comment_id).first()


def get_comments_by_bug(db, bug_id: str, skip: int = 0, limit: int = 100):
    ''' Get multiple comments '''
    return db.query(model.Comment).filter(model.Comment.bug_id == bug_id).offset(skip).limit(limit).all()


def get_comments(db, skip: int = 0, limit: int = 100):
    ''' Get multiple comments '''
    return db.query(model.Comment).offset(skip).limit(limit).all()


def create_comment(db, comment: schemas.CommentIn, username: str):
    ''' Create a new comment '''
    db_user = users.crud.get_user_by_username(db, comment.username)
    db_bug = bugs.crud.get_bug(db, comment.bug_id)
    db_comment = model.Comment(
        content = comment.content,
        bug_id = db_bug.id,
        user_id = db_user.id
        )
    db_comment.save(db)
    return db_comment


def update_comment(db, comment: schemas.CommentUpdate):
    ''' Update a comment '''
    db_comment = get_comment(db, comment.comment_id)
    # Begin update
    db_comment.content = comment.content if comment.content != '' else db_comment.content
    db_comment.save(db)
    return get_comment(db, comment.comment_id)


def delete_comment(db, comment_id: str):
    ''' Delete a comment '''
    db_comment = get_comment(db, comment_id)
    db.delete(db_comment)
    db.commit()
