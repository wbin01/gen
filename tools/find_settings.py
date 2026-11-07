#!/usr/bin/env python3
import datetime
import os
import subprocess
import sys
import time
import pprint


class FindModifiedFiles(object):
    """..."""
    def __init__(self, paths: list, *args, **kwargs) -> None:
        """...

        :param paths: list os strings, like: ['path/a', 'path/b', 'path/c']
        """
        super().__init__(*args, **kwargs)
        self._paths = paths
        self._check_path_type()

        self._files_and_hashes = self._get_files_and_hashes()
        self._added_files = {}
        self._deleted_files = {}
        self._modified_files = {}

        self._dirs = {}
        self._added_dirs = {}
        self._deleted_dirs = {}

    def find(self):
        if self._monitoring():
            print('added files:')
            pprint.pprint(self._added_files)
            print('deleted files:')
            pprint.pprint(self._deleted_files)
            print('modified files:')
            pprint.pprint(self._modified_files)

    def _check_path_type(self):
        # ...
        for path in self._paths:
            if not isinstance(path, str):
                raise TypeError(f'The path "{path}" is not string!')

    @staticmethod
    def _find_added_files(control_files: dict, new_files: dict) -> list:
        # ...
        added_files_list = []
        if len(control_files) < len(new_files):
            for item in new_files:
                if item not in control_files:
                    added_files_list.append(item)
        return added_files_list

    @staticmethod
    def _find_deleted_files(control_files: dict, new_files: dict) -> list:
        # ...
        deleted_files_list = []
        if len(control_files) > len(new_files):
            for item in control_files:
                if item not in new_files:
                    deleted_files_list.append(item)
        return deleted_files_list

    @staticmethod
    def _find_modified_files(control_files: dict, new_files: dict) -> list:
        # ...
        modified_files_list = []
        if (len(control_files) == len(new_files) and
                control_files != new_files):
            for control_file_name, control_file_md5 in control_files.items():
                new_file_md5 = new_files[control_file_name]

                if new_file_md5 != control_file_md5:
                    modified_file_item = {
                        control_file_name: {
                            'time': datetime.datetime.now().strftime(
                                "%d-%m-%Y %I:%M.%S")}}
                    modified_files_list.append(modified_file_item)
        return modified_files_list

    @staticmethod
    def _get_command_output(command_args: list) -> str | None:
        # ['ls', '-l']
        try:
            command = subprocess.Popen(
                command_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = command.communicate()
        except ValueError as er:
            print(er)
            print(f'Error in command args: "{command_args}"')
        else:
            return stdout.decode() if not stderr.decode() else None

    def _get_files_and_hashes(self) -> dict | None:
        """..."""
        files_hashes_dict = {}
        for path in self._paths:
            files_hashes_dict[path] = {}

            ls_stdout = self._get_command_output(['ls', path])
            if not ls_stdout:
                break

            for filename in ls_stdout.split('\n'):
                file_path = os.path.join(path, filename)
                if os.path.isfile(file_path):
                    file_stdout = self._get_command_output(
                        ['md5sum', file_path])
                    if not file_stdout:
                        break

                    files_hashes_dict[path][filename] = file_stdout.split()[0]

        return files_hashes_dict if files_hashes_dict else None

    def _monitoring(self) -> bool:
        # ...
        for n in range(60):
            time.sleep(1.0)

            new_file_hashes = self._get_files_and_hashes()
            if new_file_hashes == self._files_and_hashes:
                continue

            if self._deleted_files or self._added_files:
                return True

            for path, control_files in self._files_and_hashes.items():
                new_file_items = new_file_hashes[path]

                self._added_files[path] = self._find_added_files(
                    control_files, new_file_items)
                self._deleted_files[path] = self._find_deleted_files(
                    control_files, new_file_items)
                self._modified_files[path] = self._find_modified_files(
                    control_files, new_file_items)

        return False


if __name__ == '__main__':
    import pprint
    config_path = os.path.join(os.environ['HOME'], '.config')
    f = FindModifiedFiles([
        config_path
        ])
    pprint.pprint(f.find())
