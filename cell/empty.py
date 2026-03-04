#!/usr/bin/env python3
import copy
import ctypes

import sdl3

from .cell import Cell
from ..ui import FontRender, Theme


class Empty(Cell):
    """..."""
    def __init__(
            self, width: int = 100, height: int = 32, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._base_class = 'Empty'

        self.width = width
        self.height = height

        self.__resise_w = 0
        self.__resise_h = 0

        self.__texture_default = None
        self.__texture_hover = None
        self.__texture_pressed = None
        self.__texture_w = 0
        self.__texture_h = 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __draw(self, mode: str = None):
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
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        rad = self.style[state]['radius']

        x = y = 0
        self._Cell__drawer.rect(x, y, self.width, self.height, bd_color, rad)
        self._Cell__drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2, bg_color, rad - 1)
