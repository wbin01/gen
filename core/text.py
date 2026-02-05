#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
# python3 -m pip install --upgrade Pillow


class Text(object):
    """..."""
    def __init__(
            self, text: str,
            width_to_elided: int = 0, padding: int = 20) -> None:
        """..."""
        self.__text = text
        self.__width_to_elided = width_to_elided
        self.__pad = padding

        self.__bytes = None
        self.__width = None
        self.__height = None
        self.__text_to_bytes(text)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__text!r})'

    def __str__(self) -> str:
        return self.__text
    
    @property
    def text(self) -> str:
        """..."""
        return self.__text
    
    @text.setter
    def text(self, text: str) -> None:
        self.__text = text
        self.__text_to_bytes(text)
    
    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width

    @property
    def _bytes(self) -> bytes:
        return self.__bytes
    
    @property
    def _height(self) -> int:
        return self.__height

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __text_to_bytes(
            self,
            text: str,
            color: tuple = (200, 200, 200, 255),
            font: str = 'DejaVuSans.ttf',
            size: int = 12) -> None:
        
        font = ImageFont.truetype(font, size)

        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if self.__width_to_elided and w + self.__pad > self.__width_to_elided:
            w = self.__width_to_elided - self.__pad

        raster = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(raster)
        draw.text((-bbox[0], -bbox[1]), text, font=font, fill=color)

        self.__bytes = raster.tobytes()
        self.__width, self.__height = raster.size
