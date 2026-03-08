#!/usr/bin/env python3
import time

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
        if not self._uis:
            return
        
        for ui in self._uis:
            if isinstance(ui, Layout):
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
