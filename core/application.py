#!/usr/bin/env python3
from ..mixin import Pos, Size
from ..frame import Frame

class Application(Pos, Size):
    """..."""
    def __init__(self, frame, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__frame = frame
        self.__app = None
        self.__name = 'Genesis'
        self.__title = None
        self.__size = 500, 400
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def app(self) -> int:
        """..."""
        return self.__app
    
    @app.setter
    def app(self, app: Frame) -> None:
        self.__app = app
    
    @property
    def name(self) -> str:
        """..."""
        return self.__name
    
    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
    
    @property
    def size(self) -> int:
        """..."""
        return self.__size
    
    @size.setter
    def size(self, size: tuple) -> None:
        self.__size = size
    
    @property
    def title(self) -> str:
        """..."""
        return self.__title
    
    @title.setter
    def title(self, title: str) -> None:
        self.__title = title
    
    def run(self) -> int:
        """..."""
        self.__app = self.__frame(
            title=self.__title if self.__title else self.__name,
            width=self.__size[0], height=self.__size[1])
        self.__app.run()
