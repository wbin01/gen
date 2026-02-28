#!/usr/bin/env python3
import time

from ..cell import Cell
from ..ui import UI


class Layout(UI):
    """Organizes the positioning of the elements."""
    __alpha = 240
    __debug_colors = (
        (93, 93, 62, __alpha),  (58, 78, 59, __alpha),   (52, 51, 63, __alpha),
        (88, 78, 84, __alpha),  (68, 47, 58, __alpha),   (99, 61, 61, __alpha),
        (119, 139,80, __alpha), (92, 114, 113, __alpha), (67, 67, 67, __alpha))
    __debug_color_index = 0
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

    def __redraw(self, rebuild: str = None) -> None:
        if not self._Add__uis:
            return
        
        for ui in self._Add__uis:
            if not ui.visible: continue
            if not ui._UI__dirty:
                continue

            # mro = str(type(ui).__mro__)
            # if 'layout.box.Box' in mro:
            if isinstance(ui, Layout):
                if rebuild == 'REBUILD' and not ui._Box__first:
                    ui._Box__debug_color = self.__color(ui==self._Add__uis[-1])
                    if self._app and self._app._Frame__view_layout:
                        ui._Box__draw()
                ui._Layout__redraw(rebuild)
                continue

            getattr(ui, f'_{ui.__class__.__name__}__draw')(rebuild)
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

            getattr(ui, f'_{ui.__class__.__name__}__draw')(rebuild='REBUILD')
            ui._UI__dirty = False

            if (time.perf_counter() - start) * 50 > budget_ms:
                break
    
    @classmethod
    def __color(cls, reset: bool) -> tuple:
        cls.__debug_color_index += 1
        if cls.__debug_color_index == 9: cls.__debug_color_index = 0

        if reset: cls.__debug_color_index = 0
        return cls.__debug_colors[cls.__debug_color_index]
