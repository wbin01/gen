#!/usr/bin/env python3


class Size(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__width = 100
        self.__height = 30
        self.__base_width = 100
        self.__base_height = 30
        # self.__fixed_width = False
        # self.__fixed_height = False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def width(self) -> int:
        """..."""
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width
        self.__base_width = width
        # self.__fixed_width = True if width else False

    @property
    def height(self) -> int:
        """..."""
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height = height
        self.__base_height = height
        # self.__fixed_height = True if height else False
