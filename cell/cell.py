#!/usr/bin/env python3


class Cell(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.parent = None
        self.__dirty = True
    
    def __invalidate(self) -> None:
        self.__dirty = True

        name = f'_{cell.__class__.__name__}__'
        setattr(self.parent, name + 'dirty', True)
    
    def __draw(self) -> None:
        pass
