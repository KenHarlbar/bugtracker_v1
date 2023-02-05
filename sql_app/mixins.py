from sqlalchemy import Column, String, DateTime
from datetime import datetime
from sqlalchemy.orm import Session
from uuid import uuid4

class BaseModelMixin:
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime(), default=datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.utcnow)

    def __init__(self, *args, **kwargs) -> None:
        ''' Initializes BaseModelMixin '''
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        self.id = str(uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def __str__(self) -> str:
        ''' Method that returns a string of information about the class '''
        return '[{}] ({}) {}'.format(self.__class__.__name__, self.id, self.__dict__)

    def save(self, db: Session) -> None:
        ''' Method that Updates updated_at and saves the object '''
        self.updated_at = datetime.utcnow()
        db.add(self)
        db.commit()
        db.refresh(self)

    def delete(self, db: Session) -> None:
        ''' Method for deleting an object '''
        db.delete(self)
        db.commit()
