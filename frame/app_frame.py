#!/usr/bin/env python3
from .sys_frame import SysFrame
from ..flag.fill import Fill
from ..flag.frame_state import FrameState
from ..layout.box import Box
from ..cell.control_button import ControlButton
from ..cell.drag_area import DragArea
from ..cell.tool_button import ToolButton


class Header(Box):
    def __init__(self, frame, *args, **kwargs):
        super().__init__(frame=frame, horizontal=True, *args, **kwargs)
        self.fill = Fill.X
        base = '/home/user/Dev/github/gen/static/control_button/plasma/'

        self._close_control = self.add(ControlButton(
            base + 'window-close-b-symbolic.svg',
            base + 'window-close-b-hover-symbolic.svg',
            base + 'window-close-clicked-symbolic.svg'))
        self._close_control.pressed.connect(lambda x: frame.close())

        self._max_control = self.add(ControlButton(
            base + 'go-up-symbolic.svg',
            base + 'go-up-hover-symbolic.svg',
            base + 'go-up-clicked-symbolic.svg'))
        self._max_control.pressed.connect(lambda x: frame.toggle_maximize())
        
        self._min_control = self.add(ControlButton(
            base + 'go-down-symbolic.svg',
            base + 'go-down-hover-symbolic.svg',
            base + 'go-down-clicked-symbolic.svg'))
        # self._min_control.pressed.connect(lambda x: frame.minimize())
        def minimize():
            frame.frame_state = FrameState.MIN
        self._min_control.pressed.connect(lambda x: minimize())
        
        self.add(DragArea('Title'))
        
        self.add(ToolButton('document-edit'))


class AppFrame(SysFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header = self.add(Header(self))
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
