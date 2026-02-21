#!/usr/bin/env python3


class Add(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__uis = []
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(self, ui: UI) -> UI:
        """..."""
        return self.__add(ui)

    def __add(self, ui: UI) -> UI:
        if isinstance(ui, type):
            ui = ui()

        mro = str(type(ui).__mro__)
        if 'layout.layout.Layout' not in mro and 'cell.cell.Cell' not in mro:
            raise TypeError('Layout only accepts Cell or Layout.')
        
        self.__uis.append(ui)
        ui._UI__parent = self
        ui._UI__app = self._app

        if 'cell.cell.Cell' in mro:
            ui._Cell__drawer = self._app._Frame__drawer
        elif 'layout.layout.Layout' in mro:
            ui._Layout__drawer = self._app._Frame__drawer
        return ui
