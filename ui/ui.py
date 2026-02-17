#!/usr/bin/env python3


class UI(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__app = None
        self.__parent = None
        self.__dirty = True
    
    @property
    def _app(self) -> UI:
        return self.__app
    
    @property
    def _parent(self) -> UI:
        return self.__parent
    
    def __invalidate(self) -> None:
        self.__dirty = True

        name = f'_{self._parent.__class__.__name__}'
        setattr(self._parent, name + '__dirty', True)
