from enum import Enum

class ServiceOrderStatus(str, Enum):
    OPEN = 1
    IN_PROGRESS = 2
    CLOSED = 3