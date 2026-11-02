#!/usr/bin/env python3
import time

from PIL import ImageFont
from xdg import IconTheme

from .cell import Cell
from ..flag import Fill


class DragArea(Cell):
    """..."""
    def __init__(
            self, text: str = '', width: int = 100, height: int = 32,
            elided: bool = True, fill: Fill = Fill.X, *args, **kwargs) -> None:
        """..."""
        super().__init__(fill=fill, *args, **kwargs)
        self._type_class = 'DragArea'
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
        
        self._txt_x = 0
        self._txt_y = 0
        self._txt_w = 0
        self._txt_h = 0

        self._tt_base = None
        self._tt_base_txt = None
        
        self._tt_width = 0
        self._tt_height = 0

        self._need_rebuild = False
        self._log_rebuild = False
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self._text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._text}")'
    
    @property
    def text(self) -> str:
        """..."""
        return self._text
    
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
        self._invalidate_item = 'TEXT'
        self._invalidate()
    
    def _apply_textures(self) -> None:
        self._drawer.apply_texture(
            self._tt_base,
            int(self._x), int(self._y), int(self.width), int(self.height))
        
        self._drawer.apply_texture(
            self._tt_base_txt,
            self._txt_x, self._txt_y, self._txt_w, self._txt_h)

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return

        if self.style['BASE']['font'] != self._font_name:
            self._font_name = self.style['BASE']['font']
            self._font = ImageFont.truetype(
                self._font_name, self.style['BASE']['font-size'])

        if mode == 'UNIT' and self._invalidate_item:
            self._draw_text_textures(state='BASE')
            self._invalidate_item = None
            self._need_rebuild = True
            
        elif mode == 'REBUILD':
            self._need_rebuild = False
            self._set_state('BASE')

            self._tt_base = self._drawer.reset_texture(self._tt_base)
            self._tt_base_txt = self._drawer.reset_texture(self._tt_base_txt)

            self._draw_background_textures(state='BASE')
            self._draw_text_textures(state='BASE')

            self._resize_width = 0
            self._resize_height = 0
        
        elif mode in ('RESIZE', 'POSITION'):
            if mode == 'POSITION': self._need_rebuild = True
            
            if not self._resize_height:
                self._resize_width = int(self.width)
                self._resize_height = int(self.height)
            
            # if self.fill.value == 'X':
            #     self._resize_width = int(self.width)

            self._drawer.apply_texture(
                self._tt_base, int(self._x), int(self._y),
                self._resize_width, self._resize_height)

            self._txt_x = self._x + (self._resize_width//2)-(self._txt_w//2)
            self._txt_y = self._y + (self._resize_height//2)-(self._txt_h//2)

            self._drawer.apply_texture(
                self._tt_base_txt,
                self._txt_x, self._txt_y, self._txt_w, self._txt_h)
            return
        
        self._apply_textures()
    
    def _draw_background_textures(self, state: str) -> None:
        self._tt_width = int(self.width)
        self._tt_height = int(self.height)

        self._tt_base = self._drawer.texture(self._tt_base,
            self._tt_width, self._tt_height, self._draw_rects, 'BASE')
        if self._log_rebuild: print('BASE bg', self, time.time())
    
    def _draw_text_textures(self, state: str) -> None:
        padding = 2
        width = int(self.width - padding)
        
        self._tt_base_txt, self._txt_w, self._txt_h = self._drawer.font(
            self._text, self._tt_base_txt, self._font,
            self.style['BASE']['font-size'],
            self.style['BASE']['font-color'], self._elided, width)
        if self._log_rebuild: print('BASE text', self, time.time())
        
        self._txt_x = self._x + (self.width // 2) - (self._txt_w // 2)
        self._txt_y = self._y + (self.height // 2) - (self._txt_h // 2)
    
    def _draw_rects(self, state: str = 'BASE'):
        radius = 0
        border = 0
        bg_color = self.style[state]['background-color']
        bd_color = (0, 0, 0, 0)
        bd_space = 0

        if border:
            self._drawer.rect(0, 0, self.width, self.height, bd_color, radius)
        
        self._drawer.rect(
            border, border, self.width - bd_space, self.height - bd_space,
            bg_color, radius - border)
