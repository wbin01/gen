#!/usr/bin/env python3
from enum import Enum


class State(Enum):
    """..."""
    BASE = 'BASE'
    HOVER = 'HOVER'
    PRESSED = 'PRESSED'
    DISABLED = 'DISABLED'
    CHECKED = 'CHECKED'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
