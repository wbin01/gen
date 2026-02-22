#!/usr/bin/env python3
from enum import Enum


class Align(Enum):
    """An Alignment Enum.
    
    Alignment only works in the direction of the layout with the `fill` option 
    active. This means that the `Col` needs to have `fill` set to `Fill.X` and 
    the `Row` needs to have `fill` set to `Fill.Y`.
                
    In a `Row` layout, using `Align.START` will align to the left, 
    `Align.CENTER` to the center, and `Align.END` will align to the right.
    
    In a `Col` layout, `Align.START` will align to the top, `Align.CENTER` to 
    the center, and `Align.END` will align to the bottom.
    """
    CENTER = 'CENTER'
    END = 'END'
    START = 'START'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
