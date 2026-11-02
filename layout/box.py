#!/usr/bin/env python3
from .container import Container


class Frame:
    pass


class Box(Container):
    """..."""
    def __init__(
            self, frame: Frame, horizontal: bool = False,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._type_class = 'Box'
        self.app = frame
        if horizontal: self._orientation = 'HORIZONTAL'
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
