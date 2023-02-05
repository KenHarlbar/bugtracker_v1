from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship

from sql_app.database import Base
from sql_app.mixins import BaseModelMixin


class Comment(BaseModelMixin, Base):
    ''' Comment model '''
    __tablename__ = 'comments'

    content = Column(String(500), nullable=False)
    bug_id = Column(String(60), ForeignKey('bugs.id'))
    user_id = Column(String(60), ForeignKey('users.id'))
    user = relationship('User', back_populates='comments')
    bug = relationship('Bug', back_populates='comments')
