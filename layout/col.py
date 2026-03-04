#!/usr/bin/env python3
from .box import Box


class Col(Box):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
