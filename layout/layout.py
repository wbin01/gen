#!/usr/bin/env python3
from ctypes import c_int

import sdl3

from ..cell import Cell
from ..flag import Orientation
from ..mix import Margin, Padding
from ..ui import UI


class Layout(Margin, Padding, UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        self.__spacing = 10
        self.__orientation = Orientation.VERTICAL

        self._UI__dirty = True
        self.__uis = []
    
    @property
    def orientation(self) -> Orientation:
        return self.__orientation
    
    @orientation.setter
    def orientation(self, orientation: Orientation) -> None:
        self.__orientation = orientation

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

        first = True
        for ui in self.__uis:
            # if isinstance(ui, Layout):
            #     ui._Layout__update()
            #     continue

            if self.__orientation == Orientation.VERTICAL:
                if first:
                    ui.x = tmp_x + self.padding
                    ui.y = tmp_y + self.padding
                    tmp_y += ui.height + self.__spacing + self.padding
                    first = False
                else:
                    ui.x = tmp_x + self.padding
                    ui.y = tmp_y
                    tmp_y += ui.height + self.__spacing
            else:
                if first:
                    ui.x = tmp_x + self.padding
                    ui.y = tmp_y + self.padding
                    tmp_x += ui.width + self.__spacing + self.padding
                    first = False
                else:
                    ui.x = tmp_x
                    ui.y = tmp_y + self.padding
                    tmp_x += ui.width + self.__spacing

    def __redraw(self) -> None:
        """..."""
        for ui in self.__uis:
            if ui._UI__dirty:
                if isinstance(ui, Cell):  # mro = str(type(ui).__mro__)
                    getattr(ui, f'_{ui.__class__.__name__}__draw')()
                    ui._UI__dirty = False
                # else:
                #     ui._Layout__redraw()
                #     ui._UI__dirty = False

        self._UI__dirty = False
