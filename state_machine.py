from enum import IntEnum

class StateMachine(IntEnum):
    # LATER is used to quit game - twilio reserves QUIT keyword
    LATER = -1
    FIRST_TIME_LOAD = 1
    NEW_GAME = 2
    IN_PROGRESS = 3
    GAME_OVER = 4
