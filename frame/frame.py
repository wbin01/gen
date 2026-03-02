#!/usr/bin/env python3
import time
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
        self.__view_layout = False

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
                # SDL_WINDOW_OPENGL

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
        self.__queue_list = []

        # Control Frame
        self.__running = True
        self.__render_mode = 'BASE'
        self.__render_needs_updating = True
        self.__render_count = 0
        self.__frame_base_texture = None
        self.__frame_texture = None

        # Control Frame - resize
        self.__resizing = False
        self.__resizing_count = 0
        self.__resize_area = ResizeArea.NONE
        self.__resize_border = 8
        self.__resize_wm = False

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

        self.__cursor_hit = sdl3.SDL_HitTest(self.__cursor_hit_test)
        sdl3.SDL_SetWindowHitTest(self.__frame, self.__cursor_hit, None)
    
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
        self.__draw('FRAME_BASE')
        self.__draw('FRAME')
        
        self.__event_loop()
        self.__destroy()
        return 0
    
    def __cursor_hit_test(self, window, area, data):
        x = area.contents.x
        y = area.contents.y
        border = self.__resize_border

        if self.__resize_wm:
            w = c_int()
            h = c_int()
            sdl3.SDL_GetWindowSize(self.__frame, w, h)

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

        # DRAG
        if border < y < 40:
            return sdl3.SDL_HITTEST_DRAGGABLE

        return sdl3.SDL_HITTEST_NORMAL
    
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
        if self.__resizing:
            return

        sdl3.SDL_SetCursor(self.__cursor[cursor_name])
    
    def __destroy(self):
        for c in self.__cursor.values():
            sdl3.SDL_DestroyCursor(c)

        sdl3.SDL_DestroyRenderer(self.__renderer)
        sdl3.SDL_DestroyWindow(self.__frame)
        # sdl3.SDL_DestroySurface(self.__font_surface)
        sdl3.SDL_Quit()
    
    def __draw(self, mode: str = 'FRAME') -> None:
        w = h = c_int()
        sdl3.SDL_GetWindowSize(self.__frame, w, h)

        if mode == 'FRAME':
            self.__frame_texture = self.__drawer.build_texture(
                self.width, self.height, self.__draw_ui, mode)
        
        elif mode == 'FRAME_BASE':
            self.__frame_base_texture = self.__drawer.build_texture(
                self.width, self.height, self.__draw_ui, mode)

    def __draw_ui(self, mode) -> None:
        self.__drawer.rect(
            x=0, y=0, w=self.width, h=self.height,
            color=self.__style.Frame['BASE']['border-color'],
            r=self.__style.Frame['BASE']['radius'])

        self.__drawer.rect(
            x=1, y=1, w=self.width - 2, h=self.height - 2,
            color=self.__style.Frame['BASE']['background-color'],
            r=self.__style.Frame['BASE']['radius'])

        if mode == 'FRAME':
            if self.__container._Add__uis:
                self.__container._Layout__invalidate()
                self.__container._Box__update()
                self.__container._Layout__redraw('REBUILD')

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
                            if self.__resize_wm:
                                sdl3.SDL_SetWindowHitTest(
                                    self.__frame, self.__cursor_hit, None)
                            else:
                                self.__resize_settings()
                        else:
                            ui = self.__container._Layout__hit_test(mx, my)
                            if ui:
                                ui._UI__set_state('PRESSED')
                                self.__render_mode = 'PRESSED'
                                self.__render_needs_updating = True
                            else:
                                sdl3.SDL_SetWindowHitTest(
                                    self.__frame, self.__cursor_hit, None)

                elif event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_UP:
                    if event.button.button == sdl3.SDL_BUTTON_LEFT:
                        if self.__resizing:
                            self.__resize_stop()
                            self.__render_mode = 'RESIZE'
                            self.__render_needs_updating = True
                        else:
                            ui = self.__container._Layout__hit_test(mx, my)
                            if ui:
                                ui._UI__set_state('RELEASED')
                                self.__render_mode = 'HOVER'
                                self.__render_needs_updating = True

                elif event.type == sdl3.SDL_EVENT_MOUSE_MOTION:
                    if not self.__resize_wm:
                        if self.__resize_area != ResizeArea.NONE:
                            self.__render_mode = 'RESIZE'
                            self.__render_needs_updating = True
                            self.__resize_start()

                        if resize_area == ResizeArea.NONE:
                            hv = None
                            if not self.__resizing:
                                hv = self.__container._Layout__hit_test(mx, my)
                            
                            if hv and hv != self.__hovered_ui:
                                self.__hovered_ui._UI__set_state('BASE')
                                self.__hovered_ui = hv
                                self.__hovered_ui._UI__set_state('HOVER')

                                self.__render_mode = 'HOVER'
                                self.__render_needs_updating = True

            if self.__queue_list:  # print('Queue:', len(self.__queue_list))
                self.__container._Layout__redraw_queue(self.__queue_list)
                self.__render_mode = 'QUEUE'
                self.__render_needs_updating = True

            if self.__render_needs_updating:
                self.__render()
                self.__render_count += 1
    
    def __render(self) -> None:
        self.__render_needs_updating = False
        self.__render_count += 1
        print('render', self.__render_count)
        
        sdl3.SDL_SetRenderDrawColor(self.__renderer, 0,0,0,0)
        sdl3.SDL_RenderClear(self.__renderer)

        if self.__render_mode == 'RESIZE':
            if self.__resizing:
                self.__resizing_count += 1
                sdl3.SDL_RenderTexture(
                    self.__renderer, self.__frame_base_texture, None, None)
                self.__container._Layout__invalidate()
                self.__container._Box__update()
                self.__container._Layout__redraw('RESIZE')

            if not self.__resizing:
                self.__resizing_count = 0
                self.__draw('FRAME')
                sdl3.SDL_RenderTexture(
                    self.__renderer, self.__frame_base_texture, None, None)
                self.__container._Layout__invalidate()
                self.__container._Box__update()
                # self.__container._Layout__redraw('REBUILD')

                self.__queue_list = self.__container._Layout__queue_list()
                self.__container._Layout__queue_list_clear()

        if not self.__resizing and self.__render_mode in (
                'HOVER', 'PRESSED', 'BASE', 'QUEUE'):
            sdl3.SDL_RenderTexture(
                self.__renderer, self.__frame_texture, None, None)
            self.__container._Box__update()
            self.__container._Layout__redraw(self.__render_mode)

        sdl3.SDL_RenderPresent(self.__renderer)
        sdl3.SDL_Delay(10)
    
    def __resize_settings(self) -> None:
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

    def __resize_start(self) -> None:
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
    
    def __resize_stop(self) -> None:
        self.__resize_area = ResizeArea.NONE
        self.__cursor_update_shape('NONE')
        self.__resizing = False

# SDL_RENDERER_DRIVER=vulkan python -O main.py
# SDL_VIDEODRIVER=x11 SDL_RENDERER_DRIVER=vulkan python -O frame.py
