#!/usr/bin/env python3


class Core(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._base_class = 'UIObject'
        self._app = None
        self._parent = None
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def app(self) -> UIObject:
        return self._app
    
    @property
    def base_class(self) -> bool:
        """..."""
        return self._base_class
    
    @property
    def parent(self) -> UIObject:
        return self._parent
