#!/usr/bin/env python3
from .cell import Cell
from ..flag import Fill


class ExpanderRow(Cell):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.fill = Fill.X

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __draw(self) -> None:
        pass
