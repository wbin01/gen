#!/usr/bin/env python3
from .layout import Layout
from ..flag import Fill
from ..mix import Add


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
        if self._app and self._app._Frame__debug: self.__draw()

        num_color = -1
        for ui in self._Add__uis:
            if isinstance(ui, Cell) and not ui.visible: continue
            if not ui._UI__dirty: continue

            num_color += 1
            if num_color == 9: num_color = -1

            if isinstance(ui, Layout):
                ui._Box__debug_color_index = num_color
                ui._Box__redraw()
                continue

            getattr(ui, f'_{ui.__class__.__name__}__draw')()
            ui._UI__dirty = False

        self._UI__dirty = False
