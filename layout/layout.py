#!/usr/bin/env python3
from ..cell import Cell, ExpanderCol, ExpanderRow
from ..flag import Align, Fill
from ..mix import Margin, Position, Size
from ..ui import UI


class Layout(Margin, Position, Size, UI):
    """Organizes the positioning of the elements."""
    def __init__(
            self,
            spacing: int = 0, margin: int | tuple = (0, 0, 0, 0),
            fill: Fill = Fill.ALL, align: Align = Align.START,
            width: int = 0, height: int = 0,
            *args, **kwargs) -> None:
        """Layout Initializer.

        Args:

            spacing: Space between the elements.
            
            margin: A tuple of integers with the values of the four margins 
                (top, right, bottom, and left), or a single integer 
                representing all margins. 
                Example: `margin = 8` or `margin = 8, 8, 8, 8`.
            
            fill: An `Enum` of type `Fill`. Layout (`column`, `Row`, `Pos`) 
                defined as `Fill.NONE` still expands minimally to fit the 
                internal elements, but does not expand beyond that.

                To keep the width and height fixed, you need to set the 
                `width` and `height` properties to values greater than zero. 
                Also, the `width` property does not work with `Fill.X` or 
                `Fill.ALL` and the `height` property does not work with 
                `Fill.Y` or `Fill.ALL`.

                For the `fill` property to take effect, the `width` and 
                `height` properties must have a value equal to zero.
        """
        super().__init__(*args, **kwargs)
        self.width = width
        self.height = height
        self.margin = margin
        self.__spacing = spacing
        self.__align = align
        self.__fill = fill

        self.__first = False
        self.__drawer = None
        self.__orientation = 'VERTICAL'
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
        """An `Enum` of type `Align`

        The `CENTER`, `TOP_LEFT`, `TOP_RIGHT`, `BOTTOM_RIGHT`, and 
        `BOTTOM_LEFT` alignments will only take effect if there is available 
        lateral space.

        The `align` property with values `TOP`, `BOTTOM`, `RIGHT`, and `LEFT` 
        always aligns everything in the center of its respective side.
        """
        return self.__align
    
    @align.setter
    def align(self, align: Align) -> None:
        self.__align = align
    
    @property
    def fill(self) -> Fill:
        """An `Enum` of type `Fill`.

        Layout (`column`, `Row`, `Pos`) defined as `Fill.NONE` still expands 
        minimally to fit the internal elements, but does not expand beyond 
        that.

        To keep the width and height fixed, simply set the `width` and 
        `height` properties to a value greater than zero.

        For the `fill` property to take effect, the `width` and `height` 
        properties must have a value equal to zero.
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
    
    def add(self, ui: UI) -> UI:
        """..."""
        return self.__add(ui)

    def __add(self, ui: UI) -> UI:
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
        if self.__orientation == 'POSITION':
            return

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
            elif self.__orientation == 'HORIZONTAL':
                ui_x += ui.width + ui._Margin__margin_x + self.__spacing
            
            if isinstance(ui, Layout):
                ui._Layout__update() #  Repeat for all
    
    def __update_size(self, layout: Layout) -> None:
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
        
        last = len(layout._Layout__uis) - 1  # To remove last extra 'spacing'
        for num, ui in enumerate(layout._Layout__uis):
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue

            if isinstance(ui, Layout):
                self.__update_size(ui)

            if layout._Layout__orientation == 'VERTICAL':  # Set width height
                if layout.fill in (Fill.Y, Fill.ALL):
                    h = ui._Size__base_height + ui._Margin__margin_y
                    if num != last: h += layout.spacing
                    layout._Size__height += h
                    layout._Size__base_height += h  # Set base for minimal

                if layout.fill in (Fill.X, Fill.ALL):
                        w = ui._Size__width + ui._Margin__margin_x
                        if w > layout.width:
                            layout._Size__width = w
                            layout._Size__base_width = w
            
            elif layout._Layout__orientation == 'HORIZONTAL':
                if layout.fill in (Fill.Y, Fill.ALL):
                    h = ui._Size__height + ui._Margin__margin_y
                    if h > layout.height:
                        layout._Size__height = h
                        layout._Size__base_height = h

                if layout.fill in (Fill.X, Fill.ALL):
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

                if ui.fill in (Fill.X, Fill.ALL):
                    ui._Size__width = total_width - ui._Margin__margin_x
            # Height
            vertical, height, last = [], 0, len(layout._Layout__uis) - 1
            for num, ui in enumerate(layout._Layout__uis):
                if isinstance(ui, Cell) and not ui.visible: continue

                if hasattr(ui, 'fill'):  # Collects cells that expand
                    if ui.fill in (Fill.Y, Fill.ALL): vertical.append(ui)
                
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

                if ui.fill in (Fill.Y, Fill.ALL):
                    ui._Size__height = total_height - ui._Margin__margin_y
            # Width
            horizontal, width, last = [], 0, len(layout._Layout__uis) - 1
            for num, ui in enumerate(layout._Layout__uis):
                if isinstance(ui, Cell) and not ui.visible: continue
                
                if hasattr(ui, 'fill'):
                    if ui.fill in (Fill.X, Fill.ALL): horizontal.append(ui)
                
                width += ui.width + ui._Margin__margin_x
                if num != last: width += layout.spacing
            
            horizontal_num = len(horizontal)
            free = total_width - width
            
            delta = free // horizontal_num if horizontal_num > 1 else free
            for ui in horizontal:
                ui._Size__width += delta

        for ui in layout._Layout__uis:
            if isinstance(ui, Layout):
                self.__update_fill(ui)
    
    def __update_align(self, layout: Layout) -> None:
        if layout._Layout__orientation == 'VERTICAL':
            if layout.align == Align.START:
                if isinstance(layout._Layout__uis[0], ExpanderCol):
                    del(layout._Layout__uis[0])
                
                if isinstance(layout._Layout__uis[-1], ExpanderCol):
                    del(layout._Layout__uis[-1])
            
            elif layout.align == Align.END:
                if isinstance(layout._Layout__uis[-1], ExpanderCol):
                    del(layout._Layout__uis[-1])
                
                if not isinstance(layout._Layout__uis[0], ExpanderCol):
                    layout._Layout__uis.insert(0, ExpanderCol())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._Layout__uis[0], ExpanderCol):
                    layout._Layout__uis.insert(0, ExpanderCol())

                if not isinstance(layout._Layout__uis[-1], ExpanderCol):
                    layout._Layout__uis.insert(
                        len(layout._Layout__uis), ExpanderCol())
        
        elif layout._Layout__orientation == 'HORIZONTAL':
            if layout.align == Align.START:
                if isinstance(layout._Layout__uis[0], ExpanderRow):
                    del(layout._Layout__uis[0])
            
            elif layout.align == Align.END:
                if isinstance(layout._Layout__uis[-1], ExpanderRow):
                    del(layout._Layout__uis[-1])
                
                if not isinstance(layout._Layout__uis[0], ExpanderRow):
                    layout._Layout__uis.insert(0, ExpanderRow())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._Layout__uis[0], ExpanderRow):
                    layout._Layout__uis.insert(0, ExpanderRow())

                if not isinstance(layout._Layout__uis[-1], ExpanderRow):
                    layout._Layout__uis.insert(
                        len(layout._Layout__uis), ExpanderRow())
        
        for ui in layout._Layout__uis:
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
