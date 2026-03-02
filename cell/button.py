#!/usr/bin/env python3
import copy
import ctypes

import sdl3

from .cell import Cell
from ..ui import FontRender, Theme


class Button(Cell):
    """..."""
    def __init__(
            self, text: str = '', width: int = 100, height: int = 32,
            elided: bool = False, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._UI__base_class = 'Button'

        self.__text = text
        self.width = width
        self.height = height
        self.__elided = elided

        self.__resise_w = 0
        self.__resise_h = 0

        self.__texture_default = None
        self.__texture_hover = None
        self.__texture_pressed = None
        self.__texture_w = 0
        self.__texture_h = 0
    
    @property
    def text(self):
        return self.__text

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self.__text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.__text}")'

    def __draw(self, mode: str = None):
        if mode == 'REBUILD':
            self._UI__set_state('BASE')
            self.__texture_w = int(self.width)
            self.__texture_h = int(self.height)

            self.__texture_default = self._Cell__drawer.build_texture(
                self.__texture_w, self.__texture_h, self.__draw_ui, 'BASE')
            
            self.__texture_hover = self._Cell__drawer.build_texture(
                self.__texture_w, self.__texture_h, self.__draw_ui, 'HOVER')
            
            self.__texture_pressed = self._Cell__drawer.build_texture(
                self.__texture_w, self.__texture_h, self.__draw_ui, 'PRESSED')
            
            self.__resise_w = 0
            self.__resise_h = 0
        
        elif mode == 'RESIZE':
            if not self.__resise_h:
                self.__resise_w = int(self.width)
                self.__resise_h = int(self.height)
            
            # if self.fill.value == 'X':
            #     self.__resise_w = int(self.width)

            self._Cell__drawer.set_texture(
                self.__texture_default,
                int(self._x), int(self._y), self.__resise_w, self.__resise_h)
            return
        
        if self._UI__state.name == 'BASE':
            self._Cell__drawer.set_texture(
                self.__texture_default,
                int(self._x), int(self._y), int(self.width), int(self.height))

        elif self._UI__state.name == 'HOVER':
            self._Cell__drawer.set_texture(
                self.__texture_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        elif self._UI__state.name == 'PRESSED':
            self._Cell__drawer.set_texture(
                self.__texture_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
    
    def __draw_ui(self, state: str = 'BASE'):
        text = self.style[state]['text']
        background = self.style[state]['background']
        border = self.style[state]['border']

        state = 'BASE'
        
        radius = self.style[state]['radius']
        font = self.style[state]['font']
        font_size = self.style[state]['font-size']
        pad = self.style[state]['padding'] * 2

        x = y = 0

        if self.__text:
            text = FontRender(
                self.__text, text, font, font_size,
                self.width if self.__elided else None, pad)
            if self.width < text.width + pad: self.width = text.width + pad
            if self.height < text.height + pad: self.height = text.height + pad

            tx = x + (self.width // 2) - (text.width // 2)
            ty = y + (self.height // 2) - (text.height // 2)

            self._Size__min_width = text.width + pad
            self._Size__min_height = text.height + pad

        self._Cell__drawer.rect(
            x, y, self.width, self.height, border, radius)

        self._Cell__drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2,
            background, radius - 1)

        if self.__text:
            self._Cell__drawer.text(tx, ty, text)
