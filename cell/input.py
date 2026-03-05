#!/usr/bin/env python3
import bisect

from PIL import ImageFont
import sdl3

from .cell import Cell
from ..flag import Fill
from ..ui import FontRender


class Input(Cell):
    """..."""
    def __init__(
            self, text: str = '', width: int = 100, height: int = 32,
            elided: bool = True, fill: Fill = Fill.X,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(fill=fill, *args, **kwargs)
        self._base_class = 'Button'
        self.fill = fill

        self._text = text
        self.width = width
        self.height = height
        self._elided = elided

        self._resise_w = 0
        self._resise_h = 0

        self._texture_default = None
        self._texture_hover = None
        self._texture_pressed = None
        self._texture_w = 0
        self._texture_h = 0

        # Input text
        self._text_left = []
        self._text_right = []

        self._text_font_size = self.style['BASE']['font-size']
        self._text_font_color = self.style['BASE']['font-color']
        self._text_font = ImageFont.truetype(
            self.style['BASE']['font'], self._text_font_size)

        self._text_texture = None
        self._textx = 0
        self._texty = 0
        self._textw = 0
        self._texth = 0

        self._positions = []
        self._widths = []
        self._acc = 0
    
    @property
    def text(self):
        return self._text
    
    def insert(self, text):
        for char in text:
            self._text_left.append(str(char))
        
        self._text = ''.join(self._text_left) + ''.join(self._text_right)
        self._update_positions()
        self._dirty = True

    def backspace(self):
        if self._text_left:
            self._text_left.pop()
            self._dirty = True
            self._text = ''.join(self._text_left) + ''.join(self._text_right)
            self._update_positions()
    
    def delete(self):
        if self._text_right:
            self._text_right.pop(0)
            self._dirty = True
            self._text = ''.join(self._text_left) + ''.join(self._text_right)
            self._update_positions()
    
    def move_left(self):
        if self._text_left:
            self._text_right.insert(0, self._text_left.pop())

    def move_right(self):
        if self._text_right:
            self._text_left.append(self._text_right.pop(0))
    
    def _click_update_cursor(self, mouse_x) -> None:
        pos = self._get_cursor_x_from_click(mouse_x)
        self._text_left  = list(self._text[:pos])
        self._text_right = list(self._text[pos:])
    
    def _get_cursor_x(self) -> int:
        left_text = ''.join(self._text_left)
        return self._text_font.getlength(left_text)
    
    def _get_cursor_x_from_click_bkp(self, mouse_x) -> int:
        cursor = bisect.bisect_left(self._positions, mouse_x)
        return cursor
    
    def _get_cursor_x_from_click(self, mouse_x) -> int:
        for i, x in enumerate(self._positions):
            half = x + self._widths[i] // 2

            if mouse_x < half:
                return i - 1

        end = len(self._positions)
        if mouse_x > self._text_font.getlength(self._text):
            end += 1

        return end - 1
    
    def _update_positions(self):
        self._positions = []
        self._widths = []
        x = 0

        for ch in self._text:
            w = self._text_font.getlength(ch)
            self._positions.append(x)
            self._widths.append(w)
            x += w

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self._text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._text}")'

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return

        if mode == 'UNIT':
            self._text_texture, self._textw, self._texth = self._drawer.font(
                self._text, self._text_texture,
                self._text_font, self._text_font_size, self._text_font_color)
            self._texty = self._y + (self.height / 2) - (self._texth / 2)

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
            
            self._text_texture, self._textw, self._texth = self._drawer.font(
                self._text, self._text_texture,
                self._text_font, self._text_font_size, self._text_font_color)
            self._texty = self._y + (self.height / 2) - (self._texth / 2)
            
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
            
            self._drawer.set_texture(
                self._text_texture,
                self._textx, self._texty, self._textw, self._texth)
            return
        
        self._textx = self._x + self.style['BASE']['padding'] + 5

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
        
        self._drawer.set_texture(
            self._text_texture,
            self._textx, self._texty, self._textw, self._texth)
        
        self._drawer.font_cursor(
            self._textx, self._texty, self._text_font_size,
            self._get_cursor_x(), self._text_font_color)
        
        if mode == 'REBUILD':
            self._dirty = False
    
    def _draw_ui(self, state: str = 'BASE'):
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        rad = self.style[state]['radius']
        x = y = 0
        self._drawer.rect(x, y, self.width, self.height, bd_color, rad)
        self._drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2, bg_color, rad - 1)
