#!/usr/bin/env python3
# Reference:
#   www.freedesktop.org/wiki/Specifications/
#   www.freedesktop.org/wiki/Specifications/basedir-spec/
#   www.freedesktop.org/wiki/Specifications/desktop-entry-spec/
import logging
import os
import re
import subprocess
# from subprocess import getoutput


class DesktopEntry(object):
    """Desktop files object.

    Desktop files are files with the extension '.desktop' and are used
    internally by menus to find applications. This object converts these files
    into a dictionary to provide easy access to their values.
    """
    def __init__(self, url: str) -> None:
        """Class constructor

        Initialize class properties.

        :param url:
            String from a desktop file like: "/path/file.desktop"
        """
        self._url = os.path.abspath(url)
        self._content = None
        self._url_basename = os.path.basename(self._url).rstrip('.desktop')
    
    def __gt__(self, _object) -> bool:
        if '[Desktop Entry]' in self.content:
            return self.content['[Desktop Entry]']['Name'].lower() > _object
        return self._url_basename > _object

    def __lt__(self, _object) -> bool:
        if '[Desktop Entry]' in self.content:
            return self.content['[Desktop Entry]']['Name'].lower() < _object
        return self._url_basename < _object

    def __eq__(self, _object) -> bool:
        if '[Desktop Entry]' in self.content:
            return self.content['[Desktop Entry]']['Name'].lower() == _object
        return self._url_basename == _object

    def __ge__(self, _object) -> bool:
        if '[Desktop Entry]' in self.content:
            return self.content['[Desktop Entry]']['Name'].lower() >= _object
        return self._url_basename >= _object

    def __le__(self, _object) -> bool:
        if '[Desktop Entry]' in self.content:
            return self.content['[Desktop Entry]']['Name'].lower() <= _object
        return self._url_basename <= _object

    def __ne__(self, _object) -> bool:
        if '[Desktop Entry]' in self.content:
            return self.content['[Desktop Entry]']['Name'].lower() != _object
        return self._url_basename != _object

    def __str__(self) -> str:
        if '[Desktop Entry]' in self.content:
            name = self.content['[Desktop Entry]']['Name']
            return f"<class 'DesktopFile: {name}'>"
        return f"<class 'DesktopFile: {self._url_basename}'>"

    @property
    def content(self) -> dict:
        """Contents of a desktop file as a dictionary

        Example:
        >>> desktop_file = DesktopFile(
        ... url='/usr/share/applications/firefox.desktop')
        >>> desktop_file.content['[Desktop Entry]']['Name']
        'Firefox Web Browser'
        >>> desktop_file.content['[Desktop Entry]']['Type']
        'Application'
        >>> for key in desktop_file.content.keys():
        ... print(key)
        ...
        [Desktop Entry]
        [Desktop Action new-window]
        [Desktop Action new-private-window]
        >>>
        >>> desktop_file.content['[Desktop Action new-window]']['Name']
        'Open a New Window'
        """
        if not self._content:
            self._parse_file_to_dict()
        return self._content

    @property
    def url(self) -> str:
        """URL of the desktop file

        The URL used to construct this object, like: "/path/file.desktop".

        :return: String from a desktop file
        """
        return self._url

    def _parse_file_to_dict(self) -> None:
        with open(self._url, 'r') as ini_file:
            ini_text = ini_file.read()

        self._content = {}
        for scope in ini_text.replace('][', '||').split('['):
            if not scope.strip().startswith('#'):
                scope = f'[{scope.strip()}'

            header, key, value = '', '', ''
            for line in scope.replace('||', '][').split('\n'):
                if line and not line.strip().startswith('#'):
                    line = line.strip()

                    if line.startswith('['):
                        header = line
                        self._content[header] = {}

                    elif '=' in line:
                        key, value = line.split('=', maxsplit=1)
                        self._content[header][key] = value

                    else:
                        value = self._content[header][key] + ' ' + line
                        self._content[header][key] = value


class FindDesktopFiles(object):
    """Desktop files location object.

    Locate system desktop entry file paths.
    Files that contain the '.desktop' extension and are used internally by
    menus to find applications.

    Follows the specification from freedesktop.org:
        www.freedesktop.org/wiki/Specifications/basedir-spec/
    """
    def __init__(self) -> None:
        self._paths = self._find_paths()
        self._ulrs_by_priority = None
        self._ulrs = None
    
    def __str__(self) -> str:
        return f"<class 'FindDesktopFiles'>"

    @property
    def paths(self) -> list:
        """All desktop file paths

        String list of all desktop file paths on the system as per settings
        in $XDG_DATA_HOME and $XDG_DATA_DIRS of the freedesktop.org spec.
        """
        return self._paths

    @property
    def ulrs(self) -> list:
        """All desktop files ulrs (/path/file.desktop)

        String list of all desktop file URLs. It may contain files with the
        same name in different paths. To get valid single files, use
        "files_ulr_by_priority" property.
        """
        if not self._ulrs:
            self._ulrs = (
                self._find_urls())
        return self._ulrs

    @property
    def ulrs_by_priority(self) -> list:
        """Desktop files ulrs (/path/file.desktop)

        String list of all desktop file URLs in order of priority.
        If there are files with the same name, then user files in "~/.local/",
        will have priority over system files. Likewise, files in
        "/usr/local/share" take precedence over files in "/usr/share".
        """
        if not self._ulrs_by_priority:
            self._ulrs_by_priority = (
                self._find_urls_by_priority())
        return self._ulrs_by_priority

    @staticmethod
    def _find_paths() -> list:
        # /usr/local/share/applications, /usr/share/applications ...
        desktop_file_dirs = [
            os.path.join(
                os.environ.get(
                    'XDG_DATA_HOME',
                    os.path.join(os.environ['HOME'], '.local', 'share')),
                'applications')]

        xdg_data_dirs_stdout = os.environ.get('XDG_DATA_DIRS')
        if xdg_data_dirs_stdout:
            for data_dir in xdg_data_dirs_stdout.split(':'):
                if 'applications' in os.listdir(data_dir):
                    desktop_file_dirs.append(
                        os.path.join(data_dir, 'applications'))
        else:
            desktop_file_dirs += [
                '/usr/local/share/applications', '/usr/share/applications']

        return desktop_file_dirs

    def _find_urls(self) -> list:
        # Get all url
        desktop_files = []
        for desktop_dir in self._paths:
            for desktop_file in os.listdir(desktop_dir):
                if ('~' not in desktop_file
                        and desktop_file.endswith('.desktop')):
                    desktop_files.append(
                        os.path.join(desktop_dir, desktop_file))

        return desktop_files

    def _find_urls_by_priority(self) -> list:
        # Get url in order of precedence

        checked_file_names = []
        desktop_files = []
        for desktop_dir in self._paths:
            for desktop_file in os.listdir(desktop_dir):

                if desktop_file not in checked_file_names:
                    checked_file_names.append(desktop_file)

                    if ('~' not in desktop_file
                            and desktop_file.endswith('.desktop')):
                        desktop_files.append(
                            os.path.join(desktop_dir, desktop_file))

        return desktop_files
