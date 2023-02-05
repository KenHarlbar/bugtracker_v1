from pydantic import BaseModel
from typing import List

from sql_app.bugs.schemas import BugOut


class ProjectIn(BaseModel):
    ''' Schema for project input '''
    name: str
    description: str = ''
    status: str = 'ongoing'
    

class ProjectUpdate(ProjectIn):
    project_id: str


class ProjectAddUsers(BaseModel):
    ''' Schema for adding users to project '''
    project_id: str
    usernames: List[str]


class ProjectOut(BaseModel):
    ''' Schema for project output '''
    id: str
    name: str
    description: str
    status: str
    bugs: List[BugOut] = []

    class Config:
        orm_mode = True


class UserOutForAddUser(BaseModel):
    ''' Schema for user output for ProjectAddUsersOut '''
    id: str
    email: str
    username: str

    class Config:
        orm_mode = True


class ProjectAddUsersOut(BaseModel):
    ''' Schema for ProjectAddUser output '''
    id: str
    name: str
    description: str
    status: str
    contributors: List[UserOutForAddUser]

    class Config:
        orm_mode = True


class ProjectDeleteContributorsIn(BaseModel):
    ''' Schema for deleting contributors from project '''
    project_id: str
    users_to_remove_usernames: List[str]


class ProjectDeleteContributorsOut(ProjectAddUsersOut):
    ''' Schema for ProjectDeleteUser output '''
    pass


class ProjectAddManagersIn(BaseModel):
    ''' Schema for adding managers to project '''
    project_id: str
    managers_to_add_usernames: List[str]


class ProjectAddManagersOut(BaseModel):
    ''' Schema for ProjectAddManagers output '''
    id: str
    name: str
    description: str
    status: str
    managed_by: List[UserOutForAddUser]

    class Config:
        orm_mode = True


class ProjectDeleteManagersIn(BaseModel):
    ''' Schema for deleting managers from project '''
    project_id: str
    managers_to_remove_usernames: List[str]


class ProjectDeleteManagersOut(ProjectAddManagersOut):
    ''' Schema for ProjectDeleteManagers output '''
    pass
