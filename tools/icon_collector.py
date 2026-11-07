#!/usr/bin/env python3
import pathlib
import shutil
import sys


# https://specifications.freedesktop.org/icon-naming-spec/latest/#names
icon_naming_spec = """
address-book-new
application-exit
appointment-new
call-start
call-stop
contact-new
document-new
document-open
document-open-recent
document-page-setup
document-print
document-print-preview
document-properties
document-revert
document-save
document-save-as
document-send
edit-clear
edit-copy
edit-cut
edit-delete
edit-find
edit-find-replace
edit-paste
edit-redo
edit-select-all
edit-undo
folder-new
format-indent-less
format-indent-more
format-justify-center
format-justify-fill
format-justify-left
format-justify-right
format-text-direction-ltr
format-text-direction-rtl
format-text-bold
format-text-italic
format-text-underline
format-text-strikethrough
go-bottom
go-down
go-first
go-home
go-jump
go-last
go-next
go-previous
go-top
go-up
help-about
help-contents
help-faq
insert-image
insert-link
insert-object
insert-text
list-add
list-remove
mail-forward
mail-mark-important
mail-mark-junk
mail-mark-notjunk
mail-mark-read
mail-mark-unread
mail-message-new
mail-reply-all
mail-reply-sender
mail-send
mail-send-receive
media-eject
media-playback-pause
media-playback-start
media-playback-stop
media-record
media-seek-backward
media-seek-forward
media-skip-backward
media-skip-forward
object-flip-horizontal
object-flip-vertical
object-rotate-left
object-rotate-right
process-stop
system-lock-screen
system-log-out
system-run
system-search
system-reboot
system-shutdown
tools-check-spelling
view-fullscreen
view-refresh
view-restore
view-sort-ascending
view-sort-descending
window-close
window-new
zoom-fit-best
zoom-in
zoom-original
zoom-out
"""


class IconCollector(object):
    def __init__(
            self, os: str, de: str,
            icon_theme: str, size: str, extension: str, path_copy: str
            ) -> None:
        
        self._os = os
        self._de = de
        self._icon_theme = icon_theme
        self._size = size
        self._path_to_copy = pathlib.Path(path_copy)
        self._extension = extension

        self._icon_naming_spec = icon_naming_spec.split('\n')
    
    def __str__(self) -> str:
        return "<class 'IconCollector'>"

    def collect(self) -> None:
        if not self._path_to_copy.exists():
            # Create if non exists
            # self._path_to_copy.mkdir(parents=True, exist_ok=True)
            print('Path to copy not exists!')
            sys.exit(1)

        size = f'{self._size}x{self._size}'
        if self._os == 'linux':
            # Gtk:     /usr/share/icons/icon-theme/22x22/actions/icon-name.svg
            # Qt:      /usr/share/icons/icon-theme/actions/22/icon-name.svg
            # Default: /usr/share/icons/hicolor/22x22/actions/icon-name.png
            if self._de == 'plasma':
                path = f'/usr/share/icons/icon-theme/actions/{self._size}'
            elif self._de == ['gnome', 'cinnamon']:
                # TODO: Gnome is scaled
                
                path = f'/usr/share/icons/icon-theme/{size}/actions'
            else:
                path = f'/usr/share/icons/hicolor/{size}/actions'

        # elif 'windows' in self._os_de.operational_system:
        #     pass
        # elif self._os_de.operational_system == 'mac':
        #     pass
        # elif self._os_de.operational_system == 'bsd':
        #     pass
        else:
            path = None

        if not path:
            print("Error! Icon path is 'None'")
            sys.exit(1)
        
        icons_path = pathlib.Path(
            path.replace('icon-theme', self._icon_theme))

        if not icons_path.exists():
            print(f'Error! Icon path not found: {icons_path}')
            sys.exit(1)

        founds = []
        for icon in icons_path.iterdir():
            if not icon.is_file():
                continue

            if icon.suffix != self._extension:
                print(f'Error! The extensions are "{icon.suffix}"')
                sys.exit(1)

            if icon.stem in self._icon_naming_spec:
                founds.append(icon.stem)
                shutil.copy2(icon, self._path_to_copy / icon.name)

                # item         ->  /home/user/docs/file.txt
                # item.parent  ->  /home/user/docs
                # item.name    ->  file.txt
                # item.stem    ->  file
                # item.suffix  ->  .txt

        not_founds = []
        for icon_name in self._icon_naming_spec:
            if icon_name and icon_name not in founds:
                not_founds.append(icon_name)
                print('Not found:  ', icon_name)
        
        if founds:
            print(f'\nFounds {len(founds)} icons! ', end='')
        if not_founds:
            print(f'Not found {len(not_founds)}', end='')

            with open(self._path_to_copy / '0_not_found.txt', 'w') as no_file:
                for not_found_file in not_founds:
                    no_file.write(f'{not_found_file}\n')
        
        print('\n\nCollected from:', icons_path)
        sys.exit(0)


if __name__ == '__main__':
    # dark = ''  # '-dark'
    # os = 'linux'
    # de = 'plasma'
    # icon_theme = f'breeze{dark}'
    # size = '16'
    # extension = '.svg'
    # path_to_copy = pathlib.Path(
    #     __file__).parent.parent / 'static' / 'icons' / f'linux{dark}'

    # print('OS:           ', os)
    # print('DE:           ', de)
    # print('Icon theme:   ', icon_theme)
    # print('Size:         ', size)
    # print('Extension:    ', extension)
    # print('Path to copy: ', path_to_copy)
    # print()

    # collect_icons = IconCollector(
    #     os, de, icon_theme, size, extension, path_to_copy)
    # collect_icons.collect()
    pass
