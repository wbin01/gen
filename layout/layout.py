#!/usr/bin/env python3
import copy
import time

from ..cell import Cell
from ..ui import UIObject, Theme
from .viewport import ViewPort


class Layout(UIObject):
    """Organizes the positioning of the elements."""
    def __init__(self, scroll: bool = False, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._base_class = 'Layout'
        self._orientation = 'VERTICAL'

        self._drawer = None
        self._first_redraw = True
        self._queue = []

        self._x = 0
        self._y = 0
        self._fill_height = None
        self._fill_width = None
        self._scroll = scroll
        self._viewport = ViewPort(self)
        self.style = copy.deepcopy(Theme.ViewPort)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def viewport(self) -> ViewPort:
        """..."""
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
                if hit_obj:
                    return hit_obj

            elif isinstance(obj, Cell):
                view = obj._parent._viewport if obj._parent._scroll else None
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
                    self._drawer.clip_start(obj, obj._viewport)
                    obj._redraw(mode)
                    self._drawer.clip_end()

                    if obj.viewport._vbar_rect:
                        obj.viewport._draw()
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
