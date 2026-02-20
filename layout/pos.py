#!/usr/bin/env python3
from .layout import Layout
from ..flag.fill import Fill

class Pos(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.margin = 0, 0, 0, 0
        self.width = 0
        self.height = 0
        self.fill = Fill.NONE
        self._Layout__orientation = 'POSITION'
    
    def add(self, ui: UI, x: int = None, y: int = None) -> UI:
        """..."""
        ui = self._Layout__add(ui)
        if x is not None: ui.x = x
        if y is not None: ui.y = y
        return ui
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
