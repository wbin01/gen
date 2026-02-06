#!/usr/bin/env python3
from ctypes import c_void_p, cast
import io

# python3 -m pip install --upgrade Pillow
from PIL import Image, ImageDraw, ImageFont
import sdl3


class FontRender:
    pass


class Drawer(object):
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

    def text(self, x: int, y: int, text: FontRender) -> None:
        surface = sdl3.SDL_CreateSurfaceFrom(
            text.width, text.height, sdl3.SDL_PIXELFORMAT_RGBA32,
            text._bytes, text.width * 4)
        
        texture = sdl3.SDL_CreateTextureFromSurface(self.__renderer, surface)
        sdl3.SDL_DestroySurface(surface)

        dst = sdl3.SDL_FRect(x, y, text.width, text.height)
        sdl3.SDL_RenderTexture(self.__renderer, texture, None, dst)
