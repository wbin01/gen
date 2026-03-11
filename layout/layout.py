#!/usr/bin/env python3
import time
import ctypes

import sdl3

from ..cell import Cell
from ..ui import UI


class Layout(UI):
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
    
    def _hit_test(self, x: int, y: int) -> UI | None:
        if not self.visible:
            return None

        if not self._rect_contains(self, x, y):
            return None

        for ui in self._uis:
            if isinstance(ui, Layout):
                hit_ui =  ui._hit_test(x, y)
                if hit_ui: return hit_ui
                continue

            if isinstance(ui, Cell):  # or isinstance(ui, Layout):
                hit_ui = ui._hit_test(x, y)
                if hit_ui:
                    return hit_ui
        
        return self
    
    def _invalidate(self) -> None:
        self._dirty = True
        for ui in self._uis:
            if isinstance(ui, Layout):
                ui._invalidate()
                continue
            ui._dirty = True
    
    def _queue_list(self) -> list:
        self._dirty = True

        for ui in self._uis:
            if isinstance(ui, Layout):
                self._queue.extend(ui._queue_list())
                continue

            if ui not in self._queue:
                ui._dirty = True
                self._queue.append(ui)
        
        return self._queue
    
    def _queue_list_clear(self) -> list:
        self._queue = []

        for ui in self._uis:
            if isinstance(ui, Layout):
                ui._queue_list_clear()
                continue

    def _redraw(self, mode: str = None) -> None:        
        if self._app:
            if self._app._hovered and not self._app._hovered._dirty:
                self._app._hovered._invalidate()
            
            if self._app._focus and not self._app._focus._dirty:
                self._app._focus._invalidate()
        
        if not self._uis:
            return
        
        for ui in self._uis:

            if isinstance(ui, Layout):
                if ui._scroll:
                    sdl3.SDL_RenderClipEnabled(self._app._drawer._renderer)
                    clip = sdl3.SDL_Rect(ui._x, ui._y, 500, 200)
                    sdl3.SDL_SetRenderClipRect(
                        self._app._drawer._renderer, ctypes.byref(clip))

                    if self._app and self._app._view_layout:
                        ui._draw(mode)
                    ui._redraw(mode)
                
                    sdl3.SDL_SetRenderClipRect(
                        self._app._drawer._renderer, ctypes.POINTER(sdl3.SDL_Rect)())
                else:
                    if self._app and self._app._view_layout:
                        ui._draw(mode)
                    ui._redraw(mode)
                    
                continue
            ui._draw(mode)

        self._dirty = False
    
    def _redraw_queue(
            self, queue_list: list, budget_ms: float = 3.0) -> None:
        
        if not queue_list:
            return
        
        start = time.perf_counter()
        while queue_list:
            ui = queue_list.pop(0)

            # if not ui.visible: continue
            # if not ui._dirty: continue

            ui._draw('REBUILD')
            # ui._dirty = False

            if (time.perf_counter() - start) * 50 > budget_ms:
                break
        
        return True if not queue_list else False
    
    def _roll(self):
        if self._scroll:

            # sdl3.SDL_RenderClipEnabled(self._app._drawer._renderer)
            # clip = sdl3.SDL_Rect(self._scroll._x, self._scroll._y, 500, 200)
            # sdl3.SDL_SetRenderClipRect(
            #     self._app._drawer._renderer, ctypes.byref(clip))
            
            self._draw('REBUILD')

            self._scroll_y -= 20
            for ui in self._scroll._uis:
                ui._y -= 20
                ui._invalidate()
                ui._draw('POSITION')
                if hasattr(ui, '_need_rebuild'): ui._need_rebuild = True
            
            # self._app._render_mode = 'REBUILD'
            # self._app._render_update = True
            self._scroll._invalidate()

            # sdl3.SDL_SetRenderClipRect(
            # self._app._drawer._renderer, ctypes.POINTER(sdl3.SDL_Rect)())
