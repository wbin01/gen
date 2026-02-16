#!/usr/bin/env python3


class Padding(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__padding = 0
    
    def __repr__(self) -> str:
        return self.__class__.__name__
    
    @property
    def padding(self) -> int:
        """..."""
        return self.__padding
    
    @padding.setter
    def padding(self, padding: int) -> None:
        self.__padding = padding
