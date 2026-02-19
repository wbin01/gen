#!/usr/bin/env python3


class Margin(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__margin = (0, 0, 0, 0)
        self.__margin_x = 0
        self.__margin_y = 0
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def margin(self) -> tuple:
        """..."""
        return self.__margin
    
    @margin.setter
    def margin(self, margin: tuple) -> None:
        self.__margin_x = margin[1] + margin[3]
        self.__margin_y = margin[0] + margin[2]
        self.__margin = margin
