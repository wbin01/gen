#!/usr/bin/env python3
from ..control import Signal
from ..flag import State
from ..mixin import Core


class UI(Core):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """..."""
        # self._base_class = 'UI'
        # self._app = None
        # self._parent = None
        self._dirty = True
        self._state = State.BASE
        self._visible = True
        self._timer = None

        self.enter = Signal()
        self.leave = Signal()
        self.pressed = Signal()
        self.released = Signal()
        self.right_pressed = Signal()
        self.right_released = Signal()
        self.move = Signal()
        self.drag_start = Signal()
        self.drag_end = Signal()

        self._dragging = False
        self._accept_move = False
        

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def accept_move(self) -> bool:
        """..."""
        return self._accept_move
    
    @accept_move.setter
    def accept_move(self, accept_move: bool) -> None:
        self._accept_move = accept_move
    
    @property
    def visible(self) -> bool:
        """..."""
        return self._visible
    
    @visible.setter
    def visible(self, visible: bool) -> None:
        self._visible = visible
    
    # @property
    # def app(self) -> UI:
    #     return self._app
    
    # @property
    # def base_class(self) -> bool:
    #     """..."""
    #     return self._base_class
    
    @property
    def dragging(self) -> bool:
        """..."""
        return self._dragging
    
    # @property
    # def parent(self) -> UI:
    #     return self._parent
    
    def _rect_contains(self, ui: UI, x: int, y: int) -> bool:
        ui_x, ui_y = int(ui._x), int(ui._y)
        ui_w, ui_h = int(ui.width), int(ui.height)
        if ui_x <= x.value <= ui_x + ui_w and ui_y <= y.value <= ui_y + ui_h:
            return True
        return False
    
    def _set_state(self, event: str) -> None:
        if event == 'ENTER':
            self._state = State.HOVER
            self.enter.emit(self)

        elif 'PRESSED' in event:
            self._state = State.PRESSED
            if event.startswith('RIGHT'):
                self.right_pressed.emit(self)
            else:
                self.pressed.emit(self)
        
        elif 'RELEASED' in event:
            self._state = State.HOVER
            if event.startswith('RIGHT'):
                self.right_released.emit(self)
            else:
                self.released.emit(self)
            
            if self._dragging:
                self._dragging = False
                self.drag_end.emit(self)
                
        elif event == 'MOVE':
            if self._state == State.PRESSED:
                if not self._dragging:
                    self._dragging = True
                    self.drag_start.emit(self)

            if self._accept_move:
                self.move.emit(self)
        
        elif event == 'LEAVE':
            if self._app and self._app._focus != self:
                self._state = State.BASE
            self.leave.emit(self)

        elif event == 'KEY':
            self._state = State.HOVER
        
        else:  # BASE
            self._state = State.BASE

        self._invalidate()

    def _invalidate(self, ui=None):
        if not ui: ui = self
        ui._dirty = True

        if hasattr(ui, '_parent') and ui._parent:
            ui._parent._dirty = 'HOVER'
            self._invalidate(ui._parent)
