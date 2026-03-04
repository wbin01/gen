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
            padding: int = 20,
            *args, **kwargs) -> None:
        """..."""
        self._text = text
        self._color = color
        self._font = font
        self._size = size
        self._width_to_elided = width_to_elided
        self._pad = padding

        self._bytes = None
        self._width = None
        self._height = None
        self._text_to_bytes()
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._text!r})'

    def __str__(self) -> str:
        return self._text
    
    @property
    def text(self) -> str:
        """..."""
        return self._text
    
    @text.setter
    def text(self, text: str) -> None:
        self._text = text
    
    @property
    def height(self) -> int:
        """..."""
        return self._height
    
    @height.setter
    def height(self, height: int) -> None:
        self._height = height
    
    @property
    def width(self) -> int:
        return self._width
    
    @width.setter
    def width(self, width: int) -> None:
        self._width = width
    
    @property
    def to_bytes(self) -> bytes:
        return self._bytes
    
    def update(self) -> None:
        """..."""
        self._text_to_bytes()
    
    def _text_to_bytes(self) -> None:
        
        font = ImageFont.truetype(self._font, self._size)

        bbox = font.getbbox(self._text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if self._width_to_elided and w + self._pad > self._width_to_elided:
            w = self._width_to_elided - self._pad

        raster = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(raster)
        draw.text(
            (-bbox[0], -bbox[1]), self._text, font=font, fill=self._color)

        self._bytes = raster.tobytes()
        self._width, self._height = raster.size
