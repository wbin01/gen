#!/usr/bin/env python3
from .core import Draw, Text


class AbsButton(object):
    def __init__(
            self, draw, text: str = '',
            x: int = 0, y: int = 0, w: int = 100, h: int = 32,
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
        self.__text = text
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__style = style

        self.__icon = None

        if self.__text:
            txt = Text(text)
            if self.__w < txt.width + 20: self.__w = txt.width + 20
            if self.__h < txt._height + 20: self.__h = txt._height + 20

            tx = self.__x + (self.__w // 2) - (txt.width // 2)
            ty = self.__y + (self.__h // 2) - (txt._height // 2)

            if self.__icon:
                tx -= 18
        
        self.__draw.rect(
            self.__x, self.__y, self.__w, self.__h,
            self.__style['ACTIVE']['border'],
            self.__style['ACTIVE']['radius'])
        
        self.__draw.rect(
            self.__x + 1, self.__y +1, self.__w - 2,self.__h - 2,
            self.__style['ACTIVE']['background'],
            self.__style['ACTIVE']['radius'] - 1)
        
        if self.__text:
            self.__draw.text(tx, ty, txt)
