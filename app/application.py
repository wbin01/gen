#!/usr/bin/env python3
from ..mixin import Pos, Size
from ..frame import Frame

class Application(Pos, Size):
    """..."""
    def __init__(self, frame, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._frame = frame
        self._app = None
        self._name = 'Genesis'
        self._title = None
        self._size = 500, 400
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def app(self) -> int:
        """..."""
        return self._app
    
    @app.setter
    def app(self, app: Frame) -> None:
        self._app = app
    
    @property
    def name(self) -> str:
        """..."""
        return self._name
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
    
    @property
    def size(self) -> int:
        """..."""
        return self._size
    
    @size.setter
    def size(self, size: tuple) -> None:
        self._size = size
    
    @property
    def title(self) -> str:
        """..."""
        return self._title
    
    @title.setter
    def title(self, title: str) -> None:
        self._title = title
    
    def run(self) -> int:
        """..."""
        self._app = self._frame(
            title=self._title if self._title else self._name,
            width=self._size[0], height=self._size[1])
        self._app.run()
