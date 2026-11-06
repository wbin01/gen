#!/usr/bin/env python3
import ctypes

import sdl3
# import sdl3.sdlttf as ttf

from ..control import Signal, Timer
from ..flag import ResizeArea, FrameState
from .frame import Frame


class SysFrame(Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Signal
        self.entered_fullscreen = Signal(self)
        self.exited_fullscreen = Signal(self)
        self.maximized = Signal(self)
        self.minimized = Signal(self)
        self.unmaximized = Signal(self)

        self._canvas_update_timer = Timer(
            call=self._canvas_update_render, single_shot=True, init_delay=0.01)
        self._timers.append(self._canvas_update_timer)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def frame_state(self) -> FrameState:
        """..."""
        flags = sdl3.SDL_GetWindowFlags(self._frame)
        if flags & sdl3.SDL_WINDOW_FULLSCREEN:
            return FrameState.FULL
        if flags & sdl3.SDL_WINDOW_MAXIMIZED:
            return FrameState.MAX
        if flags & sdl3.SDL_WINDOW_MINIMIZED:
            return FrameState.MIN
        if flags & sdl3.SDL_WINDOW_HIDDEN:
            return FrameState.HIDDEN
        return FrameState.FRAME
    
    @frame_state.setter
    def frame_state(self, frame_state: FrameState) -> None:
        if frame_state == self.frame_state:
            return

        flags = sdl3.SDL_GetWindowFlags(self._frame)

        if frame_state != FrameState.FULL and frame_state != FrameState.MIN:
            if flags & sdl3.SDL_WINDOW_FULLSCREEN:
                sdl3.SDL_SetWindowFullscreen(self._frame, False)
                self.exited_fullscreen.emit()

        if frame_state == FrameState.FRAME:    
            sdl3.SDL_RestoreWindow(self._frame)
            self._state = FrameState.FRAME
            self.unmaximized.emit()
        
        elif frame_state == FrameState.FULL:
            sdl3.SDL_SetWindowFullscreen(self._frame, True)
            self._state = FrameState.FULL
            self.entered_fullscreen.emit()
            
        elif frame_state == FrameState.MAX:
            sdl3.SDL_MaximizeWindow(self._frame)
            self._state = FrameState.MAX
            self.maximized.emit()
            
        elif frame_state == FrameState.MIN:
            sdl3.SDL_MinimizeWindow(self._frame)
            self._state = FrameState.MIN
            self.minimized.emit()
    
    def _sync_frame_size(self, frame_state: FrameState = None) -> None:
        sdl3.SDL_SyncWindow(self._frame)
        w = ctypes.c_int()
        h = ctypes.c_int()
        sdl3.SDL_GetWindowSize(self._frame, ctypes.byref(w), ctypes.byref(h))
        self._width, self._height = w.value, h.value
        
        if frame_state != FrameState.MIN:
            self._canvas_update_timer.active = True

    def toggle_maximize(self) -> None:
        """..."""
        flags = sdl3.SDL_GetWindowFlags(self._frame)
        self.frame_state = (FrameState.FRAME
            if flags & sdl3.SDL_WINDOW_MAXIMIZED else FrameState.MAX)
    
    def toggle_fullscreen(self) -> None:
        """..."""
        flags = sdl3.SDL_GetWindowFlags(self._frame)
        self.frame_state = (FrameState.FRAME
            if flags & sdl3.SDL_WINDOW_FULLSCREEN else FrameState.FULL)
    
    def _canvas_update_render(self) -> None:
        """..."""
        self._render_mode = 'RESIZE'
        self._render_update = True
        # sdl3.SDL_GetCurrentDisplayMode(display)
    
    def _cursor_hit_test(self, window, area, data):
        x = area.contents.x
        y = area.contents.y

        w = ctypes.c_int()
        h = ctypes.c_int()
        sdl3.SDL_GetWindowSize(self._frame, ctypes.byref(w), ctypes.byref(h))

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
        frame_x = ctypes.c_int()
        frame_y = ctypes.c_int()
        sdl3.SDL_GetWindowPosition(self._frame, frame_x, frame_y)

        frame_w = ctypes.c_int()
        frame_h = ctypes.c_int()
        sdl3.SDL_GetWindowSize(
            self._frame, ctypes.byref(frame_w), ctypes.byref(frame_h))

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
