#!/usr/bin/env python3


class Size(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__width = 100
        self.__height = 30
    
    def __repr__(self) -> str:
        return self.__class__.__name__
    
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
