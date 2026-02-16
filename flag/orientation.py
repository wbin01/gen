#!/usr/bin/env python3
from enum import Enum


class Orientation(Enum):
    """..."""
    VERTICAL = 'VERTICAL'
    HORIZONTAL = 'HORIZONTAL'

    def __repr__(self) -> str:
        return self.__class__.__name__
