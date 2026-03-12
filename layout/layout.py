#!/usr/bin/env python3
import time
import ctypes

import sdl3

from ..cell import Cell
from ..ui import UIObject


class Layout(UIObject):
    """Organizes the positioning of the elements."""
    _instances = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._base_class = 'Layout'

        self._drawer = None
        self._first_redraw = True
        self._queue = []
        self._scroll = None
    
    def _update(self) -> None:
        pass
    
    @classmethod
    def _reg_instances(cls) -> None:
        cls._instances += 1
    
    @classmethod
    def _get_instances(cls) -> int:
        return cls._instances
    
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

            if isinstance(obj, Cell):  # or isinstance(obj, Layout):
                hit_obj = obj._hit_test(x, y)
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
                    self._viewport(obj)
                    if self._app and self._app._view_layout:
                        obj._draw(mode)
                    obj._redraw(mode)
                    self._viewport()
                else:
                    if self._app and self._app._view_layout:
                        obj._draw(mode)
                    obj._redraw(mode)
                    
                continue
            obj._draw(mode)

        self._dirty = False
    
    def _viewport(self, obj: Layout = None) -> None:
        if obj:
            sdl3.SDL_RenderClipEnabled(self._app._drawer._renderer)
            clip = sdl3.SDL_Rect(obj._x, obj._y, 500, 200)
            sdl3.SDL_SetRenderClipRect(
                self._app._drawer._renderer, ctypes.byref(clip))
            return
        
        sdl3.SDL_SetRenderClipRect(
            self._app._drawer._renderer, ctypes.POINTER(sdl3.SDL_Rect)())
    
    def _redraw_queue(
            self, queue_list: list, budget_ms: float = 3.0) -> None:
        
        if not queue_list:
            return
        
        start = time.perf_counter()
        while queue_list:
            obj = queue_list.pop(0)

            # if not obj.visible: continue
            # if not obj._dirty: continue

            obj._draw('REBUILD')
            # obj._dirty = False

            if (time.perf_counter() - start) * 50 > budget_ms:
                break
        
        return True if not queue_list else False
    
    def _roll(self):
        if self._scroll:
            # self._viewport(obj)
            self._draw('REBUILD')

            self._scroll_y -= 20
            for obj in self._scroll._objects:
                obj._y -= 20
                obj._invalidate()
                obj._draw('POSITION')
            
            # self._app._render_mode = 'REBUILD'
            # self._app._render_update = True
            self._scroll._invalidate()
            # self._viewport()
