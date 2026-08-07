#!/usr/bin/env python3


class Signal:
    """..."""
    def __init__(self, parent = None) -> None:
        """..."""
        self._parent = parent
        self._slots = []
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def connect(self, func):
        """..."""
        self._slots.append(func)

    def emit(self, *args, **kwargs):
        """..."""
        if not args: args = (self._parent,)
        for func in self._slots:
            func(*args, **kwargs)
