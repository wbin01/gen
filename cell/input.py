#!/usr/bin/env python3
from PIL import ImageFont
import sdl3

from .cell import Cell
from ..control import Timer
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
        self.fill = fill
        self._invalidate_item = None

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

        self._focus = False

        # Input text
        self._left = []
        self._right = []

        self._font_name = self.style['BASE']['font']
        self._font_size = self.style['BASE']['font-size']
        self._font = ImageFont.truetype(self._font_name, self._font_size)
        
        self._text_texture = None
        self._textx = 0
        self._texty = 0
        self._textw = 0
        self._texth = 0

        # Selection
        self._selection_texture = None
        self._selx = 0
        self._sely = 0
        self._selw = 0
        self._selh = 0

        self._selection = ['', '', '']
        self._select_direction = None
        self._selecting = False
        self._selection_start = False
        self._selection_end = False

        # Cursor
        self._cursor = 0
        self._cursor_w = 1
        self._anchor = None
        self._positions = []
        self._widths = []
        self._cursor_visible = False
        self._cursor_texture_on = None
        self._cursor_texture_off = None
        self._timer = Timer(call=self._cursor_tick)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self._text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._text}")'
    
    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, text) -> None:
        self.insert(text)
        self._invalidate_item = 'TEXT'
        self._invalidate()

    def backspace(self) -> str:
        del_char = ''
        if self._selection[1]:
            del_char = self._selection[1]
            self.cut()

        elif self._left:
            del_char = self._left.pop()
            self._dirty = True
            self._text = ''.join(self._left) + ''.join(self._right)
            self._cursor = len(self._left)
            self._update_positions()
        
        self._invalidate_item = 'TEXT'
        self._invalidate()
        return del_char
    
    def clear_selection(self) -> None:
        self._selection[0] = self._left
        self._selection[1] = ''
        self._selection[2] = self._right
        self._invalidate_item = 'TEXT'
        self._invalidate()
    
    def copy(self) -> str:
        return self._selection[1]
    
    def cut(self) -> str:
        start, selected_text, end = self._selection

        self._left = list(start)
        self._right = list(end)
        self.clear_selection()

        self._cursor = len(start)
        self._anchor = self._cursor

        self._text = ''.join(self._left) + ''.join(self._right)
        self._update_positions()

        self._invalidate_item = 'TEXT'
        self._invalidate()
        return selected_text

    def delete(self) -> str:
        del_char = ''
        if self._selection[1]:
            del_char = self._selection[1]
            self.cut()
        
        elif self._right:
            del_char = self._right.pop(0)
            self._dirty = True
            self._text = ''.join(self._left) + ''.join(self._right)
            self._cursor = len(self._left)
            self._update_positions()
        
        self._invalidate_item = 'TEXT'
        self._invalidate()
        return del_char
    
    def insert(self, text) -> None:
        for char in text:
            self._left.append(str(char))
        
        self._text = ''.join(self._left) + ''.join(self._right)
        self._cursor = len(self._left)
        self._update_positions()
        # self._dirty = True

        self._invalidate_item = 'TEXT'
        self._invalidate()

    def move_left(self) -> int:
        if self._left:
            self._right.insert(0, self._left.pop())
            self._cursor = len(self._left)
        return self._cursor

    def move_left_by_jump(self) -> int:
        while self._left and self._left[-1] == ' ':
            self._right.insert(0, self._left.pop())

        while self._left and self._left[-1] != ' ':
            self._right.insert(0, self._left.pop())
        
        self._cursor = len(self._left)
        return self._cursor
    
    def move_right(self) -> int:
        if self._right:
            self._left.append(self._right.pop(0))
            self._cursor = len(self._left)
        return self._cursor
    
    def move_right_by_jump(self) -> int:
        while self._right and self._right[0] == ' ':
            self._left.append(self._right.pop(0))

        while self._right and self._right[0] != ' ':
            self._left.append(self._right.pop(0))
        
        self._cursor = len(self._left)
        return self._cursor
    
    def past(self, text) -> str:
        for c in text:
            self._left.append(c)
        
        self.clear_selection()
        self._text = ''.join(self._left) + ''.join(self._right)
        self._update_positions()

        self._invalidate_item = 'TEXT'
        self._invalidate()
        return text
    
    def select_all(self) -> str:
        self._selection[0] = ''
        self._selection[1] = self._text
        self._selection[2] = ''

        self._invalidate_item = 'SELECT'
        self._invalidate()
        return self._selection[1]
    
    def select_left(self) -> str:
        self._select_direction = 'LEFT'
        if self._anchor is None:
            self._anchor = self._cursor
            self._sely = self._texty - 2
            self._selh = self._font_size + 4
            self.clear_selection()

        start = min(self._cursor, self._anchor)
        end = max(self._cursor, self._anchor)

        self._selection[0] = self._text[:start - 1]
        self._selection[1] = self._text[start - 1:end]
        self._selection[2] = self._text[end:]
        self._selx = self._get_cursor_x() + self._textx - 1 - (
            self._font.getlength(self._selection[1][0]))
        self._selw = int(self._font.getlength(self._selection[1])) + 2

        self._invalidate_item = 'SELECT'
        self._invalidate()
        return self._selection[1]
    
    def select_right(self) -> str:
        self._select_direction = 'RIGHT'
        if self._anchor is None:
            self._anchor = self._cursor
            self._selx = self._get_cursor_x() + self._textx - 1
            self._sely = self._texty - 2
            self._selh = self._font_size + 4
            self.clear_selection()

        start = min(self._cursor, self._anchor)
        end = max(self._cursor, self._anchor)
        
        self._selection[0] = self._text[:start]
        self._selection[1] = self._text[start:end + 1]
        self._selection[2] = self._text[end + 1:]
        self._selw = int(self._font.getlength(self._selection[1])) + 2

        self._invalidate_item = 'SELECT'
        self._invalidate()
        return self._selection[1]
    
    def _click_update_cursor(self, mouse_x) -> None:
        pos = self._get_cursor_x_from_click(mouse_x)
        self._left  = list(self._text[:pos])
        self._right = list(self._text[pos:])
        self.clear_selection()
    
    def _get_cursor_x(self) -> int:
        left_text = ''.join(self._left)
        return self._font.getlength(left_text)
    
    def _get_cursor_x_from_click(self, mouse_x) -> int:
        for i, x in enumerate(self._positions):
            half = x + self._widths[i] // 2

            if mouse_x < half:
                self._cursor = i - 1
                return self._cursor

        end = len(self._positions)
        if mouse_x > self._font.getlength(self._text):
            end += 1
        
        self._cursor = end - 1
        return self._cursor
    
    def _mouse_selection(self, mouse_x) -> None:
        if not self._selecting:
            self._selecting = True
            self._anchor = self._get_cursor_x_from_click(mouse_x)

        if self._selecting:
            self._cursor = self._get_cursor_x_from_click(mouse_x)

            self._selection[1] = self._text[self._anchor:self._cursor]
            self._selection[0] = self._text[:self._anchor]
            self._selection[2] = self._text[self._cursor:]

            self._selx = self._get_cursor_x() + self._textx - 1
            self._sely = self._texty - 2
            self._selw = int(self._font.getlength(self._selection[1])) + 2
            self._selh = self._font_size + 4
        
        self._invalidate_item = 'SELECT'
        self._invalidate()
    
    def _update_positions(self):
        self._positions = []
        self._widths = []
        x = 0

        for ch in self._text:
            w = self._font.getlength(ch)
            self._positions.append(x)
            self._widths.append(w)
            x += w

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return
        self._dirty = False

        if self.style['BASE']['font'] != self._font_name:
            self._font_name = self.style['BASE']['font']
            self._font = ImageFont.truetype(
                self._font_name, self.style['BASE']['font-size'])
        
        font_color = self.style['BASE']['font-color']
        font_size = self.style['BASE']['font-size']

        if mode == 'UNIT':
            if self._invalidate_item == 'SELECT':
                self._invalidate_item = None
                if self._selection[1]:
                    self._selection_texture = self._drawer.build_texture(
                        self._selw, self._selh, self._draw_ui, 'HOVER')

            elif self._invalidate_item == 'TEXT':
                self._invalidate_item = None
                self._text_texture, self._textw, self._texth = self._drawer.font(
                    self._text, self._text_texture,
                    self._font, font_size, font_color)
                self._texty = self._y + (self.height / 2) - (self._texth / 2)
            
            self._invalidate_item = None
            self._need_rebuild = True

        if mode == 'REBUILD':
            self._set_state('BASE')
            self._need_rebuild = False

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
                self._font, font_size, font_color)
            self._texty = self._y + (self.height / 2) - (self._texth / 2)

            self._cursor_texture_on = self._drawer.build_texture(
                self._cursor_w, font_size, self._draw_ui, 'CURSOR_ON')
            
            self._cursor_texture_off = self._drawer.build_texture(
                self._cursor_w, font_size, self._draw_ui, 'CURSOR_OFF')
            
            self._resise_w = 0
            self._resise_h = 0
        
        if mode in ('RESIZE', 'POSITION'):
            if mode == 'POSITION': self._need_rebuild = True
            
            if not self._resise_h:
                self._resise_w = int(self.width)
                self._resise_h = int(self.height)
            
            # if self.fill.value == 'X':
            self._resise_w = int(self.width)

            self._drawer.set_texture(
                self._texture_default,
                int(self._x), int(self._y), self._resise_w, self._resise_h)
            
            self._drawer.set_texture(
                self._text_texture,
                self._textx, self._texty, self._textw, self._texth)
            return
        
        if self._need_rebuild: self._dirty = True
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
        
        if self._selection[1]:
            self._drawer.set_texture(
                self._selection_texture,
                self._selx, self._sely, self._selw, self._selh)

        self._drawer.set_texture(
            self._text_texture,
            self._textx, self._texty, self._textw, self._texth)

        if self._app and self._app._focus == self:
            if self._cursor_visible:
                self._drawer.set_texture(
                    self._cursor_texture_on,
                    self._textx + self._get_cursor_x(),
                    self._texty, self._cursor_w, font_size)
            else:
                self._drawer.set_texture(
                    self._cursor_texture_off,
                    self._textx + self._get_cursor_x(),
                    self._texty, self._cursor_w, font_size)
        
        if mode == 'REBUILD':
            self._dirty = False
    
    def _cursor_tick(self) -> None:
        if self._app and self._app._input:
            self._cursor_visible = False if self._cursor_visible else True
            return True
        return False
    
    def _draw_ui(self, state: str = 'BASE'):
        radius = self.style['BASE']['radius']
        border = self.style['BASE']['border']
        font_color = self.style['BASE']['font-color']
        font_size = self.style['BASE']['font-size']

        if 'CURSOR' in state:
            color = font_color if state == 'CURSOR_ON' else (0, 0, 0, 0)
            self._drawer.rect(0, 0, self._cursor_w + 1, font_size, color, 0)
            return

        if self._selection[1]:
            sel_color = self.style['BASE']['selection-color']
            self._drawer.rect(0, 0, self._selw, self._selh, sel_color, 1)
            return

        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        bd_space = border * 2

        self._drawer.rect(0, 0, self.width, self.height, bd_color, radius)
        self._drawer.rect(
            border, border, self.width - bd_space, self.height - bd_space,
            bg_color, radius - border)
