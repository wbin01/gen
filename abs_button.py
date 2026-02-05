#!/usr/bin/env python3
from .core import Draw, Text


class AbsButton(object):
    def __init__(
            self, draw, text: str = '',
            x: int = 0, y: int = 0, w: int = 100, h: int = 32,
            style: dict = {
                'NORMAL': {
                    'text': (200, 200, 200, 255),
                    'background': (40, 40, 40, 255),
                    'border': (80, 80, 80, 255),
                    'radius': 4,
                    'font-size': 12,
                    'padding': 10
                    },
                'HOVER': {
                    'text': (200, 200, 200, 255),
                    'background': (40, 40, 40, 255),
                    'border': (80, 80, 80, 255),
                    },
                'CLICKED': {
                    'text': (200, 200, 200, 255),
                    'background': (40, 40, 40, 255),
                    'border': (80, 80, 80, 255),
                    },
                }, elided: bool = False) -> None:
        """..."""
        self.__draw = draw
        self.__text = text
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__style = style
        self.__elided = elided

        self.__icon = None

        pad = self.__style['NORMAL']['padding'] * 2

        if self.__text:
            txt = Text(text, self.__w if self.__elided else None, pad)
            if self.__w < txt.width + pad: self.__w = txt.width + pad
            if self.__h < txt._height + pad: self.__h = txt._height + pad

            tx = self.__x + (self.__w // 2) - (txt.width // 2)
            ty = self.__y + (self.__h // 2) - (txt._height // 2)

            if self.__icon:
                tx -= 18
        
        self.__draw.rect(
            self.__x, self.__y, self.__w, self.__h,
            self.__style['NORMAL']['border'],
            self.__style['NORMAL']['radius'])
        
        self.__draw.rect(
            self.__x + 1, self.__y +1, self.__w - 2,self.__h - 2,
            self.__style['NORMAL']['background'],
            self.__style['NORMAL']['radius'] - 1)
        
        if self.__text:
            self.__draw.text(tx, ty, txt)
