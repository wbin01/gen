#!/usr/bin/env python3
from ctypes import c_int

import sdl3

from ..cell import Cell
from ..flag import Orientation
from ..mix import Margin
from ..ui import UI


class Layout(Margin, UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        # self.x += self.margin[3]
        # self.y += self.margin[0]
        self.width = 0
        self.height = 0
        self.__spacing = 6
        self.__orientation = Orientation.VERTICAL

        self.__drawer = None

        self._UI__dirty = True
        self.__uis = []
    
    @property
    def orientation(self) -> Orientation:
        return self.__orientation
    
    @orientation.setter
    def orientation(self, orientation: Orientation) -> None:
        self.__orientation = orientation
    
    @property
    def spacing(self) -> int:
        """..."""
        return self.__spacing
    
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self.__spacing = spacing

    def add(self, ui: UI) -> UI:
        """..."""
        self.__uis.append(ui)
        ui._UI__parent = self
        ui._UI__app = self._app
        ui._Cell__drawer = self._app._Frame__drawer # self.__drawer

        if self.orientation.value == 'VERTICAL':
            height = ui.height + ui.margin[0] + ui.margin[2] + self.spacing
            self.height += height
        
            width = ui.width + ui.margin[1] + ui.margin[3]
            if width > self.width:
                self.width = width
        else:
            height = ui.height + ui.margin[0] + ui.margin[2]
            if height > self.height:
                self.height = height
        
            width = ui.width + ui.margin[1] + ui.margin[3] + self.spacing
            self.width += width

        return ui
    
    def __invalidate(self) -> None:
        for ui in self.__uis:
            if isinstance(ui, Layout):
                ui._Layout__invalidate()
                continue

            ui._UI__dirty = True
        
        self._UI__dirty = True
    
    def __update(self) -> None:
        """..."""
        ui_x, ui_y = self.x, self.y

        for ui in self.__uis:
            if not ui._UI__dirty:
                continue
            
            ui.x = ui_x + ui.margin[3]
            ui.y = ui_y + ui.margin[0]

            if self.__orientation == Orientation.VERTICAL:
                ui_y += ui.margin[0] + ui.height + ui.margin[2] + self.__spacing
            else:
                ui_x += ui.margin[1] + ui.width + ui.margin[3] + self.__spacing
            
            if isinstance(ui, Layout):
                ui._Layout__update()

    def __redraw(self) -> None:
        """..."""
        for ui in self.__uis:
            if not ui._UI__dirty:
                continue

            if isinstance(ui, Layout):
                ui._Layout__redraw()
                continue

            # if isinstance(ui, Cell):  # mro = str(type(ui).__mro__)
            print(
                ui,
                hasattr(ui, f'_{ui.__class__.__name__}__draw'),
                ui._Cell__drawer)
            getattr(ui, f'_{ui.__class__.__name__}__draw')()
            ui._UI__dirty = False

        self._UI__dirty = False
