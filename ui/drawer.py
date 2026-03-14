#!/usr/bin/env python3
import ctypes
import io
import math

# python3 -m pip install --upgrade Pillow
from PIL import Image, ImageDraw
import pyscreenshot as ImageGrab

import sdl3


class Drawer(object):
    """..."""
    def __init__(self, renderer, *args, **kwargs) -> None:
        self._renderer = renderer
        self._visual_level = 2

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    def apply_texture(self, texture, x, y, w, h) -> None:
        dest = sdl3.SDL_FRect(x, y, w, h)
        sdl3.SDL_RenderTexture(self._renderer, texture, None, dest)
    
    def clip_start(self, obj, viewport) -> None:
        mx = my = 0
        if viewport._fill == 'X': mx = obj.margin[1] + obj.margin[3]
        if viewport._fill == 'Y': my = obj.margin[0] + obj.margin[2]

        sdl3.SDL_RenderClipEnabled(self._renderer)
        clip = sdl3.SDL_Rect(
            obj._x, obj._y, viewport.width - mx, viewport.height - my)
        sdl3.SDL_SetRenderClipRect(self._renderer, ctypes.byref(clip))

    def clip_end(self) -> None:
        sdl3.SDL_SetRenderClipRect(
            self._renderer, ctypes.POINTER(sdl3.SDL_Rect)())
    
    def font(
            self, text, texture, font, size, color, elided=False, total_width=0
            ) -> tuple:
        font_hide = 'Hhqg'
        font_hide_box = font.getbbox(font_hide)

        text += font_hide
        bbox = font.getbbox(text if text else ' ')
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if h < size: h = size
        w -= font_hide_box[2] - font_hide_box[0]

        if elided:
            if w > total_width: w = total_width
        
        if h < 1: h = 1
        if w < 1: w = 1
        img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        draw.text((-bbox[0], -bbox[1]), text, font=font, fill=color)

        raw_bytes = img.tobytes()

        surface = sdl3.SDL_CreateSurfaceFrom(
            w, h, sdl3.SDL_PIXELFORMAT_RGBA32, raw_bytes, w * 4)

        if texture:
            sdl3.SDL_DestroyTexture(texture)

        texture = sdl3.SDL_CreateTextureFromSurface(self._renderer, surface)
        sdl3.SDL_DestroySurface(surface)

        return texture, w, h
    
    def font_cursor(self, x, y, size, cursor_x, color) -> None:
        sdl3.SDL_SetRenderDrawColor(
            self._renderer, color[0], color[1], color[2], color[3])
        
        cursor_x = x + cursor_x
        sdl3.SDL_RenderLine(
            self._renderer, cursor_x, y, cursor_x, y + size)

    def image(self) -> None:
        """..."""
        pass

    def rect(
            self, x: int, y: int, w: int, h: int,
            color=(0, 0, 0, 255), r: int = 8, aa: int = 1) -> None:
        """..."""
        if h < 1: h = 1
        if w < 1: w = 1
        if self._visual_level >= 1:
            self._rounded_rect_antialiasing(x, y, w, h, color, r)
        else:
            self._rounded_rect(x, y, w, h, color, r)
    
    def texture(self, texture, w, h, draw, state = None) -> None:
        if h < 1: h = 1
        if w < 1: w = 1

        if texture: sdl3.SDL_DestroyTexture(texture)

        texture = sdl3.SDL_CreateTexture(
            self._renderer,
            sdl3.SDL_PIXELFORMAT_RGBA32,
            sdl3.SDL_TEXTUREACCESS_TARGET,
            w, h)
        
        sdl3.SDL_SetTextureScaleMode(texture, sdl3.SDL_SCALEMODE_LINEAR)

        old_target = sdl3.SDL_GetRenderTarget(self._renderer)
        sdl3.SDL_SetRenderTarget(self._renderer, texture)

        sdl3.SDL_SetRenderDrawColor(self._renderer, 0, 0, 0, 0)
        sdl3.SDL_RenderClear(self._renderer)

        # if blend:
        #     sdl3.SDL_SetRenderDrawBlendMode(
        #         self._renderer, sdl3.SDL_BLENDMODE_AD)
        if state:
            draw(state)
        else:
            draw()
        # sdl3.SDL_SetRenderDrawBlendMode(
        #     self._renderer, sdl3.SDL_BLENDMODE_NONE)

        sdl3.SDL_SetRenderTarget(self._renderer, old_target)
        
        return texture
    
    def reset_texture(self, texture) -> None:
        if texture: sdl3.SDL_DestroyTexture(texture)
        return None
    
    def _corner_filled_circle(self, cx, cy, r):
        r = int(r)
        for dy in range(-r, r + 1):
            dx = int((r*r - dy*dy) ** 0.5)
            sdl3.SDL_RenderLine(
                self._renderer, cx - dx, cy + dy, cx + dx, cy + dy)
    
    def _rounded_rect(
            self, x, y, w, h, color, r: int = 0,
            top_left: int = None, top_right: int = None,
            bottom_right: int = None, bottom_left: int = None):

        tl = tr = br = bl = r
        rmax = min(w // 2, h // 2)
        tl = min(tl, rmax)
        tr = min(tr, rmax)
        br = min(br, rmax)
        bl = min(bl, rmax)

        sdl3.SDL_SetRenderDrawColor(self._renderer, *color)

        # Middle
        sdl3.SDL_RenderFillRect(
            self._renderer, sdl3.SDL_FRect(x + tl, y, w - tl - tr, h))
        
        # Left
        sdl3.SDL_RenderFillRect(
            self._renderer, sdl3.SDL_FRect(x, y + tl, tl, h - tl - bl))
        
        # Right
        sdl3.SDL_RenderFillRect(
            self._renderer,
            sdl3.SDL_FRect(x + w - tr, y + tr, tr, h - tr - br))

        # Corners circles
        if tl:
            self._corner_filled_circle(x + tl, y + tl, tl)
        if tr:
            self._corner_filled_circle(x + w - tr - 1, y + tr, tr)
        if br:
            self._corner_filled_circle(x + w - br - 1, y + h - br - 1, br)
        if bl:
            self._corner_filled_circle(x + bl, y + h - bl - 1, bl)

    def _rounded_rect_antialiasing(
            self, x: int, y: int, w: int, h: int,
            color=(0, 0, 0, 255), r: int = 8, aa: int = 1) -> None:

        w, h = int(w), int(h)
        r = min(r, (w - 1)//2, (h - 1)//2)
        if (w - 2*r) % 2 != 0: w -= 1

        cr, cg, cb, ca = color
        r = min(r, w // 2, h // 2)
        sdl3.SDL_SetRenderDrawColor(self._renderer, cr, cg, cb, ca)

        # Body
        sdl3.SDL_RenderFillRect(
            self._renderer, sdl3.SDL_FRect(x + r, y, w - 2*r, h))

        sdl3.SDL_RenderFillRect(
            self._renderer,sdl3.SDL_FRect(x, y + r, w, h - 2*r))

        # Center
        corners = [
            (x + r,         y + r,         -1, -1),  # TL
            (x + w - r - 1, y + r,          1, -1),  # TR
            (x + r,         y + h - r - 1, -1,  1),  # BL
            (x + w - r - 1, y + h - r - 1,  1,  1)]  # BR

        # Circle (1/4 fill)
        for cx, cy, sx, sy in corners:
            for dy in range(0, r):  # range(0, r+1):
                for dx in range(0, r):  # range(0, r+1):
                    if dx*dx + dy*dy <= r*r:
                        px = cx + dx * sx
                        py = cy + dy * sy
                        sdl3.SDL_RenderPoint(self._renderer, px, py)
        # AA
        if aa > 0:
            sdl3.SDL_SetRenderDrawBlendMode(
                self._renderer, sdl3.SDL_BLENDMODE_BLEND)

            for cx, cy, sx, sy in corners:
                for dy in range(0, r+aa+1):
                    for dx in range(0, r+aa+1):

                        dist2 = dx*dx + dy*dy
                        r2 = r*r
                        outer2 = (r+aa)*(r+aa)

                        if r2 < dist2 <= outer2:
                            dist = math.sqrt(dist2)
                            edge = (r + aa) - dist
                            alpha = int(ca * (edge / aa))

                            if alpha > 0:
                                sdl3.SDL_SetRenderDrawColor(
                                    self._renderer, cr, cg, cb, alpha)
                                px = cx + dx * sx
                                py = cy + dy * sy
                                sdl3.SDL_RenderPoint(self._renderer, px, py)

            sdl3.SDL_SetRenderDrawBlendMode(
                self._renderer, sdl3.SDL_BLENDMODE_NONE)
        # SDL2
        #     SDL_RenderDrawLine
        #     SDL_RenderDrawPoint
        # SDL3 (float)
        #     SDL_RenderLine
        #     SDL_RenderPoint
        #     SDL_RenderLines
        #     SDL_RenderPoints
