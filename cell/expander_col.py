#!/usr/bin/env python3
from .cell import Cell
from ..flag import Fill


class ExpanderCol(Cell):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._Size__width_ = 0
        self._Size__width = 0
        self._Size__height_ = 0
        self._Size__height = 0
        self.fill = Fill.Y

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __draw(self) -> None:
        pass
