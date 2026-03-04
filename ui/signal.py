#!/usr/bin/env python3


class Signal:
    def __init__(self):
        self._slots = []

    def connect(self, func):
        """..."""
        self._slots.append(func)

    def emit(self, *args, **kwargs):
        """..."""
        for func in self._slots:
            func(*args, **kwargs)
