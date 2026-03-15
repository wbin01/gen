#!/usr/bin/env python3
import copy
import ctypes
import time

import sdl3

from ..cell import Cell
from ..ui import UIObject, Theme


class ViewPort(object):
    def __init__(self, parent) -> None:
        self._parent = parent
        self._fill = 'X' if parent._orientation == 'VERTICAL' else 'Y'
        self._x = self._parent._x
        self._y = self._parent._y
        self._width = 200
        self._height = 200
    
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
    
    def roll_down(self, layout: Layout = None, step: int = 20) -> None:
        if not self._parent: return
        if not self._parent._scroll: return

        if self._parent._objects[0]._y <= self._parent._y - step:
            # self._parent._draw('REBUILD')
            self._y += step
            self._parent._invalidate()
            self._parent._app._render_mode = 'POSITION'
            self._parent._app._render_update = True

    def roll_up(self, layout: Layout = None, step: int = 20) -> None:
        if not self._parent: return
        if not self._parent._scroll: return

        last_obj = self._parent._objects[-1]
        if last_obj._y + last_obj._height > self._parent._y + self.height:
            # self._parent._draw('REBUILD')
            self._y -= step
            self._parent._invalidate()
            self._parent._app._render_mode = 'POSITION'
            self._parent._app._render_update = True


class Layout(UIObject):
    """Organizes the positioning of the elements."""
    def __init__(self, scroll: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._base_class = 'Layout'
        self._orientation = 'VERTICAL'

        self._drawer = None
        self._first_redraw = True
        self._queue = []

        self._x = 0
        self._y = 0
        self._scroll = scroll
        self._viewport = ViewPort(self)
        self.style = copy.deepcopy(Theme.Layout)
    
    @property
    def viewport(self) -> ViewPort:
        return self._viewport

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
                if hit_obj: return hit_obj
                continue

            if isinstance(obj, Cell):
                view = obj._parent._viewport if obj.parent._scroll else None
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
                if obj._scroll:
                    obj._draw(mode)
                    self._drawer.clip_start(obj, self._viewport)
                    obj._redraw(mode)
                    self._drawer.clip_end()
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
