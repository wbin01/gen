#!/usr/bin/env python3
from enum import Enum


class State(Enum):
    """..."""
    NORMAL = 'NORMAL'
    HOVER = 'HOVER'
    PRESSED = 'PRESSED'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
