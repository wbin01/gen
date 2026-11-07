#!/usr/bin/env python3
import os
import subprocess
import sys

from .icon import Icon
from .os_desk import OSDesk
from .style import Style
from ..tools import color, DesktopEntry


class Platform(object):
    """..."""
    def __init__(self, theme: str = None, icon_theme: str = None) -> None:
        self._os_desk = OSDesk()
        self._de = self._args('desktop')
        self._icon = Icon(self._de)
        self._style = Style(self._de)

        # Properties
        self._accent_color = None
        self._controls_order = None
        self._dark_variant = None
        self._display_server = None
        self._global_menu = None
        self._icon_theme = icon_theme
        self._os = None
        self._theme = theme

        # Set
        self._breezerc = None
        self._kde_globals = None
        self._kwinrc = None

    @property
    def accent_color(self) -> str:
        """..."""
        if not self._accent_color:
            self._accent_color = self._style.accent_color()
        return self._accent_color

    @accent_color.setter
    def accent_color(self, accent_color: str) -> None:
        self._accent_color = accent_color

    @property
    def control_buttons_order(self) -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        if self._controls_order:
            return self._controls_order

        self._controls_order = ('icon',), ('min', 'max', 'close')

        if self.de == 'cinnamon':
            cmd = subprocess.run(
                'gsettings get org.cinnamon.desktop.wm.preferences '
                'button-layout', shell=True, capture_output=True, text=True)
            button_layout = cmd.stdout.strip().strip("'").strip('"')

            self._controls_order = ('',), ('min', 'max', 'close')
            if button_layout:
                buttons_l, buttons_r = button_layout.replace(
                    'minimize', 'min').replace(
                    'maximize', 'max').split(':')
                
                self._controls_order = tuple(
                    buttons_l.split(',')), tuple(buttons_r.split(','))

        elif self.de == 'pantheon':
            self._controls_order = ('close',), ('max',)

        elif self.de == 'plasma':
            filerc = os.path.join(os.environ['HOME'], '.config', 'kwinrc')
            if not os.path.isfile(filerc):
                self._controls_order = ('close', 'max', 'min'), ('icon',)
            kwinrc = DesktopEntry(url=filerc).content

            left_buttons = 'M'  # M = icon, F = above all
            right_buttons = 'IAX'  # X = close, A = max, I = min

            kdecoration = '[org.kde.kdecoration2]'
            buttons_on_left = 'ButtonsOnLeft'
            buttons_on_right = 'ButtonsOnRight'
            if kdecoration in kwinrc:
                if buttons_on_left in kwinrc[kdecoration]:
                    left_buttons = kwinrc[kdecoration][buttons_on_left]

                if buttons_on_right in kwinrc[kdecoration]:
                    right_buttons = kwinrc[kdecoration][buttons_on_right]

            d = {'X': 'close', 'A': 'max', 'I': 'min', 'M': 'icon'}
            self._controls_order = tuple(
                d[x] for x in left_buttons
                if x == 'X' or x == 'A' or x == 'I' or x == 'M'), tuple(
                d[x] for x in right_buttons
                if x == 'X' or x == 'A' or x == 'I' or x == 'M')

        elif self.de == 'glitch':
            self._controls_order = ('min',), ('close',)

        return self._controls_order

    @property
    def dark_variant(self) -> bool:
        """..."""
        if self._dark_variant is not None:
            return self._dark_variant

        self._dark_variant = color.is_dark(
            color.hex_to_rgba(self.style['[MainFrame]']['background_color']))

        return self._dark_variant

    @dark_variant.setter
    def dark_variant(self, dark_variant: bool) -> None:
        self._dark_variant = dark_variant

    @property
    def de(self) -> str:
        """..."""
        return self._de

    @de.setter
    def de(self, desktop_environment: str | None) -> None:
        self._de = desktop_environment

    @property
    def display_server(self) -> str:
        if not self._display_server:
            self._display_server = self._os_desk.display_server

        return self._display_server

    @display_server.setter
    def display_server(self, display_server: str | None) -> None:
        self._display_server = display_server

    @property
    def icon_theme(self) -> str | None:
        """..."""
        if not self._icon_theme:
            self._icon_theme = self._icon.icon_theme()
        
        return self._icon_theme

    @icon_theme.setter
    def icon_theme(self, icon_theme: str | None) -> None:
        """..."""
        self._icon_theme = icon_theme

    @property
    def global_menu(self) -> bool:
        """..."""
        if self._global_menu is not None:
            return self._global_menu

        if not self._kwinrc:
            self._set_kwinrc()

        self._global_menu = False
        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self._kwinrc and key in self._kwinrc[group]:
            if self._kwinrc[group][key] == 'true': self._global_menu = True

        return self._global_menu

    @global_menu.setter
    def global_menu(self, global_menu: bool) -> None:
        self._global_menu = global_menu

    @property
    def os(self) -> str:
        """..."""
        if not self._os:
            self._os = self._os_desk.operational_system

        return self._os

    @os.setter
    def os(self, operational_system: str | None) -> None:
        self._os = operational_system

    @property
    def style(self) -> dict:
        """..."""
        if not self._style:
            self._style = Style()

        return self._style.style

    @style.setter
    def style(self, style: dict | None) -> None:
        self._style = style

    @property
    def theme(self) -> str | None:
        """..."""
        return self._style.theme

    @theme.setter
    def theme(self, theme: str | None) -> None:
        """..."""
        self._style.theme = theme

    def icon_source(
            self, source: str | None, dark: bool = None, size: int = 16
            ) -> str:
        return self._icon.icon_source(source, dark=dark, size=size)

    def icon_theme_variant(
            self, icon_theme: str = None, dark: bool = None) -> str:
        """..."""
        if not icon_theme: icon_theme = self.icon_theme
        if dark is None:
            dark = False if self._dark_variant else True

        return self._icon.icon_theme_variant(icon_theme, dark)

    def _args(self, arg: str = None) -> str:
        desktop = None
        if arg == 'desktop':
            for arg in sys.argv:
                if '--desktop=' in arg:
                    desktop = arg.split('=')[1].strip('"').strip("'").strip()

            if desktop:
                if 'windows' in desktop:
                    desktop = 'windows-11'

                elif desktop not in [
                        'cinnamon', 'plasma', 'pantheon', 'lxqt']:
                    desktop = 'glitch'

            return desktop if desktop else self._os_desk.desktop_environment
        return None

    def _set_kwinrc(self) -> dict:
        filerc = os.path.join(os.environ['HOME'], '.config', 'kwinrc')
        self._kwinrc = (
            DesktopEntry(url=filerc).content if os.path.isfile(filerc) else {})

    def _set_breezerc(self) -> dict:
        filerc = os.path.join(os.environ['HOME'], '.config', 'breezerc')
        self._breezerc = (
            DesktopEntry(url=filerc).content if os.path.isfile(filerc) else {})
    
    def _set_kde_globals(self) -> dict:
        filerc = os.path.join(os.environ['HOME'], '.config', 'kdeglobals')
        self._kde_globals = (
            DesktopEntry(url=filerc).content if os.path.isfile(filerc) else {})
