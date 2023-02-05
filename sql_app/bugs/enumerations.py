from enum import Enum

class Status(str, Enum):
    '''
    Enum Description:
        fixed means bug is fixed
        not fixed means bug is not fixed
    '''
    fixed = 'fixed'
    not_fixed = 'not fixed'


class Priority(str, Enum):
    '''
    Enum Description:
        normal means low priority
        important means medium priority
        very important means high priority
    '''
    normal = 'normal'
    important = 'important'
    very_important = 'very important'
