#!/usr/bin/env python3
from ..control import Signal, Timer


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
        
        if ui._base_class not in ('Layout', 'Cell', 'Control'):
            raise TypeError(
                'Layout only accepts Cell, Layout or Control objects.')
        
        if isinstance(ui, Timer):
            self._app._timers.append(ui)
            return

        if not isinstance(ui, Signal):
            self._uis.append(ui)
            ui._parent = self
            ui._app = self._app

        if ui._base_class == 'Cell':
            ui._drawer = self._app._drawer
        
        elif ui._base_class == 'Layout':
            ui._drawer = self._app._drawer
        return ui
