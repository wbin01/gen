#!/usr/bin/env python3
from ctypes import c_int

import sdl3
# import sdl3.sdlttf as ttf

from ..control import Signal
from ..flag import ResizeArea,FrameState
from .frame import Frame


class SysFrame(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Signal
        self.entered_fullscreen = Signal(self)
        self.exited_fullscreen = Signal(self)
        self.maximized = Signal(self)
        self.minimized = Signal(self)
        self.unmaximized = Signal(self)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def exit_fullscreen(self):
        self._state = FrameState.FRAME
        self.exited_fullscreen.emit()
        sdl3.SDL_SetWindowFullscreen(self._frame, False)
    
    def fullscreen(self):
        self._state = FrameState.FULL
        self.entered_fullscreen.emit()
        sdl3.SDL_SetWindowFullscreen(self._frame, True)
    
    def maximize(self):
        self._state = FrameState.MAX
        self.maximized.emit()
        sdl3.SDL_MaximizeWindow(self._frame)
    
    def minimize(self):
        self._state = FrameState.MIN
        self.minimized.emit()
        sdl3.SDL_MinimizeWindow(self._frame)

    def unmaximize(self):
        self._state = FrameState.FRAME
        self.unmaximized.emit()
        sdl3.SDL_RestoreWindow(self._frame)

    def toggle_maximize(self):
        flags = sdl3.SDL_GetWindowFlags(self._frame)

        if flags & sdl3.SDL_WINDOW_MAXIMIZED:
            sdl3.SDL_RestoreWindow(self._frame)
            self._state = FrameState.FRAME
            self.unmaximized.emit()
        else:
            sdl3.SDL_MaximizeWindow(self._frame)
            self._state = FrameState.MAX
            self.maximized.emit()
    
    def toggle_fullscreen(self):
        flags = sdl3.SDL_GetWindowFlags(self._frame)

        if flags & sdl3.SDL_WINDOW_FULLSCREEN:
            sdl3.SDL_SetWindowFullscreen(self._frame, False)
            self._state = FrameState.FRAME
            self.exited_fullscreen.emit()
        else:
            sdl3.SDL_SetWindowFullscreen(self._frame, True)
            self._state = FrameState.FULL
            self.entered_fullscreen.emit()
    
    def _cursor_hit_test(self, window, area, data):
        x = area.contents.x
        y = area.contents.y

        w = c_int()
        h = c_int()
        sdl3.SDL_GetWindowSize(self._frame, w, h)

        border = self._resize_border
        
        if self._resize_wm:
            # Corners
            if x < border and y < border:
                return sdl3.SDL_HITTEST_RESIZE_TOPLEFT
            if x > w.value - border and y < border:
                return sdl3.SDL_HITTEST_RESIZE_TOPRIGHT
            if x < border and y > h.value - border:
                return sdl3.SDL_HITTEST_RESIZE_BOTTOMLEFT
            if x > w.value - border and y > h.value - border:
                return sdl3.SDL_HITTEST_RESIZE_BOTTOMRIGHT

            # Borders
            if y < border:
                return sdl3.SDL_HITTEST_RESIZE_TOP
            if y > h.value - border:
                return sdl3.SDL_HITTEST_RESIZE_BOTTOM
            if x < border:
                return sdl3.SDL_HITTEST_RESIZE_LEFT
            if x > w.value - border:
                return sdl3.SDL_HITTEST_RESIZE_RIGHT
        else:
            # DRAG
            for drag in self._drag_areas:
                delta_top = 5 if drag._y < 3 else 0

                if (drag._x + 4 < x < drag._x + drag.width - 4 and
                        drag._y + delta_top < y < drag._y + drag.height):
                    return sdl3.SDL_HITTEST_DRAGGABLE
            return sdl3.SDL_HITTEST_NORMAL
    
    def _cursor_resize_area(self, cursor_x, cursor_y) -> ResizeArea:
        # cursor_x = c_float()
        # cursor_y = c_float()
        # sdl3.SDL_GetGlobalMouseState(cursor_x, cursor_y)
        frame_x = c_int()
        frame_y = c_int()
        sdl3.SDL_GetWindowPosition(self._frame, frame_x, frame_y)

        frame_w = c_int()
        frame_h = c_int()
        sdl3.SDL_GetWindowSize(self._frame, frame_w, frame_h)

        x = cursor_x.value - frame_x.value
        y = cursor_y.value - frame_y.value
        w = frame_w.value
        h = frame_h.value

        left = x < self._resize_border
        right = x > w - self._resize_border
        top = y < self._resize_border
        bottom = y > h - self._resize_border

        if top and left:
            return ResizeArea.TOP_LEFT
        if top and right:
            return ResizeArea.TOP_RIGHT
        if bottom and left:
            return ResizeArea.BOTTOM_LEFT
        if bottom and right:
            return ResizeArea.BOTTOM_RIGHT
        if top:
            return ResizeArea.TOP
        if bottom:
            return ResizeArea.BOTTOM
        if left:
            return ResizeArea.LEFT
        if right:
            return ResizeArea.RIGHT

        return ResizeArea.NONE
