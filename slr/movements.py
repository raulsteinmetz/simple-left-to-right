from enum import Enum

class Action(Enum):
    STACK = 's'
    REDUCE = 'r'
    NOP = 'n' # nop is the one after reductions
    ACCEPT = 'ac'