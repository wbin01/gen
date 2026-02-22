#!/usr/bin/env python3
from .layout import Layout
from ..cell import Cell, ExpanderCol, ExpanderRow
from ..flag import Align, Fill
from ..mix import Add, Margin, Position, Size


class Box(Margin, Position, Size, Add, Layout):
    """Organizes the positioning of the elements."""
    def __init__(
            self,
            spacing: int = 0, margin: tuple | int = 0, fill: Fill = Fill.ALL,
            align: Align = Align.START, base_align: Align = Align.CENTER,
            width: int = None, height: int = None,
            *args, **kwargs) -> None:
        """Layout Initializer.

        Args:

            spacing: Space between the elements.
            
            margin: A tuple of integers with the values of the four margins 
                (top, right, bottom, and left), or a single integer 
                representing all margins. 
                Example: `margin = 8` or `margin = 8, 8, 8, 8`.
            
            fill: An `Enum` of type `Fill`. Fills the empty space in the 
                layout and stretches the items in the configured direction 
                (`Fill.X`, `Fill.Y`, `Fill.ALL`, `Fill.NONE`).
                
                `Fill` takes precedence over the `width` and `height` 
                properties, so the `width` property does not work together 
                with `Fill.X` and the `height` property does not work together 
                with `Fill.Y`.
            
            align: An Enum of type `Align`. Alignment only works in the 
                direction of the layout with the `fill` option active. This 
                means that the `Col` needs to have `fill` set to `Fill.X` and 
                the `Row` needs to have `fill` set to `Fill.Y`.
                
                In a `Row` layout, using `Align.START` will align to the left, 
                `Align.CENTER` to the center, and `Align.END` will align to 
                the right. In a `Col` layout, `Align.START` will align to the 
                top, `Align.CENTER` to the center, and `Align.END` will align 
                to the bottom.
        """
        super().__init__(*args, **kwargs)
        if width: self.width = width
        if height: self.height = height
        self.margin = margin
        self.__spacing = spacing
        self.__align = align
        self.__base_align = base_align
        self.__fill = fill
        self.__min_height = 0
        self.__min_width = 0

        self.__first = False
        self.__orientation = 'VERTICAL'
        self._UI__dirty = True
        self.__debug_color = (93, 93, 62, 255)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def align(self) -> Align:
        """Align: An Enum of type `Align`.

        Alignment only works in the direction of the layout with the `fill` 
        option active. This means that the `Col` needs to have `fill` set 
        to `Fill.X` and the `Row` needs to have `fill` set to `Fill.Y`.
        
        In a `Row` layout, using `Align.START` will align to the left, 
        `Align.CENTER` to the center, and `Align.END` will align to the right. 
        In a `Col` layout, `Align.START` will align to the top, `Align.CENTER` 
        to the center, and `Align.END` will align to the bottom.
        """
        return self.__align
    
    @align.setter
    def align(self, align: Align) -> None:
        self.__align = align
    
    @property
    def base_align(self) -> Align:
        """Align: An Enum of type `Align`."""
        return self.__base_align
    
    @base_align.setter
    def base_align(self, base_align: Align) -> None:
        self.__base_align = base_align
    
    @property
    def fill(self) -> Fill:
        """An `Enum` of type `Fill`.
        
        Fills the empty space in the layout and stretches the items in the 
        configured direction (`Fill.X`, `Fill.Y`, `Fill.ALL`, `Fill.NONE`).
        
        `Fill` takes precedence over the `width` and `height` properties, so 
        the `width` property does not work together with `Fill.X` and the 
        `height` property does not work together with `Fill.Y`.
        """
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
    
    def __invalidate(self) -> None:
        for ui in self._Add__uis:
            if isinstance(ui, Layout):
                ui._Box__invalidate()
                continue

            ui._UI__dirty = True
        
        self._UI__dirty = True
    
    def __update(self) -> None:
        # Updates the width, fill, alignment, and position of cells.
        if self.__orientation == 'POSITION':
            return

        if self._Box__first:
            self.__update_size(self)
            self.__update_align(self)
            self.__update_fill(self)
        
        ui_x, ui_y = self.x, self.y  # Reset
        for ui in self._Add__uis:
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue

            ui.x = ui_x + ui.margin[3]  # Set current position
            ui.y = ui_y + ui.margin[0]

            if self.__orientation == 'VERTICAL':  # Prepare next position
                ui_y += ui.height + ui._Margin__margin_y + self.__spacing
            elif self.__orientation == 'HORIZONTAL':
                ui_x += ui.width + ui._Margin__margin_x + self.__spacing
            
            if isinstance(ui, Layout):
                ui._Box__update() #  Repeat for all
    
    def __update_size(self, layout: Box) -> None:
        # Make sure the layout size are compatible with the number 
        # of stacked cells.
        layout._Size__width = layout._Size__base_width
        if layout.fill in (Fill.X, Fill.ALL):
            layout._Size__width = 0
            layout._Size__base_width = 0
            
        layout._Size__height = layout._Size__base_height
        if layout.fill in (Fill.Y, Fill.ALL):
            layout._Size__height = 0
            layout._Size__base_height = 0
        
        last = len(layout._Add__uis) - 1  # To remove last extra 'spacing'
        for num, ui in enumerate(layout._Add__uis):
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue

            if isinstance(ui, Layout):
                self.__update_size(ui)

            if layout._Box__orientation == 'VERTICAL':  # Set width height
                if layout.fill in (Fill.X, Fill.ALL):
                    w = ui._Size__width + ui._Margin__margin_x
                    if w > layout.width:
                        layout._Size__width = w
                        layout._Size__base_width = w

                if layout.fill in (Fill.Y, Fill.ALL):
                    h = ui._Size__base_height + ui._Margin__margin_y
                    if num != last: h += layout.spacing
                    layout._Size__height += h
                    layout._Size__base_height += h
                    
                if isinstance(ui, Cell):  # Minimal
                    if self.__min_width < ui._Size__base_width:
                        self.__min_width = ui._Size__base_width
                
                    # if self.__min_height < layout._Size__base_height:
                    #     self.__min_height = layout._Size__base_height

            elif layout._Box__orientation == 'HORIZONTAL':
                if layout.fill in (Fill.X, Fill.ALL):
                    w = ui._Size__base_width + ui._Margin__margin_x
                    if num != last: w += layout.spacing
                    layout._Size__width += w
                    layout._Size__base_width += w
                
                if layout.fill in (Fill.Y, Fill.ALL):
                    h = ui._Size__height + ui._Margin__margin_y
                    if h > layout.height:
                        layout._Size__height = h
                        layout._Size__base_height = h
                
                # if isinstance(ui, Cell):  # Minimal
                #     if self.__min_width < layout._Size__base_width:
                #         self.__min_width = layout._Size__base_width
                
                #     if self.__min_height < ui._Size__base_height:
                #         self.__min_height = ui._Size__base_height

    def __update_fill(self, layout: Box) -> None:
        # Updates the fill of layouts and cells.
        if layout._Box__first:
            layout._Size__width = layout._parent.width
            layout._Size__height = layout._parent.height
        
        total_width = layout.width
        total_height = layout.height

        if layout._Box__orientation == 'VERTICAL':
            # Width
            for ui in layout._Add__uis:  # Fill: Width equal to the layout
                if isinstance(ui, Cell) and not ui.visible: continue

                if ui.fill in (Fill.X, Fill.ALL):
                    ui._Size__width = total_width - ui._Margin__margin_x
                
                if isinstance(ui, Layout):
                    if ui._Size__width < self.__min_width:
                        ui._Size__width = self.__min_width
                
                if isinstance(ui, Cell) and ui.fill in (Fill.Y, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_width - ui.width) // 2
                        ui.margin = ui.margin[0], dt, ui.margin[2], dt

                    elif layout.base_align == Align.END:
                        dt = (total_width - ui.width)
                        ui.margin = ui.margin[0], ui.margin[1],ui.margin[2], dt

            # Height
            vertical, height, last = [], 0, len(layout._Add__uis) - 1
            for num, ui in enumerate(layout._Add__uis):
                if isinstance(ui, Cell) and not ui.visible: continue

                if hasattr(ui, 'fill'):  # Collects cells that expand
                    if ui.fill in (Fill.Y, Fill.ALL): vertical.append(ui)
                
                height += ui.height + ui._Margin__margin_y  # Save height
                if num != last: height += layout.spacing
            
            vertical_num = len(vertical)
            free = total_height - height  # Discover available space
            
            delta = free / vertical_num if vertical_num > 1 else free
            for ui in vertical:  # Distributes space to the cells that require
                ui._Size__height += delta

                # if isinstance(ui, Layout):
                #     if ui._Size__height < self.__min_height:
                #         ui._Size__height = self.__min_height
        
        elif layout._Box__orientation == 'HORIZONTAL':
            # Height
            for ui in layout._Add__uis:
                if isinstance(ui, Cell) and not ui.visible: continue

                if ui.fill in (Fill.Y, Fill.ALL):
                    ui._Size__height = total_height - ui._Margin__margin_y
                
                # if isinstance(ui, Layout):
                #     if ui._Size__height < self.__min_height:
                #         ui._Size__height = self.__min_height

                if isinstance(ui, Cell) and ui.fill in (Fill.X, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_height - ui.height) // 2
                        ui.margin = dt, ui.margin[1], dt, ui.margin[3]
                    
                    elif layout.base_align == Align.END:
                        dt = (total_height - ui.height)
                        ui.margin = dt, ui.margin[1], ui.margin[2],ui.margin[3]
        
            # Width
            horizontal, width, last = [], 0, len(layout._Add__uis) - 1
            for num, ui in enumerate(layout._Add__uis):
                if isinstance(ui, Cell) and not ui.visible: continue
                
                if hasattr(ui, 'fill'):
                    if ui.fill in (Fill.X, Fill.ALL): horizontal.append(ui)
                
                width += ui.width + ui._Margin__margin_x
                if num != last: width += layout.spacing
            
            horizontal_num = len(horizontal)
            free = total_width - width
            
            delta = free / horizontal_num if horizontal_num > 1 else free
            for ui in horizontal:
                ui._Size__width += delta

                if isinstance(ui, Layout):
                    if ui._Size__width < self.__min_width:
                        ui._Size__width = self.__min_width

        for ui in layout._Add__uis:
            if isinstance(ui, Layout):
                self.__update_fill(ui)
    
    def __update_align(self, layout: Box) -> None:
        if layout._Box__orientation == 'VERTICAL':
            if layout.align == Align.START:
                if isinstance(layout._Add__uis[0], ExpanderCol):
                    del(layout._Add__uis[0])
                
                if isinstance(layout._Add__uis[-1], ExpanderCol):
                    del(layout._Add__uis[-1])
            
            elif layout.align == Align.END:
                if isinstance(layout._Add__uis[-1], ExpanderCol):
                    del(layout._Add__uis[-1])
                
                if not isinstance(layout._Add__uis[0], ExpanderCol):
                    layout._Add__uis.insert(0, ExpanderCol())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._Add__uis[0], ExpanderCol):
                    layout._Add__uis.insert(0, ExpanderCol())

                if not isinstance(layout._Add__uis[-1], ExpanderCol):
                    layout._Add__uis.insert(
                        len(layout._Add__uis), ExpanderCol())
        
        elif layout._Box__orientation == 'HORIZONTAL':
            if layout.align == Align.START:
                if isinstance(layout._Add__uis[0], ExpanderRow):
                    del(layout._Add__uis[0])
            
            elif layout.align == Align.END:
                if isinstance(layout._Add__uis[-1], ExpanderRow):
                    del(layout._Add__uis[-1])
                
                if not isinstance(layout._Add__uis[0], ExpanderRow):
                    layout._Add__uis.insert(0, ExpanderRow())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._Add__uis[0], ExpanderRow):
                    layout._Add__uis.insert(0, ExpanderRow())

                if not isinstance(layout._Add__uis[-1], ExpanderRow):
                    layout._Add__uis.insert(
                        len(layout._Add__uis), ExpanderRow())
        
        for ui in layout._Add__uis:
            if isinstance(ui, Layout):
                self.__update_align(ui)

    def __draw(self) -> None:
        if not self._Box__first:
            self._Layout__drawer.rect(
                self.x - self.margin[3], self.y - self.margin[0],
                self.width + self.margin[3] + self.margin[1],
                self.height + self.margin[0] + self.margin[2],
                self.__debug_color, 4)
