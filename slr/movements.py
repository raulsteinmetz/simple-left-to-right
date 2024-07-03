from enum import Enum

class Action(Enum):
    STACK = 's'
    REDUCE = 'r'
    NOP = 'n'
    ACCEPT = 'ac'