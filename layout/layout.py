#!/usr/bin/env python3
from ..ui import UI


class Layout(UI):
    """Organizes the positioning of the elements."""
    __debug_colors = (
        (93, 93, 62, 255),   (58, 78, 59, 255),   (52, 51, 63, 255),
        (88, 78, 84, 255),   (68, 47, 58, 255),   (99, 61, 61, 255),
        (119, 139, 80, 255), (92, 114, 113, 255), (67, 67, 67, 255))
    __debug_color_index = 0

    def __init__(self, *args, **kwargs) -> None:
        self.__drawer = None
    
    def __update(self) -> None:
        pass

    def __redraw(self) -> None:
        """..."""
        for ui in self._Add__uis:
            mro = str(type(ui).__mro__)
            if 'cell.cell.Cell' in mro and not ui.visible: continue
            if not ui._UI__dirty: continue

            if 'layout.box.Box' in mro:
                ui._Box__debug_color = self.__get_debug_color()
                if self._app and self._app._Frame__debug: ui._Box__draw()
                ui._Layout__redraw()
                continue

            getattr(ui, f'_{ui.__class__.__name__}__draw')()
            ui._UI__dirty = False

        self._UI__dirty = False
    
    @classmethod
    def __get_debug_color(cls) -> tuple:
        cls.__debug_color_index += 1
        if cls.__debug_color_index == 9: cls.__debug_color_index = 0
        return cls.__debug_colors[cls.__debug_color_index]
