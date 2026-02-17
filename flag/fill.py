#!/usr/bin/env python3
from enum import Enum


class Fill(Enum):
    """..."""
    X = 'X'
    Y = 'Y'
    ALL = 'ALL'
    NONE = 'NONE'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
