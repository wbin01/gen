#!/usr/bin/env python3
from .col import Col


class Scroll(Col):
    """..."""
    def __init__(
            self, width: int = None, height: int = None,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(width=width, height=height, *args, **kwargs)
        self._view_width = width
        self._view_heigh = height
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
