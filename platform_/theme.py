#!/usr/bin/env python3
import os
import platform
import subprocess
from pathlib import Path

from ..tools import color
from ..tools import DesktopEntry


class Theme(object):
    """..."""
    def __init__(self, desktop: str) -> None:
        """..."""
        self._desktop = desktop
        
        self._accent = '#FF3C8CBD'
        self._conf = self._get_conf()
        self._dark = False
        self._name = 'glitch'
        self._set_themes()

    def __repr__(self) -> str:
        return self._class__.__name__
    
    @property
    def accent(self) -> str:
        """..."""
        return self._accent

    @accent.setter
    def accent(self, accent: str) -> None:
        self._accent = accent

    @property
    def config(self) -> dict:
        """..."""
        return self._conf

    @config.setter
    def config(self, config: dict) -> None:
        self._conf = config

    @property
    def dark(self) -> bool:
        """..."""
        return self._dark

    @dark.setter
    def dark(self, dark: str) -> None:
        self._dark = dark

    @property
    def name(self) -> str:
        """..."""
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def _get_conf(self) -> dict:
        path = None
        if self._desktop == 'plasma':
            path = Path(os.environ['HOME']) / '.config' / 'kdeglobals'
        elif self._desktop == 'lxqt':
            path = Path(os.environ['HOME']) / '.config' / 'lxqt' / 'lxqt.conf'

        if path and path.exists():
            return DesktopEntry(path).content
        return {}
    
    def _set_themes(self) -> None:
        cinnamon_themes = {
            'aqua':   '#FF1F9EDE', 'blue':   '#FF0C75DE', 'brown': '#FFB7865E',
            'grey':   '#FF70737A', 'orange': '#FFFF7139', 'pink':  '#FFE54980',
            'purple': '#FF8C5DD9', 'red':    '#FFE82127', 'sand':  '#FFC5A07C',
            'teal':   '#FF199CA8'}

        if self._desktop == 'cinnamon':
            # Name
            cmd = subprocess.run(
                'gsettings get org.cinnamon.theme name',
                shell=True, capture_output=True, text=True)
            theme = cmd.stdout.strip().strip("'").strip('"')
            self._name = theme if theme else 'Mint-Y'

            # Accent
            theme_name_end = self._name.lower().split('-')[-1]
            accent = '#FF35A854'
            if theme_name_end in cinnamon_themes:
                accent = cinnamon_themes[theme_name_end]
            self._accent = accent

            # Dark
            if 'dark' in self._name.lower():
                self._dark = True

        elif self._desktop == 'lxqt':
            # Name
            self._name = 'Greybird'

            # Accent
            if ('[Palette]' in self._conf and
                    'highlight_color' in self._conf['[Palette]']):
                accent = self._conf['[Palette]']['highlight_color']

                if accent: self._accent = accent

            # Dark
            self._dark = True
            if ('[Palette]' in self._conf and
                    'window_color' in self._conf['[Palette]']):
                bg = self._conf['[Palette]']['window_color']
                
                if bg:self._dark = color.is_dark(color.hex_to_rgba(app_bg))

        elif self._desktop == 'pantheon':
            # Name
            self._name = 'elementary'

            # Dark
            self._dark = True

        elif self._desktop == 'plasma':
            # Name
            if ('[General]' in self._conf and
                    'ColorScheme' in self._conf['[General]']):
                theme = self._conf['[General]']['ColorScheme']
                self._name = theme if theme else 'breeze'

            # Accent
            if ('[General]' in self._conf and
                    'AccentColor' in self._conf['[General]']):
                accent = color.plasma_color_to_hex(
                    self._conf['[General]']['AccentColor'])

                if accent: self._accent = accent

            # Dark
            if ('[Colors:Window]' in self._conf and
                    'BackgroundNormal' in self._conf['[Colors:Window]']):
                bg = color.plasma_color_to_hex(
                    self._conf['[Colors:Window]']['BackgroundNormal'])

                if bg: self._dark = color.is_dark(color.hex_to_rgba(bg))

        elif 'windows' in self._desktop:
            # Name
            self._name = 'windows'

            # Dark
            self._dark = False

        else: # Glitch
            # Name
            self._name = 'glitch'

            # Dark
            self._dark = True
