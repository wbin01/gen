#!/usr/bin/env python3
from enum import Enum


class Align(Enum):
    """..."""
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'
    FILL = 'FILL'

    def __repr__(self) -> str:
        return self.__class__.__name__
