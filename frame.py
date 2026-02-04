#!/usr/bin/env python3
import sys
from ctypes import c_float, c_int

import sdl3

from .core import Draw
from .flag import ResizeArea


class Frame(object):
    """..."""
    def __init__(self) -> None:
        # Init
        if sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO) < 0: # X SDL_INIT_EVERYTHING
            print('SDL3 init error:', sdl3.SDL_GetError())
            sys.exit(1) # X SDL_SetHint(sdl3.SDL_HINT_RENDER_DRIVER, b'vulkan')

        # Frame
        self.__frame = sdl3.SDL_CreateWindow(
            b'Transparente Frame - SDL3 + PySDL3', 640, 480,
            (sdl3.SDL_WINDOW_BORDERLESS | sdl3.SDL_WINDOW_TRANSPARENT))

        if not self.__frame:
            print('Frame creation error:', sdl3.SDL_GetError())
            sdl3.SDL_Quit()
            sys.exit(1)

        sdl3.SDL_SetWindowOpacity(self.__frame, 0.80)

        # Renderer Draw
        self.__renderer = sdl3.SDL_CreateRenderer(self.__frame, None)

        if not self.__renderer:
            print('Renderer creation error:', sdl3.SDL_GetError())
            sdl3.SDL_DestroyWindow(self.__frame)
            sdl3.SDL_Quit()
            sys.exit(1)

        sdl3.SDL_SetRenderVSync(self.__renderer, 1)  # Opt 1=on 0=off -1=adapt
        self.__draw = Draw(self.__renderer)

        # Control Frame
        self.__running = True

        # Control Frame - Drag 
        self.__dragging = False
        self.__drag_offset_x = 0
        self.__drag_offset_y = 0

        # Control Frame - resize
        self.__resizing = False
        self.__resize_area = ResizeArea.NONE
        self.__resize_border = 8

        # Control Cursor
        self.__cursor = {
            'TOP': sdl3.SDL_CreateSystemCursor(8),
            'BOTTOM': sdl3.SDL_CreateSystemCursor(8),
            'LEFT': sdl3.SDL_CreateSystemCursor(7),
            'RIGHT': sdl3.SDL_CreateSystemCursor(7),
            'TOPLEFT': sdl3.SDL_CreateSystemCursor(5),
            'BOTTOMRIGHT': sdl3.SDL_CreateSystemCursor(5),
            'TOPRIGHT': sdl3.SDL_CreateSystemCursor(6),
            'BOTTOMLEFT': sdl3.SDL_CreateSystemCursor(6),
            'NONE': sdl3.SDL_CreateSystemCursor(0),
            'DRAG': sdl3.SDL_CreateSystemCursor(9),
        }
        self.__last_resize_cursor_on_hover = 'NONE'
        
    def run(self) -> int:
        self.__event_loop()
        self.__destroy()
        return 0
    
    def __cursor_find_resize_area(self) -> ResizeArea:
        mx = c_float()
        my = c_float()
        sdl3.SDL_GetGlobalMouseState(mx, my)

        wx = c_int()
        wy = c_int()
        sdl3.SDL_GetWindowPosition(self.__frame, wx, wy)

        ww = c_int()
        wh = c_int()
        sdl3.SDL_GetWindowSize(self.__frame, ww, wh)

        x = mx.value - wx.value
        y = my.value - wy.value

        b = self.__resize_border
        w = ww.value
        h = wh.value

        left   = x < b
        right  = x > w - b
        top    = y < b
        bottom = y > h - b

        if top and left:
            return ResizeArea.TOPLEFT
        if top and right:
            return ResizeArea.TOPRIGHT
        if bottom and left:
            return ResizeArea.BOTTOMLEFT
        if bottom and right:
            return ResizeArea.BOTTOMRIGHT
        if top:
            return ResizeArea.TOP
        if bottom:
            return ResizeArea.BOTTOM
        if left:
            return ResizeArea.LEFT
        if right:
            return ResizeArea.RIGHT

        return ResizeArea.NONE
    
    def __cursor_update_shape(self, cursor_name: str) -> None:
        if self.__resizing or self.__dragging:
            return

        sdl3.SDL_SetCursor(self.__cursor[cursor_name])
    
    def __destroy(self):
        for c in self.__cursor.values():
            sdl3.SDL_DestroyCursor(c)

        sdl3.SDL_DestroyRenderer(self.__renderer)
        sdl3.SDL_DestroyWindow(self.__frame)
        sdl3.SDL_Quit()

    def __event_loop(self) -> None:
        while self.__running:
            event = sdl3.SDL_Event()

            while sdl3.SDL_PollEvent(event):
                resize_area = self.__cursor_find_resize_area()

                if resize_area.value != self.__last_resize_cursor_on_hover:
                    self.__cursor_update_shape(resize_area.value)
                    self.__last_resize_cursor_on_hover = resize_area.value

                if event.type == sdl3.SDL_EVENT_QUIT:
                    self.__running = False
                
                if event.type == sdl3.SDL_EVENT_KEY_DOWN:
                    if event.key.keysym.sym == sdl3.SDLK_ESCAPE:
                        self.__running = False
                
                if event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_DOWN:
                    if event.button.button == sdl3.SDL_BUTTON_LEFT:
                        self.__resize_area = self.__cursor_find_resize_area()
                        if self.__resize_area != ResizeArea.NONE:
                            self.__cursor_update_shape(self.__resize_area.value)
                            self.__frame_update_resize_settings()
                        else:
                            self.__cursor_update_shape('DRAG')
                            self.__frame_update_drag_settings()

                elif event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_UP:
                    if event.button.button == sdl3.SDL_BUTTON_LEFT:
                        self.__frame_stop_resize()
                        self.__frame_stop_drag()

                elif event.type == sdl3.SDL_EVENT_MOUSE_MOTION:
                    if self.__resize_area != ResizeArea.NONE:
                        self.__frame_start_resize()
                    elif self.__dragging:
                        self.__frame_start_drag()

            # Draw background Frame
            sdl3.SDL_SetRenderDrawColor(self.__renderer, 0, 0, 0, 0)
            sdl3.SDL_RenderClear(self.__renderer)

            w = c_int()
            h = c_int()
            sdl3.SDL_GetWindowSize(self.__frame, w, h)
            self.__draw.rect(0, 0, w.value, h.value, (55, 55, 55, 255), 8) # 40
            self.__draw.rect(
                1, 1, w.value - 2, h.value - 2, (20, 20, 20, 255), 8)  # 30

            sdl3.SDL_RenderPresent(self.__renderer)
            sdl3.SDL_Delay(10)
    
    def __frame_start_drag(self) -> None:        
        if hasattr(sdl3, 'SDL_StartWindowMove'):
            sdl3.SDL_StartWindowMove(self.__frame)
        else:
            mx = c_float()
            my = c_float()
            sdl3.SDL_GetGlobalMouseState(mx, my)

            new_x = int(mx.value - self.__drag_offset_x)
            new_y = int(my.value - self.__drag_offset_y)

            sdl3.SDL_SetWindowPosition(self.__frame, new_x, new_y)
    
    def __frame_start_resize(self) -> None:
        if not self.__resizing:
            return

        mx = c_float()
        my = c_float()
        sdl3.SDL_GetGlobalMouseState(mx, my)

        dx = mx.value - self.__start_mx.value
        dy = my.value - self.__start_my.value

        x = self.__start_x.value
        y = self.__start_y.value
        w = self.__start_w.value
        h = self.__start_h.value

        r = self.__resize_area.value

        if r in ('RIGHT', 'TOPRIGHT', 'BOTTOMRIGHT'):
            w += dx
        if r in ('LEFT', 'TOPLEFT', 'BOTTOMLEFT'):
            x += dx
            w -= dx
        if r in ('BOTTOM', 'BOTTOMLEFT', 'BOTTOMRIGHT'):
            h += dy
        if r in ('TOP', 'TOPLEFT', 'TOPRIGHT'):
            y += dy
            h -= dy

        w = max(100, int(w))
        h = max(100, int(h))

        sdl3.SDL_SetWindowPosition(self.__frame, int(x), int(y))
        sdl3.SDL_SetWindowSize(self.__frame, w, h)
    
    def __frame_stop_drag(self) -> None:
        self.__dragging = False
        self.__cursor_update_shape('NONE')
    
    def __frame_stop_resize(self) -> None:
        self.__resizing = False
        self.__resize_area = ResizeArea.NONE
        self.__cursor_update_shape('NONE')
    
    def __frame_update_drag_settings(self) -> None:
        self.__dragging = True

        mx = c_float()
        my = c_float()
        sdl3.SDL_GetGlobalMouseState(mx, my)

        wx = c_int()
        wy = c_int()
        sdl3.SDL_GetWindowPosition(self.__frame, wx, wy)

        self.__drag_offset_x = mx.value - wx.value
        self.__drag_offset_y = my.value - wy.value
    
    def __frame_update_resize_settings(self) -> None:
        self.__resizing = True

        self.__start_mx = c_float()
        self.__start_my = c_float()
        sdl3.SDL_GetGlobalMouseState(self.__start_mx, self.__start_my)

        self.__start_x = c_int()
        self.__start_y = c_int()
        sdl3.SDL_GetWindowPosition(self.__frame, self.__start_x, self.__start_y)

        self.__start_w = c_int()
        self.__start_h = c_int()
        sdl3.SDL_GetWindowSize(self.__frame, self.__start_w, self.__start_h)


if __name__ == "__main__":
    app = Frame()
    sys.exit(app.run())

# SDL_RENDERER_DRIVER=vulkan python -O main.py
# SDL_VIDEODRIVER=x11 SDL_RENDERER_DRIVER=vulkan python -O frame.py
