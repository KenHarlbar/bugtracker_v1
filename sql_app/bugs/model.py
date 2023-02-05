from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from sql_app.database import Base
from sql_app.mixins import BaseModelMixin


class Bug(BaseModelMixin, Base):
    ''' Bug model '''
    __tablename__ = 'bugs'

    title = Column(String(250), nullable=False)
    description = Column(String(500))
    status = Column(String(60), nullable=False)
    priority = Column(String(60), nullable=False)
    project_id = Column(String(60), ForeignKey('projects.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    project = relationship('Project', back_populates='bugs')
    user = relationship('User', back_populates='bugs')
    comments = relationship('Comment', back_populates='bug')