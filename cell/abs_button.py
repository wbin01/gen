#!/usr/bin/env python3
import copy

from .cell import Cell
from ..core import FontRender
from ..style import Theme


class AbsButton(Cell):
    """..."""
    def __init__(
            self, drawer, text: str = '',
            x: int = 0, y: int = 0, w: int = 100, h: int = 32,
            elided: bool = False, style_class: str = None) -> None:
        """..."""
        super().__init__()
        self.__drawer = drawer
        self.__text = text
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__elided = elided
        self.__style_class = style_class
        
        if self.__style_class:
            if self.__style_class not in Theme.classes:
                Theme.classes[self.__style_class] = copy.deepcopy(Theme.button)
            self.__style = Theme.classes[self.__style_class]
        else:
            self.__style = Theme.button

    def __draw(self):
        pad = self.__style['NORMAL']['padding'] * 2

        if self.__text:
            text = FontRender(
                self.__text,
                self.__style['NORMAL']['text'],
                self.__style['NORMAL']['font'],
                self.__style['NORMAL']['font-size'],
                self.__w if self.__elided else None,
                pad)
            if self.__w < text.width + pad: self.__w = text.width + pad
            if self.__h < text.height + pad: self.__h = text.height + pad

            tx = self.__x + (self.__w // 2) - (text.width // 2)
            ty = self.__y + (self.__h // 2) - (text.height // 2)
        
        self.__drawer.rect(
            self.__x, self.__y, self.__w, self.__h,
            self.__style['NORMAL']['border'],
            self.__style['NORMAL']['radius'])
        
        self.__drawer.rect(
            self.__x + 1, self.__y +1, self.__w - 2,self.__h - 2,
            self.__style['NORMAL']['background'],
            self.__style['NORMAL']['radius'] - 1)
        
        if self.__text:
            self.__drawer.text(tx, ty, text)
