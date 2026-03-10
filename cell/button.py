#!/usr/bin/env python3
from PIL import ImageFont

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
        self.fill = fill
        self._invalidate_item = None

        self._text = text
        self.width = width
        self.height = height
        self._elided = elided

        self._resize_width = 0
        self._resize_height = 0

        self._tx_base = None
        self._tx_hover = None
        self._tx_pressed = None

        self._padding = self.style['BASE']['padding'] * 2
        self._tx_text = None
        self._font_size = self.style['BASE']['font-size']
        self._font_color = self.style['BASE']['font-color']
        self._font = ImageFont.truetype(
            self.style['BASE']['font'], self._font_size)
        
        self._text_x = 0
        self._text_y = 0
        self._text_w = 0
        self._text_h = 0

        self._tx_width = 0
        self._tx_height = 0
    
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
        # if not self._dirty: return
        # self._dirty = False

        if mode == 'UNIT' and self._invalidate_item:
            self._invalidate_item = None

            self._tx_text, self._text_w, self._text_h = self._drawer.font(
                self._text, self._tx_text,
                self._font, self._font_size, self._font_color)
            
            self._text_x = self._x + (self.width // 2) - (self._text_w // 2)
            self._text_y = self._y + (self.height // 2) - (self._text_h // 2)

        elif mode == 'REBUILD':
            self._set_state('BASE')
            self._tx_width = int(self.width)
            self._tx_height = int(self.height)

            self._tx_base = self._drawer.build_texture(
                self._tx_width, self._tx_height, self._render_bg, 'BASE')
            
            self._tx_hover = self._drawer.build_texture(
                self._tx_width, self._tx_height, self._render_bg, 'HOVER')
            
            self._tx_pressed = self._drawer.build_texture(
                self._tx_width, self._tx_height, self._render_bg, 'PRESSED')
            
            width = int(self.width - self._padding)
            self._tx_text, self._text_w, self._text_h = self._drawer.font(
                self._text, self._tx_text, self._font, self._font_size,
                self._font_color, self._elided, width)
            
            self._text_x = self._x + (self.width // 2) - (self._text_w // 2)
            self._text_y = self._y + (self.height // 2) - (self._text_h // 2)
            
            self._resize_width = 0
            self._resize_height = 0
        
        elif mode == 'RESIZE':
            if not self._resize_height:
                self._resize_width = int(self.width)
                self._resize_height = int(self.height)
            
            # if self.fill.value == 'X':
            #     self._resize_width = int(self.width)

            self._drawer.set_texture(
                self._tx_base, int(self._x), int(self._y),
                self._resize_width, self._resize_height)
            
            self._text_x = self._x + (self._resize_width//2)-(self._text_w//2)
            self._text_y = self._y + (self._resize_height//2)-(self._text_h//2)

            self._drawer.set_texture(
                self._tx_text,
                self._text_x, self._text_y, self._text_w, self._text_h)
            return
        
        if self._state.value == 'BASE':
            self._drawer.set_texture(
                self._tx_base,
                int(self._x), int(self._y), int(self.width), int(self.height))

        elif self._state.value == 'HOVER':
            self._drawer.set_texture(
                self._tx_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        elif self._state.value == 'PRESSED':
            self._drawer.set_texture(
                self._tx_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        self._drawer.set_texture(
            self._tx_text,
            self._text_x, self._text_y, self._text_w, self._text_h)
    
    def _render_bg(self, state: str = 'BASE'):
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        rad = self.style[state]['radius']

        self._drawer.rect(0, 0, self.width, self.height, bd_color, rad)
        self._drawer.rect(
            1, 1, self.width - 2,self.height - 2, bg_color, rad - 1)
    