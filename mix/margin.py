#!/usr/bin/env python3


class Margin(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__margin = (0, 0, 0, 0)
    
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
        self.__margin = margin
