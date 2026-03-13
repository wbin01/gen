#!/usr/bin/env python3
import time

from .cell import Cell


class Empty(Cell):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._invalidate_item = None

        self._resize_width = 0
        self._resize_height = 0

        self._tt_base = None
        self._tt_hover = None
        self._tt_pressed = None
        
        self._tt_width = 0
        self._tt_height = 0

        self._need_rebuild = False
        self._log_rebuild = False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return

        if mode == 'UNIT' and self._invalidate_item:
            self._invalidate_item = None
            self._need_rebuild = True
            
        elif mode == 'REBUILD':
            self._need_rebuild = False
            self._set_state('BASE')

            self._tt_base = self._drawer.reset(self._tt_base)
            self._tt_hover = self._drawer.reset(self._tt_hover)
            self._tt_pressed = self._drawer.reset(self._tt_pressed)

            self._build_background_textures(state='BASE')
            self._resize_width = 0
            self._resize_height = 0
        
        elif mode in ('RESIZE', 'POSITION'):
            if mode == 'POSITION': self._need_rebuild = True
            
            if not self._resize_height:
                self._resize_width = int(self.width)
                self._resize_height = int(self.height)
            
            # if self.fill.value == 'X':
            #     self._resize_width = int(self.width)

            self._drawer.set_texture(
                self._tt_base, int(self._x), int(self._y),
                self._resize_width, self._resize_height)
            return
        
        self._set_textures()
    
    def _build_background_textures(self, state: str) -> None:
        self._tt_width = int(self.width)
        self._tt_height = int(self.height)

        if state == 'BASE':
            self._tt_base = self._drawer.build_texture(self._tt_base,
                self._tt_width, self._tt_height, self._build_render, 'BASE')
            if self._log_rebuild: print('BASE bg', self, time.time())
        
        elif state == 'HOVER':
            self._tt_hover = self._drawer.build_texture(self._tt_hover,
                self._tt_width, self._tt_height, self._build_render, 'HOVER')
            if self._log_rebuild: print('HOVER bg', self, time.time())

        elif state == 'PRESSED':
            self._tt_pressed = self._drawer.build_texture(self._tt_pressed,
                self._tt_width, self._tt_height, self._build_render, 'CLICKED')
            if self._log_rebuild: print('PRESSED bg', self, time.time())
    
    def _build_render(self, state: str = 'BASE'):
        radius = self.style['BASE']['radius']
        border = self.style['BASE']['border']
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        bd_space = border * 2

        if border:
            self._drawer.rect(0, 0, self.width, self.height, bd_color, radius)
        
        self._drawer.rect(
            border, border, self.width - bd_space, self.height - bd_space,
            bg_color, radius - border)
    
    def _set_textures(self) -> None:
        if self._state.value == 'BASE':
            self._drawer.set_texture(
                self._tt_base,
                int(self._x), int(self._y), int(self.width), int(self.height))

        elif self._state.value == 'HOVER':
            if not self._tt_hover:
                self._build_background_textures(state='HOVER')

            self._drawer.set_texture(
                self._tt_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        elif self._state.value == 'PRESSED':
            if not self._tt_pressed:
                self._build_background_textures(state='PRESSED')

            self._drawer.set_texture(
                self._tt_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
