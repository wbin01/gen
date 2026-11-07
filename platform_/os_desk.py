#!/usr/bin/env python3
import os
import platform


class OSDesk(object):
    """Platform Selector."""
    def __init__(self) -> None:
        # linux bsd mac windows unknown
        self._operational_system = None

        # plasma gnome cinnamon xfce mac
        # windows-7 windows-10 windows-11 unknown
        self._desktop_environment = None

        self._display_server = None

    def __repr__(self) -> str:
        return self._class__.__name__

    @property
    def desktop_environment(self) -> str:
        """Desktop environment name.

        For linux: 'plasma', 'cinnamon', 'xubuntu', 'mate', 'gnome'.
        For Windos: 'windows-7', 'windows-10', 'windows-11'.
        For BSD for now it's 'bsd', but it will be like in Linux.
        For Mac OS for now it's 'mac'.
        """
        if not self._desktop_environment:
            self._desktop_environment = self._de()
        return self._desktop_environment

    @desktop_environment.setter
    def desktop_environment(self, desktop_environment_name: str) -> None:
        self._desktop_environment = desktop_environment_name

    @property
    def display_server(self) -> str:
        """..."""
        if not self._display_server:
            self._get_display_server()
        return self._display_server

    @display_server.setter
    def display_server(self, display_server: str) -> None:
        self._display_server = display_server

    @property
    def operational_system(self) -> str:
        """Operational system name.

        Is 'linux', 'windows'and 'mac' for now.
        """
        if not self._operational_system:
            self._operational_system = self._os()
        return self._operational_system

    @operational_system.setter
    def operational_system(self, operational_system_name: str) -> None:
        self._operational_system = operational_system_name

    def clear_cache(self) -> None:
        """Clear properties cache"""
        self._operational_system = None
        self._desktop_environment = None

    def _de(self) -> str:
        # ...
        if not self._operational_system:
            self._operational_system = self._os()

        de = os.environ['DESKTOP_SESSION'].lower()
        de_s = os.environ['XDG_SESSION_DESKTOP'].lower()
        de_c = os.environ['XDG_CURRENT_DESKTOP'].lower()
        de = de_s.strip("'").strip('"')
        
        if self._operational_system == 'linux':
            if de == 'plasma' or de_s == 'kde' or de_c == 'kde':
                de = 'plasma'

            elif 'pantheon' in de or 'pantheon' in de_s or 'Pantheon' in de_c:
                de = 'pantheon'

            elif de == 'cinnamon' or de_s == 'cinnamon' or de_c == 'x-cinnamon':
                de = 'cinnamon'

            elif de == 'xubuntu' or de_s == 'xubuntu' or de_c == 'xfce':
                de = 'xfce'

            elif de == 'mate' or de_s == 'mate' or de_c == 'mate':
                de = 'mate'

            elif de == 'lubuntu' or de_s == 'lxqt' or de_c == 'lxqt':
                de = 'lxqt'

            elif de == 'gnome' or de_s == 'gnome' or de_c == 'gnome':
                de = 'gnome'

            return de if de else 'glitch'

        elif self._operational_system == 'windows':
            if platform.release() == '10':
                return 'windows-10'

            elif platform.release() == '11':
                return 'windows-11'

            return 'windows-7'

        elif self._operational_system == 'mac':
            return 'mac'

        elif self._operational_system == 'bsd':
            return 'bsd'

        return 'unknown'

    def _get_display_server(self) -> str:
        # command = subprocess.run('echo $XDG_SESSION_TYPE',
        #     shell=True, capture_output=True, text=True)
        # command.stdout
        # command.stderr
        # command.returncode
        if self.operational_system == 'linux':
            self._display_server = os.environ['XDG_SESSION_TYPE'].lower()
        else:
            self._display_server = self.operational_system

    @staticmethod
    def _os() -> str:
        # 'unknown', 'linux', 'bsd', 'mac', 'windows'

        # Win config path: $HOME + AppData\Roaming\
        # Linux config path: $HOME + .config
        if os.name == 'posix':
            if platform.system() == 'Linux':
                return 'linux'

            elif platform.system() == 'Darwin':
                return 'mac'

        elif os.name == 'nt' and platform.system() == 'Windows':
            return 'windows'
