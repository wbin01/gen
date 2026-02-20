#!/usr/bin/env python3
from enum import Enum


class Align(Enum):
    """..."""
    BOTTOM = 'BOTTOM'
    BOTTOM_LEFT = 'BOTTOM_LEFT'
    BOTTOM_RIGHT = 'BOTTOM_RIGHT'
    CENTER = 'CENTER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    TOP = 'TOP'
    TOP_LEFT = 'TOP_LEFT'
    TOP_RIGHT = 'TOP_RIGHT'
    NONE = 'NONE'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
