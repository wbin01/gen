#!/usr/bin/env python3
from pathlib import Path

from .sys_frame import SysFrame
from ..flag.fill import Fill
from ..flag.frame_state import FrameState
from ..layout.box import Box
from ..layout.col import Col
from ..cell.control_button import ControlButton
from ..cell.drag_area import DragArea
from ..cell.tool_button import ToolButton


PATH = Path(__file__).resolve().parent.parent


class Header(Box):
    def __init__(self, frame, *args, **kwargs) -> None:
        super().__init__(frame=frame, horizontal=True, *args, **kwargs)
        self.fill = Fill.X
        self.padding = 2
        self.margin = 0, 0, 1, 0

        desk_env = 'plasma'
        buttons_path = PATH/'static'/'control_button'
        base = buttons_path/desk_env

        icon_close = base/'window-close-b-symbolic.svg'
        icon_close_hover = base/'window-close-b-hover-symbolic.svg'
        icon_close_clicked = base/'window-close-clicked-symbolic.svg'
        self._close_control = self.add(
            ControlButton(icon_close, icon_close_hover, icon_close_clicked))
        self._close_control.pressed.connect(lambda _: frame.close())

        icon_max = base/'go-up-symbolic.svg'
        icon_max_hover = base/'go-up-hover-symbolic.svg'
        icon_max_clicked = base/'go-up-clicked-symbolic.svg'
        self._max_control = self.add(
            ControlButton(icon_max, icon_max_hover, icon_max_clicked))
        self._max_control.pressed.connect(lambda _: frame.toggle_maximize())
        
        icon_min = base/'go-down-symbolic.svg'
        icon_min_hover = base/'go-down-hover-symbolic.svg'
        icon_min_clicked = base/'go-down-clicked-symbolic.svg'
        self._min_control = self.add(
            ControlButton(icon_min, icon_min_hover, icon_min_clicked))
        self._min_control.pressed.connect(
            lambda _: setattr(frame, 'frame_state', FrameState.MIN))
        
        self.add(DragArea('Title'))
        tb = self.add(ToolButton('document-edit'))


class AppFrame(SysFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.header = self.add(Header(self))
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
