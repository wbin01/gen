#!/usr/bin/env python3
from ..control import Signal, Timer


class Add(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._objects = []
        self._objects_height = 0
        self._objects_width = 0
        self._height_free = 0
        self._width_free = 0
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def add(self, obj: UIObject) -> UIObject:
        """..."""
        return self._add(obj)

    def _add(self, obj: UIObject) -> UIObject:
        if isinstance(obj, type):
            obj = obj()
        
        if obj._base_class not in ('Layout', 'Cell', 'Control'):
            raise TypeError(
                'Layout only accepts Cell, Layout or Control objects.')
        
        obj._parent = self
        obj._app = self._app

        if not isinstance(obj, Signal):
            self._objects.append(obj)
        
        if isinstance(obj, Timer):
            self._app._timers.append(obj)
            return

        if obj._base_class == 'Cell':
            obj._drawer = self._app._drawer

            if hasattr(obj, '_timer') and isinstance(obj._timer, Timer):
                self._app._timers.append(obj._timer)
                obj._timer._parent = self
                obj._timer._app = self._app

            if obj._timer:
                self._app._timers.append(obj._timer)
        
        elif obj._base_class == 'Layout':
            obj._drawer = self._app._drawer
        return obj
