from enum import Enum

class StateMachineError(Exception): pass

class StateMachine(Enum):
    FIRST_TIME_LOAD = auto()
    NEW_GAME = auto()
    IN_PROGRESS = auto()
    GAME_OVER = auto()
    UNDEFINED = auto()
