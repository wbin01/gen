#!/usr/bin/env python3
import logging
import time
import sys
from ctypes import c_float, c_int

import sdl3
# import sdl3.sdlttf as ttf

from ..flag import ResizeArea, Cursor, StyleClass
from ..layout import Col
from ..ui import UI, Drawer, Theme


class Frame(UI):
    """..."""
    _theme = Theme

    def __init__(
            self, title: str,
            x: int = 0, y: int = 0, width: int = 500, height: int = 300,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._title = title
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._view_layout = False

        sdl3.SDL_SetHint(
            sdl3.SDL_HINT_X11_WINDOW_TYPE, b'_NET_WM_WINDOW_TYPE_NORMAL')
        # Init
        if sdl3.SDL_Init(sdl3.SDL_INIT_VIDEO) < 0: # X SDL_INIT_EVERYTHING
            logging.error('SDL3 init error:', sdl3.SDL_GetError())
            sys.exit(1) # X SDL_SetHint(sdl3.SDL_HINT_RENDER_DRIVER, b'vulkan')

        # Frame
        self._frame = sdl3.SDL_CreateWindow(
            self._title.encode('utf-8'), self._width, self._height, (
                sdl3.SDL_WINDOW_OPENGL | sdl3.SDL_WINDOW_BORDERLESS |
                sdl3.SDL_WINDOW_TRANSPARENT | sdl3.SDL_WINDOW_RESIZABLE))
                # SDL_WINDOW_OPENGL SDL_WINDOW_TOOLTIP
                # SDL_WINDOW_POPUP SDL_WINDOW_UTILITY

        if not self._frame:
            logging.error('Frame error:', sdl3.SDL_GetError())
            sdl3.SDL_Quit()
            sys.exit(1)

        sdl3.SDL_SetWindowOpacity(self._frame, 1.0)

        # Style
        self._renderer  = sdl3.SDL_CreateRenderer(self._frame, None)
        if not self._renderer :
            logging.error('Renderer error:', sdl3.SDL_GetError())
            sdl3.SDL_DestroyWindow(self._frame)
            sdl3.SDL_Quit()
            sys.exit(1)
        
        sdl3.SDL_SetRenderVSync(self._renderer , 1)  # Opt 1=on 0=off -1=adapt

        self._drawer = Drawer(self._renderer )
        self._style = self._theme

        # Container
        self._container = Col()
        self._container._first = True
        self._container._parent = self
        self._container._app = self
        self._container._drawer = self._drawer

        # Loop
        self._running = True
        self._queue_list = []

        # Render
        self._render_mode = 'UNIT'
        self._render_needs_updating = True
        self._render_count = 0
        self._first_render = True

        # Frame
        self._frame_base_texture = None
        self._frame_texture = None

        # Frame - resize
        self._resizing = False
        self._resizing_count = 0
        self._resize_area = ResizeArea.NONE
        self._resize_border = 8
        self._resize_wm = False

        # Cursor
        self._cursor = {
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
        self._last_resize_cursor_on_hover = 'NONE'
        self._cursor_hit = sdl3.SDL_HitTest(self._cursor_hit_test)
        sdl3.SDL_SetWindowHitTest(self._frame, self._cursor_hit, None)

        # Cell
        self._hovered = self._container
        self._input = None
        self._focus = None
        self._default = None
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def view_layout(self) -> bool:
        """..."""
        return self._view_layout
    
    @view_layout.setter
    def view_layout(self, view_layout: bool) -> None:
        self._view_layout = view_layout
    
    @property
    def height(self) -> int:
        """..."""
        return self._height
    
    @height.setter
    def height(self, height: int) -> None:
        self._height = height
        sdl3.SDL_SetWindowSize(self._frame, self._width, self._height)
    
    @property
    def spacing(self) -> int:
        """..."""
        return self.__spacing
    
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._container.spacing = spacing
    
    @property
    def width(self) -> int:
        """..."""
        return self._width
    
    @width.setter
    def width(self, width: int) -> None:
        self._width = width
        sdl3.SDL_SetWindowSize(self._frame, self._width, self._height)
    
    @property
    def x(self) -> int:
        """..."""
        return self._x
    
    @x.setter
    def x(self, x: int) -> None:
        self._x = int(x)
        sdl3.SDL_SetWindowPosition(self._frame, self._x, self._y)
    
    @property
    def y(self) -> int:
        """..."""
        return self._y
    
    @y.setter
    def y(self, y: int) -> None:
        self._y = int(y)
        sdl3.SDL_SetWindowPosition(self._frame, self._x, self._y)
    
    def add(self, ui: Cell | Box, fill=None) -> Cell | Box:
        ui._drawer = self._drawer
        return self._container.add(ui)
        
    def run(self) -> int:
        self._draw('FRAME_BASE')
        self._draw('FRAME')
        
        self._event_loop()
        self._destroy()
        return 0
    
    @property
    def default(self) -> Cell:
        """..."""
        return self._default
    
    @default.setter
    def default(self, cell: Cell) -> None:
        self._default = cell
        self._default.style_class = StyleClass.DEFAULT
    
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

        # DRAG
        if border < x < w.value - border and border < y < 40:
            return sdl3.SDL_HITTEST_DRAGGABLE

        return sdl3.SDL_HITTEST_NORMAL
    
    def _cursor_resize_area(self, mouse_x, mouse_y) -> ResizeArea:
        # mx = c_float()
        # my = c_float()
        # sdl3.SDL_GetGlobalMouseState(mx, my)
        mx = mouse_x
        my = mouse_y

        wx = c_int()
        wy = c_int()
        sdl3.SDL_GetWindowPosition(self._frame, wx, wy)

        ww = c_int()
        wh = c_int()
        sdl3.SDL_GetWindowSize(self._frame, ww, wh)

        x = mx.value - wx.value
        y = my.value - wy.value

        b = self._resize_border
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
    
    def _cursor_update_shape(self, cursor_name: str) -> None:
        if self._resizing:
            return

        sdl3.SDL_SetCursor(self._cursor[cursor_name])
    
    def _destroy(self):
        for c in self._cursor.values():
            sdl3.SDL_DestroyCursor(c)

        sdl3.SDL_DestroyRenderer(self._renderer )
        sdl3.SDL_DestroyWindow(self._frame)
        # sdl3.SDL_DestroySurface(self.__font_surface)
        sdl3.SDL_Quit()
    
    def _draw(self, mode: str = 'FRAME') -> None:
        w = h = c_int()
        sdl3.SDL_GetWindowSize(self._frame, w, h)

        if mode == 'FRAME':
            self._frame_texture = self._drawer.build_texture(
                self.width, self.height, self._draw_ui, mode)
        
        elif mode == 'FRAME_BASE':
            self._frame_base_texture = self._drawer.build_texture(
                self.width, self.height, self._draw_ui, mode)

    def _draw_ui(self, mode) -> None:
        self._drawer.rect(
            x=0, y=0, w=self.width, h=self.height,
            color=self._style.Frame['BASE']['border-color'],
            r=self._style.Frame['BASE']['radius'])

        self._drawer.rect(
            x=1, y=1, w=self.width - 2, h=self.height - 2,
            color=self._style.Frame['BASE']['background-color'],
            r=self._style.Frame['BASE']['radius'])

        if mode == 'FRAME':
            if self._container._uis:
                self._container._invalidate()
                self._container._update()
                self._container._redraw('REBUILD')

    def _event_loop(self) -> None:
        while self._running:
            event = sdl3.SDL_Event()
            
            mouse_x = c_float()
            mouse_y = c_float()
            sdl3.SDL_GetGlobalMouseState(mouse_x, mouse_y)
            resize_area = self._cursor_resize_area(mouse_x, mouse_y)

            mx = c_float()
            my = c_float()
            sdl3.SDL_GetMouseState(mx, my)

            if sdl3.SDL_WaitEventTimeout(event, 16):
                if event.type != 0:
                    self._handle_events(event, resize_area, mx, my)

                    while sdl3.SDL_PollEvent(event):
                        self._handle_events(event, resize_area, mx, my)

            if self._queue_list:
                self._container._redraw_queue(self._queue_list)
                self._render_mode = 'UNIT'
                self._render_needs_updating = True

            if self._render_needs_updating:
                self._render()
                self._render_count += 1
    
    def _handle_events(self, event, resize_area, mx, my) -> None:
        if resize_area.value != self._last_resize_cursor_on_hover:
            self._cursor_update_shape(resize_area.value)
            self._last_resize_cursor_on_hover = resize_area.value

        if event.type == sdl3.SDL_EVENT_QUIT:
            self._running = False
        
        if event.type == sdl3.SDL_EVENT_KEY_DOWN:
            if event.key.key == sdl3.SDLK_ESCAPE:
                self._running = False
        
        if event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_DOWN:
            if event.button.button == sdl3.SDL_BUTTON_LEFT:
                self._resize_area = resize_area

                if self._resize_area == ResizeArea.NONE:
                    item = self._container._hit_test(mx, my)
                    if item:
                        item._set_state('PRESSED')
                        self._render_mode = 'UNIT'
                        self._render_needs_updating = True

                        if item._base_class == 'Input':
                            self._input = item
                            sdl3.SDL_StartTextInput(self._frame)
                            self._focus = self._input
                            self._input._click_update_cursor(mx.value)
                        else:
                            if self._input:
                                input_item = self._input
                                self._focus = None
                                self._input = None
                                input_item._set_state('BASE')
                                sdl3.SDL_StopTextInput(self._frame)
                    else:
                        drag = sdl3.SDL_SetWindowHitTest(
                            self._frame, self._cursor_hit, None)

                elif self._resize_area != ResizeArea.NONE:
                    self._cursor_update_shape(self._resize_area.value)
                    if self._resize_wm:
                        sdl3.SDL_SetWindowHitTest(
                            self._frame, self._cursor_hit, None)
                    else:
                        self._resize_settings()
            
            elif event.button.button == sdl3.SDL_BUTTON_RIGHT:
                item = self._container._hit_test(mx, my)
                if item:
                    item._set_state('RIGHT_PRESSED')
                    self._render_mode = 'UNIT'
                    self._render_needs_updating = True
                else:
                    sdl3.SDL_SetWindowHitTest(
                        self._frame, self._cursor_hit, None)

        elif event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_UP:
            if event.button.button == sdl3.SDL_BUTTON_LEFT:
                if self._resizing:
                    self._resize_stop()
                    self._render_mode = 'RESIZE'
                    self._render_needs_updating = True
                else:
                    item = self._container._hit_test(mx, my)
                    if item:
                        item._set_state('RELEASED')
                        self._render_mode = 'UNIT'
                        self._render_needs_updating = True
                    
                    if self._input: self._input._selecting = False
            
            elif event.button.button == sdl3.SDL_BUTTON_RIGHT:
                item = self._container._hit_test(mx, my)
                if item:
                    item._set_state('RIGHT_RELEASED')
                    self._render_mode = 'UNIT'
                    self._render_needs_updating = True

        elif event.type == sdl3.SDL_EVENT_MOUSE_MOTION:
            if not self._resize_wm:
                if self._resize_area != ResizeArea.NONE:
                    self._render_mode = 'RESIZE'
                    self._render_needs_updating = True
                    self._resize_start()
            
            if self._hovered:
                self._hovered._set_state('MOVE')

                if self._input:
                    if self._input._state.value == 'PRESSED':
                        self._input._mouse_selection(mx.value)
                        self._render_mode = 'UNIT'
                        self._render_needs_updating = True

            if resize_area == ResizeArea.NONE:
                ui = None
                if not self._resizing:
                    ui = self._container._hit_test(mx, my)
                
                if ui and ui != self._hovered:
                    self._hovered._set_state('LEAVE')
                    self._hovered = ui
                    self._hovered._set_state('ENTER')

                    self._render_mode = 'UNIT'
                    self._render_needs_updating = True
        
        elif event.type == sdl3.SDL_EVENT_TEXT_INPUT:
            if self._input:
                text = event.text.text.decode('utf-8')
                self._input.insert(text)
                self._input._set_state('KEY')
                self._render_mode = 'UNIT'
                self._render_needs_updating = True

        elif event.type == sdl3.SDL_EVENT_KEY_DOWN:
            key = event.key.key
            mods = event.key.mod
            ctrl = mods & sdl3.SDL_KMOD_CTRL
            shift = mods & sdl3.SDL_KMOD_SHIFT

            if ctrl:
                if key == ord('a'):
                    if self._input: self._input.select_all()
                
                elif key == ord('c'):
                    if self._input:
                        sdl3.SDL_SetClipboardText(self._input.copy().encode())

                elif key == ord('v'):
                    clip = sdl3.SDL_GetClipboardText()
                    if clip:
                        clip = clip.decode()
                        if self._input: self._input.past(clip)
                
                elif key == ord('x'):
                    if self._input:
                        sdl3.SDL_SetClipboardText(self._input.cut().encode())
                
                elif key == sdl3.SDLK_LEFT:
                    if self._input: self._input.move_left_by_jump()
                
                elif key == sdl3.SDLK_RIGHT:
                    if self._input: self._input.move_right_by_jump()
            
            if shift:
                if key == sdl3.SDLK_LEFT:
                    if self._input: self._input.select_left()
                
                elif key == sdl3.SDLK_RIGHT:
                    if self._input: self._input.select_right()

            if shift and ctrl:
                if key == sdl3.SDLK_LEFT:
                    if self._input: self._input.select_left()
                
                elif key == sdl3.SDLK_RIGHT:
                    if self._input: self._input.select_right()

            if key == sdl3.SDLK_BACKSPACE:
                if self._input: self._input.backspace()

            elif key == sdl3.SDLK_DELETE:
                if self._input: self._input.delete()

            elif key == sdl3.SDLK_LEFT:
                if self._input: self._input.move_left()
                
            elif key == sdl3.SDLK_RIGHT:
                if self._input: self._input.move_right()
            
            elif key ==  sdl3.SDLK_RETURN:
                if self._default:
                    for fn in self._default.pressed._slots:
                        fn(self._default)
                    
                    for fn in self._default.released._slots:
                        fn(self._default)
            
            # elif key == sdl3.SDLK_ESCAPE:
            #     pass
            if self._input:
                self._input._set_state('KEY')
                self._render_mode = 'UNIT'
                self._render_needs_updating = True
        
        elif event.type == sdl3.SDL_EVENT_KEY_UP:
            key = event.key.key
            mods = event.key.mod
            shift = mods & sdl3.SDL_KMOD_SHIFT

            if not shift:
                if self._input: self._input._anchor = None
    
    def _render(self) -> None:
        self._render_needs_updating = False
        self._render_count += 1
        
        sdl3.SDL_SetRenderDrawColor(self._renderer , 0,0,0,0)
        sdl3.SDL_RenderClear(self._renderer )

        if self._render_mode == 'RESIZE':
            if self._resizing:
                self._resizing_count += 1
                sdl3.SDL_RenderTexture(
                    self._renderer , self._frame_base_texture, None, None)
                self._container._invalidate()
                self._container._update()
                self._container._redraw('RESIZE')

            if not self._resizing:
                self._resizing_count = 0
                self._draw('FRAME')
                sdl3.SDL_RenderTexture(
                    self._renderer , self._frame_base_texture, None, None)
                self._container._invalidate()
                self._container._update()
                self._queue_list = self._container._queue_list()
                self._container._queue_list_clear()

        if not self._resizing and self._render_mode == 'UNIT':
            sdl3.SDL_RenderTexture(
                self._renderer, self._frame_texture, None, None)

            if self._first_render:
                self._container._invalidate()
                self._first_render = False
            
            self._container._update()
            self._container._redraw(self._render_mode)

        sdl3.SDL_RenderPresent(self._renderer )
        sdl3.SDL_Delay(16)
    
    def _resize_settings(self) -> None:
        self._resizing = True

        self.__start_mx = c_float()
        self.__start_my = c_float()
        sdl3.SDL_GetGlobalMouseState(self.__start_mx, self.__start_my)

        self.__start_x = c_int()
        self.__start_y = c_int()
        sdl3.SDL_GetWindowPosition(self._frame, self.__start_x, self.__start_y)

        self.__start_w = c_int()
        self.__start_h = c_int()
        sdl3.SDL_GetWindowSize(self._frame, self.__start_w, self.__start_h)

    def _resize_start(self) -> None:
        if not self._resizing:
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

        r = self._resize_area.value

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

        sdl3.SDL_SetWindowPosition(self._frame, int(x), int(y))
        sdl3.SDL_SetWindowSize(self._frame, w, h)
        self.width = w
        self.height = h
        self.x = x
        self.y = y
    
    def _resize_stop(self) -> None:
        self._resize_area = ResizeArea.NONE
        self._cursor_update_shape('NONE')
        self._resizing = False

# SDL_RENDERER_DRIVER=vulkan python -O main.py
# SDL_VIDEODRIVER=x11 SDL_RENDERER_DRIVER=vulkan python -O frame.py
