#!/usr/bin/env python3
import copy
from ctypes import c_float, c_int
import time

import sdl3

from ..cell import Cell
from ..ui import UIObject, Theme


class Layout(object):
    pass


class Scroll(UIObject):
    """..."""
    def __init__(self, parent: Cell | Layout, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """..."""
        self._parent = parent
        self._fill = 'X' if parent._orientation == 'VERTICAL' else 'Y'
        self._control_x = self._parent._x
        self._control_y = self._parent._y
        self._width = 200
        self._height = 200

        self._side = None
        self._hbar_rect = None
        self._vbar_rect = None

        self._tt_bar = None
        self._tt_base_bar = None

        self._bar_thickness = 10
        self._roll_step = 20
        self._offset = None
        self._cursor_point = None
        self.style = copy.deepcopy(Theme.Scroll)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def height(self) -> int:
        """..."""
        if 'Y' in self._fill:
            return self._parent._height
        return self._height
    
    @height.setter
    def height(self, height: int) -> None:
        self._height = height
    
    @property
    def width(self) -> int:
        """..."""
        if 'X' in self._fill:
            return self._parent._width
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
        if not self._parent: return
        if not self._parent._scrollable: return

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
        if not self._parent: return
        if not self._parent._scrollable: return
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
    
    def _bar_area(self, mx: float, my: float) -> tuple | None:
        w = self._parent._x + self.width
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

        if h - self._bar_thickness < my < h and self._parent._x < mx < w:
            # return ('H', self._hbar_rect)
            return None
        
        elif w - self._bar_thickness < mx < w and self._parent._y < my < h:
            return ('V', self._vbar_rect)
        
        return None

    def _hovering(self, mx: c_float, my: c_float) -> None:
        mx, my = mx.value, my.value
        bar = self._bar_area(mx, my)
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

    def _bar_drag(self, mx: c_float, my: c_float) -> None:
        mx, my = mx.value, my.value

        if not self._offset:
            self._offset = mx, my
        
        bar = self._bar_area(mx, my)
        if not self._side and bar: self._side = bar[0]

        if self._side == 'V':
            if not self._cursor_point:
                self._cursor_point = my - self._vbar_rect[1]
            point = (my - self._cursor_point)

            if my < self._offset[1]:
                self._roll_down(my, self._vbar_rect[1] - point)
            elif my > self._offset[1]:
                self._roll_up(my, point - self._vbar_rect[1])
        # else:
        #     self._roll_down()

        self._offset = mx, my

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


class Layout(UIObject):
    """Organizes the positioning of the elements."""
    def __init__(self, scrollable: bool = False, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._base_class = 'Layout'
        self._orientation = 'VERTICAL'

        self._drawer = None
        self._first_redraw = True
        self._queue = []

        self._x = 0
        self._y = 0
        self._scrollable = scrollable
        self._scroll = Scroll(self)
        self.style = copy.deepcopy(Theme.Layout)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def scroll(self) -> Scroll:
        """..."""
        return self._scroll

    def _update(self) -> None:
        pass
    
    def _hit_test(self, x: int, y: int) -> UIObject | None:
        if not self.visible:
            return None

        if not self._rect_contains(self, x, y):
            return None

        for obj in self._objects:
            if isinstance(obj, Layout):
                hit_obj =  obj._hit_test(x, y)
                if hit_obj:
                    return hit_obj

            elif isinstance(obj, Cell):
                view = obj._parent._scroll if obj._parent._scrollable else None
                hit_obj = obj._hit_test(x, y, view)
                if hit_obj:
                    return hit_obj
        
        return self
    
    def _invalidate(self) -> None:
        self._dirty = True
        for obj in self._objects:
            if isinstance(obj, Layout):
                obj._invalidate()
                continue
            obj._dirty = True
    
    def _queue_list(self) -> list:
        self._dirty = True

        for obj in self._objects:
            if isinstance(obj, Layout):
                self._queue.extend(obj._queue_list())
                continue

            if obj not in self._queue:
                obj._dirty = True
                self._queue.append(obj)
        
        return self._queue
    
    def _queue_list_clear(self) -> list:
        self._queue = []

        for obj in self._objects:
            if isinstance(obj, Layout):
                obj._queue_list_clear()
                continue

    def _redraw(self, mode: str = None) -> None:        
        if self._app:
            if self._app._hovered and not self._app._hovered._dirty:
                self._app._hovered._invalidate()
            
            if self._app._focus and not self._app._focus._dirty:
                self._app._focus._invalidate()
        
        if not self._objects:
            return
        
        for obj in self._objects:

            if isinstance(obj, Layout):
                if obj._scrollable:
                    obj._draw(mode)
                    self._drawer.clip_start(obj, obj._scroll)
                    obj._redraw(mode)
                    self._drawer.clip_end()

                    if obj.scroll._vbar_rect:
                        obj.scroll._draw()
                else:
                    if self._app and self._app._view_layout:
                        obj._draw(mode)
                    obj._redraw(mode)
                    
                continue
            obj._draw(mode)

        self._dirty = False
    
    def _redraw_queue(
            self, queue_list: list, budget_ms: float = 3.0) -> None:
        if not queue_list:
            return
        
        start = time.perf_counter()
        while queue_list:
            obj = queue_list.pop(0)
            obj._draw('REBUILD')
            if (time.perf_counter() - start) * 50 > budget_ms:
                break
        
        return True if not queue_list else False
