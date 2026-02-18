#!/usr/bin/env python3
from ctypes import c_int
import random

import sdl3

from ..cell import Cell
from ..flag import Align, Fill
from ..mix import Margin, Position, Size
from ..ui import UI


class Layout(Margin, Position, Size, UI):
    """..."""
    __colors = (
            (30, 55, 100, 255), (150, 55, 55, 255), (205, 190, 100, 255),
            (75, 110, 60, 255), (140, 170, 200, 255), (75, 60, 80, 255),
            (190, 140, 80, 255), (30, 55, 100, 255), (150, 55, 55, 255),
            (205, 190, 100, 255), (75, 110, 60, 255), (140, 170, 200, 255),
            (75, 60, 80, 255), (190, 140, 80, 255))
    __color = (190, 140, 80, 255)
    def __init__(self, align: Align = Align.VERTICAL, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__first = False
        self.__drawer = None
        self.width = 0
        self.height = 0
        self.__spacing = 0
        self.__align = align
        self.__fill = Fill.ALL

        self.__drawer = None

        self._UI__dirty = True
        self.__uis = []
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def align(self) -> Align:
        """..."""
        return self.__align
    
    @align.setter
    def align(self, align: Align) -> None:
        self.__align = align
    
    @property
    def fill(self) -> Fill:
        """..."""
        return self.__fill
    
    @fill.setter
    def fill(self, fill: Fill) -> None:
        self.__fill = fill
    
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
            self.__layout_size(self)
            self.__layout_fill(self)
        
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
    
    def __layout_size(self, layout) -> None:
        layout.height = 0
        layout.width = 0

        for ui in layout._Layout__uis:
            if not ui._UI__dirty:
                continue
            
            if isinstance(ui, Layout):
                self.__layout_size(ui)

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
    
    def __layout_fill(self, layout) -> None:
        if layout._Layout__first:
            layout.width = layout._parent.width
            layout.height = layout._parent.height
        
        total_w = layout.width # - x margins
        total_h = layout.height # - y margins

        if layout.align.value == 'VERTICAL':
            for ui in layout._Layout__uis:
                ui.width = total_w - ui.margin[1] - ui.margin[3]
            
            fill_h = []
            height = 0
            last = len(layout._Layout__uis) - 1
            for num, ui in enumerate(layout._Layout__uis):
                if hasattr(ui, 'fill'):
                    if ui.fill.value == 'HEIGHT' or ui.fill.value == 'ALL':
                        fill_h.append(ui)
                
                height += ui.height + ui.margin[0] + ui.margin[2]
                if num != last: height += layout.spacing
            
            fill_h_num = len(fill_h)
            free = total_h - height
            
            delta = free // fill_h_num if fill_h_num > 1 else free
            for ui in fill_h:
                ui.height += delta
        
        elif layout.align.value == 'HORIZONTAL':
            for ui in layout._Layout__uis:
                ui.height = total_h - ui.margin[0] - ui.margin[2]
            
            fill_w = []
            width = 0
            last = len(layout._Layout__uis) - 1
            for num, ui in enumerate(layout._Layout__uis):
                if hasattr(ui, 'fill'):
                    if ui.fill.value == 'WIDTH' or ui.fill.value == 'ALL':
                        fill_w.append(ui)
                
                width += ui.width + ui.margin[1] + ui.margin[3]
                if num != last: width += layout.spacing
            
            fill_w_num = len(fill_w)
            free = total_w - width
            
            delta = free // fill_w_num if fill_w_num > 1 else free
            for ui in fill_w:
                ui.width += delta

        for ui in layout._Layout__uis:
            if isinstance(ui, Layout):
                self.__layout_fill(ui)

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
    
    @classmethod
    def __get_bg(cls) -> tuple:
        num_color = 0
        for num, color in enumerate(cls.__colors):
            if color == cls.__color:
                num_color = num + 1

                if num_color > 14: num_color = 0
                cls.__color = cls.__colors[num_color]
                return cls.__color
    
    def __draw(self) -> None:
        color = (125, 125, 125, 10) if self._Layout__first else self.__get_bg()
        self._Layout__drawer.rect(
            self.x - self.margin[3], self.y - self.margin[0],
            self.width + self.margin[3] + self.margin[1],
            self.height + self.margin[0] + self.margin[2],
            color, 4)
