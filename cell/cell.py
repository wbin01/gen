#!/usr/bin/env python3
from ..ui import UI


class Cell(UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__parent = None
        self.__dirty = True
    
    @property
    def _parent(self) -> UI:
        return self.__parent
    
    def __invalidate(self) -> None:
        self.__dirty = True

        name = f'_{cell.__class__.__name__}'
        setattr(self.parent, name + '__dirty', True)
    
    def __draw(self) -> None:
        pass
