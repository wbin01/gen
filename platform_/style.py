#!/usr/bin/env python3
import os
from pathlib import Path

from .theme import Theme
from ..tools import color


class Style(object):
    """Application style.
    
    Manages style information according to the platform.
    """
    def __init__(self, desktop_environment: str = 'plasma') -> None:
        self._desktop = desktop_environment

        self._theme = Theme(self._desktop)
        self._dark = self._theme.dark
        self._accent_color = self._theme.accent
        self._style = None

        self._path = Path(__file__).parent.parent
        self._icon_path = str(
            self._path) + f'/static/control_button/{self._desktop}/'

        if not Path(self._icon_path).exists():
            self._icon_path = str(
                self._path) + f'/static/control_button/glitch/'

        self._plasma_close_button_with_circle = False
        self._symbolic = ''
        self._set_styles()

    @property
    def accent_color(self) -> str:
        """..."""
        return self._accent_color

    @accent_color.setter
    def accent_color(self, accent_color: str) -> None:
        self._accent_color = accent_color

    @property
    def dark(self) -> bool:
        """..."""
        return self._dark

    @dark.setter
    def dark(self, dark: bool) -> None:
        self._dark = dark

    @property
    def theme(self) -> str:
        """..."""
        return self._theme.name

    @theme.setter
    def theme(self, theme: str) -> None:
        self._theme.name = theme

    @property
    def style(self) -> dict:
        """..."""
        if self._style:
            return self._style

        self._style = {
            '[Button]': {
                'background_color': self._button_bg,
                'border_color': self._button_bd,
                'font_color': self._button_fg,
                'icon_opacity': self._button_io,
                'border_width': '1',
                'border_radius': self._button_rd,
                },
            '[Button:inactive]': {
                'background_color': self._button_in_bg,
                'border_color': self._button_in_bd,
                'font_color': self._button_in_fg,
                'icon_opacity': self._button_in_io,
                },
            '[Button:hover]': {
                'background_color': self._button_hv_bg,
                'border_color': self._button_hv_bd,
                'font_color': self._button_hv_fg,
                # 'icon_opacity': self._button_hv_io,
                },
            '[Button:clicked]': {
                'background_color': self._button_ck_bg,
                'border_color': self._button_ck_bd,
                'font_color': self._button_ck_fg,
                # 'icon_opacity': self._button_ck_io,
                },
            '[Button:checked]': {
                'background_color': self._button_ch_bg,
                'border_color': self._button_ch_bd,
                'font_color': self._button_ch_fg,
                # 'icon_opacity': self._button_ch_io,
                },
            '[Button:checked:inactive]': {
                'background_color': self._button_ch_in_bg,
                'border_color': self._button_ch_in_bd,
                'font_color': self._button_ch_in_fg,
                'icon_opacity': self._button_ch_in_io,
                },
            '[Button:checked:hover]': {
                'background_color': self._button_ch_hv_bg,
                'border_color': self._button_ch_hv_bd,
                'font_color': self._button_ch_hv_fg,
                # 'icon_opacity': self._button_ch_hv_io,
                },
            '[CloseButton]': {
                'background_color': self._close_button_bg,
                'border_color': self._close_button_bd,
                'font_color': self._close_button_fg,
                'icon_opacity': self._close_button_io,
                'icon': self._close_button_i,
                'border_width': '0',
                'border_radius': self._close_button_rd,
                },
            '[CloseButton:inactive]': {
                'background_color': self._close_button_in_bg,
                'border_color': self._close_button_in_bd,
                'font_color': self._close_button_in_fg,
                'icon_opacity': self._close_button_in_io,
                'icon': self._close_button_in_i,
                },
            '[CloseButton:hover]': {
                'background_color': self._close_button_hv_bg,
                'border_color': self._close_button_hv_bd,
                'font_color': self._close_button_hv_fg,
                'icon_opacity': self._close_button_hv_io,
                'icon': self._close_button_hv_i,
                },
            '[CloseButton:clicked]': {
                'background_color': self._close_button_ck_bg,
                'border_color': self._close_button_ck_bd,
                'font_color': self._close_button_ck_fg,
                'icon_opacity': self._close_button_ck_io,
                'icon': self._close_button_ck_i,
                },
            '[Frame]': {
                'background_color': self._frame_bg,
                'border_color_inner': self._frame_bd_inner,
                'border_color': self._frame_bd,
                'border_radius': self._frame_rd,
                },
            '[Frame:inactive]': {
                'background_color': self._frame_in_bg,
                'border_color_inner': self._frame_in_bd_inner,
                'border_color': self._frame_in_bd,
                },
            '[Label]': {
                'font_color': self._label_fg,
                'background_color': self._label_bg,
                },
            '[Label:inactive]': {
                'font_color': self._label_in_fg,
                'background_color': self._label_in_bg,
                },
            '[MainFrame]': {
                'background_color': self._app_frame_bg,
                'border_color_inner': self._app_frame_bd_inner,
                'border_color': self._app_frame_bd,
                'border_radius': self._app_frame_rd,
                },
            '[MainFrame:inactive]': {
                'background_color': self._app_frame_in_bg,
                'border_color_inner': self._app_frame_in_bd_inner,
                'border_color': self._app_frame_in_bd,
                },
            '[MaxButton]': {
                'background_color': self._max_button_bg,
                'border_color': self._max_button_bd,
                'font_color': self._max_button_fg,
                'icon_opacity': self._max_button_io,
                'icon': self._max_button_i,
                'restore_icon': self._max_button_ir,
                'border_width': '0',
                'border_radius': self._max_button_rd,
                },
            '[MaxButton:inactive]': {
                'background_color': self._max_button_in_bg,
                'border_color': self._max_button_in_bd,
                'font_color': self._max_button_in_fg,
                'icon_opacity': self._max_button_in_io,
                'icon': self._max_button_in_i,
                'restore_icon': self._max_button_in_ir,
                },
            '[MaxButton:hover]': {
                'background_color': self._max_button_hv_bg,
                'border_color': self._max_button_hv_bd,
                'font_color': self._max_button_hv_fg,
                'icon_opacity': self._max_button_hv_io,
                'icon': self._max_button_hv_i,
                'restore_icon': self._max_button_hv_ir,
                },
            '[MaxButton:clicked]': {
                'background_color': self._max_button_ck_bg,
                'border_color': self._max_button_ck_bd,
                'font_color': self._max_button_ck_fg,
                'icon_opacity': self._max_button_ck_io,
                'icon': self._max_button_ck_i,
                'restore_icon': self._max_button_ck_ir,
                },
            '[MinButton]': {
                'background_color': self._min_button_bg,
                'border_color': self._min_button_bd,
                'font_color': self._min_button_fg,
                'icon_opacity': self._min_button_io,
                'icon': self._min_button_i,
                'border_width': '0',
                'border_radius': self._min_button_rd,
                },
            '[MinButton:inactive]': {
                'background_color': self._min_button_in_bg,
                'border_color': self._min_button_in_bd,
                'font_color': self._min_button_in_fg,
                'icon_opacity': self._min_button_in_io,
                'icon': self._min_button_in_i,
                },
            '[MinButton:hover]': {
                'background_color': self._min_button_hv_bg,
                'border_color': self._min_button_hv_bd,
                'font_color': self._min_button_hv_fg,
                'icon_opacity': self._min_button_hv_io,
                'icon': self._min_button_hv_i,
                },
            '[MinButton:clicked]': {
                'background_color': self._min_button_ck_bg,
                'border_color': self._min_button_ck_bd,
                'font_color': self._min_button_ck_fg,
                'icon_opacity': self._min_button_ck_io,
                'icon': self._min_button_ck_i,
                },
            '[Panel]': {
                'background_color': self._panel_bg,
                'border_color': self._panel_bd,
                'border_radius': self._panel_rd,
                },
            '[Panel:inactive]': {
                'background_color': self._panel_in_bg,
                'border_color': self._panel_in_bd,
                # 'border_radius': '10',
                },
            '[ToolButton]': {
                'background_color': self._tool_button_bg,
                'border_color': self._tool_button_bd,
                'icon_opacity': self._tool_button_io,
                'border_width': '1',
                'border_radius': self._tool_button_rd,
                },
            '[ToolButton:inactive]': {
                'background_color': self._tool_button_in_bg,
                'border_color': self._tool_button_in_bd,
                'icon_opacity': self._tool_button_in_io,
                },
            '[ToolButton:hover]': {
                'background_color': self._tool_button_hv_bg,
                'border_color': self._tool_button_hv_bd,
                'icon_opacity': self._tool_button_hv_io,
                },
            '[ToolButton:clicked]': {
                'background_color': self._tool_button_ck_bg,
                'border_color': self._tool_button_ck_bd,
                'icon_opacity': self._tool_button_ck_io,
                },
            '[ToolButton:checked]': {
                'background_color': self._tool_button_ch_bg,
                'border_color': self._tool_button_ch_bd,
                'icon_opacity': self._tool_button_ch_io,
                },
            '[ToolButton:checked:inactive]': {
                'background_color': self._tool_button_ch_in_bg,
                'border_color': self._tool_button_ch_in_bd,
                'icon_opacity': self._tool_button_ch_in_io,
                },
            '[ToolButton:checked:hover]': {
                'background_color': self._tool_button_ch_hv_bg,
                'border_color': self._tool_button_ch_hv_bd,
                'icon_opacity': self._tool_button_ch_hv_io,
                },
            }
        return self._style

    @style.setter
    def style(self, style: dict) -> None:
        self._style = style

    def print(self) -> None:
        for key, value in self.style().items():
            print(key)
            for k, v in value.items():
                print(f'{k}: {v}')
            print()

    def _set_styles(self) -> None:
        self.accent_color

        # Needs to have this order. The settings below need the settings above.
        if self._desktop == 'cinnamon':
            self._cinnamon_app_frame()
            self._cinnamon_frame()
            self._cinnamon_label()
            self._cinnamon_button()
            self._cinnamon_tool_button()
            self._cinnamon_close_button()
            self._cinnamon_max_button()
            self._cinnamon_min_button()
            self._cinnamon_panel()
        elif self._desktop == 'lxqt':
            self._lxqt_app_frame()
            self._plasma_frame()
            self._plasma_label()
            self._lxqt_button()
            self._cinnamon_tool_button()
            self._lxqt_close_button()
            self._lxqt_max_button()
            self._lxqt_min_button()
            self._cinnamon_panel()
        elif self._desktop == 'pantheon':
            self._pantheon_app_frame()
            self._plasma_frame()
            self._plasma_label()
            self._pantheon_button()
            self._cinnamon_tool_button()
            self._lxqt_close_button()
            self._lxqt_max_button()
            self._lxqt_min_button()
            self._cinnamon_panel()
        elif self._desktop == 'plasma':
            self._plasma_app_frame()
            self._plasma_frame()
            self._plasma_label()
            self._plasma_button()
            self._plasma_tool_button()
            self._plasma_close_button()
            self._plasma_max_button()
            self._plasma_min_button()
            self._plasma_panel()
        elif 'windows' in self._desktop:
            self._windows11_app_frame()
            self._plasma_frame()
            self._plasma_label()
            self._glitch_button()
            self._cinnamon_tool_button()
            self._windows11_close_button()
            self._windows11_max_button()
            self._windows11_min_button()
            self._cinnamon_panel()
        else:
            self._glitch_app_frame()
            self._plasma_frame()
            self._plasma_label()
            self._glitch_button()
            self._cinnamon_tool_button()
            self._glitch_close_button()
            self._glitch_max_button()
            self._glitch_min_button()
            self._cinnamon_panel()

    def _cinnamon_app_frame(self) -> None:
        if self._dark:
            self._app_frame_fg = '#FFCCCCCC'
            self._app_frame_bg = '#FF222226'
            self._app_frame_bd = '#FF111111'
        else:
            self._app_frame_fg = '#FF333333'
            self._app_frame_bg = '#FFEBEBED'
            self._app_frame_bd = '#FFAAAAAA'

        self._app_frame_bd_inner = self._app_frame_bg
        self._app_frame_rd = '8, 8, 0, 0'
        self._app_frame_io = '1.0'

        # Inactive
        self._app_frame_in_fg = self._app_frame_fg
        self._app_frame_in_bg = self._app_frame_bg
        self._app_frame_in_io = self._app_frame_io
        self._app_frame_in_bd = self._app_frame_bd
        self._app_frame_in_bd_inner = self._app_frame_bg

    def _cinnamon_button(self) -> None:
        self._button_fg = self._app_frame_fg

        self._button_bg = self._app_frame_bg
        if self._dark:
            self._button_bg = color.lighten_hex(self._app_frame_bg, 3)

        self._button_bd = color.darken_hex(self._button_bg, 35)
        if self._dark: self._button_bd = '#FF181818'
        
        self._button_rd = '6'
        self._button_io = self._app_frame_io

        # Inactive
        self._button_in_fg = self._app_frame_in_fg
        self._button_in_bg = self._button_bg
        self._button_in_bd = self._button_bd
        self._button_in_io = self._app_frame_in_io

        # Hover
        self._button_hv_fg = self._button_fg
        self._button_hv_bg = self._button_bg
        self._button_hv_bd = self._button_bd

        if 'dark' in self._theme.name.lower():
            self._button_hv_bg = color.lighten_hex(self._button_bg, 5)
        else:
            self._button_hv_bg = color.darken_hex(self._button_bg, 4)

        self._button_hv_io = self._button_io

        # Clicked
        self._button_ck_fg = self._button_fg
        self._button_ck_bg = '#33' + self._button_hv_bd[3:]
        self._button_ck_bd = self._button_hv_bd
        self._button_ck_io = self._button_io

        # Checked
        self._button_ch_fg = self._button_fg
        self._button_ch_bg = '#AA' + self._button_bd[3:]
        self._button_ch_bd = self._button_bd
        self._button_ch_io = self._button_io

        # Checked inactive
        self._button_ch_in_fg = self._button_in_fg
        self._button_ch_in_bg = self._button_ch_bg
        self._button_ch_in_bd = self._button_in_bd
        self._button_ch_in_io = self._button_in_io
        
        # Checked hover
        self._button_ch_hv_fg = self._button_ch_fg
        self._button_ch_hv_bg = self._button_ch_bg
        self._button_ch_hv_bd = self._button_hv_bd
        self._button_ch_hv_io = self._button_ch_io

    def _cinnamon_close_button(self) -> None:
        icon = 'window-close'
        self._symbolic = '-symbolic' if self._dark else ''

        self._close_button_bg = self._accent_color
        self._close_button_bd = '#00000000'
        self._close_button_fg = self._app_frame_fg
        self._close_button_io = self._button_io
        self._close_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._close_button_rd = '10'

        # Inactive
        self._close_button_in_bg = '#77999999'
        self._close_button_in_bd = self._app_frame_in_bg
        self._close_button_in_fg = self._app_frame_in_fg
        self._close_button_in_io = self._button_in_io
        self._close_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._close_button_hv_bg = color.lighten_hex(self._accent_color, 15)
        self._close_button_hv_bd = self._app_frame_bg
        self._close_button_hv_fg = self._app_frame_fg
        self._close_button_hv_io = self._button_hv_io
        self._close_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._close_button_ck_bg = color.darken_hex(self._accent_color, 15)
        self._close_button_ck_bd = self._app_frame_bg
        self._close_button_ck_fg = self._app_frame_fg
        self._close_button_ck_io = self._button_ck_io
        self._close_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _cinnamon_frame(self) -> None:
        self._frame_fg = self._app_frame_fg
        self._frame_bg = self._app_frame_bg
        self._frame_bd = self._app_frame_bd
        self._frame_bd_inner = self._app_frame_bg
        self._frame_rd = (self._app_frame_rd.split(',')[0] + ',') * 4

        self._frame_in_fg = self._app_frame_in_fg
        self._frame_in_bg = self._app_frame_in_bg
        self._frame_in_bd = self._app_frame_in_bd
        self._frame_in_bd_inner = self._app_frame_bg

    def _cinnamon_label(self) -> None:
        self._label_fg = self._app_frame_fg
        self._label_bg = self._app_frame_bg
        self._label_in_fg = self._app_frame_in_fg
        self._label_in_bg = self._app_frame_in_bg

    def _cinnamon_max_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self._max_button_bg = '#00000000'
        self._max_button_bd = '#00000000'
        self._max_button_fg = self._close_button_fg
        self._max_button_io = self._close_button_io
        self._max_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._max_button_ir = (
            self._icon_path + restore + self._symbolic + '.svg')
        self._max_button_rd = '10'

        # Inactive
        self._max_button_in_bg = '#00000000'
        self._max_button_in_bd = '#00000000'
        self._max_button_in_fg = self._close_button_in_fg
        self._max_button_in_io = self._close_button_in_io
        self._max_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')
        self._max_button_in_ir = (
            self._icon_path + restore + '-inactive' + self._symbolic +'.svg')
        
        # Hover
        self._max_button_hv_bg = '#FFFFFFFF'
        if self._dark:self._max_button_hv_bg = '#77999999'
        
        self._max_button_hv_bd = self._max_button_hv_bg
        self._max_button_hv_fg = self._close_button_hv_fg
        self._max_button_hv_io = self._close_button_hv_io
        self._max_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')
        self._max_button_hv_ir = (
            self._icon_path + restore + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._max_button_ck_bg = self._close_button_ck_bg
        self._max_button_ck_bd = self._close_button_ck_bd
        self._max_button_ck_fg = self._close_button_ck_fg
        self._max_button_ck_io = self._close_button_ck_io
        self._max_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')
        self._max_button_ck_ir = (
            self._icon_path + restore + '-clicked' + self._symbolic + '.svg')

    def _cinnamon_min_button(self) -> None:
        icon = 'go-down'
        self._min_button_bg = '#00000000'
        self._min_button_bd = '#00000000'
        self._min_button_fg = self._close_button_fg
        self._min_button_io = self._close_button_io
        self._min_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._min_button_rd = '10'

        # Inactive
        self._min_button_in_bg = '#00000000'
        self._min_button_in_bd = '#00000000'
        self._min_button_in_fg = self._close_button_in_fg
        self._min_button_in_io = self._close_button_in_io
        self._min_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._min_button_hv_bg = '#FFFFFFFF'
        if self._dark: self._min_button_hv_bg = '#77999999'

        self._min_button_hv_bd = self._min_button_hv_bg
        self._min_button_hv_fg = self._close_button_hv_fg
        self._min_button_hv_io = self._close_button_hv_io
        self._min_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._min_button_ck_bg = self._close_button_ck_bg
        self._min_button_ck_bd = self._close_button_ck_bd
        self._min_button_ck_fg = self._close_button_ck_fg
        self._min_button_ck_io = self._close_button_ck_io
        self._min_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _cinnamon_panel(self) -> None:
        self._panel_bg = color.darken_hex(self._app_frame_bg, 10)
        if self._dark:
            self._panel_bg = color.darken_hex(self._app_frame_bg, 5)

        self._panel_bd = self._panel_bg
        self._panel_rd = self._app_frame_rd

        # Inactive
        self._panel_in_bg = color.darken_hex(self._app_frame_in_bg, 5)
        self._panel_in_bd = self._panel_in_bg

    def _cinnamon_tool_button(self) -> None:
        self._tool_button_bg = self._app_frame_bg
        self._tool_button_bd = self._app_frame_bg
        self._tool_button_io = self._button_io
        self._tool_button_rd = self._button_rd

        # Inactive
        self._tool_button_in_bg = '#00000000'  # self._app_frame_in_bg
        self._tool_button_in_bd = '#00000000'  # self._app_frame_in_bg
        self._tool_button_in_io = self._button_in_io
        
        # Hover
        self._tool_button_hv_bg = self._tool_button_bg
        self._tool_button_hv_bd = self._button_hv_bd
        self._tool_button_hv_io = self._tool_button_io

        # Clicked
        self._tool_button_ck_bg = self._button_ck_bg
        self._tool_button_ck_bd = self._button_ck_bd
        self._tool_button_ck_io = self._button_ck_io

        # Checked
        self._tool_button_ch_bg = '#88' + self._button_ch_bg[3:]
        self._tool_button_ch_bd = self._button_ch_bd
        self._tool_button_ch_io = self._button_ch_io

        # Checked inactive
        self._tool_button_ch_in_bg = self._tool_button_ch_bg
        self._tool_button_ch_in_bd = self._tool_button_ch_bd
        self._tool_button_ch_in_io = self._tool_button_in_io

        # Checked hover
        self._tool_button_ch_hv_bg = self._tool_button_ch_bg
        self._tool_button_ch_hv_bd = self._tool_button_hv_bd
        self._tool_button_ch_hv_io = self._tool_button_ch_io

    def _glitch_app_frame(self) -> None:
        if self._dark:
            self._app_frame_fg = '#FFCCCCCC'
            self._app_frame_bg = '#FF202020'
            self._app_frame_bd = '#44999999'
            self._app_frame_bd_inner = '#11000000'
        else:
            self._app_frame_fg = '#FF333333'
            self._app_frame_bg = '#FFEBEBED'
            self._app_frame_bd = '#44000000'
            self._app_frame_bd_inner = '#11000000'

        self._app_frame_rd = '8, 8, 8, 8'
        self._app_frame_io = '1.0'
        
        # Inactive
        self._app_frame_in_fg = self._app_frame_fg
        self._app_frame_in_bg = self._app_frame_bg
        self._app_frame_in_io = self._app_frame_io
        self._app_frame_in_bd = self._app_frame_bd
        self._app_frame_in_bd_inner = self._app_frame_bd_inner

    def _glitch_button(self) -> None:
        self._button_fg = self._app_frame_fg

        self._button_bg = self._app_frame_bg
        if self._dark:
            self._button_bg = color.lighten_hex(self._app_frame_bg, 5)    

        self._button_bd = color.darken_hex(self._button_bg, 35)
        if self._dark: self._button_bd = self._button_bg
        
        self._button_rd = '6'
        self._button_io = self._app_frame_io

        # Inactive
        self._button_in_fg = self._app_frame_in_fg
        self._button_in_bg = self._button_bg
        self._button_in_bd = self._button_bd
        self._button_in_io = self._app_frame_in_io

        # Hover
        self._button_hv_fg = self._button_fg
        self._button_hv_bg = self._button_bg
        self._button_hv_bd = self._button_bd

        self._button_hv_bg = color.darken_hex(self._button_bg, 4)
        if self._dark:
            self._button_hv_bg = color.lighten_hex(self._button_bg, 5)

        self._button_hv_io = self._button_io

        # Clicked
        self._button_ck_fg = self._button_fg
        self._button_ck_bg = '#33' + self._button_hv_bd[3:]
        self._button_ck_bd = self._button_hv_bd
        self._button_ck_io = self._button_io

        # Checked
        self._button_ch_fg = self._button_fg
        self._button_ch_bg = '#AA' + self._button_bd[3:]
        self._button_ch_bd = self._button_bd
        self._button_ch_io = self._button_io

        # Checked inactive
        self._button_ch_in_fg = self._button_in_fg
        self._button_ch_in_bg = self._button_ch_bg
        self._button_ch_in_bd = self._button_in_bd
        self._button_ch_in_io = self._button_in_io
        
        # Checked hover
        self._button_ch_hv_fg = self._button_ch_fg
        self._button_ch_hv_bg = self._button_ch_bg
        self._button_ch_hv_bd = self._button_hv_bd
        self._button_ch_hv_io = self._button_ch_io

    def _glitch_close_button(self) -> None:
        icon = 'window-close'
        self._symbolic = '-symbolic' if self._dark else ''

        self._close_button_bg = '#00000000'
        self._close_button_bd = '#00000000'
        self._close_button_fg = self._app_frame_fg
        self._close_button_io = self._button_io
        self._close_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._close_button_rd = '10'

        # Inactive
        self._close_button_in_bg = '#00000000'
        self._close_button_in_bd = '#00000000'
        self._close_button_in_fg = self._app_frame_in_fg
        self._close_button_in_io = self._button_in_io
        self._close_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._close_button_hv_bg = '#00000000'
        self._close_button_hv_bd = '#00000000'
        self._close_button_hv_fg = self._app_frame_fg
        self._close_button_hv_io = self._button_hv_io
        self._close_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._close_button_ck_bg = '#00000000'
        self._close_button_ck_bd = '#00000000'
        self._close_button_ck_fg = self._app_frame_fg
        self._close_button_ck_io = self._button_ck_io
        self._close_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _glitch_max_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self._max_button_bg = '#00000000'
        self._max_button_bd = '#00000000'
        self._max_button_fg = self._close_button_fg
        self._max_button_io = self._close_button_io
        self._max_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._max_button_ir = (
            self._icon_path + restore + self._symbolic + '.svg')
        self._max_button_rd = '10'

        # Inactive
        self._max_button_in_bg = '#00000000'
        self._max_button_in_bd = '#00000000'
        self._max_button_in_fg = self._close_button_in_fg
        self._max_button_in_io = self._close_button_in_io
        self._max_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')
        self._max_button_in_ir = (
            self._icon_path + restore + '-inactive' + self._symbolic +'.svg')
        
        # Hover
        self._max_button_hv_bg = '#00000000'
        self._max_button_hv_bd = '#00000000'
        self._max_button_hv_fg = self._close_button_hv_fg
        self._max_button_hv_io = self._close_button_hv_io
        self._max_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')
        self._max_button_hv_ir = (
            self._icon_path + restore + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._max_button_ck_bg = '#00000000'
        self._max_button_ck_bd = '#00000000'
        self._max_button_ck_fg = self._close_button_ck_fg
        self._max_button_ck_io = self._close_button_ck_io
        self._max_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')
        self._max_button_ck_ir = (
            self._icon_path + restore + '-clicked' + self._symbolic + '.svg')

    def _glitch_min_button(self) -> None:
        icon = 'go-down'
        self._min_button_bg = '#00000000'
        self._min_button_bd = '#00000000'
        self._min_button_fg = self._close_button_fg
        self._min_button_io = self._close_button_io
        self._min_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._min_button_rd = '10'

        # Inactive
        self._min_button_in_bg = '#00000000'
        self._min_button_in_bd = '#00000000'
        self._min_button_in_fg = self._close_button_in_fg
        self._min_button_in_io = self._close_button_in_io
        self._min_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._min_button_hv_bg = '#00000000'
        self._min_button_hv_bd = '#00000000'
        self._min_button_hv_fg = self._close_button_hv_fg
        self._min_button_hv_io = self._close_button_hv_io
        self._min_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._min_button_ck_bg = '#00000000'
        self._min_button_ck_bd = '#00000000'
        self._min_button_ck_fg = self._close_button_ck_fg
        self._min_button_ck_io = self._close_button_ck_io
        self._min_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _lxqt_app_frame(self) -> None:
        self._app_frame_fg = '#FFCCCCCC'
        self._app_frame_bg = '#FF272727'

        if '[Palette]' in self._theme.config:    
            if 'window_text_color' in self._theme.config['[Palette]']:
                self._app_frame_fg = self._theme.config[
                    '[Palette]']['window_text_color']

            if 'window_color' in self._theme.config['[Palette]']:
                self._app_frame_bg = self._theme.config[
                    '[Palette]']['window_color']

        if self._app_frame_fg.lower().endswith('ffffff'):
            self._app_frame_fg = '#FFAAAAAA'
        if self._app_frame_fg.lower().endswith('000000'):
            self._app_frame_fg = '#FF333333'

        self._app_frame_bd = self._accent_color
        self._app_frame_bd_inner = self._app_frame_bg
        self._app_frame_rd = '0, 0, 0, 0'
        self._app_frame_io = '1.0'

        # Inactive
        self._app_frame_in_fg = self._app_frame_fg
        self._app_frame_in_bg = color.darken_hex(self._app_frame_bg, 4)
        self._app_frame_in_io = self._app_frame_io
        self._app_frame_in_bd = '#FF2D3036'
        self._app_frame_in_bd_inner = self._app_frame_bg

    def _lxqt_button(self) -> None:
        self._button_fg = self._app_frame_fg
        
        self._button_bg = self._app_frame_bg
        if self._dark:
            self._button_bg = color.lighten_hex(self._app_frame_bg, 5)
        
        self._button_bd = color.darken_hex(self._button_bg, 35)
        if self._dark: self._button_bd = self._button_bg
        
        self._button_rd = '6'
        self._button_io = self._app_frame_io

        # Inactive
        self._button_in_fg = self._app_frame_in_fg
        self._button_in_bg = self._button_bg
        self._button_in_bd = self._button_bd
        self._button_in_io = self._app_frame_in_io

        # Hover
        self._button_hv_fg = '#FF000000'
        if self._dark: self._button_hv_fg = '#FFFFFFFF'

        self._button_hv_bg = self._button_bg
        self._button_hv_bd = self._button_bd

        self._button_hv_bg = color.darken_hex(self._button_bg, 4)
        if self._dark:
            self._button_hv_bg = color.lighten_hex(self._button_bg, 5)

        self._button_hv_io = self._button_io

        # Clicked
        self._button_ck_fg = self._button_fg
        self._button_ck_bg = '#33' + self._button_hv_bd[3:]
        self._button_ck_bd = self._button_hv_bd
        self._button_ck_io = self._button_io

        # Checked
        self._button_ch_fg = self._button_fg
        self._button_ch_bg = '#AA' + self._button_bd[3:]
        self._button_ch_bd = self._button_bd
        self._button_ch_io = self._button_io

        # Checked inactive
        self._button_ch_in_fg = self._button_in_fg
        self._button_ch_in_bg = self._button_ch_bg
        self._button_ch_in_bd = self._button_in_bd
        self._button_ch_in_io = self._button_in_io
        
        # Checked hover
        self._button_ch_hv_fg = self._button_ch_fg
        self._button_ch_hv_bg = self._button_ch_bg
        self._button_ch_hv_bd = self._button_hv_bd
        self._button_ch_hv_io = self._button_ch_io

    def _lxqt_close_button(self) -> None:
        icon = 'window-close'
        self._symbolic = '-symbolic' if self._dark else ''

        self._close_button_bg = '#00000000'
        self._close_button_bd = '#00000000'
        self._close_button_fg = self._app_frame_fg
        self._close_button_io = self._button_io
        self._close_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._close_button_rd = '10'

        # Inactive
        self._close_button_in_bg = '#00000000'
        self._close_button_in_bd = '#00000000'
        self._close_button_in_fg = self._app_frame_in_fg
        self._close_button_in_io = self._button_in_io
        self._close_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._close_button_hv_bg = '#00000000'
        self._close_button_hv_bd = '#00000000'
        self._close_button_hv_fg = self._app_frame_fg
        self._close_button_hv_io = self._button_hv_io
        self._close_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._close_button_ck_bg = self._app_frame_bg
        self._close_button_ck_bd = self._app_frame_bg
        self._close_button_ck_fg = self._app_frame_fg
        self._close_button_ck_io = self._button_ck_io
        self._close_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _lxqt_max_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self._max_button_bg = '#00000000'
        self._max_button_bd = '#00000000'
        self._max_button_fg = self._close_button_fg
        self._max_button_io = self._close_button_io
        self._max_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._max_button_ir = (
            self._icon_path + restore + self._symbolic + '.svg')
        self._max_button_rd = '10'

        # Inactive
        self._max_button_in_bg = '#00000000'
        self._max_button_in_bd = '#00000000'
        self._max_button_in_fg = self._close_button_in_fg
        self._max_button_in_io = self._close_button_in_io
        self._max_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')
        self._max_button_in_ir = (
            self._icon_path + restore + '-inactive' + self._symbolic +'.svg')
        
        # Hover
        self._max_button_hv_bg = '#00000000'
        self._max_button_hv_bd = '#00000000'
        self._max_button_hv_fg = self._close_button_hv_fg
        self._max_button_hv_io = self._close_button_hv_io
        self._max_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')
        self._max_button_hv_ir = (
            self._icon_path + restore + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._max_button_ck_bg = '#00000000'
        self._max_button_ck_bd = '#00000000'
        self._max_button_ck_fg = self._close_button_ck_fg
        self._max_button_ck_io = self._close_button_ck_io
        self._max_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')
        self._max_button_ck_ir = (
            self._icon_path + restore + '-clicked' + self._symbolic + '.svg')

    def _lxqt_min_button(self) -> None:
        icon = 'go-down'
        self._min_button_bg = '#00000000'
        self._min_button_bd = '#00000000'
        self._min_button_fg = self._close_button_fg
        self._min_button_io = self._close_button_io
        self._min_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._min_button_rd = '10'

        # Inactive
        self._min_button_in_bg = '#00000000'
        self._min_button_in_bd = '#00000000'
        self._min_button_in_fg = self._close_button_in_fg
        self._min_button_in_io = self._close_button_in_io
        self._min_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._min_button_hv_bg = '#00000000'
        self._min_button_hv_bd = '#00000000'
        self._min_button_hv_fg = self._close_button_hv_fg
        self._min_button_hv_io = self._close_button_hv_io
        self._min_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._min_button_ck_bg = '#00000000'
        self._min_button_ck_bd = '#00000000'
        self._min_button_ck_fg = self._close_button_ck_fg
        self._min_button_ck_io = self._close_button_ck_io
        self._min_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _pantheon_app_frame(self) -> None:
        self._app_frame_fg = '#FFFEFEFE'
        self._app_frame_bg = '#FF303030'
        self._app_frame_bd = '#FF111111'
        self._app_frame_bd_inner = '#FF303030'
        self._app_frame_rd = '7, 7, 7, 7'
        self._app_frame_io = '1.0'

        # Inactive
        self._app_frame_in_fg = self._app_frame_fg
        self._app_frame_in_bg = color.lighten_hex(self._app_frame_bg, 2)
        self._app_frame_in_io = self._app_frame_io
        self._app_frame_in_bd = self._app_frame_bd
        self._app_frame_in_bd_inner = self._app_frame_in_bg

    def _pantheon_button(self) -> None:
        self._button_fg = self._app_frame_fg

        self._button_bg = self._app_frame_bg
        if self._dark: self._button_bg = '#FF404040'

        self._button_bd = color.darken_hex(self._button_bg, 35)
        if self._dark: self._button_bd = '#FF222222'
        
        self._button_rd = '3'
        self._button_io = self._app_frame_io

        # Inactive
        self._button_in_fg = self._app_frame_in_fg
        self._button_in_bg = color.lighten_hex(self._button_bg, 5)
        self._button_in_bd = self._button_bd
        self._button_in_io = self._app_frame_in_io

        # Hover
        self._button_hv_fg = self._button_fg
        self._button_hv_bg = self._button_bg
        self._button_hv_bd = self._button_bd
        self._button_hv_io = self._button_io

        # Clicked
        self._button_ck_fg = self._button_fg
        self._button_ck_bg = '#FF2C2C2C'
        self._button_ck_bd = self._button_hv_bd
        self._button_ck_io = self._button_io

        # Checked
        self._button_ch_fg = self._button_fg
        self._button_ch_bg = '#AA' + self._button_bd[3:]
        self._button_ch_bd = self._button_bd
        self._button_ch_io = self._button_io

        # Checked inactive
        self._button_ch_in_fg = self._button_in_fg
        self._button_ch_in_bg = self._button_ch_bg
        self._button_ch_in_bd = self._button_in_bd
        self._button_ch_in_io = self._button_in_io
        
        # Checked hover
        self._button_ch_hv_fg = self._button_ch_fg
        self._button_ch_hv_bg = self._button_ch_bg
        self._button_ch_hv_bd = self._button_hv_bd
        self._button_ch_hv_io = self._button_ch_io

    def _plasma_app_frame(self) -> None:
        self._app_frame_fg = color.plasma_color_to_hex(
            self._theme.config['[Colors:Window]']['ForegroundNormal'],
            '#FFFFFF')
        
        self._app_frame_bg = color.plasma_color_to_hex(
            self._theme.config['[Colors:Window]']['BackgroundNormal'],
            '#2A2A2A')  # Alt 282828

        self._app_frame_bd = color.darken_hex(self._app_frame_bg, 100)
        if self._dark:
            self._app_frame_bd = '#88' + color.lighten_hex(
                self._app_frame_bg, 50)[3:]

        self._app_frame_bd_inner = self._app_frame_bg
        self._app_frame_rd = '6, 6, 6, 6'
        self._app_frame_io = '1.0'

        # Inactive
        self._app_frame_in_fg = self._app_frame_fg
        self._app_frame_in_bg = color.darken_hex(self._app_frame_bg, 4)
        self._app_frame_in_io = self._app_frame_io
        self._app_frame_in_bd = self._app_frame_bd
        self._app_frame_in_bd_inner = self._app_frame_bg

    def _plasma_button(self) -> None:
        self._button_fg = self._app_frame_fg
        self._button_bg = color.plasma_color_to_hex(
            self._theme.config['[Colors:Button]']['BackgroundNormal'],
            '#33333333')

        self._button_bd = color.darken_hex(self._button_bg, 35)
        if self._dark:
            self._button_bd = color.lighten_hex(self._button_bg, 35)
        
        self._button_rd = '6'
        self._button_io = self._app_frame_io

        # Inactive
        self._button_in_fg = self._app_frame_in_fg
        self._button_in_bg = self._button_bg
        self._button_in_bd = self._button_bd
        self._button_in_io = self._app_frame_in_io

        # Hover
        self._button_hv_fg = self._button_fg
        self._button_hv_bg = self._button_bg

        self._button_hv_bd = '#99' + color.plasma_color_to_hex(
            self._theme.config['[Colors:Button]']['DecorationHover'],
            '#3C8CBD')[3:]
        self._button_hv_io = self._button_io

        # Clicked
        self._button_ck_fg = self._button_fg
        self._button_ck_bg = '#33' + self._button_hv_bd[3:]
        self._button_ck_bd = self._button_hv_bd
        self._button_ck_io = self._button_io

        # Checked
        self._button_ch_fg = self._button_fg
        self._button_ch_bg = '#AA' + self._button_bd[3:]
        self._button_ch_bd = self._button_bd
        self._button_ch_io = self._button_io

        # Checked inactive
        self._button_ch_in_fg = self._button_in_fg
        self._button_ch_in_bg = self._button_ch_bg
        self._button_ch_in_bd = self._button_in_bd
        self._button_ch_in_io = self._button_in_io
        
        # Checked hover
        self._button_ch_hv_fg = self._button_ch_fg
        self._button_ch_hv_bg = self._button_ch_bg
        self._button_ch_hv_bd = self._button_hv_bd
        self._button_ch_hv_io = self._button_ch_io

    def _plasma_close_button(self) -> None:
        icon = 'window-close'
        ico = icon if self._plasma_close_button_with_circle else icon + '-b'
        self._symbolic = '-symbolic' if self._dark else ''

        self._close_button_bg = '#00000000'
        self._close_button_bd = '#00000000'
        self._close_button_fg = self._app_frame_fg
        self._close_button_io = self._button_io
        self._close_button_i = (
            self._icon_path + ico + self._symbolic + '.svg')
        self._close_button_rd = self._tool_button_rd

        # Inactive
        self._close_button_in_bg = self._app_frame_in_bg
        self._close_button_in_bd = self._app_frame_in_bg
        self._close_button_in_fg = self._app_frame_in_fg
        self._close_button_in_io = self._button_in_io
        self._close_button_in_i = (
            self._icon_path + ico + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._close_button_hv_bg = self._app_frame_bg
        self._close_button_hv_bd = self._app_frame_bg
        self._close_button_hv_fg = self._app_frame_fg
        self._close_button_hv_io = self._button_hv_io
        self._close_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._close_button_ck_bg = self._app_frame_bg
        self._close_button_ck_bd = self._app_frame_bg
        self._close_button_ck_fg = self._app_frame_fg
        self._close_button_ck_io = self._button_ck_io
        self._close_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _plasma_frame(self) -> None:
        self._frame_fg = self._app_frame_fg
        self._frame_bg = self._app_frame_bg
        self._frame_bd = self._app_frame_bd
        self._frame_bd_inner = self._app_frame_bg
        self._frame_rd = (self._app_frame_rd.split(',')[0] + ',') * 4
        self._frame_in_fg = self._app_frame_in_fg
        self._frame_in_bg = self._app_frame_in_bg
        self._frame_in_bd = self._app_frame_in_bd
        self._frame_in_bd_inner = self._app_frame_bg

    def _plasma_label(self) -> None:
        self._label_fg = self._app_frame_fg
        self._label_bg = self._app_frame_bg
        self._label_in_fg = self._app_frame_in_fg
        self._label_in_bg = self._app_frame_in_bg

    def _plasma_max_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self._max_button_bg = self._close_button_bg
        self._max_button_bd = self._close_button_bd
        self._max_button_fg = self._close_button_fg
        self._max_button_io = self._close_button_io
        self._max_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._max_button_ir = (
            self._icon_path + restore + self._symbolic + '.svg')
        self._max_button_rd = self._tool_button_rd

        # Inactive
        self._max_button_in_bg = self._close_button_in_bg
        self._max_button_in_bd = self._close_button_in_bd
        self._max_button_in_fg = self._close_button_in_fg
        self._max_button_in_io = self._close_button_in_io
        self._max_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')
        self._max_button_in_ir = (
            self._icon_path + restore + '-inactive' + self._symbolic +'.svg')
        
        # Hover
        self._max_button_hv_bg = self._close_button_hv_bg
        self._max_button_hv_bd = self._close_button_hv_bd
        self._max_button_hv_fg = self._close_button_hv_fg
        self._max_button_hv_io = self._close_button_hv_io
        self._max_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')
        self._max_button_hv_ir = (
            self._icon_path + restore + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._max_button_ck_bg = self._close_button_ck_bg
        self._max_button_ck_bd = self._close_button_ck_bd
        self._max_button_ck_fg = self._close_button_ck_fg
        self._max_button_ck_io = self._close_button_ck_io
        self._max_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')
        self._max_button_ck_ir = (
            self._icon_path + restore + '-clicked' + self._symbolic + '.svg')

    def _plasma_min_button(self) -> None:
        icon = 'go-down'
        self._min_button_bg = self._close_button_bg
        self._min_button_bd = self._close_button_bd
        self._min_button_fg = self._close_button_fg
        self._min_button_io = self._close_button_io
        self._min_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._min_button_rd = self._tool_button_rd

        # Inactive
        self._min_button_in_bg = self._close_button_in_bg
        self._min_button_in_bd = self._close_button_in_bd
        self._min_button_in_fg = self._close_button_in_fg
        self._min_button_in_io = self._close_button_in_io
        self._min_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._min_button_hv_bg = self._close_button_hv_bg
        self._min_button_hv_bd = self._close_button_hv_bd
        self._min_button_hv_fg = self._close_button_hv_fg
        self._min_button_hv_io = self._close_button_hv_io
        self._min_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._min_button_ck_bg = self._close_button_ck_bg
        self._min_button_ck_bd = self._close_button_ck_bd
        self._min_button_ck_fg = self._close_button_ck_fg
        self._min_button_ck_io = self._close_button_ck_io
        self._min_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _plasma_panel(self) -> None:
        self._panel_bg = '#FA' + color.darken_hex(self._app_frame_bg, 15)[3:]
        if self._dark: self._panel_bg = '#FA' + color.darken_hex(
            self._app_frame_bg, 5)[3:]

        self._panel_bd = self._panel_bg
        self._panel_rd = self._app_frame_rd

        # Inactive
        self._panel_in_bg = color.darken_hex(self._app_frame_in_bg, 5)
        self._panel_in_bd = self._panel_in_bg

    def _plasma_tool_button(self) -> None:
        self._tool_button_bg = self._app_frame_bg
        self._tool_button_bd = self._app_frame_bg
        self._tool_button_io = self._button_io
        self._tool_button_rd = self._button_rd

        # Inactive
        self._tool_button_in_bg = '#00000000'
        self._tool_button_in_bd = '#00000000'
        self._tool_button_in_io = self._button_in_io
        
        # Hover
        self._tool_button_hv_bg = self._tool_button_bg
        self._tool_button_hv_bd = self._button_hv_bd
        self._tool_button_hv_io = self._tool_button_io

        # Clicked
        self._tool_button_ck_bg = self._button_ck_bg
        self._tool_button_ck_bd = self._button_ck_bd
        self._tool_button_ck_io = self._button_ck_io

        # Checked
        self._tool_button_ch_bg = '#88' + self._button_ch_bg[3:]
        self._tool_button_ch_bd = self._button_ch_bd
        self._tool_button_ch_io = self._button_ch_io

        # Checked inactive
        self._tool_button_ch_in_bg = self._tool_button_ch_bg
        self._tool_button_ch_in_bd = self._tool_button_ch_bd
        self._tool_button_ch_in_io = self._tool_button_in_io

        # Checked hover
        self._tool_button_ch_hv_bg = self._tool_button_ch_bg
        self._tool_button_ch_hv_bd = self._tool_button_hv_bd
        self._tool_button_ch_hv_io = self._tool_button_ch_io

    def _windows11_app_frame(self) -> None:
        if self._dark:
            self._app_frame_fg = '#FFCCCCCC'
            self._app_frame_bg = '#FF202020'
            self._app_frame_bd = '#44999999'
            self._app_frame_bd_inner = '#11000000'
        else:
            self._app_frame_fg = '#FF333333'
            self._app_frame_bg = '#FFEBEBED'
            self._app_frame_bd = '#44000000'
            self._app_frame_bd_inner = '#11000000'

        self._app_frame_rd = '8, 8, 8, 8'
        self._app_frame_io = '1.0'
        
        # Inactive
        self._app_frame_in_fg = self._app_frame_fg
        self._app_frame_in_bg = self._app_frame_bg
        self._app_frame_in_io = self._app_frame_io
        self._app_frame_in_bd = self._app_frame_bd
        self._app_frame_in_bd_inner = self._app_frame_bd_inner

    def _windows11_close_button(self) -> None:
        icon = 'window-close'
        self._symbolic = '-symbolic' if self._dark else ''

        self._close_button_bg = '#00000000'
        self._close_button_bd = '#00000000'
        self._close_button_fg = self._app_frame_fg
        self._close_button_io = self._button_io
        self._close_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._close_button_rd = '10'

        # Inactive
        self._close_button_in_bg = '#00000000'
        self._close_button_in_bd = '#00000000'
        self._close_button_in_fg = self._app_frame_in_fg
        self._close_button_in_io = self._button_in_io
        self._close_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._close_button_hv_bg = '#00000000'
        self._close_button_hv_bd = '#00000000'
        self._close_button_hv_fg = self._app_frame_fg
        self._close_button_hv_io = self._button_hv_io
        self._close_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._close_button_ck_bg = '#00000000'
        self._close_button_ck_bd = '#00000000'
        self._close_button_ck_fg = self._app_frame_fg
        self._close_button_ck_io = self._button_ck_io
        self._close_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')

    def _windows11_max_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self._max_button_bg = '#00000000'
        self._max_button_bd = '#00000000'
        self._max_button_fg = self._close_button_fg
        self._max_button_io = self._close_button_io
        self._max_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._max_button_ir = (
            self._icon_path + restore + self._symbolic + '.svg')
        self._max_button_rd = '10'

        # Inactive
        self._max_button_in_bg = '#00000000'
        self._max_button_in_bd = '#00000000'
        self._max_button_in_fg = self._close_button_in_fg
        self._max_button_in_io = self._close_button_in_io
        self._max_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')
        self._max_button_in_ir = (
            self._icon_path + restore + '-inactive' + self._symbolic +'.svg')
        
        # Hover
        self._max_button_hv_bg = '#00000000'
        self._max_button_hv_bd = '#00000000'
        self._max_button_hv_fg = self._close_button_hv_fg
        self._max_button_hv_io = self._close_button_hv_io
        self._max_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')
        self._max_button_hv_ir = (
            self._icon_path + restore + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._max_button_ck_bg = '#00000000'
        self._max_button_ck_bd = '#00000000'
        self._max_button_ck_fg = self._close_button_ck_fg
        self._max_button_ck_io = self._close_button_ck_io
        self._max_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')
        self._max_button_ck_ir = (
            self._icon_path + restore + '-clicked' + self._symbolic + '.svg')

    def _windows11_min_button(self) -> None:
        icon = 'go-down'
        self._min_button_bg = '#00000000'
        self._min_button_bd = '#00000000'
        self._min_button_fg = self._close_button_fg
        self._min_button_io = self._close_button_io
        self._min_button_i = (
            self._icon_path + icon + self._symbolic + '.svg')
        self._min_button_rd = '10'

        # Inactive
        self._min_button_in_bg = '#00000000'
        self._min_button_in_bd = '#00000000'
        self._min_button_in_fg = self._close_button_in_fg
        self._min_button_in_io = self._close_button_in_io
        self._min_button_in_i = (
            self._icon_path + icon + '-inactive' + self._symbolic + '.svg')

        # Hover
        self._min_button_hv_bg = '#00000000'
        self._min_button_hv_bd = '#00000000'
        self._min_button_hv_fg = self._close_button_hv_fg
        self._min_button_hv_io = self._close_button_hv_io
        self._min_button_hv_i = (
            self._icon_path + icon + '-hover' + self._symbolic + '.svg')

        # Clicked
        self._min_button_ck_bg = '#00000000'
        self._min_button_ck_bd = '#00000000'
        self._min_button_ck_fg = self._close_button_ck_fg
        self._min_button_ck_io = self._close_button_ck_io
        self._min_button_ck_i = (
            self._icon_path + icon + '-clicked' + self._symbolic + '.svg')
