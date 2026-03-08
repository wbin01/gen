#!/usr/bin/env python3
import copy
import ctypes

import sdl3

from ..flag import Fill
from ..mixin import Margin, Size
from ..ui import UI, Theme
from ..flag import StyleClass


class Cell(Margin, Size, UI):
    """..."""
    def __init__(
            self, style_class: str = None, fill: Fill = Fill.XY,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._base_class = 'Cell'
        
        self._drawer = None
        self._fill = fill
        self._style_class = style_class

        self._x = 0
        self._y = 0

        self._style = None
        self.style_class = style_class

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def fill(self) -> Fill:
        """..."""
        return self._fill
    
    @fill.setter
    def fill(self, fill: Fill) -> None:
        self._fill = fill
    
    @property
    def style(self) -> dict:
        return self._style
    
    @style.setter
    def style(self, style: dict) -> None:
        self._style = style
    
    @property
    def style_class(self) -> str:
        return self._style_class
    
    @style_class.setter
    def style_class(self, style_class: str) -> None:

        class_name = self.__class__.__name__
        if not hasattr(Theme, class_name):
            class_name = self.__class__.__base__.__name__
        
        theme = None
        if hasattr(Theme, class_name):
            theme = getattr(Theme, class_name)

        class_theme = None
        if style_class:
            if isinstance(style_class, StyleClass):
                class_theme = Theme.classes[style_class.value]
            else:
                if style_class in Theme.classes:
                    class_theme = Theme.classes[style_class]
                else:
                    Theme.classes[style_class] = theme
                    class_theme = Theme.classes[style_class]

        theme = copy.deepcopy(theme)
        if theme and class_theme:
            for state in ('BASE', 'HOVER', 'PRESSED'):
                for key in (
                        'font-color', 'background-color', 'border-color'):
                    if key in theme[state]:
                        theme[state][key] = class_theme[state][key]
            
            state_id = style_class.value + str(id(self))
            Theme.classes[state_id] = copy.deepcopy(theme)
            theme = Theme.classes[state_id]
        
        self._style = theme
    
    def _hit_test(self, x: int, y: int) -> UI | None:
        if not self.visible:
            return None

        if self._rect_contains(self, x, y):
            return self
        
        return None
