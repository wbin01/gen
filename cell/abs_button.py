#!/usr/bin/env python3
import copy

from .cell import Cell
from ..style import Theme
from ..ui import FontRender


class AbsButton(Cell):
    """..."""
    def __init__(
            self, text: str = '',
            x: int = 0, y: int = 0, width: int = 100, height: int = 32,
            elided: bool = False, style_class: str = None) -> None:
        """..."""
        super().__init__()
        self.__drawer = None
        self.__text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.__elided = elided
        self.__style_class = style_class
        
        if self.__style_class:
            if self.__style_class not in Theme.classes:
                Theme.classes[self.__style_class] = copy.deepcopy(Theme.button)
            self.__style = Theme.classes[self.__style_class]
        else:
            self.__style = Theme.button
    @property
    def style(self) -> dict:
        return self.__style
    
    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    def __draw(self):
        pad = self.__style['NORMAL']['padding'] * 2

        if self.__text:
            text = FontRender(
                self.__text,
                self.__style['NORMAL']['text'],
                self.__style['NORMAL']['font'],
                self.__style['NORMAL']['font-size'],
                self.width if self.__elided else None,
                pad)
            if self.width < text.width + pad: self.width = text.width + pad
            if self.height < text.height + pad: self.height = text.height + pad

            tx = self.x + (self.width // 2) - (text.width // 2)
            ty = self.y + (self.height // 2) - (text.height // 2)
        
        self.__drawer.rect(
            self.x, self.y, self.width, self.height,
            self.__style['NORMAL']['border'],
            self.__style['NORMAL']['radius'])
        
        self.__drawer.rect(
            self.x + 1, self.y +1, self.width - 2,self.height - 2,
            self.__style['NORMAL']['background'],
            self.__style['NORMAL']['radius'] - 1)
        
        if self.__text:
            self.__drawer.text(tx, ty, text)
