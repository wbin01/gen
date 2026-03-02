#!/usr/bin/env python3
import copy
import ctypes

import sdl3

from ..flag import Fill
from ..mixin import Margin, Pos, Size
from ..ui import UI, Theme
from ..flag import StyleClass


class Cell(Margin, Pos, Size, UI):
    """..."""
    def __init__(self, style_class: str = None, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__drawer = None
        self.__fill = Fill.X
        self.__style_class = style_class
        
        class_name = self.__class__.__name__
        if not hasattr(Theme, class_name):
            class_name = self.__class__.__base__.__name__
        
        theme = None
        if hasattr(Theme, class_name):
            if class_name not in ('ui', 'cell'):
                theme = getattr(Theme, class_name)

            state_theme = None
            if isinstance(style_class, StyleClass):
                state_theme = Theme.classes[style_class.value]

            elif style_class in Theme.classes:
                theme = Theme.classes[style_class]
            
            elif style_class not in Theme.classes:
                Theme.classes[style_class] = copy.deepcopy(theme)
                theme = Theme.classes[style_class]
            
            if theme and state_theme:
                for state in ('BASE', 'HOVER', 'PRESSED'):
                    for key in ('text', 'background', 'border'):
                        if key in theme[state]:
                            theme[state][key] = state_theme[state][key]
        
        self.__style = theme
        
        # if self.__style_class:
        #     if self.__style_class not in Theme.classes:
        #         Theme.classes[self.__style_class] = copy.deepcopy(theme)
        #     self.__style = Theme.classes[self.__style_class]
        # else:
        #     self.__style = theme

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
