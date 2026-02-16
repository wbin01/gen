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
        self.height = self.padding * 2
        self.width = self.padding * 2
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
        ui._Cell__drawer = self.__drawer

        height = ui.padding * 2 + ui.height
        if height > self.height:
            self.height = height
        
        width = ui.padding * 2 + ui.width
        if width > self.width:
            self.width = width

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
        tmp_x, tmp_y = self.x, self.y

        first = True
        for ui in self.__uis:
            if not ui._UI__dirty:
                continue

            if self.__orientation == Orientation.VERTICAL:
                if first:
                    ui.x = tmp_x + self.padding
                    ui.y = tmp_y + self.padding
                    tmp_y += (ui.padding * 2 + ui.height
                        ) + self.__spacing + self.padding
                    first = False
                else:
                    ui.x = tmp_x + self.padding
                    ui.y = tmp_y
                    tmp_y += (ui.padding * 2 + ui.height) + self.__spacing
                
                self.height += tmp_y
                
            else:
                if first:
                    ui.x = tmp_x + self.padding
                    ui.y = tmp_y + self.padding
                    tmp_x += (ui.padding * 2 + ui.width
                        ) + self.__spacing + self.padding
                    first = False
                else:
                    ui.x = tmp_x
                    ui.y = tmp_y + self.padding
                    tmp_x += (ui.padding * 2 + ui.width) + self.__spacing
                
                self.width += tmp_x
            
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
            getattr(ui, f'_{ui.__class__.__name__}__draw')()
            ui._UI__dirty = False

        self._UI__dirty = False
