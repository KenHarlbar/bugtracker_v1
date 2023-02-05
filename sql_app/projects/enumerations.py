from enum import Enum

class Status(str, Enum):
    '''
    Enum Description:
        ongoing means the project is undergoing development
        upcoming means the project isn't currently undergoing development but will, later!
        ended means the project isn't undergoing development and won't anymore
    '''
    ongoing = 'ongoing'
    upcoming = 'upcoming'
    ended = 'ended'
