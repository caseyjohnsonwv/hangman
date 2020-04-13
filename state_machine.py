from enum import Enum, auto

class StateMachine(Enum):
    FIRST_TIME_LOAD = auto()
    NEW_GAME = auto()
    IN_PROGRESS = auto()
    GAME_OVER = auto()
    QUIT = auto()
    UNDEFINED = auto()
