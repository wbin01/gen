#!/usr/bin/env python3
from ctypes import c_int
import random

import sdl3

from ..cell import Cell, ExpanderCol, ExpanderRow
from ..flag import Align, Fill
from ..mix import Margin, Position, Size
from ..ui import UI


class Layout(Margin, Position, Size, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__first = False
        self.__drawer = None
        self.width = 0
        self.height = 0
        self.__spacing = 0
        self.__align = Align.NONE
        self.__orientation = 'VERTICAL'
        self.__fill = Fill.ALL

        self.__drawer = None

        self._UI__dirty = True
        self.__uis = []

        self.__debug_colors = (
            (93, 93, 62, 255),   (58, 78, 59, 255),   (52, 51, 63, 255),
            (88, 78, 84, 255),   (68, 47, 58, 255),   (99, 61, 61, 255),
            (119, 139, 80, 255), (92, 114, 113, 255), (67, 67, 67, 255))
        self.__debug_color_index = 0
    
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
        if isinstance(ui, type):
            ui = ui()

        if not isinstance(ui, (Layout, Cell)):
            raise TypeError('Layout only accepts Cell or Layout.')
            
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
        # Updates the width, fill, alignment, and position of cells.

        if self._Layout__first:
            self.__update_size(self)
            self.__update_align(self)
            self.__update_fill(self)
        
        ui_x, ui_y = self.x, self.y  # Reset
        for ui in self.__uis:
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue

            ui.x = ui_x + ui.margin[3]  # Set current position
            ui.y = ui_y + ui.margin[0]

            if self.__orientation == 'VERTICAL':  # Prepare next position
                ui_y += ui.height + ui._Margin__margin_y + self.__spacing
            else:
                ui_x += ui.width + ui._Margin__margin_x + self.__spacing
            
            if isinstance(ui, Layout):  # Repeat for all
                ui._Layout__update()
    
    def __update_size(self, layout: Layout) -> None:
        # Make sure the layout size are compatible with the number 
        # of stacked cells.
        
        layout._Size__height = 0  # Reset
        layout._Size__width = 0
        layout._Size__base_height = 0
        layout._Size__base_width = 0
        
        last = len(layout._Layout__uis) - 1  # To remove last extra 'spacing'
        for num, ui in enumerate(layout._Layout__uis):
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue
            
            if isinstance(ui, Layout):
                self.__update_size(ui)

            if layout._Layout__orientation == 'VERTICAL':  # Set width height
                h = ui._Size__base_height + ui._Margin__margin_y
                if num != last: h += layout.spacing
                layout._Size__height += h
                layout._Size__base_height += h  # Set base for minimal
            
                w = ui._Size__width + ui._Margin__margin_x
                if w > layout.width:
                    layout._Size__width = w
                    layout._Size__base_width = w
            else:
                h = ui._Size__height + ui._Margin__margin_y
                if h > layout.height:
                    layout._Size__height = h
                    layout._Size__base_height = h
            
                w = ui._Size__base_width + ui._Margin__margin_x
                if num != last: w += layout.spacing
                layout._Size__width += w
                layout._Size__base_width += w
    
    def __update_fill(self, layout: Layout) -> None:
        # Updates the fill of layouts and cells.
        
        if layout._Layout__first:
            layout._Size__width = layout._parent.width
            layout._Size__height = layout._parent.height
        
        total_width = layout.width
        total_height = layout.height

        if layout._Layout__orientation == 'VERTICAL':
            # Width
            for ui in layout._Layout__uis:  # Fill: Width equal to the layout
                if isinstance(ui, Cell) and not ui.visible: continue

                if ui.fill.value == 'X' or ui.fill.value == 'ALL':
                    ui._Size__width = total_width - ui._Margin__margin_x
                
                elif ui.fill.value == 'NONE':  # Center
                    if layout.align.value in ['CENTER', 'TOP', 'BOTTOM']:
                        dt = (total_width - ui.width) // 2
                        ui._Margin__margin = ui.margin[0], dt, ui.margin[2], dt
                    
                    elif 'RIGHT' in layout.align.value:  # Right: LEFT default
                        dt = total_width - ui.width
                        ui._Margin__margin = (
                            ui.margin[0], ui.margin[1], ui.margin[2], dt)

            # Height
            vertical, height, last = [], 0, len(layout._Layout__uis) - 1
            for num, ui in enumerate(layout._Layout__uis):
                if isinstance(ui, Cell) and not ui.visible: continue

                if hasattr(ui, 'fill'):  # Collects cells that expand
                    if ui.fill.value == 'Y' or ui.fill.value == 'ALL':
                        vertical.append(ui)
                
                height += ui.height + ui._Margin__margin_y  # Save height
                if num != last: height += layout.spacing
            
            vertical_num = len(vertical)
            free = total_height - height  # Discover available space
            
            delta = free // vertical_num if vertical_num > 1 else free
            for ui in vertical:  # Distributes space to the cells that require
                ui._Size__height += delta
        
        elif layout._Layout__orientation == 'HORIZONTAL':
            # Height
            for ui in layout._Layout__uis:
                if isinstance(ui, Cell) and not ui.visible: continue

                if ui.fill.value == 'Y' or ui.fill.value == 'ALL':
                    ui._Size__height = total_height - ui._Margin__margin_y
                
                elif ui.fill.value == 'NONE':  # Center
                    if layout.align.value in ['CENTER', 'LEFT', 'RIGHT']:
                        dt = (total_height - ui.height) // 2
                        ui._Margin__margin = dt, ui.margin[1], dt, ui.margin[3]
                    
                    elif 'BOTTOM' in layout.align.value:  # Bottom: TOP default
                        dt = total_height - ui.height
                        ui._Margin__margin = (
                            dt, ui.margin[1], ui.margin[2], ui.margin[3])
            
            # Width
            horizontal, width, last = [], 0, len(layout._Layout__uis) - 1
            for num, ui in enumerate(layout._Layout__uis):
                if isinstance(ui, Cell) and not ui.visible: continue
                
                if hasattr(ui, 'fill'):
                    if ui.fill.value == 'X' or ui.fill.value == 'ALL':
                        horizontal.append(ui)
                
                width += ui.width + ui._Margin__margin_x
                if num != last: width += layout.spacing
            
            horizontal_num = len(horizontal)
            free = total_width - width
            
            delta = free // horizontal_num if horizontal_num > 1 else free
            for ui in horizontal:
                ui._Size__width += delta

        for ui in layout._Layout__uis:  # Repeat for all
            if isinstance(ui, Layout):
                self.__update_fill(ui)
    
    def __update_align(self, layout: Layout) -> None:
        if layout._Layout__orientation == 'VERTICAL':
            # CENTER
            if 'TOP' in layout.align.value:  # Default: rm exp bottom
                if isinstance(layout._Layout__uis[0], ExpanderCol):
                    del(layout._Layout__uis[0])
            
            elif 'BOTTOM' in layout.align.value:  # Add exp top and rm bottom
                if isinstance(layout._Layout__uis[-1], ExpanderCol):
                    del(layout._Layout__uis[-1])
                
                if not isinstance(layout._Layout__uis[0], ExpanderCol):
                    layout._Layout__uis.insert(0, ExpanderCol())
            
            elif layout.align.value in ['CENTER', 'RIGHT', 'LEFT']:
                if not isinstance(layout._Layout__uis[0], ExpanderCol):
                    layout._Layout__uis.insert(0, ExpanderCol())

                if not isinstance(layout._Layout__uis[-1], ExpanderCol):
                    layout._Layout__uis.insert(
                        len(layout._Layout__uis), ExpanderCol())

        elif layout._Layout__orientation == 'HORIZONTAL':
            if 'LEFT' in layout.align.value:  # Default: rm exp left
                if isinstance(layout._Layout__uis[0], ExpanderRow):
                    del(layout._Layout__uis[0])
            
            elif 'RIGHT' in layout.align.value:  # Add exp left and rm right
                if isinstance(layout._Layout__uis[-1], ExpanderRow):
                    del(layout._Layout__uis[-1])
                
                if not isinstance(layout._Layout__uis[0], ExpanderRow):
                    layout._Layout__uis.insert(0, ExpanderRow())
                
            elif layout.align.value in ['CENTER', 'TOP', 'BOTTOM']:
                if not isinstance(layout._Layout__uis[0], ExpanderRow):
                    layout._Layout__uis.insert(0, ExpanderRow())

                if not isinstance(layout._Layout__uis[-1], ExpanderRow):
                    layout._Layout__uis.insert(
                        len(layout._Layout__uis), ExpanderRow())

        
        for ui in layout._Layout__uis:  # Repeat for all
            if isinstance(ui, Layout):
                self.__update_align(ui)

    def __redraw(self) -> None:
        """..."""
        if self._app and self._app._Frame__debug: self.__draw()

        num_color = -1
        for ui in self.__uis:
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue

            num_color += 1
            if num_color == 9: num_color = -1

            if isinstance(ui, Layout):
                ui._Layout__debug_color_index = num_color
                ui._Layout__redraw()
                continue

            # if isinstance(ui, Cell):  # mro = str(type(ui).__mro__)
            getattr(ui, f'_{ui.__class__.__name__}__draw')()
            ui._UI__dirty = False

        self._UI__dirty = False
    
    def __draw(self) -> None:
        color = self.__debug_colors[self.__debug_color_index]
        if self._Layout__first: color = (125, 125, 125, 10)
        if not self._Layout__first:
            self._Layout__drawer.rect(
                self.x - self.margin[3], self.y - self.margin[0],
                self.width + self.margin[3] + self.margin[1],
                self.height + self.margin[0] + self.margin[2],
                color, 4)
