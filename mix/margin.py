#!/usr/bin/env python3


class Margin(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__margin = 10
    
    def __repr__(self) -> str:
        return self.__class__.__name__
    
    @property
    def margin(self) -> int:
        """..."""
        return self.__margin
    
    @margin.setter
    def margin(self, margin: int) -> None:
        self.__margin = margin
