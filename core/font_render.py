#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
# python3 -m pip install --upgrade Pillow


class FontRender(object):
    """..."""
    def __init__(
            self,
            text: str,
            color: tuple = (200, 200, 200, 255),
            font: str = 'DejaVuSans.ttf',
            size: int = 12,
            width_to_elided: int = 0,
            padding: int = 20) -> None:
        """..."""
        self.__text = text
        self.__color = color
        self.__font = font
        self.__size = size
        self.__width_to_elided = width_to_elided
        self.__pad = padding

        self.__bytes = None
        self.__width = None
        self.__height = None
        self.__text_to_bytes()
    
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
    
    @property
    def height(self) -> int:
        """..."""
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height = height
    
    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def width(self, width: int) -> None:
        self.__width = width

    @property
    def _bytes(self) -> bytes:
        return self.__bytes
    
    def update(self) -> None:
        """..."""
        self.__text_to_bytes()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def __text_to_bytes(self) -> None:
        
        font = ImageFont.truetype(self.__font, self.__size)

        bbox = font.getbbox(self.__text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if self.__width_to_elided and w + self.__pad > self.__width_to_elided:
            w = self.__width_to_elided - self.__pad

        raster = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(raster)
        draw.text(
            (-bbox[0], -bbox[1]), self.__text, font=font, fill=self.__color)

        self.__bytes = raster.tobytes()
        self.__width, self.__height = raster.size
