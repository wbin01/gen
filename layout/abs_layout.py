#!/usr/bin/env python3
from ctypes import c_int

import sdl3

from ..ui import UI


class AbsLayout(UI):
    """..."""
    def __init__(self, parent, padding=10, fill=False) -> None:
        """..."""
        self.__parent = parent
        self.__pad = padding
        self.__fill = fill

        self.__dirty = True
        self.__uis = []
        self.x = 0 + self.__pad
        self.y = 10
        self.width = c_int()
        self.height = c_int()

        self.__spacing = 10

    def add(self, ui: UI, fill=None) -> UI:
        """..."""
        self.__uis.append(ui)
        ui._UI__parent = self

        if fill is not None:
            self.__fill = fill
        return ui
    
    def __invalidate(self) -> None:
        for ui in self.__uis:
            ui._UI__dirty = True

        self.__dirty = True
    
    def __update(self) -> None:
        """..."""
        sdl3.SDL_GetWindowSize(self.__parent, self.width, self.height)

        for ui in self.__uis:
            setattr(ui, 'x', self.x)
            setattr(ui, 'y', self.y)
            if self.__fill:
                setattr(ui, 'width', self.width.value - (self.__pad * 2))
            # setattr(ui, 'h', self.height.value)
            self.y += getattr(ui, 'height') + self.__spacing
        
        self.x = 0 + self.__pad
        self.y = 10

    def __redraw(self) -> None:
        """..."""
        for ui in self.__uis:
            if ui._UI__dirty:
                name = f'_{ui.__class__.__name__}'
                getattr(ui, name + '__draw')()
                ui._UI__dirty = False

        self.__dirty = False
