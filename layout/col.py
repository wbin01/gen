#!/usr/bin/env python3
from .layout import Layout


class Col(Layout):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

