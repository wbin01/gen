#!/usr/bin/env python3


class Core(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._base_class = 'UI'
        self._app = None
        self._parent = None
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def app(self) -> UI:
        return self._app
    
    @property
    def base_class(self) -> bool:
        """..."""
        return self._base_class
    
    @property
    def parent(self) -> UI:
        return self._parent
