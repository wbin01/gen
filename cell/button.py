#!/usr/bin/env python3
import copy

from .cell import Cell
from ..ui import FontRender, Theme


class Button(Cell):
    """..."""
    def __init__(
            self, text: str = '',
            x: int = 0, y: int = 0, width: int = 100, height: int = 32,
            elided: bool = False, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = text
        self._Pos_x = x
        self._Pos_y = y
        self.width = width
        self.height = height
        self.__elided = elided
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self.__text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.__text}")'

    def __draw(self):
        print(self, self._UI__state.name)
        state = self._UI__state.name

        text = self._Cell__style[state]['text']
        background = self._Cell__style[state]['background']
        border = self._Cell__style[state]['border']

        if self._UI__state.name != 'NORMAL':
            state = 'NORMAL'
        
        radius = self._Cell__style[state]['radius']
        font = self._Cell__style[state]['font']
        font_size = self._Cell__style[state]['font-size']
        pad = self._Cell__style[state]['padding'] * 2

        if self.__text:
            text = FontRender(
                self.__text, text, font, font_size,
                self.width if self.__elided else None, pad)
            if self.width < text.width + pad: self.width = text.width + pad
            if self.height < text.height + pad: self.height = text.height + pad

            tx = self._x + (self.width // 2) - (text.width // 2)
            ty = self._y + (self.height // 2) - (text.height // 2)

        self._Cell__drawer.rect(
            self._x, self._y, self.width, self.height, border, radius)

        self._Cell__drawer.rect(
            self._x + 1, self._y +1, self.width - 2,self.height - 2,
            background, radius - 1)

        if self.__text:
            self._Cell__drawer.text(tx, ty, text)
    
    def __draw_bkp(self):
        print(self, self._UI__state.name)
        state = self._UI__state.name

        text = self.__style[state]['text']
        background = self.__style[state]['background']
        border = self.__style[state]['border']

        if self._UI__state.name != 'NORMAL':
            state = 'NORMAL'
        
        radius = self.__style[state]['radius']
        font = self.__style[state]['font']
        font_size = self.__style[state]['font-size']
        pad = self.__style[state]['padding'] * 2

        if self.__text:
            text = FontRender(
                self.__text, text, font, font_size,
                self.width if self.__elided else None, pad)
            if self.width < text.width + pad: self.width = text.width + pad
            if self.height < text.height + pad: self.height = text.height + pad

            tx = self._x + (self.width // 2) - (text.width // 2)
            ty = self._y + (self.height // 2) - (text.height // 2)

        self._Cell__drawer.rect(
            self._x, self._y, self.width, self.height, border, radius)

        self._Cell__drawer.rect(
            self._x + 1, self._y +1, self.width - 2,self.height - 2,
            background, radius - 1)

        if self.__text:
            self._Cell__drawer.text(tx, ty, text)
