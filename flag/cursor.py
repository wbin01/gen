#!/usr/bin/env python3
from enum import Enum


class Cursor(Enum):
    """..."""
    TOP = 'TOP'
    BOTTOM = 'BOTTOM'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    TOP_LEFT = 'TOP_LEFT'
    BOTTOM_RIGHT = 'BOTTOM_RIGHT'
    TOP_RIGHT = 'TOP_RIGHT'
    BOTTOM_LEFT = 'BOTTOM_LEFT'
    NONE = 'NONE'
    DRAG = 'DRAG'
    BEAM = 'BEAM'
    WAIT = 'WAIT'
    CROSSHAIR = 'CROSSHAIR'
    ARROW_WAIT = 'ARROW_WAIT'
    NOT_ALLOWED = 'NOT_ALLOWED'
    POINTER = 'POINTER'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
