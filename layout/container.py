#!/usr/bin/env python3
from .layout import Layout
from ..cell import Cell, ColExpander, RowExpander
from ..flag import Align, Fill
from ..mixin import Add, Margin, Padding, Size
from ..ui import Theme


class Container(Margin, Padding, Size, Add, Layout):
    """Organizes the positioning of the elements."""
    def __init__(
            self,
            spacing: int = 0, fill: Fill = Fill.XY,
            margin: tuple | int = 0, padding: tuple | int = 0,
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
        self.padding = padding
        self._spacing = spacing
        self._align = align
        self._base_align = base_align
        self._fill = fill
        self._first = False
        self._orientation = 'VERTICAL'
        self._tx_background = None
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
    
    def _draw_tx(self) -> None:
        if not self._tx_background:
            self._tx_background = self._drawer.build_texture(
                self.width + self.margin[3] + self.margin[1] - 2,
                self.height + self.margin[0] + self.margin[2] - 2,
                self._draw_obj, 'BASE')

        self._drawer.set_texture(
            self._tx_background,
            self._x - self.margin[3], self._y - self.margin[0],
            self.width + self.margin[3] + self.margin[1] - 2,
            self.height + self.margin[0] + self.margin[2] - 2)
    
    def _draw_obj(self, mode: str = None) -> None:
        self._drawer.rect(
            0, 0,
            self.width + self.margin[3] + self.margin[1],
            self.height + self.margin[0] + self.margin[2],
            Theme.Frame['BASE']['accent-color'],
            Theme.Frame['BASE']['radius'])
        
        color = Theme.Frame['BASE']['background-color']
        self._drawer.rect(
            0, 0,
            self.width + self.margin[3] + self.margin[1] - 2,
            self.height + self.margin[0] + self.margin[2] - 2,
            (color[0], color[1], color[2], 255), Theme.Frame['BASE']['radius'])
        
    def _draw(self, mode: str = None) -> None:
        # if self._scrollable or not self._first and mode == 'REBUILD':
        if True:
            bd_color = self.style['BASE']['border-color']
            if not self._scrollable:
                bd_color = Theme.Frame['BASE']['accent-color']
            
            self._drawer.rect(
                self._x, self._y, self.width, self.height,
                bd_color, self.style['BASE']['radius'])
            
            bd = self.style['BASE']['border']
            self._drawer.rect(
                self._x + bd, self._y + bd,
                self.width - (bd * 2), self.height - (bd * 2),
                self.style['BASE']['background-color'],
                self.style['BASE']['radius'])
    
    def _update(self, mode: str = 'REBUILD') -> None:
        # Updates the width, fill, alignment, and position of cells.
        if self._orientation == 'POSITION': return
        if mode == 'UNIT': return
        if not self._objects: return
        
        if self._first:
            self._update_size(self)
            self._update_align(self)
            self._update_fill(self)
        
        x, y = self._x + self.padding[3], self._y + self.padding[0] # Reset
        if self._scrollable: y += self._scroll._control_y

        for obj in self._objects:
            if not obj.visible: continue
            if not obj._dirty: continue

            obj._x = x + obj.margin[3]  # Current position
            obj._y = y + obj.margin[0]

            if self._orientation == 'VERTICAL':  # Next position
                y += obj.height + obj._margin_y + self._spacing
            elif self._orientation == 'HORIZONTAL':
                x += obj.width + obj._margin_x + self._spacing
            
            if isinstance(obj, Layout):
                obj._y += 1
                obj._update()
    
    def _update_align(self, layout) -> None:
        if not layout._objects: return
        
        if layout._orientation == 'VERTICAL':
            if layout.align == Align.START:
                if isinstance(layout._objects[0], ColExpander):
                    del(layout._objects[0])
                
                if isinstance(layout._objects[-1], ColExpander):
                    del(layout._objects[-1])
            
            elif layout.align == Align.END:
                if isinstance(layout._objects[-1], ColExpander):
                    del(layout._objects[-1])
                
                if not isinstance(layout._objects[0], ColExpander):
                    layout._objects.insert(0, ColExpander())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._objects[0], ColExpander):
                    layout._objects.insert(0, ColExpander())

                if not isinstance(layout._objects[-1], ColExpander):
                    layout._objects.insert(
                        len(layout._objects), ColExpander())
        
        elif layout._orientation == 'HORIZONTAL':
            if layout.align == Align.START:
                if isinstance(layout._objects[0], RowExpander):
                    del(layout._objects[0])
            
            elif layout.align == Align.END:
                if isinstance(layout._objects[-1], RowExpander):
                    del(layout._objects[-1])
                
                if not isinstance(layout._objects[0], RowExpander):
                    layout._objects.insert(0, RowExpander())
            
            elif layout.align == Align.CENTER:
                if not isinstance(layout._objects[0], RowExpander):
                    layout._objects.insert(0, RowExpander())

                if not isinstance(layout._objects[-1], RowExpander):
                    layout._objects.insert(
                        len(layout._objects), RowExpander())
        
        for obj in layout._objects:
            if isinstance(obj, Layout):
                self._update_align(obj)
    
    def _update_fill(self, layout) -> None:
        if not layout._objects: return
        
        if layout._first:
            layout._width = layout._parent.width
            layout._height = layout._parent.height
        
        total_width = layout.width - layout._padding_x
        total_height = layout.height

        if layout._orientation == 'VERTICAL':
            # Width
            min_width = 0
            for obj in layout._objects:  # Fill: Width equal to the layout
                mg, pd = obj.margin, obj.padding
                if not obj.visible: continue
                if not obj._dirty: continue

                if obj.fill in (Fill.X, Fill.XY):
                    obj._width = total_width - obj._margin_x
                
                if isinstance(obj, Cell):
                    if obj._width < obj._min_width:
                        obj._width = obj._min_width
                
                if isinstance(obj, Cell) and obj.fill in (Fill.Y, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_width - obj.width) / 2
                        obj.margin = mg[0], dt, mg[2], dt

                    elif layout.base_align == Align.END:
                        dt = (total_width - obj.width)
                        obj.margin = (mg[0], mg[1], mg[2], dt)
                
                if min_width < obj._width + obj._margin_x:
                    min_width = obj._width + obj._margin_x
            
            if layout._width < min_width:
                layout._width = min_width
            
            # Height
            min_height = 0
            vertical, height, last = [], 0, len(layout._objects) - 1
            for num, obj in enumerate(layout._objects):
                if isinstance(obj, Cell) and not obj.visible: continue

                if isinstance(obj, Cell) and obj.height < obj._min_height:
                    obj.height = obj._min_height

                if hasattr(obj, 'fill'):  # Collects cells that expand
                    if obj.fill in (Fill.Y, Fill.XY): vertical.append(obj)
                
                height += obj.height + obj._margin_y  # Save height
                min_height += obj._height
                if num != last:
                    height += layout.spacing
                    min_height += layout.spacing

            vertical_num = len(vertical)
            free = total_height - height  # Discover available space

            delta = free / vertical_num if vertical_num > 1 else free
            for obj in vertical:  # Distributes space to the cells that require
                obj._height += delta
                if isinstance(obj, Cell) and obj._height < obj._min_height:
                    obj._height = obj._min_height
            
            if layout._height < min_height:
                layout._height = min_height
            
            if layout._scrollable:
                layout._height = layout._base_height
        
        elif layout._orientation == 'HORIZONTAL':
            # Height
            min_height = 0
            for obj in layout._objects:
                mg, pd = obj.margin, obj.padding
                if isinstance(obj, Cell) and not obj.visible: continue

                if obj.fill in (Fill.Y, Fill.XY):
                    obj._height = total_height - obj._margin_y
                    if obj._height < obj._min_height:
                        obj._height = obj._min_height

                if isinstance(obj, Cell) and obj.fill in (Fill.X, Fill.NONE):
                    if layout.base_align == Align.CENTER:
                        dt = (total_height - obj.height) / 2
                        obj.margin = dt, mg[1], dt, mg[3]
                    
                    elif layout.base_align == Align.END:
                        dt = (total_height - obj.height)
                        obj.margin = (dt, mg[1], mg[2], mg[3])
                
                if isinstance(obj, Cell):
                    if min_height < obj.height + obj._margin_y:
                        min_height = obj.height + obj._margin_y

            if layout._height < min_height:
                layout._height = min_height
        
            # Width
            min_width = 0
            horizontal, width, last = [], 0, len(layout._objects) - 1
            for num, obj in enumerate(layout._objects):
                if isinstance(obj, Cell):
                    if not obj.visible: continue

                if obj._width < obj._min_width:
                    obj._width = obj._min_width

                if obj.fill.value in (Fill.NONE, Fill.Y):  # Fixed width
                    obj._width = obj._base_width

                if hasattr(obj, 'fill'):
                    if obj.fill in (Fill.X, Fill.XY): horizontal.append(obj)
                
                width += obj.width + obj._margin_x
                min_width += obj._min_width
                if num != last:
                    width += layout.spacing
                    min_width += layout.spacing
            
            horizontal_num = len(horizontal)
            free = total_width - width
            
            delta = free / horizontal_num if horizontal_num > 1 else free
            for obj in horizontal:
                obj._width += delta
                if isinstance(obj, Cell) and obj._width < obj._min_width:
                    obj._width = obj._min_width
            
            if layout._width < min_width:
                layout._width = min_width

        for obj in layout._objects:
            if isinstance(obj, Layout):
                self._update_fill(obj)
        
        layout._height += layout._padding_y

    def _update_size(self, layout) -> None:
        # Make sure the layout size are compatible with the number 
        # of stacked cells.
        if not layout._objects:
            return
        
        layout._width = layout._base_width
        if layout.fill in (Fill.X, Fill.XY):
            layout._width = 0
            layout._base_width = 0
            
        layout._height = layout._base_height
        if layout.fill in (Fill.Y, Fill.XY):
            layout._height = 0
            layout._base_height = 0
        
        last = len(layout._objects) - 1  # To remove last extra 'spacing'
        for num, obj in enumerate(layout._objects):
            if not obj.visible: continue
            if not obj._dirty: continue

            if isinstance(obj, Layout):
                self._update_size(obj)

            if layout._orientation == 'VERTICAL':  # Set width height
                if layout.fill in (Fill.X, Fill.XY):
                    w = obj._width + obj._margin_x
                    if w > layout.width:
                        layout._width = w
                        layout._base_width = w

                if layout.fill in (Fill.Y, Fill.XY):
                    h = obj._base_height + obj._margin_y
                    if num != last: h += layout.spacing
                    layout._height += h
                    layout._base_height += h

                if layout._scrollable:
                    layout._base_height = layout._scroll._height

            elif layout._orientation == 'HORIZONTAL':
                if layout.fill in (Fill.X, Fill.XY):
                    w = obj._base_width + obj._margin_x
                    if num != last: w += layout.spacing
                    layout._width += w
                    layout._base_width += w
                
                if layout.fill in (Fill.Y, Fill.XY):
                    h = obj._height + obj._margin_y
                    if h > layout.height:
                        layout._height = h
                        layout._base_height = h
