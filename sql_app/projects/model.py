from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY

from sql_app.database import Base
from sql_app.mixins import BaseModelMixin
from sql_app.users.model import user_project


class Project(BaseModelMixin, Base):
    ''' Project model '''
    __tablename__ = 'projects'

    name = Column(String(250), nullable=False)
    description = Column(String(500))
    status = Column(String(60))
    created_by = Column(String(60))
    managed_by = Column(ARRAY(String(60)))
    bugs = relationship('Bug', back_populates='project')
    contributors = relationship('User', secondary=user_project,
                        back_populates='projects', passive_deletes=True)