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
        self._UI__base_class = 'Empty'

        self.width = width
        self.height = height

        self.__resise_w = 0
        self.__resise_h = 0

        self.__texture_normal = None
        self.__texture_hover = None

        self.__texture_w = 0
        self.__texture_h = 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self.__text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self.__text}")'

    def __draw(self, mode: str = None):
        if mode == 'REBUILD':
            self._UI__set_state('DEFAULT')
            self.__texture_w = int(self.width)
            self.__texture_h = int(self.height)

            self.__texture_normal = self._Cell__drawer.build_texture(
                self.__texture_w, self.__texture_h, self.__draw_ui, 'DEFAULT')
            
            self.__texture_hover = self._Cell__drawer.build_texture(
                self.__texture_w, self.__texture_h, self.__draw_ui, 'HOVER')
            
            self.__resise_w = 0
            self.__resise_h = 0
        
        elif mode == 'RESIZE':
            if not self.__resise_h:
                self.__resise_w = int(self.width)
                self.__resise_h = int(self.height)
            
            # if self.fill.value == 'X':
            #     self.__resise_w = int(self.width)

            self._Cell__drawer.set_texture(
                self.__texture_normal,
                int(self._x), int(self._y), self.__resise_w, self.__resise_h)
            return

        if self._UI__state.name == 'HOVER':
            self._Cell__drawer.set_texture(
                self.__texture_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
            return

        self._Cell__drawer.set_texture(
            self.__texture_normal,
            int(self._x), int(self._y), int(self.width), int(self.height))
    
    def __draw_ui(self, state: str = 'DEFAULT'):
        background = self.style[state]['background']
        border = self.style[state]['border']

        state = 'DEFAULT'

        radius = self.style[state]['radius']
        pad = self.style[state]['padding'] * 2

        x = y = 0
        self._Cell__drawer.rect(
            x, y, self.width, self.height, border, radius)

        self._Cell__drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2,
            background, radius - 1)
