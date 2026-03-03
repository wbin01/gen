#!/usr/bin/env python3


class Size(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__width = 100
        self.__height = 30
        self.__base_width = 60
        self.__base_height = 30

        self.__min_width = 0
        self.__min_height = 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def min_height(self) -> int:
        """..."""
        return self.__min_height
    
    @min_height.setter
    def min_height(self, min_height: int) -> None:
        self.__min_height = min_height
    
    @property
    def min_width(self) -> int:
        """..."""
        return self.__min_width
    
    @min_width.setter
    def min_width(self, min_width: int) -> None:
        self.__min_width = min_width
    
    @property
    def width(self) -> int:
        """..."""
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width
        self.__base_width = width

    @property
    def height(self) -> int:
        """..."""
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height = height
        self.__base_height = height
