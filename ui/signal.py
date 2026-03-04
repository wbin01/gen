#!/usr/bin/env python3


class Signal:
    def __init__(self):
        self.__slots = []

    def connect(self, func):
        """..."""
        self.__slots.append(func)

    def emit(self, *args, **kwargs):
        """..."""
        for func in self.__slots:
            func(*args, **kwargs)
