#!/usr/bin/env python3
from ..flag import Fill
from ..mix import Margin, Position, Size
from ..ui import UI


class Cell(Margin, Position, Size, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__drawer = None
        self.__fill = Fill.X
        self.__visible = True

    @property
    def fill(self) -> Fill:
        """..."""
        return self.__fill
    
    @fill.setter
    def fill(self, fill: Fill) -> None:
        self.__fill = fill
    
    @property
    def visible(self) -> bool:
        """..."""
        return self.__visible
    
    @visible.setter
    def visible(self, visible: bool) -> None:
        self.__visible = visible
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def __draw(self) -> None:
        pass
