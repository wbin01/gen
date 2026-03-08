#!/usr/bin/env Python3
from ..ui import UI


class Control(UI):
    def __init__(self, *args, **kwargs) -> None:
        self._base_class = 'Control'
