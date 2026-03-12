#!/usr/bin/env python3
from .layout import Layout
from ..flag import Fill
from ..mixin import Add


class Pos(Add, Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.margin = 0, 0, 0, 0
        self.width = 0
        self.height = 0
        self.fill = Fill.NONE
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __update(self) -> None:
        pass
    
    def __redraw(self) -> None:
        """..."""
        if self._app and self._app._debug: self.__draw()

        num_color = -1
        for obj in self._objects:
            if isinstance(obj, Cell) and not obj.visible: continue
            if not obj._dirty: continue

            num_color += 1
            if num_color == 9: num_color = -1

            if isinstance(obj, Layout):
                obj._debug_color_index = num_color
                obj._redraw()
                continue

            obj._draw()
            obj._dirty = False

        self._dirty = False
