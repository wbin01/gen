#!/usr/bin/env python3
import copy
from ctypes import c_float

from ..ui import UIObject, Theme


class Cell(object):
    pass


class Layout(object):
    pass


class ViewPort(UIObject):
    """..."""
    def __init__(self, parent: Cell | Layout, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """..."""
        self._parent = parent
        self._fill = 'X' if parent._orientation == 'VERTICAL' else 'Y'
        self._control_x = self._parent._x
        self._control_y = self._parent._y
        self._width = None
        self._height = None
        self._first_roll_up = False
        self._first_roll_down = False

        self._side = None
        self._hbar_rect = None
        self._vbar_rect = None

        self._tt_bar = None
        self._tt_base_bar = None

        self._bar_thickness = 10
        self._roll_step = 20
        self._offset = None
        self._cursor_point = None
        self.style = copy.deepcopy(Theme.ScrollBar)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def height(self) -> int:
        """..."""
        if not self._height:
            return self._parent._height if 'Y' in self._fill else 200
        return self._height
    
    @height.setter
    def height(self, height: int) -> None:
        self._height = height
    
    @property
    def width(self) -> int:
        """..."""
        if not self._width:
            return self._parent._width if 'X' in self._fill else 200
        return self._width
    
    @width.setter
    def width(self, width: int) -> None:
        self._width = width
    
    @property
    def x(self) -> int:
        """..."""
        return self._parent._x
    
    @property
    def y(self) -> int:
        """..."""
        return self._parent._y
    
    def _roll_down(self, cursor_y: float, step: float = 0) -> None:
        self._first_roll_down = True
        if not self._parent: return
        if not self._parent._scroll: return

        stop = (
            cursor_y < self._parent._y,
            cursor_y > self._parent._y + self.height,
            self._parent._objects[0]._y > self._parent._y)
        if any(stop): return
        
        if self._parent._objects[0]._y <= self._parent._y:
            self._control_y += step if step else self._roll_step
            self._parent._invalidate()
            self._parent._app._render_mode = 'POSITION'
            self._parent._app._render_update = True

    def _roll_up(self, cursor_y: float, step: float = 0) -> None:
        self._first_roll_up = True
        if not self._parent: return
        if not self._parent._scroll: return
        last_obj = self._parent._objects[-1]

        stop = (
            cursor_y < self._parent._y,
            cursor_y > self._parent._y + self.height,
            last_obj._y + last_obj._height < self._parent._y + self.height)
        if any(stop): return
        
        if last_obj._y + last_obj._height >= self._parent._y + self.height:
            self._control_y -= step if step else self._roll_step
            self._parent._invalidate()
            self._parent._app._render_mode = 'POSITION'
            self._parent._app._render_update = True
    
    def _bar_area(self, cursor_x: float, cursor_y: float) -> tuple | None:
        w = self._parent._x + self.width # + self._parent._padding_x
        h = self._parent._y + self.height + self._parent._padding_y

        height_delta = h - self._parent._y
        y_delta = self.y
        if self._parent._objects_height > self.height:
            x = self._parent._objects_height // self.height
            height_delta = self.height // x

            y_delta = self.y - (self.y + self._control_y)
            y_delta = y_delta // x
        
        bar_y = self._parent._y + y_delta
        if bar_y + height_delta > h: bar_y = h - height_delta
        if bar_y < self._parent._y: bar_y = self._parent._y

        self._vbar_rect = (
            w - self._bar_thickness, bar_y,
            w - (w - self._bar_thickness), height_delta)
        
        width_delta = w - self._parent._x
        if self._parent._objects_width > self.width:
            width_delta = self._parent._objects_width // self.width
            width_delta = self.width // width_delta

        self._hbar_rect = (
            self._parent._x, h - self._bar_thickness,
            width_delta, h - (h - self._bar_thickness))

        if (h - self._bar_thickness < cursor_y < h and
                self._parent._x < cursor_x < w):
            return ('H', self._hbar_rect)
        
        elif (w - self._bar_thickness < cursor_x < w and
                self._parent._y < cursor_y < h):
            return ('V', self._vbar_rect)
        
        return None

    def _hovering(self, cursor_x: c_float, cursor_y: c_float) -> None:
        bar = self._bar_area(cursor_x.value, cursor_y.value)
        if not bar:
            self._side = None
            return
        
        self._side = bar[0]
        if self._side == 'V':
            self._vbar_rect = bar[1]
        else:
            self._hbar_rect = bar[1]
        
        self._tt_bar = self._parent._drawer.texture(
            self._tt_bar, bar[1][2], bar[1][3], self._draw_bar, self._side)
        
        self._tt_base_bar = self._parent._drawer.texture(
            self._tt_base_bar, bar[1][2], bar[1][3], self._draw_bar, 'BASE')

    def _bar_drag(self, cursor_x: c_float, cursor_y: c_float) -> None:
        cursor_x, cursor_y = cursor_x.value, cursor_y.value

        if not self._offset:
            self._offset = cursor_x, cursor_y
        
        bar = self._bar_area(cursor_x, cursor_y)
        if not self._side and bar: self._side = bar[0]

        if self._side == 'V':
            if not self._cursor_point:
                self._cursor_point = cursor_y - self._vbar_rect[1]
            point = (cursor_y - self._cursor_point)

            if cursor_y < self._offset[1]:
                self._roll_down(cursor_y, self._vbar_rect[1] - point)
            elif cursor_y > self._offset[1]:
                self._roll_up(cursor_y, point - self._vbar_rect[1])
        # else:
        #     self._roll_down()

        self._offset = cursor_x, cursor_y

    def _draw(self):
        bar = self._vbar_rect if self._side == 'V' else self._hbar_rect

        if not self._side:
            self._parent._drawer.apply_texture(
                self._tt_base_bar, bar[0], bar[1], bar[2], bar[3])
            return
        
        self._parent._drawer.apply_texture(
            self._tt_bar, bar[0], bar[1], bar[2], bar[3])
    
    def _draw_bar(self, mode: str) -> None:
        bar = self._vbar_rect if self._side == 'V' else self._hbar_rect

        if mode == 'BASE':
            self._parent._drawer.rect(0, 0, bar[2], bar[3], (0, 0, 0, 0), 0)
            return
        
        self._parent._drawer.rect(
            0, 0, bar[2], bar[3],
            self.style['BASE']['background-color'],
            self.style['BASE']['radius'])
