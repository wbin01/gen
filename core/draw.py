#!/usr/bin/env python3
from ctypes import c_void_p, cast
import io

# python3 -m pip install --upgrade Pillow
from PIL import Image, ImageDraw, ImageFont
import sdl3


class Draw(object):
    """..."""
    def __init__(self, renderer) -> None:
        self.__renderer = renderer
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def image(self) -> None:
        """..."""
        pass

    def rect(self, x, y, w, h, color, r):
        tl = tr = br = bl = r
        rmax = min(w // 2, h // 2)
        tl = min(tl, rmax)
        tr = min(tr, rmax)
        br = min(br, rmax)
        bl = min(bl, rmax)

        sdl3.SDL_SetRenderDrawColor(self.__renderer, *color)

        # Middle
        sdl3.SDL_RenderFillRect(
            self.__renderer, sdl3.SDL_FRect(x + tl, y, w - tl - tr, h))
        
        # Left
        sdl3.SDL_RenderFillRect(
            self.__renderer, sdl3.SDL_FRect(x, y + tl, tl, h - tl - bl))
        
        # Right
        sdl3.SDL_RenderFillRect(
            self.__renderer,
            sdl3.SDL_FRect(x + w - tr, y + tr, tr, h - tr - br))

        # Corners circles
        if tl:
            self.__corner_filled_circle(x + tl, y + tl, tl)
        if tr:
            self.__corner_filled_circle(x + w - tr - 1, y + tr, tr)
        if br:
            self.__corner_filled_circle(x + w - br - 1, y + h - br - 1, br)
        if bl:
            self.__corner_filled_circle(x + bl, y + h - bl - 1, bl)
    
    def __corner_filled_circle(self, cx, cy, r):
        for dy in range(-r, r + 1):
            dx = int((r*r - dy*dy) ** 0.5)
            sdl3.SDL_RenderLine(
                self.__renderer, cx - dx, cy + dy, cx + dx, cy + dy)

    def text(self, x: int, y: int, text: str) -> None:
        text_bytes, w, h = self.__text_to_raster_bytes_font(text)
        surface = sdl3.SDL_CreateSurfaceFrom(
            w, h, sdl3.SDL_PIXELFORMAT_RGBA32, text_bytes, w * 4)
        texture = sdl3.SDL_CreateTextureFromSurface(self.__renderer, surface)
        sdl3.SDL_DestroySurface(surface)

        dst = sdl3.SDL_FRect(x, y, w, h)
        sdl3.SDL_RenderTexture(self.__renderer, texture, None, dst)
    
    def __text_to_raster_bytes_font(
            self,
            text: str,
            color: tuple = (200, 200, 200, 255),
            font: str = 'DejaVuSans.ttf',
            size: int = 12) -> None:
        
        font = ImageFont.truetype(font, size)

        bbox = font.getbbox(text)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        raster = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(raster)
        draw.text((-bbox[0], -bbox[1]), text, font=font, fill=color)

        pixels = raster.tobytes()
        w, h = raster.size
        return pixels, w, h

    def text_old(
            self, x: int, y: int, text: str, color: tuple = None,
            font: str = None, size: int = 12) -> None:
        """..."""
        if font:
            self.__font = self.__ttf.TTF_OpenFont(b'DejaVuSans.ttf', size)
        
        if color:
            self.__font_color = sdl3.SDL_Color(
                color[0], color[1], color[2], color[3])
        
        if text:
            self.__font_surface = self.__ttf.TTF_RenderUTF8_Blended(
                self.__font, str.encode('Hello world!'), self.__font_color)

        texture = sdl3.SDL_CreateTextureFromSurface(
            self.__renderer, cast(self.__font_surface, c_void_p))

        dst = sdl3.SDL_FRect(
            x, y, self.__font_surface.w, self.__font_surface.h)
        sdl3.SDL_RenderTexture(self.__renderer, texture, None, dst)

