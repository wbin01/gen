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

        self._resise_w = 0
        self._resise_h = 0

        self._texture_default = None
        self._texture_hover = None
        self._texture_pressed = None
        self._texture_w = 0
        self._texture_h = 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'

    def _draw(self, mode: str = None):
        if mode == 'REBUILD':
            self._set_state('BASE')
            self._texture_w = int(self.width)
            self._texture_h = int(self.height)

            self._texture_default = self._drawer.build_texture(
                self._texture_w, self._texture_h, self._draw_ui, 'BASE')
            
            self._texture_hover = self._drawer.build_texture(
                self._texture_w, self._texture_h, self._draw_ui, 'HOVER')
            
            self._texture_pressed = self._drawer.build_texture(
                self._texture_w, self._texture_h, self._draw_ui, 'PRESSED')
            
            self._resise_w = 0
            self._resise_h = 0
        
        elif mode == 'RESIZE':
            if not self._resise_h:
                self._resise_w = int(self.width)
                self._resise_h = int(self.height)
            
            # if self.fill.value == 'X':
            #     self._resise_w = int(self.width)

            self._drawer.set_texture(
                self._texture_default,
                int(self._x), int(self._y), self._resise_w, self._resise_h)
            return

        if self._state.value == 'BASE':
            self._drawer.set_texture(
                self._texture_default,
                int(self._x), int(self._y), int(self.width), int(self.height))

        elif self._state.value == 'HOVER':
            self._drawer.set_texture(
                self._texture_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        elif self._state.value == 'PRESSED':
            self._drawer.set_texture(
                self._texture_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
    
    def _draw_ui(self, state: str = 'BASE'):
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        rad = self.style[state]['radius']

        x = y = 0
        self._drawer.rect(x, y, self.width, self.height, bd_color, rad)
        self._drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2, bg_color, rad - 1)
