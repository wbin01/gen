#!/usr/bin/env python3
from .layout import Layout
from ..cell import Cell, ColExpander, RowExpander
from ..flag import Align, Fill
from ..mixin import Add, Margin, Pos, Size
from ..ui import Theme


class Box(Margin, Pos, Size, Add, Layout):
    """Organizes the positioning of the elements."""
    def __init__(
            self,
            spacing: int = 0, margin: tuple | int = 0, fill: Fill = Fill.XY,
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
                (`Fill.X`, `Fill.Y`, `Fill.XY`, `Fill.NONE`).
                
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
        self.__first = False
        self.__orientation = 'VERTICAL'
        self._dirty = True

        self.__texture_hover = None
    
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
        configured direction (`Fill.X`, `Fill.Y`, `Fill.XY`, `Fill.NONE`).
        
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
        """Space between the elements."""
        return self.__spacing
    
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self.__spacing = spacing
    
    def __update(self) -> None:
        # Updates the width, fill, alignment, and position of cells.
        if self.__orientation == 'POSITION':
            return
        
        if self._dirty == 'HOVER':
            return
        
        if not self._Add__uis:
            return
        
        if self._Box__first:
            self.__update_size(self)
            self.__update_align(self)
            self.__update_fill(self)
        
        ui_x, ui_y = self._x, self._y  # Reset
        for ui in self._Add__uis:
            if not ui.visible: continue
            if not ui._dirty: continue

            ui._Pos__x = ui_x + ui.margin[3]  # Set current position
            ui._Pos__y = ui_y + ui.margin[0]

            if self.__orientation == 'VERTICAL':  # Prepare next position
                ui_y += ui.height + ui._Margin__margin_y + self.__spacing
            elif self.__orientation == 'HORIZONTAL':
                ui_x += ui.width + ui._Margin__margin_x + self.__spacing
            
            if isinstance(ui, Layout):
                ui._Box__update() #  Repeat for all
    
    def __update_size(self, layout: Box) -> None:
        # Make sure the layout size are compatible with the number 
        # of stacked cells.
        if not layout._Add__uis:
            return
        
        layout._Size__width = layout._Size__base_width
        if layout.fill in (Fill.X, Fill.XY):
            layout._Size__width = 0
            layout._Size__base_width = 0
            
        layout._Size__height = layout._Size__base_height
        if layout.fill in (Fill.Y, Fill.XY):
            layout._Size__height = 0
            layout._Size__base_height = 0
        
        last = len(layout._Add__uis) - 1  # To remove last extra 'spacing'
        for num, ui in enumerate(layout._Add__uis):
            if not ui.visible: continue
            if not ui._dirty: continue

            if isinstance(ui, Layout):
                self.__update_size(ui)

            if layout._Box__orientation == 'VERTICAL':  # Set width height
                if layout.fill in (Fill.X, Fill.XY):
                    w = ui._Size__width + ui._Margin__margin_x
                    if w > layout.width:
                        layout._Size__width = w
                        layout._Size__base_width = w

                if layout.fill in (Fill.Y, Fill.XY):
                    h = ui._Size__base_height + ui._Margin__margin_y
                    if num != last: h += layout.spacing
                    layout._Size__height += h
                    layout._Size__base_height += h

            elif layout._Box__orientation == 'HORIZONTAL':
                if layout.fill in (Fill.X, Fill.XY):
                    w = ui._Size__base_width + ui._Margin__margin_x
                    if num != last: w += layout.spacing
                    layout._Size__width += w
                    layout._Size__base_width += w
                
                if layout.fill in (Fill.Y, Fill.XY):
                    h = ui._Size__height + ui._Margin__margin_y
                    if h > layout.height:
                        layout._Size__height = h
                        layout._Size__base_height = h

    def __update_fill(self, layout: Box) -> None:
        # Updates the fill of layouts and cells.
        if not layout._Add__uis:
            return
        
        if layout._Box__first:
            layout._Size__width = layout._parent.width
            layout._Size__height = layout._parent.height
        
        total_width = layout.width
        total_height = layout.height

        if layout._Box__orientation == 'VERTICAL':
            # Width
            min_width = 0
            for ui in layout._Add__uis:  # Fill: Width equal to the layout
                if not ui.visible: continue
                if not ui._dirty: continue

                if ui.fill in (Fill.X, Fill.XY):
                    ui._Size__width = total_width - ui._Margin__margin_x
                
                if isinstance(ui, Cell):
                    if ui._Size__width < ui._Size__min_width:
                        ui._Size__width = ui._Size__min_width
                
                if isinstance(ui, Cell) and ui.fill in (Fill.Y, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_width - ui.width) // 2
                        ui.margin = ui.margin[0], dt, ui.margin[2], dt

                    elif layout.base_align == Align.END:
                        dt = (total_width - ui.width)
                        ui.margin = ui.margin[0], ui.margin[1],ui.margin[2], dt
                
                if min_width < ui._Size__width + ui._Margin__margin_x:
                    min_width = ui._Size__width + ui._Margin__margin_x
            
            if layout._Size__width < min_width:
                layout._Size__width = min_width
            
            # Height
            min_height = 0
            vertical, height, last = [], 0, len(layout._Add__uis) - 1
            for num, ui in enumerate(layout._Add__uis):
                if isinstance(ui, Cell) and not ui.visible: continue

                if isinstance(ui, Cell) and ui.height < ui._Size__min_height:
                    ui.height = ui._Size__min_height

                if hasattr(ui, 'fill'):  # Collects cells that expand
                    if ui.fill in (Fill.Y, Fill.XY): vertical.append(ui)
                
                height += ui.height + ui._Margin__margin_y  # Save height
                min_height += ui._Size__height
                if num != last:
                    height += layout.spacing
                    min_height += layout.spacing

            vertical_num = len(vertical)
            free = total_height - height  # Discover available space

            delta = free / vertical_num if vertical_num > 1 else free
            for ui in vertical:  # Distributes space to the cells that require
                ui._Size__height += delta
                if isinstance(ui, Cell) and ui._Size__height < ui._Size__min_height:
                    ui._Size__height = ui._Size__min_height
            
            if layout._Size__height < min_height:
                layout._Size__height = min_height
        
        elif layout._Box__orientation == 'HORIZONTAL':
            # Height
            min_height = 0
            for ui in layout._Add__uis:
                if isinstance(ui, Cell) and not ui.visible: continue

                if ui.fill in (Fill.Y, Fill.XY):
                    ui._Size__height = total_height - ui._Margin__margin_y
                    if ui._Size__height < ui._Size__min_height:
                        ui._Size__height = ui._Size__min_height

                if isinstance(ui, Cell) and ui.fill in (Fill.X, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_height - ui.height) // 2
                        ui.margin = dt, ui.margin[1], dt, ui.margin[3]
                    
                    elif layout.base_align == Align.END:
                        dt = (total_height - ui.height)
                        ui.margin = dt, ui.margin[1], ui.margin[2],ui.margin[3]
                
                if isinstance(ui, Cell):
                    if min_height < ui.height + ui._Margin__margin_y:
                        min_height = ui.height + ui._Margin__margin_y

            if layout._Size__height < min_height:
                layout._Size__height = min_height
        
            # Width
            min_width = 0
            horizontal, width, last = [], 0, len(layout._Add__uis) - 1
            for num, ui in enumerate(layout._Add__uis):
                if isinstance(ui, Cell):
                    if not ui.visible: continue

                if ui._Size__width < ui._Size__min_width:
                    ui._Size__width = ui._Size__min_width
                    print(ui._Size__min_width)

                if ui.fill.value in (Fill.NONE, Fill.Y):  # Fixed width
                    ui._Size__width = ui._Size__base_width

                if hasattr(ui, 'fill'):
                    if ui.fill in (Fill.X, Fill.XY): horizontal.append(ui)
                
                width += ui.width + ui._Margin__margin_x
                min_width += ui._Size__min_width
                if num != last:
                    width += layout.spacing
                    min_width += layout.spacing
            
            horizontal_num = len(horizontal)
            free = total_width - width
            
            delta = free / horizontal_num if horizontal_num > 1 else free
            for ui in horizontal:
                ui._Size__width += delta
                if isinstance(ui, Cell) and ui._Size__width < ui._Size__min_width:
                    ui._Size__width = ui._Size__min_width
            
            if layout._Size__width < min_width:
                layout._Size__width = min_width

        for ui in layout._Add__uis:
            if isinstance(ui, Layout):
                self.__update_fill(ui)
    
    def __update_align(self, layout: Box) -> None:
        if not layout._Add__uis:
            return
        
        if layout._Box__orientation == 'VERTICAL':
            if layout.align == Align.START:
                if isinstance(layout._Add__uis[0], ColExpander):
                    del(layout._Add__uis[0])
                
                if isinstance(layout._Add__uis[-1], ColExpander):
                    del(layout._Add__uis[-1])
            
            elif layout.align == Align.END:
                if isinstance(layout._Add__uis[-1], ColExpander):
                    del(layout._Add__uis[-1])
                
                if not isinstance(layout._Add__uis[0], ColExpander):
                    layout._Add__uis.insert(0, ColExpander())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._Add__uis[0], ColExpander):
                    layout._Add__uis.insert(0, ColExpander())

                if not isinstance(layout._Add__uis[-1], ColExpander):
                    layout._Add__uis.insert(
                        len(layout._Add__uis), ColExpander())
        
        elif layout._Box__orientation == 'HORIZONTAL':
            if layout.align == Align.START:
                if isinstance(layout._Add__uis[0], RowExpander):
                    del(layout._Add__uis[0])
            
            elif layout.align == Align.END:
                if isinstance(layout._Add__uis[-1], RowExpander):
                    del(layout._Add__uis[-1])
                
                if not isinstance(layout._Add__uis[0], RowExpander):
                    layout._Add__uis.insert(0, RowExpander())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._Add__uis[0], RowExpander):
                    layout._Add__uis.insert(0, RowExpander())

                if not isinstance(layout._Add__uis[-1], RowExpander):
                    layout._Add__uis.insert(
                        len(layout._Add__uis), RowExpander())
        
        for ui in layout._Add__uis:
            if isinstance(ui, Layout):
                self.__update_align(ui)

    def __draw(self, mode: str = None) -> None:
        if not self._Box__first and mode == 'REBUILD':
            self._Layout__drawer.rect(
                self._x - self.margin[3], self._y - self.margin[0],
                self.width + self.margin[3] + self.margin[1],
                self.height + self.margin[0] + self.margin[2],
                Theme.Frame['BASE']['accent-color'],
                Theme.Frame['BASE']['radius'])
            
            self._Layout__drawer.rect(
                self._x - self.margin[3] + 1, self._y - self.margin[0] + 1,
                self.width + self.margin[3] + self.margin[1] - 2,
                self.height + self.margin[0] + self.margin[2] - 2,
                Theme.Frame['BASE']['background-color'],
                Theme.Frame['BASE']['radius'])
