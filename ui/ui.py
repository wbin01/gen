#!/usr/bin/env python3
from ..flag import State
from ..ui import Signal


class UI(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self._base_class = 'UI'
        self._app = None
        self._parent = None
        self._dirty = True
        self._state = State.BASE
        self._visible = True

        self.enter = Signal()
        self.leave = Signal()
        self.pressed = Signal()
        self.released = Signal()
        self.move = Signal()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def app(self) -> UI:
        return self._app
    
    @property
    def base_class(self) -> bool:
        """..."""
        return self._base_class
    
    @property
    def parent(self) -> UI:
        return self._parent
    
    @property
    def visible(self) -> bool:
        """..."""
        return self._visible
    
    @visible.setter
    def visible(self, visible: bool) -> None:
        self._visible = visible
    
    def _rect_contains(self, ui: UI, x: int, y: int) -> bool:
        ui_x, ui_y = int(ui._x), int(ui._y)
        ui_w, ui_h = int(ui.width), int(ui.height)
        if ui_x <= x.value <= ui_x + ui_w and ui_y <= y.value <= ui_y + ui_h:
            return True
        return False
    
    def _set_state(self, event: str) -> None:
        if event == 'RELEASED':
            self._state = State.HOVER

        elif event == 'HOVER':
            self._state = State.HOVER
        
        elif event == 'PRESSED':
            self._state = State.PRESSED
            self.pressed.emit(self)

        else:  # if event == 'BASE':
            self._state = State.BASE

        self._dirty = 'HOVER'

        def inv(ui):
            if hasattr(ui, '_parent') and ui._parent:
                ui._parent._dirty = 'HOVER'
                inv(ui._parent)
        
        inv(self)
