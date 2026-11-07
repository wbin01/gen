#!/usr/bin/env python3
import logging
import sys
import ctypes

import sdl3
# import sdl3.sdlttf as ttf

from ..cell import Input
from ..control import Signal
from ..flag import ResizeArea, Cursor, StyleClass, FrameState
from ..layout import Col
from ..ui import UIObject, Drawer, Theme


class Layout:
    pass


class Frame(UIObject):
    """..."""
    _theme = Theme

    def __init__(
            self, title: str,
            x: int = 0, y: int = 0, width: int = 100, height: int = 100,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._base_class = 'Frame'
        self._title = title
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._layout_view = False

        # Signal
        self.closed = Signal(self)

        # Init
        sdl3.SDL_SetHint(
            sdl3.SDL_HINT_X11_WINDOW_TYPE, b'_NET_WM_WINDOW_TYPE_NORMAL')
        
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

        self._start_cursor_x = ctypes.c_float()
        self._start_cursor_y = ctypes.c_float()
        self._start_x = ctypes.c_int()
        self._start_y = ctypes.c_int()
        self._start_w = ctypes.c_int()
        self._start_h = ctypes.c_int()
        self._state = FrameState.FRAME

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
        self._tt_frame = None

        # Loop
        self._running = True
        self._queue_list = []
        self._timers = []
        self._recalculate = False

        # Container
        self._container = Col()
        self._container._first = True
        self._container._parent = self
        self._container._app = self
        self._container._drawer = self._drawer
        self._container._global_objects.append(self)

        # Render
        self._render_mode = 'UNIT'
        self._render_update = True
        self._render_count = 0
        self._first_render = True

        # Resize
        self._resizing = False
        self._resizing_count = 0
        self._resize_area = ResizeArea.NONE
        self._resize_border = 8
        self._resize_wm = False

        # Cursor
        self._cursor = {
            'BEAM': sdl3.SDL_CreateSystemCursor(1),
            'WAIT': sdl3.SDL_CreateSystemCursor(2),
            'CROSSHAIR': sdl3.SDL_CreateSystemCursor(3),
            'ARROW_WAIT': sdl3.SDL_CreateSystemCursor(4),
            'NOT_ALLOWED': sdl3.SDL_CreateSystemCursor(10),
            'POINTER': sdl3.SDL_CreateSystemCursor(11),
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
        self._drag_areas = []

        # Objects
        self._hovered = self._container
        self._input = None
        self._focus = None
        self._default = None
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    @property
    def default(self) -> Cell:
        """..."""
        return self._default
    
    @default.setter
    def default(self, cell: Cell) -> None:
        self._default = cell
        self._default.style_class = StyleClass.DEFAULT
    
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
        return self._container.spacing
    
    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._container.spacing = spacing

    @property
    def layout_view(self) -> bool:
        """..."""
        return self._layout_view
    
    @layout_view.setter
    def layout_view(self, layout_view: bool) -> None:
        self._layout_view = layout_view
    
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
    
    def add(self, obj: Cell | Layout, fill=None) -> Cell | Layout:
        obj._drawer = self._drawer
        return self._container.add(obj)
    
    def close(self) -> None:
        """..."""
        self.closed.emit()
        self._running = False
    
    def run(self) -> int:
        if self._layout_view:
            for obj in self._container._objects:
                if obj._base_class == 'Layout':
                    p, m = obj.padding, obj.margin
                    obj.padding = p[0] + 2, p[1] + 2, p[2] + 2, p[3] + 2
                    obj.margin = m[0] + 1, m[1] + 1, m[2] + 1, m[3] + 1
        
        self._draw()
        self._event_loop()
        self._destroy()
        return 0
    
    def _cursor_hit_test(self, window, area, data):
        # SysFrame
        return sdl3.SDL_HITTEST_NORMAL
    
    def _cursor_resize_area(self, cursor_x, cursor_y) -> ResizeArea:
        # SysFrame
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
        sdl3.SDL_Quit()
    
    def _draw(self) -> None:
        w = ctypes.c_int()
        h = ctypes.c_int()
        sdl3.SDL_GetWindowSize(self._frame, ctypes.byref(w), ctypes.byref(h))

        self._tt_frame = self._drawer.texture(
            self._tt_frame, self.width, self.height, self._draw_obj, 'FRAME')
        
        if self._container._objects:
            self._container._invalidate()
            self._container._update()
            self._container._redraw('REBUILD')

    def _draw_obj(self, mode) -> None:
        bg_color = self._style.Frame['BASE']['background-color']
        bd_color = self._style.Frame['BASE']['border-color']
        bd_radius = self._style.Frame['BASE']['radius']

        flags = sdl3.SDL_GetWindowFlags(self._frame)
        if (flags & sdl3.SDL_WINDOW_FULLSCREEN or
                flags & sdl3.SDL_WINDOW_MAXIMIZED):
            bd_color = bg_color
            bd_radius = 0
        
        self._drawer.rect(
            x=0, y=0, w=self.width, h=self.height, color=bd_color, r=bd_radius)

        self._drawer.rect(
            x=1, y=1, w=self.width - 2, h=self.height - 2,
            color=bg_color, r=bd_radius)

    def _event_loop(self) -> None:
        while self._running:
            event = sdl3.SDL_Event()
            
            cursor_x = ctypes.c_float()
            cursor_y = ctypes.c_float()
            sdl3.SDL_GetGlobalMouseState(cursor_x, cursor_y)
            resize_area = self._cursor_resize_area(cursor_x, cursor_y)

            cursor_x = ctypes.c_float()
            cursor_y = ctypes.c_float()
            sdl3.SDL_GetMouseState(cursor_x, cursor_y)

            if sdl3.SDL_WaitEventTimeout(event, 16):
                if event.type != 0:
                    self._handle_events(event, resize_area, cursor_x, cursor_y)

                    while sdl3.SDL_PollEvent(event):
                        self._handle_events(
                            event, resize_area, cursor_x, cursor_y)

            for timer in self._timers:
                if timer._exec() and self._render_mode == 'UNIT':
                    if self._resize_area == ResizeArea.NONE:
                        self._render_update = True

            if self._queue_list:
                self._container._redraw_queue(self._queue_list)
                self._render_mode = 'UNIT'
                self._render_update = True

            if self._render_update or self._container._dirty:
                self._render()
    
    def _event_name(self, event_type):
        for name in dir(sdl3):
            if name.startswith("SDL_EVENT_"):
                if getattr(sdl3, name) == event_type:
                    return name
        return str(event_type)
    
    def _handle_events(self, event, resize_area, cursor_x, cursor_y) -> None:
        # print(self._event_name(event.type))

        if resize_area.value != self._last_resize_cursor_on_hover:
            self._cursor_update_shape(resize_area.value)
            self._last_resize_cursor_on_hover = resize_area.value

        if event.type == sdl3.SDL_EVENT_QUIT:
            self._running = False
        
        if event.type == sdl3.SDL_EVENT_KEY_DOWN:
            if event.key.key == sdl3.SDLK_ESCAPE:
                self._running = False
        
        if event.type == sdl3.SDL_EVENT_WINDOW_EXPOSED:
            # or SDL_EVENT_WINDOW_SAFE_AREA_CHANGED
            if not self._resizing:
                self._render_mode = 'SYS_RESIZE'
                self._render_update = True
        
        if event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_DOWN:
            if event.button.button == sdl3.SDL_BUTTON_LEFT:
                self._resize_area = resize_area

                if self._resize_area == ResizeArea.NONE:
                    item = self._container._hit_test(cursor_x, cursor_y)
                    if item:
                        item._set_state('PRESSED')
                        self._render_mode = 'UNIT'
                        self._render_update = True

                        if isinstance(item, Input):
                            self._input = item
                            sdl3.SDL_StartTextInput(self._frame)
                            self._focus = self._input
                            self._input._click_update_cursor(cursor_x.value)
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
                item = self._container._hit_test(cursor_x, cursor_y)
                if item:
                    item._set_state('RIGHT_PRESSED')
                    self._render_mode = 'UNIT'
                    self._render_update = True
                else:
                    sdl3.SDL_SetWindowHitTest(
                        self._frame, self._cursor_hit, None)

        elif event.type == sdl3.SDL_EVENT_MOUSE_BUTTON_UP:
            if event.button.button == sdl3.SDL_BUTTON_LEFT:

                if self._resizing:
                    self._resize_stop()
                    self._render_mode = 'RESIZE'
                    self._render_update = True
                else:
                    item = self._container._hit_test(cursor_x, cursor_y)
                    if item:
                        item._set_state('RELEASED')
                        self._render_mode = 'UNIT'
                        self._render_update = True
                    
                    if self._input:
                        self._input._selecting = False
            
            elif event.button.button == sdl3.SDL_BUTTON_RIGHT:
                item = self._container._hit_test(cursor_x, cursor_y)
                if item:
                    item._set_state('RIGHT_RELEASED')
                    self._render_mode = 'UNIT'
                    self._render_update = True

        elif event.type == sdl3.SDL_EVENT_MOUSE_MOTION:
            if not self._resize_wm:
                if self._resize_area != ResizeArea.NONE:
                    self._render_mode = 'RESIZE'
                    self._render_update = True
                    self._resize_start()
            
            if self._hovered:
                self._hovered._set_state('MOVE')

            if self._input:
                if self._input._state.value == 'PRESSED':
                    self._input._mouse_selection(cursor_x.value)
                    self._render_mode = 'UNIT'
                    self._render_update = True
            
            if resize_area == ResizeArea.NONE:
                obj = None
                if not self._resizing:
                    obj = self._container._hit_test(cursor_x, cursor_y)
                
                if obj and obj != self._hovered:
                    self._hovered._set_state('LEAVE')
                    if isinstance(self._hovered, Input):
                        self._cursor_update_shape('NONE')

                    self._hovered = obj
                    self._hovered._set_state('ENTER')

                    self._render_mode = 'UNIT'
                    self._render_update = True
                
                if isinstance(self._hovered, Input):
                    self._cursor_update_shape('BEAM')
        
        elif event.type == sdl3.SDL_EVENT_TEXT_INPUT:
            if self._input:
                text = event.text.text.decode('utf-8')
                self._input.insert(text)
                self._input._set_state('KEY')
                self._render_mode = 'UNIT'
                self._render_update = True

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
                self._render_update = True
        
        elif event.type == sdl3.SDL_EVENT_KEY_UP:
            key = event.key.key
            mods = event.key.mod
            shift = mods & sdl3.SDL_KMOD_SHIFT

            if not shift:
                if self._input: self._input._anchor = None
        
        elif event.type == sdl3.SDL_EVENT_MOUSE_WHEEL:
            obj = self._container._hit_test(cursor_x, cursor_y)

            if event.wheel.y > 0:
                obj.wheel_up.emit()
            
            elif event.wheel.y < 0:
                obj.wheel_down.emit()
    
    def _render(self) -> None:
        self._render_update = False
        self._render_count += 1
        
        sdl3.SDL_SetRenderDrawColor(self._renderer, 0, 0, 0, 0)
        sdl3.SDL_RenderClear(self._renderer )

        if self._render_mode == 'SYS_RESIZE':
            self._sync_frame_size()
        
        if self._recalculate:
            for _ in range(5):
                self._container._invalidate()
                self._container._update(self._render_mode)
        
        if self._render_mode == 'RESIZE':
            if self._resizing:
                self._resizing_count += 1
                sdl3.SDL_RenderTexture(
                    self._renderer , self._tt_frame, None, None)
                self._container._invalidate()
                self._container._update(self._render_mode)
                self._container._redraw('RESIZE')

            if not self._resizing:
                self._resizing_count = 0
                self._draw()
                sdl3.SDL_RenderTexture(
                    self._renderer , self._tt_frame, None, None)
                self._container._invalidate()
                self._container._update(self._render_mode)
                self._queue_list = self._container._queue_list()
                self._container._queue_list_clear()

        if self._render_mode == 'POSITION':
            sdl3.SDL_RenderTexture(
                self._renderer , self._tt_frame, None, None)
            self._container._invalidate()
            self._container._update(self._render_mode)
            self._container._redraw('POSITION')

        if not self._resizing and self._render_mode == 'UNIT':
            sdl3.SDL_RenderTexture(self._renderer, self._tt_frame, None, None)

            if self._first_render:
                for _ in range(5):
                    self._container._invalidate()
                    self._container._update('RESIZE')
                self._first_render = False
            
            self._container._update(self._render_mode)
            self._container._redraw(self._render_mode)

        sdl3.SDL_RenderPresent(self._renderer )
        sdl3.SDL_Delay(16)
    
    def _sync_frame_size(self, frame_state = None) -> None:
        # SysFrame
        self._render_mode = 'RESIZE'
    
    def _resize_settings(self) -> None:
        self._resizing = True
        sdl3.SDL_GetGlobalMouseState(self._start_cursor_x, self._start_cursor_y)
        sdl3.SDL_GetWindowPosition(self._frame, self._start_x, self._start_y)
        sdl3.SDL_GetWindowSize(self._frame, self._start_w, self._start_h)

    def _resize_start(self) -> None:
        if not self._resizing:
            return

        cursor_x = ctypes.c_float()
        cursor_y = ctypes.c_float()
        sdl3.SDL_GetGlobalMouseState(cursor_x, cursor_y)

        dx = cursor_x.value - self._start_cursor_x.value
        dy = cursor_y.value - self._start_cursor_y.value

        x = self._start_x.value
        y = self._start_y.value
        w = self._start_w.value
        h = self._start_h.value

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
