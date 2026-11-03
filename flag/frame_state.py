#!/usr/bin/env python3
from enum import Enum


class FrameState(Enum):
    """..."""
    FRAME = 'FRAME'
    FULL = 'FULL'
    HIDDEN = 'HIDDEN'
    MAX = 'MAX'
    MIN = 'MIN'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
