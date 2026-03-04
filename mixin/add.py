#!/usr/bin/env python3


class Add(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._uis = []
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(self, ui: UI) -> UI:
        """..."""
        return self._add(ui)

    def _add(self, ui: UI) -> UI:
        if isinstance(ui, type):
            ui = ui()

        mro = str(type(ui).__mro__)
        if 'layout.layout.Layout' not in mro and 'cell.cell.Cell' not in mro:
            raise TypeError('Layout only accepts Cell or Layout.')
        
        self._uis.append(ui)
        ui._parent = self
        ui._app = self._app

        if 'cell.cell.Cell' in mro:
            ui._drawer = self._app._drawer
        elif 'layout.layout.Layout' in mro:
            ui._drawer = self._app._drawer
        return ui
