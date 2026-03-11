#!/usr/bin/env python3
from .container import Container


class Scroll(Container):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._scroll = self
        self._scroll_y = self._y
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
