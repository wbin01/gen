#!/usr/bin/env python3
from .layout import Layout
from ..cell import Cell, ColExpander, RowExpander
from ..flag import Align, Fill
from ..mixin import Add, Margin, Size
from ..ui import Theme


class Box(Margin, Size, Add, Layout):
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
        self._spacing = spacing
        self._align = align
        self._base_align = base_align
        self._fill = fill
        self._first = False
        self._orientation = 'VERTICAL'
        self._dirty = True

        self._x = 0
        self._y = 0
    
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
        return self._align
    
    @align.setter
    def align(self, align: Align) -> None:
        self._align = align
    
    @property
    def base_align(self) -> Align:
        """Align: An Enum of type `Align`."""
        return self._base_align
    
    @base_align.setter
    def base_align(self, base_align: Align) -> None:
        self._base_align = base_align
    
    @property
    def fill(self) -> Fill:
        """An `Enum` of type `Fill`.
        
        Fills the empty space in the layout and stretches the items in the 
        configured direction (`Fill.X`, `Fill.Y`, `Fill.XY`, `Fill.NONE`).
        
        `Fill` takes precedence over the `width` and `height` properties, so 
        the `width` property does not work together with `Fill.X` and the 
        `height` property does not work together with `Fill.Y`.
        """
        return self._fill
    
    @fill.setter
    def fill(self, fill: Fill) -> None:
        self._fill = fill
    
    @property
    def spacing(self) -> int:
        """Space between the elements."""
        return self._spacing
    
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._spacing = spacing
    
    def _draw(self, mode: str = None) -> None:
        if not self._first and mode == 'REBUILD':
            self._drawer.rect(
                self._x - self.margin[3], self._y - self.margin[0],
                self.width + self.margin[3] + self.margin[1],
                self.height + self.margin[0] + self.margin[2],
                Theme.Frame['BASE']['accent-color'],
                Theme.Frame['BASE']['radius'])
            
            self._drawer.rect(
                self._x - self.margin[3] + 1, self._y - self.margin[0] + 1,
                self.width + self.margin[3] + self.margin[1] - 2,
                self.height + self.margin[0] + self.margin[2] - 2,
                Theme.Frame['BASE']['background-color'],
                Theme.Frame['BASE']['radius'])
    
    def _update(self, mode: str = 'REBUILD') -> None:
        # Updates the width, fill, alignment, and position of cells.
        if self._orientation == 'POSITION': return
        if mode == 'UNIT': return
        if not self._uis: return
        
        if self._first:
            self._update_size(self)
            self._update_align(self)
            self._update_fill(self)
        
        ui_x, ui_y = self._x, self._y  # Reset
        for ui in self._uis:
            if not ui.visible: continue
            if not ui._dirty: continue

            ui._x = ui_x + ui.margin[3]  # Set current position
            ui._y = ui_y + ui.margin[0]

            if self._orientation == 'VERTICAL':  # Prepare next position
                ui_y += ui.height + ui._margin_y + self._spacing
            elif self._orientation == 'HORIZONTAL':
                ui_x += ui.width + ui._margin_x + self._spacing
            
            if isinstance(ui, Layout):
                ui._update() #  Repeat for all
    
    def _update_align(self, layout: Box) -> None:
        if not layout._uis: return
        
        if layout._orientation == 'VERTICAL':
            if layout.align == Align.START:
                if isinstance(layout._uis[0], ColExpander):
                    del(layout._uis[0])
                
                if isinstance(layout._uis[-1], ColExpander):
                    del(layout._uis[-1])
            
            elif layout.align == Align.END:
                if isinstance(layout._uis[-1], ColExpander):
                    del(layout._uis[-1])
                
                if not isinstance(layout._uis[0], ColExpander):
                    layout._uis.insert(0, ColExpander())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._uis[0], ColExpander):
                    layout._uis.insert(0, ColExpander())

                if not isinstance(layout._uis[-1], ColExpander):
                    layout._uis.insert(
                        len(layout._uis), ColExpander())
        
        elif layout._orientation == 'HORIZONTAL':
            if layout.align == Align.START:
                if isinstance(layout._uis[0], RowExpander):
                    del(layout._uis[0])
            
            elif layout.align == Align.END:
                if isinstance(layout._uis[-1], RowExpander):
                    del(layout._uis[-1])
                
                if not isinstance(layout._uis[0], RowExpander):
                    layout._uis.insert(0, RowExpander())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._uis[0], RowExpander):
                    layout._uis.insert(0, RowExpander())

                if not isinstance(layout._uis[-1], RowExpander):
                    layout._uis.insert(
                        len(layout._uis), RowExpander())
        
        for ui in layout._uis:
            if isinstance(ui, Layout):
                self._update_align(ui)
    
    def _update_fill(self, layout: Box) -> None:
        # Updates the fill of layouts and cells.
        if not layout._uis: return
        
        if layout._first:
            layout._width = layout._parent.width
            layout._height = layout._parent.height
        
        total_width = layout.width
        total_height = layout.height

        if layout._orientation == 'VERTICAL':
            # Width
            min_width = 0
            for ui in layout._uis:  # Fill: Width equal to the layout
                if not ui.visible: continue
                if not ui._dirty: continue

                if ui.fill in (Fill.X, Fill.XY):
                    ui._width = total_width - ui._margin_x
                
                if isinstance(ui, Cell):
                    if ui._width < ui._min_width:
                        ui._width = ui._min_width
                
                if isinstance(ui, Cell) and ui.fill in (Fill.Y, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_width - ui.width) // 2
                        ui.margin = ui.margin[0], dt, ui.margin[2], dt

                    elif layout.base_align == Align.END:
                        dt = (total_width - ui.width)
                        ui.margin = ui.margin[0], ui.margin[1],ui.margin[2], dt
                
                if min_width < ui._width + ui._margin_x:
                    min_width = ui._width + ui._margin_x
            
            if layout._width < min_width:
                layout._width = min_width
            
            # Height
            min_height = 0
            vertical, height, last = [], 0, len(layout._uis) - 1
            for num, ui in enumerate(layout._uis):
                if isinstance(ui, Cell) and not ui.visible: continue

                if isinstance(ui, Cell) and ui.height < ui._min_height:
                    ui.height = ui._min_height

                if hasattr(ui, 'fill'):  # Collects cells that expand
                    if ui.fill in (Fill.Y, Fill.XY): vertical.append(ui)
                
                height += ui.height + ui._margin_y  # Save height
                min_height += ui._height
                if num != last:
                    height += layout.spacing
                    min_height += layout.spacing

            vertical_num = len(vertical)
            free = total_height - height  # Discover available space

            delta = free / vertical_num if vertical_num > 1 else free
            for ui in vertical:  # Distributes space to the cells that require
                ui._height += delta
                if isinstance(ui, Cell) and ui._height < ui._min_height:
                    ui._height = ui._min_height
            
            if layout._height < min_height:
                layout._height = min_height
        
        elif layout._orientation == 'HORIZONTAL':
            # Height
            min_height = 0
            for ui in layout._uis:
                if isinstance(ui, Cell) and not ui.visible: continue

                if ui.fill in (Fill.Y, Fill.XY):
                    ui._height = total_height - ui._margin_y
                    if ui._height < ui._min_height:
                        ui._height = ui._min_height

                if isinstance(ui, Cell) and ui.fill in (Fill.X, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_height - ui.height) // 2
                        ui.margin = dt, ui.margin[1], dt, ui.margin[3]
                    
                    elif layout.base_align == Align.END:
                        dt = (total_height - ui.height)
                        ui.margin = dt, ui.margin[1], ui.margin[2],ui.margin[3]
                
                if isinstance(ui, Cell):
                    if min_height < ui.height + ui._margin_y:
                        min_height = ui.height + ui._margin_y

            if layout._height < min_height:
                layout._height = min_height
        
            # Width
            min_width = 0
            horizontal, width, last = [], 0, len(layout._uis) - 1
            for num, ui in enumerate(layout._uis):
                if isinstance(ui, Cell):
                    if not ui.visible: continue

                if ui._width < ui._min_width:
                    ui._width = ui._min_width
                    print(ui._min_width)

                if ui.fill.value in (Fill.NONE, Fill.Y):  # Fixed width
                    ui._width = ui._base_width

                if hasattr(ui, 'fill'):
                    if ui.fill in (Fill.X, Fill.XY): horizontal.append(ui)
                
                width += ui.width + ui._margin_x
                min_width += ui._min_width
                if num != last:
                    width += layout.spacing
                    min_width += layout.spacing
            
            horizontal_num = len(horizontal)
            free = total_width - width
            
            delta = free / horizontal_num if horizontal_num > 1 else free
            for ui in horizontal:
                ui._width += delta
                if isinstance(ui, Cell) and ui._width < ui._min_width:
                    ui._width = ui._min_width
            
            if layout._width < min_width:
                layout._width = min_width

        for ui in layout._uis:
            if isinstance(ui, Layout):
                self._update_fill(ui)

    def _update_size(self, layout: Box) -> None:
        # Make sure the layout size are compatible with the number 
        # of stacked cells.
        if not layout._uis:
            return
        
        layout._width = layout._base_width
        if layout.fill in (Fill.X, Fill.XY):
            layout._width = 0
            layout._base_width = 0
            
        layout._height = layout._base_height
        if layout.fill in (Fill.Y, Fill.XY):
            layout._height = 0
            layout._base_height = 0
        
        last = len(layout._uis) - 1  # To remove last extra 'spacing'
        for num, ui in enumerate(layout._uis):
            if not ui.visible: continue
            if not ui._dirty: continue

            if isinstance(ui, Layout):
                self._update_size(ui)

            if layout._orientation == 'VERTICAL':  # Set width height
                if layout.fill in (Fill.X, Fill.XY):
                    w = ui._width + ui._margin_x
                    if w > layout.width:
                        layout._width = w
                        layout._base_width = w

                if layout.fill in (Fill.Y, Fill.XY):
                    h = ui._base_height + ui._margin_y
                    if num != last: h += layout.spacing
                    layout._height += h
                    layout._base_height += h

            elif layout._orientation == 'HORIZONTAL':
                if layout.fill in (Fill.X, Fill.XY):
                    w = ui._base_width + ui._margin_x
                    if num != last: w += layout.spacing
                    layout._width += w
                    layout._base_width += w
                
                if layout.fill in (Fill.Y, Fill.XY):
                    h = ui._height + ui._margin_y
                    if h > layout.height:
                        layout._height = h
                        layout._base_height = h
