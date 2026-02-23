#!/usr/bin/env python3
from ..flag import State


class UI(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__app = None
        self.__parent = None
        self.__dirty = True
        self.__state = State.NORMAL
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
        ui_x = int(ui._x)
        ui_y = int(ui._y)
        ui_w = int(ui.width)
        ui_h = int(ui.height)
        if ui_x <= x.value <= (ui_x + ui_w) and ui_y <= y.value <= (ui_y + ui_h):
            # print(ui_x, 'a', ui_x + ui_w, '|', ui_y, 'a', ui_y + ui_h, ui, ui_x, 'x', ui_y)
            return True

        return False
    
    def __set_state(self, state: State | str) -> None:
        if state == 'RELEASED':
            if self.__state == State.PRESSED:
                self.__state = State.HOVER
                # self.emit_click()
                # self.emit_released()
        
        elif self.__state != state:
            self.__state = state
        
        self._UI__dirty = True
