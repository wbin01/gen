#!/usr/bin/env python3
import time

from xdg import IconTheme

from .cell import Cell
from ..flag import Fill


class ToolButton(Cell):
    """..."""
    def __init__(
            self, icon_name: str = '', width: int = 32, height: int = 32,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(fill=Fill.NONE, *args, **kwargs)
        self._invalidate_item = None

        self._icon_name = icon_name
        self.width = width
        self.height = height
        self._elided = None

        self._resize_width = 0
        self._resize_height = 0
        
        self._icon_path = IconTheme.getIconPath(
            iconname=self._icon_name,
            size=22,
            theme='breeze-dark',
            extensions=['png', 'svg', 'xpm'])

        self._icon_x = 0
        self._icon_y = 0
        self._icon_w = 22
        self._icon_h = 22

        self._tt_icon = None
        self._tt_base = None
        self._tt_hover = None
        self._tt_pressed = None
        
        self._tt_width = 0
        self._tt_height = 0

        self._need_rebuild = False
        self._log_rebuild = False
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self._icon_name}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._icon_name}")'
    
    @property
    def icon_name(self) -> str:
        """..."""
        return self._icon_name
    
    @icon_name.setter
    def icon_name(self, icon_name: str) -> None:
        self._icon_name = icon_name
        self._invalidate_item = 'TEXT'
        self._invalidate()
    
    def _apply_textures(self) -> None:
        
        if self._state.value == 'BASE':
            self._drawer.apply_texture(
                self._tt_base,
                int(self._x), int(self._y), int(self.width), int(self.height))
            
            self._drawer.apply_texture(
                self._tt_icon,
                self._icon_x, self._icon_y, self._icon_w, self._icon_h)

        elif self._state.value == 'HOVER':
            if not self._tt_hover:
                self._draw_background_textures(state='HOVER')
                self._draw_icon_textures(state='HOVER')
            
            self._drawer.apply_texture(
                self._tt_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
            
            self._drawer.apply_texture(
                self._tt_icon,
                self._icon_x, self._icon_y, self._icon_w, self._icon_h)
        
        elif self._state.value == 'PRESSED':
            if not self._tt_pressed:
                self._draw_background_textures(state='PRESSED')
                self._draw_icon_textures(state='PRESSED')
            
            self._drawer.apply_texture(
                self._tt_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
            
            self._drawer.apply_texture(
                self._tt_icon,
                self._icon_x, self._icon_y, self._icon_w, self._icon_h)

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return

        if mode == 'UNIT' and self._invalidate_item:
            self._draw_icon_textures(state='BASE')
            self._draw_icon_textures(state='HOVER')
            self._draw_icon_textures(state='PRESSED')
            self._invalidate_item = None
            self._need_rebuild = True
            
        elif mode == 'REBUILD':
            self._need_rebuild = False
            self._set_state('BASE')

            self._tt_base = self._drawer.reset_texture(self._tt_base)
            self._tt_hover = self._drawer.reset_texture(self._tt_hover)
            self._tt_pressed = self._drawer.reset_texture(self._tt_pressed)

            self._draw_background_textures(state='BASE')
            self._draw_icon_textures(state='BASE')

            self._resize_width = 0
            self._resize_height = 0
        
        elif mode in ('RESIZE', 'POSITION'):
            if mode == 'POSITION': self._need_rebuild = True
            
            if not self._resize_height:
                self._resize_width = int(self.width)
                self._resize_height = int(self.height)

            self._drawer.apply_texture(
                self._tt_base, int(self._x), int(self._y),
                self._resize_width, self._resize_height)
            
            self._icon_x = self._x + (self.width//2)-(self._icon_w//2)
            self._icon_y = self._y + (self.height//2)-(self._icon_h//2)

            self._drawer.apply_texture(
                self._tt_icon,
                self._icon_x, self._icon_y, self._icon_w, self._icon_h)
            return
        
        self._apply_textures()
    
    def _draw_background_textures(self, state: str) -> None:
        self._tt_width = int(self.width)
        self._tt_height = int(self.height)

        if state == 'BASE':
            self._tt_base = self._drawer.texture(self._tt_base,
                self._tt_width, self._tt_height, self._draw_rects, 'BASE')
            if self._log_rebuild: print('BASE bg', self, time.time())
        
        elif state == 'HOVER':
            self._tt_hover = self._drawer.texture(self._tt_hover,
                self._tt_width, self._tt_height, self._draw_rects, 'HOVER')
            if self._log_rebuild: print('HOVER bg', self, time.time())
        
        elif state == 'PRESSED':
            self._tt_pressed = self._drawer.texture(self._tt_pressed,
                self._tt_width, self._tt_height, self._draw_rects, 'CLICKED')
            if self._log_rebuild: print('PRESSED bg', self, time.time())
    
    def _draw_icon_textures(self, state: str) -> None:
        padding = self.style['BASE']['padding'] * 2
        width = int(self.width - padding)

        self._tt_icon = self._drawer.icon(
            self._icon_path, self._icon_w, self._icon_h)
        
        if state == 'BASE':
            if self._log_rebuild: print('BASE text', self, time.time())

        elif state == 'HOVER':
            if self._log_rebuild: print('HOVER text', self, time.time())

        elif state == 'PRESSED':
            if self._log_rebuild: print('PRESSED text', self, time.time())

        self._icon_x = self._x + (self.width//2)-(self._icon_w//2)
        self._icon_y = self._y + (self.height//2)-(self._icon_h//2)
    
    def _draw_rects(self, state: str = 'BASE'):
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
