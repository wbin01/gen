#!/usr/bin/env python3
from .core import Draw


class AbsButton(object):
    def __init__(
            self, draw, x: int = 0, y: int = 0, w: int = 100, h: int = 32,
            style: dict = {
                'ACTIVE': {
                    'text': (200, 200, 200, 255),
                    'background': (50, 50, 50, 255),
                    'border': (100, 100, 100, 255),
                    'radius': 4
                    },
                'HOVER': {
                    'text': (200, 200, 200, 255),
                    'background': (50, 50, 50, 255),
                    'border': (100, 100, 100, 255),
                    },
                'CLICKED': {
                    'text': (200, 200, 200, 255),
                    'background': (50, 50, 50, 255),
                    'border': (100, 100, 100, 255),
                    },
                }) -> None:
        """..."""
        self.__draw = draw
        self.__style = style
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h

        self.__draw.rect(
            self.__x, self.__y, self.__w, self.__h,
            self.__style['ACTIVE']['border'],
            self.__style['ACTIVE']['radius'])
        
        self.__draw.rect(
            self.__x + 1, self.__y +1, self.__w - 2,self.__h - 2,
            self.__style['ACTIVE']['background'],
            self.__style['ACTIVE']['radius'] - 1)
