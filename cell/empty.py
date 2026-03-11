#!/usr/bin/env python3
from .cell import Cell
from ..flag import Fill


class Empty(Cell):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._invalidate_item = None

        self._resize_width = 0
        self._resize_height = 0

        self._tx_base = None
        self._tx_hover = None
        self._tx_pressed = None
        
        self._tx_width = 0
        self._tx_height = 0

        self._need_rebuild = False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text="{self._text}")'
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._text}")'

    def _draw(self, mode: str = None) -> None:
        if not self._dirty: return
        self._dirty = False

        if mode == 'UNIT' and self._invalidate_item:
            # build...
            self._invalidate_item = None
            self._need_rebuild = True
            
        elif mode == 'REBUILD':
            self._need_rebuild = False
            self._set_state('BASE')
            self._build_background_textures()

            self._resize_width = 0
            self._resize_height = 0
        
        elif mode in ('RESIZE', 'POSITION'):
            if mode == 'POSITION': self._need_rebuild = True
            
            if not self._resize_height:
                self._resize_width = int(self.width)
                self._resize_height = int(self.height)
            
            # if self.fill.value == 'X':
            #     self._resize_width = int(self.width)

            self._drawer.set_texture(
                self._tx_base, int(self._x), int(self._y),
                self._resize_width, self._resize_height)
            return
        
        if self._need_rebuild: self._dirty = True
        self._set_textures()
    
    def _render_bg(self, state: str = 'BASE'):
        radius = self.style['BASE']['radius']
        border = self.style['BASE']['border']
        bg_color = self.style[state]['background-color']
        bd_color = self.style[state]['border-color']
        bd_space = border * 2

        self._drawer.rect(0, 0, self.width, self.height, bd_color, radius)
        self._drawer.rect(
            border, border, self.width - bd_space, self.height - bd_space,
            bg_color, radius - border)
    
    def _build_background_textures(self) -> None:
        self._tx_width = int(self.width)
        self._tx_height = int(self.height)

        self._tx_base = self._drawer.build_texture(
            self._tx_width, self._tx_height, self._render_bg, 'BASE')
        
        self._tx_hover = self._drawer.build_texture(
            self._tx_width, self._tx_height, self._render_bg, 'HOVER')
        
        self._tx_pressed = self._drawer.build_texture(
            self._tx_width, self._tx_height, self._render_bg, 'PRESSED')
    
    def _set_textures(self) -> None:
        if self._state.value == 'BASE':
            self._drawer.set_texture(
                self._tx_base,
                int(self._x), int(self._y), int(self.width), int(self.height))

        elif self._state.value == 'HOVER':
            self._drawer.set_texture(
                self._tx_hover,
                int(self._x), int(self._y), int(self.width), int(self.height))
        
        elif self._state.value == 'PRESSED':
            self._drawer.set_texture(
                self._tx_pressed,
                int(self._x), int(self._y), int(self.width), int(self.height))
