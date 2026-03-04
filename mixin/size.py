#!/usr/bin/env python3


class Size(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._width = 100
        self._height = 30
        self._base_width = 60
        self._base_height = 30

        self._min_width = 0
        self._min_height = 0

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def min_height(self) -> int:
        """..."""
        return self._min_height
    
    @min_height.setter
    def min_height(self, min_height: int) -> None:
        self._min_height = min_height
    
    @property
    def min_width(self) -> int:
        """..."""
        return self._min_width
    
    @min_width.setter
    def min_width(self, min_width: int) -> None:
        self._min_width = min_width
    
    @property
    def width(self) -> int:
        """..."""
        return self._width
    
    @width.setter
    def width(self, width: int) -> None:
        self._width = width
        self._base_width = width

    @property
    def height(self) -> int:
        """..."""
        return self._height
    
    @height.setter
    def height(self, height: int) -> None:
        self._height = height
        self._base_height = height
