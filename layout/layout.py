#!/usr/bin/env python3
from ctypes import c_int
import random

import sdl3

from ..cell import Cell
from ..flag import Align
from ..mix import Margin, Position, Size
from ..ui import UI


class Layout(Margin, Position, Size, UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        self.__first = False
        self.__drawer = None
        self.width = 0
        self.height = 0
        self.__spacing = 0
        self.__align = Align.VERTICAL

        self.__drawer = None

        self._UI__dirty = True
        self.__uis = []
    
    @property
    def align(self) -> Align:
        return self.__align
    
    @align.setter
    def align(self, align: Align) -> None:
        self.__align = align
    
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

        if isinstance(ui, Cell):
            ui._Cell__drawer = self._app._Frame__drawer
        elif isinstance(ui, Layout):
            ui._Layout__drawer = self._app._Frame__drawer
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
        if self._Layout__first:
            self.__expand_layouts_size(self)
        
        ui_x, ui_y = self.x, self.y
        for ui in self.__uis:

            if not ui._UI__dirty:
                continue
            
            ui.x = ui_x + ui.margin[3]
            ui.y = ui_y + ui.margin[0]

            if self.__align == Align.VERTICAL:
                ui_y += ui.margin[0] + ui.height + ui.margin[2] + self.__spacing
            else:
                ui_x += ui.margin[1] + ui.width + ui.margin[3] + self.__spacing
            
            if isinstance(ui, Layout):
                ui._Layout__update()
    
    def __expand_layouts_size(self, layout) -> None:
        layout.height = 0
        layout.width = 0

        for ui in layout._Layout__uis:
            if not ui._UI__dirty:
                continue
            
            if isinstance(ui, Layout):
                self.__expand_layouts_size(ui)

            if layout.align.value == 'VERTICAL':
                h = ui.height + ui.margin[0] + ui.margin[2] + layout.spacing
                layout.height += h
            
                w = ui.width + ui.margin[1] + ui.margin[3]
                if w > layout.width:
                    layout.width = w
            else:
                h = ui.height + ui.margin[0] + ui.margin[2]
                if h > layout.height:
                    layout.height = h
            
                w = ui.width + ui.margin[1] + ui.margin[3] + layout.spacing
                layout.width += w

    def __redraw(self) -> None:
        """..."""
        if self._app and self._app._Frame__debug: self.__draw()

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
    
    def __draw(self) -> None:
        red = random.randint(50, 100)
        green = random.randint(50, 100)
        blue = random.randint(50, 100)

        if not self._Layout__first:
            self._Layout__drawer.rect(
                self.x - self.margin[3], self.y - self.margin[0],
                self.width + self.margin[3] + self.margin[1],
                self.height + self.margin[0] + self.margin[2],
                (red, green, blue, 255), 0)
