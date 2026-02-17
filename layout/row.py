#!/usr/bin/env python3
from ..flag import Align
from .layout import Layout


class Row(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(align=Align.HORIZONTAL, *args, **kwargs)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
