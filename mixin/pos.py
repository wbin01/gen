#!/usr/bin/env python3


class Pos(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__x = 0
        self.__y = 0
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def _x(self) -> int:
        """..."""
        return self.__x
    
    @property
    def _y(self) -> int:
        """..."""
        return self.__y
