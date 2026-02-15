#!/usr/bin/env python3


class UI(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__x = 0
        self.__y = 0
        self.__width = 100
        self.__height = 30
    
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
    
    @property
    def width(self) -> int:
        """..."""
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width

    @property
    def height(self) -> int:
        """..."""
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height = height
