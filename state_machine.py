from enum import IntEnum

class StateMachine(IntEnum):
    QUIT = -1
    UNDEFINED = 0
    FIRST_TIME_LOAD = 1
    NEW_GAME = 2
    IN_PROGRESS = 3
    GAME_OVER = 4
