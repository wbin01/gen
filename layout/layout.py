#!/usr/bin/env python3
from ctypes import c_int

import sdl3

from ..ui import UI


class Layout(UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        self.__padding = 10
        self.__spacing = 10

        self._UI__dirty = True
        self.__uis = []

    def add(self, ui: UI) -> UI:
        """..."""
        self.__uis.append(ui)
        ui._UI__parent = self
        return ui
    
    def __invalidate(self) -> None:
        for ui in self.__uis:
            ui._UI__dirty = True

        self._UI__dirty = True
    
    def __update(self) -> None:
        """..."""
        tmp_x, tmp_y = self.x, self.y
        for ui in self.__uis:
            ui.x = tmp_x
            ui.y = tmp_y
            tmp_y += ui.height + self.__spacing

    def __redraw(self) -> None:
        """..."""
        for ui in self.__uis:
            if ui._UI__dirty:
                name = f'_{ui.__class__.__name__}'
                getattr(ui, name + '__draw')()
                ui._UI__dirty = False

        self.__dirty = False
