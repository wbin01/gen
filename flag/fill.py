#!/usr/bin/env python3
from enum import Enum


class Fill(Enum):
    """Fills the empty space in the layout.
        
    Stretches the items in the configured direction: `Fill.X`, `Fill.Y`, 
    `Fill.XY`, `Fill.NONE`.
                
    `Fill` takes precedence over the `width` and `height` properties, so the 
    `width` property does not work together with `Fill.X` and the `height` 
    property does not work together with `Fill.Y`.
    """
    X = 'X'
    Y = 'Y'
    XY = 'XY'
    NONE = 'NONE'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
