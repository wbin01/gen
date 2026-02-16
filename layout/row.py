#!/usr/bin/env python3
from ..flag import Orientation
from .layout import Layout


class Row(Layout):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        self.orientation = Orientation.HORIZONTAL
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

