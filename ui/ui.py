#!/usr/bin/env python3
from ..flag import State


class UI(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__base_class = 'UI'
        self.__app = None
        self.__parent = None
        self.__dirty = True
        self.__state = State.DEFAULT
        self.__visible = True
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def visible(self) -> bool:
        """..."""
        return self.__visible
    
    @visible.setter
    def visible(self, visible: bool) -> None:
        self.__visible = visible
    
    @property
    def _app(self) -> UI:
        return self.__app
    
    @property
    def _parent(self) -> UI:
        return self.__parent
    
    def __rect_contains(self, ui: UI, x: int, y: int) -> bool:
        ui_x, ui_y = int(ui._x), int(ui._y)
        ui_w, ui_h = int(ui.width), int(ui.height)
        if ui_x <= x.value <= ui_x + ui_w and ui_y <= y.value <= ui_y + ui_h:
            return True
        return False
    
    def __set_state(self, event: str) -> None:
        if event == 'RELEASED':
            self.__state = State.HOVER
            # self.__click_signal.emit()
            # self.__released_signal.emit()

        elif event == 'HOVER':
            self.__state = State.HOVER
            # self.__hover_signal.emit()
        
        elif event == 'PRESSED':
            self.__state = State.PRESSED
            # self.__pressed_signal.emit()

        else:  # if event == 'DEFAULT':
            self.__state = State.DEFAULT
            # self.__leave_signal.emit()

        self._UI__dirty = 'HOVER'

        def inv(ui):
            if hasattr(ui, '_parent') and ui._parent:
                ui._parent._UI__dirty = 'HOVER'
                inv(ui._parent)
        
        inv(self)
