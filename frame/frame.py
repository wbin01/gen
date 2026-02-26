#!/usr/bin/env python3
import sys
from ctypes import c_float, c_int

import sdl3
# import sdl3.sdlttf as ttf

from ..flag import ResizeArea, Cursor
from ..layout import Col
from ..ui import UI, Drawer, Theme


class Frame(UI):
    """..."""
    __theme = Theme

    def __init__(
            self, title: str,
            x: int = 0, y: int = 0, width: int = 500, height: int = 300,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__title = title
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height
        self.__logging = False
        self.__log = None
        self.__view_layout = False
        self.cached_rendering = True
        self.texture = False
        if self.__view_layout: self.texture = False

        sdl3.SDL_SetHint(
            sdl3.SDL_HINT_X11_WINDOW_TYPE, b'_NET_WM_WINDOW_TYPE_NORMAL')
        # Init
        if sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO) < 0: # X SDL_INIT_EVERYTHING
            print('SDL3 init error:', sdl3.SDL_GetError())
            sys.exit(1) # X SDL_SetHint(sdl3.SDL_HINT_RENDER_DRIVER, b'vulkan')

        # Frame
        self.__frame = sdl3.SDL_CreateWindow(
            self.__title.encode('utf-8'), self.__width, self.__height, (
                sdl3.SDL_WINDOW_BORDERLESS |   # SDL_WINDOW_TOOLTIP
                sdl3.SDL_WINDOW_TRANSPARENT |  # SDL_WINDOW_POPUP
                sdl3.SDL_WINDOW_RESIZABLE))    # SDL_WINDOW_UTILITY

        if not self.__frame:
            print('Frame error:', sdl3.SDL_GetError())
            sdl3.SDL_Quit()
            sys.exit(1)

        sdl3.SDL_SetWindowOpacity(self.__frame, 1.0)

        # Style
        self.__renderer = sdl3.SDL_CreateRenderer(self.__frame, None)
        if not self.__renderer:
            print('Renderer error:', sdl3.SDL_GetError())
            sdl3.SDL_DestroyWindow(self.__frame)
            sdl3.SDL_Quit()
            sys.exit(1)
        
        sdl3.SDL_SetRenderVSync(self.__renderer, 1)  # Opt 1=on 0=off -1=adapt

        self.__drawer = Drawer(self.__renderer)
        self.__style = self._Frame__theme

        # Container
        self.__container = Col()
        self.__container._Box__first = True
        self.__container._UI__parent = self
        self.__container._UI__app = self
        self.__container._Box__drawer = self.__drawer

        # Control Frame
        self.__running = True
        self.__render_update_mode = 'RESIZE'
        self.__render_needs_updating = True
        self.__render_count = 0
        self.__frame_texture = None
        self.__frame_background = None

        # Control Frame - Drag
        self.__dragging = False
        self.__dragging_count = 0
        self.__drag_offset_x = 0
        self.__drag_offset_y = 0

        # Control Frame - resize
        self.__resizing = False
        self.__resizing_end = 3
        self.__resizing_first = True
        self.__resize_area = ResizeArea.NONE
        self.__resize_border = 8

        # Control Cursor
        self.__cursor = {
            'TOP': sdl3.SDL_CreateSystemCursor(8),
            'BOTTOM': sdl3.SDL_CreateSystemCursor(8),
            'LEFT': sdl3.SDL_CreateSystemCursor(7),
            'RIGHT': sdl3.SDL_CreateSystemCursor(7),
            'TOP_LEFT': sdl3.SDL_CreateSystemCursor(5),
            'BOTTOM_RIGHT': sdl3.SDL_CreateSystemCursor(5),
            'TOP_RIGHT': sdl3.SDL_CreateSystemCursor(6),
            'BOTTOM_LEFT': sdl3.SDL_CreateSystemCursor(6),
            'NONE': sdl3.SDL_CreateSystemCursor(0),
            'DRAG': sdl3.SDL_CreateSystemCursor(9),
        }
        self.__last_resize_cursor_on_hover = 'NONE'
        self.__hovered_ui = self.__container
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def view_layout(self) -> bool:
        """..."""
        return self.__view_layout
    
    @view_layout.setter
    def view_layout(self, view_layout: bool) -> None:
        self.__view_layout = view_layout
    
    @property
    def height(self) -> int:
        """..."""
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height = height
        sdl3.SDL_SetWindowSize(self.__frame, self.__width, self.__height)
    
    @property
    def spacing(self) -> int:
        """..."""
        return self.__spacing
    
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self.__container.spacing = spacing
    
    @property
    def width(self) -> int:
        """..."""
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width
        sdl3.SDL_SetWindowSize(self.__frame, self.__width, self.__height)
    
    @property
    def x(self) -> int:
        """..."""
        return self.__x
    
    @x.setter
    def x(self, x: int) -> None:
        self.__x = int(x)
        sdl3.SDL_SetWindowPosition(self.__frame, self.__x, self.__y)
    
    @property
    def y(self) -> int:
        """..."""
        return self.__y
    
    @y.setter
    def y(self, y: int) -> None:
        self.__y = int(y)
        sdl3.SDL_SetWindowPosition(self.__frame, self.__x, self.__y)
    
    def add(self, cell: Cell | Box, fill=None) -> Cell | Box:
        name = f'_{cell.__class__.__name__}'
        setattr(cell, name + '__drawer', self.__drawer)

        return self.__container.add(cell)
        
    def run(self) -> int:
        if self.cached_rendering:
            if self.texture:
                wx = c_int()
                wy = c_int()
                sdl3.SDL_GetWindowPosition(self.__frame, wx, wy)
                self.__frame_texture = self.__drawer.screen_texture(
                    wx.value, wy.value, self.width, self.height,
                    self.__style.frame['NORMAL']['radius'])
        
            self.__frame_build_background()
        else:
            self.__draw()
        
        self.__event_loop()
        self.__destroy()
        return 0
    
    def __cursor_resize_area(self, mouse_x, mouse_y) -> ResizeArea:
        # mx = c_float()
        # my = c_float()
        # sdl3.SDL_GetGlobalMouseState(mx, my)
        mx = mouse_x
        my = mouse_y

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
    
    def __cursor_update_shape(self, cursor_name: str) -> None:
        if self.__resizing or self.__dragging:
            return

        sdl3.SDL_SetCursor(self.__cursor[cursor_name])
    
    def __destroy(self):
        for c in self.__cursor.values():
            sdl3.SDL_DestroyCursor(c)

        sdl3.SDL_DestroyRenderer(self.__renderer)
        sdl3.SDL_DestroyWindow(self.__frame)
        # sdl3.SDL_DestroySurface(self.__font_surface)
        sdl3.SDL_Quit()
    
    def __draw(self) -> None:
        sdl3.SDL_SetRenderDrawColor(self.__renderer, 0, 0, 0, 0)
        sdl3.SDL_RenderClear(self.__renderer)

        w = c_int()
        h = c_int()
        sdl3.SDL_GetWindowSize(self.__frame, w, h)
        self.__drawer.rect(
            x=0, y=0, w=w.value, h=h.value,
            color=self.__style.frame['NORMAL']['border'], r=8)
        
        self.__drawer.rect(
            x=1, y=1, w=w.value - 2, h=h.value - 2,
            color=self.__style.frame['NORMAL']['background'], r=8)

    def __event_loop(self) -> None:
        while self.__running:
            event = sdl3.SDL_Event()
            
            mouse_x = c_float()
            mouse_y = c_float()
            sdl3.SDL_GetGlobalMouseState(mouse_x, mouse_y)
            resize_area = self.__cursor_resize_area(mouse_x, mouse_y)

            mx = c_float()
            my = c_float()
            sdl3.SDL_GetMouseState(mx, my)

            while sdl3.SDL_PollEvent(event):
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
                        self.__resize_area = resize_area
                        if self.__resize_area != ResizeArea.NONE:
                            self.__cursor_update_shape(self.__resize_area.value)
                            self.__frame_update_resize_settings()
                        else:
                            self.__cursor_update_shape('DRAG')
                            self.__frame_update_drag_settings()

                elif event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_UP:
                    if event.button.button == sdl3.SDL_BUTTON_LEFT:
                        if self.__dragging:
                            self.__frame_stop_drag()
                        else:
                            self.__frame_stop_resize()

                elif event.type == sdl3.SDL_EVENT_MOUSE_MOTION:
                    if self.__resize_area != ResizeArea.NONE:
                        self.__frame_start_resize()
                    elif self.__dragging:
                        self.__frame_start_drag()

                    if resize_area == ResizeArea.NONE:
                        hovered = self.__container._Layout__hit_test(mx, my)
                        if hovered and hovered != self.__hovered_ui:
                            self.__hovered_ui._UI__set_state('NORMAL')
                            self.__hovered_ui = hovered
                            self.__hovered_ui._UI__set_state('HOVER')

                            self.__render_update_mode = 'HOVER'
                            self.__render_needs_updating = True

                    if resize_area != ResizeArea.NONE:
                        self.__hovered_ui._UI__set_state('NORMAL')
                        self.__render_update_mode = 'HOVER'
                        self.__render_needs_updating = True
                
                if self.__logging and self.__log:
                    print(self.__log, self.__render_count)

            if self.__render_needs_updating:
                if self.cached_rendering:
                    if self.__resizing:
                        self.__render_fast()
                    else:
                        self.__render_fast()
                else:
                    self.__render_base()
                                
                self.__render_count += 1
    
    def __frame_build_background(self) -> None:
        width = c_int()
        height = c_int()
        sdl3.SDL_GetWindowSize(self.__frame, width, height)

        texture = sdl3.SDL_CreateTexture(
            self.__renderer,
            sdl3.SDL_PIXELFORMAT_RGBA8888,
            sdl3.SDL_TEXTUREACCESS_TARGET,
            width.value, height.value)

        old_target = sdl3.SDL_GetRenderTarget(self.__renderer)
        sdl3.SDL_SetRenderTarget(self.__renderer, texture)

        sdl3.SDL_SetRenderDrawColor(self.__renderer, 0, 0, 0, 0)
        sdl3.SDL_RenderClear(self.__renderer)

        self.__drawer.rect(
            x=0, y=0, w=width.value, h=height.value,
            color=self.__style.frame['NORMAL']['border'], r=8)

        self.__drawer.rect(
            x=1, y=1, w=width.value - 2, h=height.value - 2,
            color=self.__style.frame['NORMAL']['background'], r=8)

        if self.__container._Add__uis:
            self.__container._Box__update()
            self.__container._Layout__redraw(rebuild=True)

        sdl3.SDL_SetRenderTarget(self.__renderer, old_target)
        self.__frame_background = texture
    
    def __frame_rebuild_background(self) -> None:
        if not self.__resizing and self.__resizing_end:
            self.__container._Layout__invalidate()
            self.__frame_build_background()

    def __frame_rebuild_texture(self) -> None:
        self.__container._Layout__invalidate()
        wx = c_int()
        wy = c_int()
        sdl3.SDL_GetWindowPosition(self.__frame, wx, wy)
        self.__frame_texture = self.__drawer.screen_texture(
            wx.value, wy.value, self.width, self.height,
            self.__style.frame['NORMAL']['radius'])
    
    def __frame_start_drag(self) -> None:
        if self.texture and self.__dragging_count == 0:
            self.__frame_update('BACKGROUND')
            self.__dragging_count += 1
        
        if hasattr(sdl3, 'SDL_StartWindowMove'):
            sdl3.SDL_StartWindowMove(self.__frame)
        else:
            mx = c_float()
            my = c_float()
            sdl3.SDL_GetGlobalMouseState(mx, my)

            new_x = int(mx.value - self.__drag_offset_x)
            new_y = int(my.value - self.__drag_offset_y)

            sdl3.SDL_SetWindowPosition(self.__frame, new_x, new_y)
            self.x = new_x
            self.y = new_y
        
        self.__log = f'MOVING: {new_x}x{new_y}'

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

        if r in ('RIGHT', 'TOP_RIGHT', 'BOTTOM_RIGHT'):
            w += dx
        if r in ('LEFT', 'TOP_LEFT', 'BOTTOM_LEFT'):
            x += dx
            w -= dx
        if r in ('BOTTOM', 'BOTTOM_LEFT', 'BOTTOM_RIGHT'):
            h += dy
        if r in ('TOP', 'TOP_LEFT', 'TOP_RIGHT'):
            y += dy
            h -= dy

        w = max(100, int(w))
        h = max(100, int(h))

        sdl3.SDL_SetWindowPosition(self.__frame, int(x), int(y))
        sdl3.SDL_SetWindowSize(self.__frame, w, h)
        self.width = w
        self.height = h
        self.x = x
        self.y = y

        self.__render_needs_updating = True
        self.__log = f'RESIZING: {w}x{h}'
    
    def __frame_stop_drag(self) -> None:
        if self.texture:
            self.__frame_rebuild_texture()
            self.__frame_update('TEXTURE')
            self.__dragging_count = 0
            self.__render_needs_updating = True
        
        self.__dragging = False
        self.__cursor_update_shape('NONE')
        self.__log = None
    
    def __frame_stop_resize(self) -> None:
        self.__resize_area = ResizeArea.NONE
        self.__cursor_update_shape('NONE')
        self.__resizing = False
        self.__resizing_end = 3
        self.__render_needs_updating = True
        self.__log = None
    
    def __frame_update(self, mode: str = 'TEXTURE') -> None:
        sdl3.SDL_SetRenderDrawColor(self.__renderer, 0,0,0,0)
        sdl3.SDL_RenderClear(self.__renderer)
        
        if mode == 'TEXTURE' and self.texture:
            if self.__frame_texture and self.__dragging_count == 0:
                dst = sdl3.SDL_FRect(0, 0, self.width, self.height)
                sdl3.SDL_RenderTexture(
                    self.__renderer, self.__frame_texture, None, dst)
        
        sdl3.SDL_RenderTexture(
            self.__renderer, self.__frame_background, None, None)

        if mode == 'TEXTURE' and not self.__resizing:
            self.__container._Box__update()
            self.__container._Layout__redraw()

        sdl3.SDL_RenderPresent(self.__renderer)
        sdl3.SDL_Delay(10)
    
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
    
    def __render_base(self) -> None:
        self.__render_needs_updating = False
        self.__render_count += 1

        if self.__render_update_mode == 'RESIZE':
            if self.__resizing or self.__resizing_end <= 3:
                if not self.__resizing and not self.__resizing_first:
                    if self.__resizing_end > 2:
                        self.__resizing_end -= 1
                        self.__render_needs_updating = True
                    
                    if self.__resizing_end < 2:
                        self.__resizing_end = 3
                
                if self.__resizing_first:
                    self.__resizing_first = False
        
        self.__container._Layout__invalidate()
        self.__draw()

        if self.__container._Add__uis and self.__container._UI__dirty:
            self.__container._Box__update()
            self.__container._Layout__redraw()

        sdl3.SDL_RenderPresent(self.__renderer)
        sdl3.SDL_Delay(10)
    
    def __render_fast(self) -> None:
        self.__render_needs_updating = False
        self.__render_count += 1

        if self.__render_update_mode == 'RESIZE':
            if self.__resizing or self.__resizing_end <= 3:
                if not self.__resizing and not self.__resizing_first:
                    if self.__resizing_end > 2:
                        self.__resizing_end -= 1
                        self.__render_needs_updating = True
                    
                    if self.__resizing_end < 2:
                        self.__resizing_end = 3
                
                if self.__resizing_first:
                    self.__resizing_first = False
                self.__frame_rebuild_background()

        self.__render_update_mode = 'RESIZE'
        self.__frame_update()


if __name__ == "__main__":
    app = Frame()
    sys.exit(app.run())

# SDL_RENDERER_DRIVER=vulkan python -O main.py
# SDL_VIDEODRIVER=x11 SDL_RENDERER_DRIVER=vulkan python -O frame.py
