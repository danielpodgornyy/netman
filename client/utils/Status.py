from enum import Enum

class Status(Enum):
    SUCCESS = 1
    SYNTAX_ERROR = -1
    CONNECTION_FAILED = 0
