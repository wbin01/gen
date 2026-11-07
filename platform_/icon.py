#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

from xdg import IconTheme

from ..tools import DesktopEntry


class Icon(object):
    """Information about operating system icons."""
    def __init__(self, desktop_environment: str) -> None:
        """
        :param desktop_environment: DE name, like 'plasma' or 'mate'.
        """
        self._desktop_environment = desktop_environment
        self._icon_theme = None

        self._path = Path(__file__).parent.parent
        self._icon_path = self._path / 'static' / 'icons'

        self._light_suffixes = ['-light', '-Light', ' light', ' Light']
        self._dark_suffixes = ['-dark', '-Dark', ' dark', ' Dark']
        self._icon_theme_paths = [
            '/usr/share/icons/', '/home/user/.local/share/icons/',
            '/home/user/.icons/']

    def clear_cache(self) -> None:
        """Clear properties cache"""
        self._icon_theme = None

    def icon_theme(self) -> str | None:
        """Icon theme name.

        Retrieve the name of the system icon theme.
        """
        if self._icon_theme:
            return self._icon_theme

        if self._desktop_environment == 'plasma':
            kdeglobals = Path(os.environ['HOME']) / '.config' / 'kdeglobals'
            if kdeglobals.exists():
                ini = DesktopEntry(kdeglobals)

                self._icon_theme = 'breeze'
                if ('[Icons]' in ini.content and
                        'Theme' in ini.content['[Icons]']):
                    self._icon_theme = ini.content['[Icons]']['Theme']

        elif self._desktop_environment == 'cinnamon':
            cmd = subprocess.run(
                'gsettings get org.cinnamon.theme name',
                shell=True, capture_output=True, text=True)
            self._icon_theme = cmd.stdout.strip()

        elif self._desktop_environment == 'mate':
            gtk_icons = subprocess.getoutput(
                'dconf read /org/mate/desktop/interface/icon-theme')
            self._icon_theme = gtk_icons.strip("'") if gtk_icons else None

        elif self._desktop_environment == 'gnome':
            gtk_icons = subprocess.getoutput(
                'gsettings get org.gnome.desktop.interface icon-theme')
            self._icon_theme = gtk_icons.strip("'") if gtk_icons else None

        elif self._desktop_environment == 'lxqt':
            conf = Path(os.environ['HOME']) / '.config' / 'lxqt' / 'lxqt.conf'

            if conf.exists():
                ini = DesktopEntry(conf)

                self._icon_theme = 'glitch'
                if ('[General]' in ini.content and
                        'icon_theme' in ini.content['[General]']):
                    self._icon_theme = ini.content['[General]']['icon_theme']

        elif 'pantheon' in self._desktop_environment.lower():
            self._icon_theme = 'elementary'

        if not self._icon_theme: self._icon_theme = 'glitch'
        return self._icon_theme

    def icon_source(
            self, icon: str | None, size: int = 16, dark: bool = None) -> str:
        """..."""
        if not self._icon_theme:
            self.icon_theme()

        if self._desktop_environment == 'plasma':
            return self._icon_source_plasma(icon, size, dark)
        elif self._desktop_environment == 'cinnamon':
            return self._icon_source_gtk(icon, size, dark)
        else:
            return self._icon_source_plasma(icon, size, dark)

    def icon_theme_variant(
            self, theme: str = None, dark: bool = True) -> str | None:
        """Dark or light variant icon theme"""
        if not theme:
            theme = self.icon_theme()

        new_theme = ''
        for path in self._icon_theme_paths:
            for suffix in self._dark_suffixes:
                
                if dark and 'dark' not in theme.lower():
                    if 'light' in theme.lower():
                        
                        for x in self._light_suffixes:
                            theme = theme.replace(x, '')

                    if Path(path + theme + suffix).exists():
                        new_theme = theme + suffix

                elif not dark and 'dark' in theme.lower():
                    temp = theme.replace(suffix, '')
                    if Path(path+temp).exists() and 'dark' not in temp.lower():
                        new_theme = temp

        return new_theme if new_theme else None

    def icon_theme_dark_variant(self, theme: str = None) -> str | None:
        return self.icon_theme_variant(theme, True)

    def icon_theme_light_variant(self, theme: str = None) -> str | None:
        return self.icon_theme_variant(theme, False)

    def _icon_source_gtk(
            self, icon: str | None, size: int = 16, dark: bool = None) -> str:
        if dark or dark is None and 'dark' in self._icon_theme.lower():
            self._icon_path =self._path/'static'/'icons'/'linux-gtk-dark'
        else:
            self._icon_path = self._path/'static'/'icons'/'linux-gtk'

        if not icon:
            return str(self._path / 'static' / 'icons' / 'empty.svg')

        if '/' in icon:
            if not Path(icon).exists():
                return str(self._path / 'static' / 'icons' / 'empty.svg')
            return icon

        variant_theme = self._icon_theme
        if dark and 'dark' not in self._icon_theme.lower():
            variant_theme = self.icon_theme_dark_variant(self._icon_theme)
        elif not dark and 'dark' in self._icon_theme.lower():
            variant_theme = self.icon_theme_light_variant(self._icon_theme)

        if variant_theme: self._icon_theme = variant_theme
        
        icon_path = IconTheme.getIconPath(
            iconname=icon,
            size=size,
            theme=self._icon_theme,
            extensions=['png', 'svg', 'xpm'])

        if icon_path:
            return icon_path
        
        icon = icon + '.svg'
        path = self._icon_path / icon
        return str(path) if path.exists() else str(
            self._path / 'static' / 'icons' / 'empty.svg')

    def _icon_source_plasma(
            self, icon: str | None, size: int = 16, dark: bool = None) -> str:
        if dark or dark is None and 'dark' in self._icon_theme.lower():
            self._icon_path = self._path/'static'/'icons'/'linux-qt-dark'
        else:
            self._icon_path = self._path/'static'/'icons'/'linux-qt'
        
        if not icon:
            return str(self._path / 'static' / 'icons' / 'empty.svg')

        if '/' in icon:
            if not Path(icon).exists():
                return str(self._path / 'static' / 'icons' / 'empty.svg')
            return icon

        variant_theme = self._icon_theme
        if dark and 'dark' not in self._icon_theme.lower():
            variant_theme = self.icon_theme_dark_variant(self._icon_theme)
        elif not dark and 'dark' in self._icon_theme.lower():
            variant_theme = self.icon_theme_light_variant(self._icon_theme)

        if variant_theme: self._icon_theme = variant_theme
        
        icon_path = IconTheme.getIconPath(
            iconname=icon,
            size=size,
            theme=self._icon_theme,
            extensions=['png', 'svg', 'xpm'])

        if icon_path:
            return icon_path
        
        icon = icon + '.svg'
        path = self._icon_path / icon
        return str(path) if path.exists() else str(
            self._path / 'static' / 'icons' / 'empty.svg')
