#!/usr/bin/env Python3
from ..mixin.core import Core


class Control(Core):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._base_class = 'Control'
