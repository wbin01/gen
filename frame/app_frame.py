#!/usr/bin/env python3
from .sys_frame import SysFrame


class AppFrame(SysFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
