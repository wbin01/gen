#!/usr/bin/env python3
import time
from PIL import ImageFont

from .cell import Cell
from ..flag import Fill


class Button(Cell):
    """..."""
    def __init__(
            self, text: str = '', width: int = 100, height: int = 32,
            elided: bool = True, fill: Fill = Fill.X,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(fill=fill, *args, **kwargs)
        self.fill = fill
        self._invalidate_item = None

        self._text = text
        self.width = width
        self.height = height
        self._elided = elided

        self._resize_width = 0
        self._resize_height = 0

        self._font_name = self.style['BASE']['font']
        self._font = ImageFont.truetype(
            self._font_name, self.style['BASE']['font-size'])
        
        self._text_x = 0
        self._text_y = 0
        self._text_w = 0
        self._text_h = 0

        self._tt_base = None
        self._tt_base_text = None
        self._tt_hover = None
        self._tt_hover_text = None
        self._tt_pressed = None
        self._tt_pressed_text = None
        
        self._tt_width = 0
        self._tt_height = 0

        self._need_rebuild = False
        self._log_rebuild = False
    
    @property
    def text(self) -> str:
        """..."""
        return self._text
    
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self._invalidate_item = 'TEXT'
        self._invalidate()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self._text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._text}")'

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return

        if self.style['BASE']['font'] != self._font_name:
            self._font_name = self.style['BASE']['font']
            self._font = ImageFont.truetype(
                self._font_name, self.style['BASE']['font-size'])

        if mode == 'UNIT' and self._invalidate_item:
            self._build_text_textures('BASE')
            self._invalidate_item = None
            self._need_rebuild = True
            
        elif mode == 'REBUILD':
            self._need_rebuild = False
            self._set_state('BASE')

            self._tt_base = self._drawer.reset(self._tt_base)
            self._tt_base_text = self._drawer.reset(self._tt_base_text)
            self._tt_hover = self._drawer.reset(self._tt_hover)
            self._tt_hover_text = self._drawer.reset(self._tt_hover_text)
            self._tt_pressed = self._drawer.reset(self._tt_pressed)
            self._tt_pressed_text = self._drawer.reset(self._tt_pressed_text)

            self._build_background_textures('BASE')
            self._build_text_textures('BASE')

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
            
            self._text_x = self._x + (self._resize_width//2)-(self._text_w//2)
            self._text_y = self._y + (self._resize_height//2)-(self._text_h//2)

            self._drawer.set_texture(
                self._tt_base_text,
                self._text_x, self._text_y, self._text_w, self._text_h)
            return
        
        self._set_textures()
    
    def _build_background_textures(self, mode: str) -> None:
        self._tt_width = int(self.width)
        self._tt_height = int(self.height)

        if mode == 'BASE':
            self._tt_base = self._drawer.build_texture(self._tt_base,
                self._tt_width, self._tt_height, self._build_render, 'BASE')
            if self._log_rebuild: print('BASE bg', self, time.time())
        
        elif mode == 'HOVER':
            self._tt_hover = self._drawer.build_texture(self._tt_hover,
                self._tt_width, self._tt_height, self._build_render, 'HOVER')
            if self._log_rebuild: print('HOVER bg', self, time.time())
        
        elif mode == 'PRESSED':
            self._tt_pressed = self._drawer.build_texture(self._tt_pressed,
                self._tt_width, self._tt_height, self._build_render, 'PRESSED')
            if self._log_rebuild: print('PRESSED bg', self, time.time())
    
    def _build_text_textures(self, mode: str) -> None:
        padding = self.style['BASE']['padding'] * 2
        width = int(self.width - padding)
        if mode == 'BASE':
            self._tt_base_text, self._text_w, self._text_h = self._drawer.font(
                self._text, self._tt_base_text, self._font,
                self.style['BASE']['font-size'],
                self.style['BASE']['font-color'], self._elided, width)
            if self._log_rebuild: print('BASE text', self, time.time())

        elif mode == 'HOVER':
            self._tt_hover_text, self._text_w, self._text_h = self._drawer.font(
                self._text, self._tt_hover_text, self._font,
                self.style['BASE']['font-size'],
                self.style['HOVER']['font-color'], self._elided, width)
            if self._log_rebuild: print('HOVER text', self, time.time())

        elif mode == 'PRESSED':
            self._tt_pressed_text, self._text_w, self._text_h = self._drawer.font(
                self._text, self._tt_pressed_text, self._font,
                self.style['BASE']['font-size'],
                self.style['PRESSED']['font-color'], self._elided, width)
            if self._log_rebuild: print('PRESSED text', self, time.time())
        
        self._text_x = self._x + (self.width // 2) - (self._text_w // 2)
        self._text_y = self._y + (self.height // 2) - (self._text_h // 2)
    
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
            
            self._drawer.set_texture(
                self._tt_base_text,
                self._text_x, self._text_y, self._text_w, self._text_h)

        elif self._state.value == 'HOVER':
            if not self._tt_hover:
                self._build_background_textures('HOVER')
                self._build_text_textures('HOVER')
            
            self._drawer.set_texture(
                self._tt_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
            
            self._drawer.set_texture(
                self._tt_hover_text,
                self._text_x, self._text_y, self._text_w, self._text_h)
        
        elif self._state.value == 'PRESSED':
            if not self._tt_pressed:
                self._build_background_textures('PRESSED')
                self._build_text_textures('PRESSED')
            
            self._drawer.set_texture(
                self._tt_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
            
            self._drawer.set_texture(
                self._tt_pressed_text,
                self._text_x, self._text_y, self._text_w, self._text_h)
