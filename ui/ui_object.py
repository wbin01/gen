#!/usr/bin/env python3
from ..control import Signal
from ..flag import State
from ..mixin import Core


class Scroll:
    pass


class UIObject(Core):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        """..."""
        self._dirty = True
        self._state = State.BASE
        self._visible = True
        self._timer = None

        self.enter = Signal(self)
        self.leave = Signal(self)
        self.pressed = Signal(self)
        self.released = Signal(self)
        self.right_pressed = Signal(self)
        self.right_released = Signal(self)
        self.move = Signal(self)
        self.drag_start = Signal(self)
        self.drag_end = Signal(self)

        self._dragging = False
        self._accept_move = False

        self._container = None
        
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
    
    @property
    def dragging(self) -> bool:
        """..."""
        return self._dragging
    
    def _rect_contains(
            self, obj: UIObject, x: int, y: int, scroll: Scroll = None
            ) -> bool:
        obj_x, obj_y = int(obj._x), int(obj._y)
        obj_w, obj_h = int(obj.width), int(obj.height)
        
        if scroll:
            vp_x, vp_y = int(scroll._parent._x), int(scroll._parent._y)
            vp_w, vp_h = int(scroll.width), int(scroll.height)
            vp_y += + int(scroll._parent.padding[0])
        
            if not (vp_x <= x.value <= vp_x + vp_w and
                vp_y <= y.value <= vp_y + vp_h):
                return False
        
        if (obj_x <= x.value <= obj_x + obj_w and
                obj_y <= y.value <= obj_y + obj_h):
            return True
        return False
    
    def _set_state(self, event: str) -> None:
        if self._container:
            self._container._set_state(event)

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

    def _invalidate(self, parent=None) -> None:
        if not parent: parent = self
        parent._dirty = True

        if parent._parent:
            self._invalidate(parent._parent)
