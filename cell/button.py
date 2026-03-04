#!/usr/bin/env python3
import copy
import ctypes

import sdl3

from .cell import Cell
from ..flag import Fill
from ..ui import FontRender


class Button(Cell):
    """..."""
    def __init__(
            self, text: str = '', width: int = 100, height: int = 32,
            elided: bool = True, fill: Fill = Fill.X,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(fill=fill, *args, **kwargs)
        self._base_class = 'Button'
        self.fill = fill

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

    def __draw(self, mode: str = None) -> None:
        if mode == 'REBUILD':
            self._set_state('BASE')
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
        
        if self._state.name == 'BASE':
            self._Cell__drawer.set_texture(
                self.__texture_default,
                int(self._x), int(self._y), int(self.width), int(self.height))

        elif self._state.name == 'HOVER':
            self._Cell__drawer.set_texture(
                self.__texture_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        elif self._state.name == 'PRESSED':
            self._Cell__drawer.set_texture(
                self.__texture_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
    
    def __draw_ui(self, state: str = 'BASE'):
        font_color = self.style[state]['font-color']
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        rad = self.style[state]['radius']
        font = self.style[state]['font']
        font_size = self.style[state]['font-size']
        pad = self.style[state]['padding'] * 2
        x = y = 0

        if self.__text:
            text = FontRender(
                self.__text, font_color, font, font_size,
                int(self.width) - pad if self.__elided else None, pad)
            if self.width < text.width + pad: self.width = text.width + pad
            if self.height < text.height + pad: self.height = text.height + pad

            tx = x + (self.width // 2) - (text.width // 2)
            ty = y + (self.height // 2) - (text.height // 2)
            if not self.__elided:
                minw = text.width + pad
                if self._Size__min_width < minw: self._Size__min_width = minw
                
                minh = text.height + pad
                if self._Size__min_height < minh: self._Size__min_height = minh

        self._Cell__drawer.rect(x, y, self.width, self.height, bd_color, rad)
        self._Cell__drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2, bg_color, rad - 1)
        if self.__text:
            self._Cell__drawer.text(tx, ty, text)
