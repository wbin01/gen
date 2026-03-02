#!/usr/bin/env python3
from enum import Enum


class StyleClass(Enum):
    """..."""
    CHECKED = 'CHECKED'
    DEFAULT = 'DEFAULT'
    DISABLED = 'DISABLED'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    WARNING = 'WARNING'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
