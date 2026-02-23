#!/usr/bin/env python3
from ..flag import Fill
from ..mixin import Margin, Pos, Size
from ..ui import UI


class Cell(Margin, Pos, Size, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__drawer = None
        self.__fill = Fill.X
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def fill(self) -> Fill:
        """..."""
        return self.__fill
    
    @fill.setter
    def fill(self, fill: Fill) -> None:
        self.__fill = fill
    
    def __hit_test(self, x: int, y: int) -> UI | None:
        if not self.visible:
            return None

        if self._UI__rect_contains(self, x, y):
            return self
        
        return None

    def __draw(self) -> None:
        pass
