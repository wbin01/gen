#!/usr/bin/env python3
import time

from ..cell import Cell
from ..ui import UI


class Layout(UI):
    """Organizes the positioning of the elements."""
    __instances = 0

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__drawer = None
        self.__first_redraw = True
        self.__queue = []
    
    def __update(self) -> None:
        pass
    
    @classmethod
    def __reg_instances(cls) -> None:
        cls.__instances += 1
    
    @classmethod
    def __get_instances(cls) -> int:
        return cls.__instances
    
    def __hit_test(self, x: int, y: int) -> UI | None:
        if not self.visible:
            return None

        if not self._UI__rect_contains(self, x, y):
            return None

        for ui in self._Add__uis:
            if isinstance(ui, Layout):
                hit_ui =  ui._Layout__hit_test(x, y)
                if hit_ui: return hit_ui
                continue

            if isinstance(ui, Cell):  # or isinstance(ui, Layout):
                hit_ui = ui._Cell__hit_test(x, y)
                if hit_ui:
                    return hit_ui
        
        return self
    
    def __queue_list(self) -> list:
        self._UI__dirty = True

        for ui in self._Add__uis:
            if isinstance(ui, Layout):
                self.__queue.extend(ui._Layout__queue_list())
                continue

            if ui not in self.__queue:
                ui._UI__dirty = True
                self.__queue.append(ui)
        
        return self.__queue
    
    def __queue_list_clear(self) -> list:
        self.__queue = []

        for ui in self._Add__uis:
            if isinstance(ui, Layout):
                ui._Layout__queue_list_clear()
                continue

    def __invalidate(self) -> None:
        self._UI__dirty = True
        for ui in self._Add__uis:
            if isinstance(ui, Layout):
                ui._Layout__invalidate()
                continue
            ui._UI__dirty = True

    def __redraw(self, mode: str = None) -> None:
        if not self._Add__uis:
            return
        
        for ui in self._Add__uis:
            if not ui.visible: continue
            if not ui._UI__dirty:
                continue

            if isinstance(ui, Layout):
                if self._app and self._app._Frame__view_layout:
                    ui._Box__draw(mode)
                
                ui._Layout__redraw(mode)
                continue
            
            getattr(ui, f'_{ui._UI__base_class}__draw')(mode)
            ui._UI__dirty = False

        self._UI__dirty = False
    
    def __redraw_queue(
            self, queue_list: list, budget_ms: float = 3.0) -> None:
        
        if not queue_list:
            return
        
        start = time.perf_counter()
        while queue_list:
            ui = queue_list.pop(0)

            if not ui.visible: continue
            if not ui._UI__dirty: continue

            getattr(ui, f'_{ui.__class__.__name__}__draw')('REBUILD')
            ui._UI__dirty = False

            if (time.perf_counter() - start) * 50 > budget_ms:
                break
        
        return True if not queue_list else False
