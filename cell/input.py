#!/usr/bin/env python3
import copy
import ctypes

from PIL import Image, ImageDraw, ImageFont
import sdl3

from .cell import Cell
from ..ui import FontRender, Theme
from ..flag import Fill


class TextInput:
    def __init__(self, font_path, font_size, parent):
        self.parent = parent
        self.left = []
        self.right = []

        self.font = ImageFont.truetype(font_path, font_size)
        self.font_size = font_size

        self.texture = None
        self.width = 0
        self.height = 0

        self.parent._dirty = True
    
    def insert(self, text):
        for char in text:
            self.left.append(str(char))
        self.parent._dirty = True

    def backspace(self):
        if self.left:
            self.left.pop()
            self.parent._dirty = True
    
    def delete(self):
        if self.right:
            self.right.pop(0)
            self.parent._dirty = True
    
    def move_left(self):
        if self.left:
            self.right.insert(0, self.left.pop())

    def move_right(self):
        if self.right:
            self.left.append(self.right.pop(0))
    
    def get_text(self):
        return ''.join(self.left) + ''.join(self.right)
    
    def get_cursor_x(self):
        left_text = ''.join(self.left)
        return self.font.getlength(left_text)
    
    """
    cursor_x = x + input.get_cursor_x()
    sdl3.SDL_RenderLine(renderer,
                        cursor_x, y,
                        cursor_x, y + input.height)
    """
    
    def rebuild_texture(self, renderer):
        # if not self.parent._dirty: return

        text = self.get_text()

        bbox = self.font.getbbox(text if text else " ")
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text((-bbox[0], -bbox[1]), text, font=self.font, fill=(255,255,255,255))

        raw_bytes = img.tobytes()

        surface = sdl3.SDL_CreateSurfaceFrom(
            w, h,
            sdl3.SDL_PIXELFORMAT_RGBA32,
            raw_bytes,
            w * 4
        )

        if self.texture:
            sdl3.SDL_DestroyTexture(self.texture)

        self.texture = sdl3.SDL_CreateTextureFromSurface(renderer, surface)
        sdl3.SDL_DestroySurface(surface)

        self.width = w
        self.height = h
        # self.parent._dirty = False


class Input(Cell):
    """..."""
    def __init__(
            self, width: int = 100, height: int = 32, fill: Fill = Fill.X,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(fill=fill, *args, **kwargs)
        self._base_class = 'Input'

        self.width = width
        self.height = height

        self._resise_w = 0
        self._resise_h = 0

        self._texture_default = None
        self._texture_hover = None
        self._texture_pressed = None
        self._texture_w = 0
        self._texture_h = 0

        self._text = TextInput('DejaVuSans.ttf', 12, self)
        self._first_rebuild = False
        self._dirty = True

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'

    def _draw(self, mode: str = None) -> None:
        if mode == 'UNIT':
            print('UNIT')
            self._text.rebuild_texture(self._drawer._renderer)

        elif mode == 'REBUILD':
            print('REBUILD')
            # self._set_state('BASE')
            self._texture_w = int(self.width)
            self._texture_h = int(self.height)

            self._text.rebuild_texture(self._drawer._renderer)

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
            
            self._drawer.set_texture(
                self._text.texture,
                10, int(self._y) + 10, self._text.width, self._text.height)
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
        
        self._drawer.set_texture(
            self._text.texture,
            10, int(self._y) + 10, self._text.width, self._text.height)
        self._text._dirty = False
    
    def _draw_ui(self, state: str = 'BASE'):
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        rad = self.style[state]['radius']

        x = y = 0
        self._drawer.rect(x, y, self.width, self.height, bd_color, rad)
        self._drawer.rect(
            x + 1, y + 1, self.width - 2,self.height - 2, bg_color, rad - 1)
