from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from sql_app.database import Base
from sql_app.mixins import BaseModelMixin


user_project = Table(
    'user_project',
    Base.metadata,
    Column('user_id', String(60), ForeignKey('users.id',
            ondelete='CASCADE', onupdate='CASCADE'), primary_key=True),
    Column('project_id', String(60), ForeignKey('projects.id',
            ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
)


class User(BaseModelMixin, Base):
    ''' User model '''
    __tablename__ = 'users'

    email = Column(String(60), unique=True, nullable=False)
    username = Column(String(60), unique=True, nullable=False)
    hashed_password = Column(String(60), nullable=False)
    bugs = relationship('Bug', back_populates='user')
    comments = relationship('Comment', back_populates='user')
    projects = relationship('Project', secondary=user_project,
                            back_populates='contributors', cascade='all, delete')
