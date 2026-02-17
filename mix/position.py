#!/usr/bin/env python3


class Position(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__x = 0
        self.__y = 0
    
    def __repr__(self) -> str:
        return self.__class__.__name__
    
    @property
    def x(self) -> int:
        """..."""
        return self.__x
    
    @x.setter
    def x(self, x: int) -> None:
        self.__x = x
    
    @property
    def y(self) -> int:
        """..."""
        return self.__y
    
    @y.setter
    def y(self, y: int) -> None:
        self.__y = y
