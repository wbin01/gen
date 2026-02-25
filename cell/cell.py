#!/usr/bin/env python3
import copy

from ..flag import Fill
from ..mixin import Margin, Pos, Size
from ..ui import UI, Theme


class Cell(Margin, Pos, Size, UI):
    """..."""
    def __init__(self, style_class: str = None, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__drawer = None
        self.__fill = Fill.X
        self.__style_class = style_class

        theme = getattr(Theme, self.__class__.__name__.lower())  # Theme.button
        if self.__style_class:
            if self.__style_class not in Theme.classes:
                Theme.classes[self.__style_class] = copy.deepcopy(theme)
            self.__style = Theme.classes[self.__style_class]
        else:
            self.__style = theme # Theme.button
        
        self.texture_base = None
        self.texture_hover = None
        self.needs_rebuild = True
    
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
    
    @property
    def style(self) -> dict:
        return self.__style
    
    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style
    
    def __hit_test(self, x: int, y: int) -> UI | None:
        if not self.visible:
            return None

        if self._UI__rect_contains(self, x, y):
            return self
        
        return None

    def __draw(self) -> None:
        pass
