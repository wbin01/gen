#!/usr/bin/env python3
from enum import Enum


class Event(Enum):
    """..."""
    PRESSED = 'PRESSED'
    RELEASED = 'RELEASED'
    LEAVE = 'LEAVE'
    ENTER = 'ENTER'
    MOVE = 'MOVE'

    CLICKED = 'CLICKED'
    HOVER = 'HOVER'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
