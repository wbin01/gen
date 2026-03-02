#!/usr/bin/env python3
import io
import math

# python3 -m pip install --upgrade Pillow
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageDraw2
import pyscreenshot as ImageGrab

import sdl3


class FontRender:
    pass


class Drawer(object):
    """..."""
    def __init__(self, renderer, *args, **kwargs) -> None:
        self.__renderer = renderer
        self.__light = True
        self.__visual_level = 2
        
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__

    def image(self) -> None:
        """..."""
        pass

    def rect(
            self, x: int, y: int, w: int, h: int,
            color=(0, 0, 0, 255), r: int = 8, aa: int = 1) -> None:
        """..."""
        if self.__visual_level >= 1:
            self.__rounded_rect_antialiasing(x, y, w, h, color, r)
        else:
            self.__rounded_rect(x, y, w, h, color, r)
    
    def text(self, x: int, y: int, text: FontRender) -> None:
        """..."""
        surface = sdl3.SDL_CreateSurfaceFrom(
            text.width, text.height, sdl3.SDL_PIXELFORMAT_RGBA32,
            text._bytes, text.width * 4)
        
        texture = sdl3.SDL_CreateTextureFromSurface(self.__renderer, surface)
        sdl3.SDL_DestroySurface(surface)

        dst = sdl3.SDL_FRect(x, y, text.width, text.height)
        sdl3.SDL_RenderTexture(self.__renderer, texture, None, dst)

    def __rounded_rect_antialiasing(
            self, x: int, y: int, w: int, h: int,
            color=(0, 0, 0, 255), r: int = 8, aa: int = 1) -> None:

        w, h = int(w), int(h)
        r = min(r, (w - 1)//2, (h - 1)//2)
        if (w - 2*r) % 2 != 0: w -= 1

        cr, cg, cb, ca = color
        r = min(r, w // 2, h // 2)
        sdl3.SDL_SetRenderDrawColor(self.__renderer, cr, cg, cb, ca)

        # Body
        sdl3.SDL_RenderFillRect(
            self.__renderer, sdl3.SDL_FRect(x + r, y, w - 2*r, h))

        sdl3.SDL_RenderFillRect(
            self.__renderer,sdl3.SDL_FRect(x, y + r, w, h - 2*r))

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
                        sdl3.SDL_RenderPoint(self.__renderer, px, py)
        # AA
        if aa > 0:
            sdl3.SDL_SetRenderDrawBlendMode(
                self.__renderer, sdl3.SDL_BLENDMODE_BLEND)

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
                                    self.__renderer, cr, cg, cb, alpha)
                                px = cx + dx * sx
                                py = cy + dy * sy
                                sdl3.SDL_RenderPoint(self.__renderer, px, py)

            sdl3.SDL_SetRenderDrawBlendMode(
                self.__renderer, sdl3.SDL_BLENDMODE_NONE)
        # SDL2
        #     SDL_RenderDrawLine
        #     SDL_RenderDrawPoint
        # SDL3 (float)
        #     SDL_RenderLine
        #     SDL_RenderPoint
        #     SDL_RenderLines
        #     SDL_RenderPoints

    def __rounded_rect(
            self, x, y, w, h, color, r: int = 0,
            top_left: int = None, top_right: int = None,
            bottom_right: int = None, bottom_left: int = None):

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
        r = int(r)
        for dy in range(-r, r + 1):
            dx = int((r*r - dy*dy) ** 0.5)
            sdl3.SDL_RenderLine(
                self.__renderer, cx - dx, cy + dy, cx + dx, cy + dy)
    
    def screen_texture(self, x, y, w, h, r) -> None:
        # import mss
        # import mss.tools
        #
        # with mss.mss() as sct:
        #     monitor = sct.monitors[1]
        #     im = sct.grab(monitor)
        #     mss.tools.to_png(im.rgb, im.size, output='screenshot_mss.png')


        im = ImageGrab.grab(bbox=(int(x), int(y), w+(w//3), h+(h//3)))
        # im.save('screen.png')
        blurred = im.filter(ImageFilter.GaussianBlur(radius=8))

        mask = Image.new("L", blurred.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle(
            (0, 0, blurred.width, blurred.height), radius=r, fill=255)

        # aplica como alpha
        blurred.putalpha(mask)

        # small = im.resize(
        #     (im.width // 2, im.height // 2), resample=Image.BILINEAR)
        # blurred = small.resize((im.width, im.height), resample=Image.BILINEAR)

        # enhancer = ImageEnhance.Color(blurred)
        # blurred = enhancer.enhance(0.8)

        data = blurred.tobytes()
        # SDL_PIXELFORMAT_RGBA8888
        # 370546692
        # SDL_PIXELFORMAT_BGRA8888
        # SDL_PIXELFORMAT_ARGB8888

        texture = sdl3.SDL_CreateTexture(
            self.__renderer,
            sdl3.SDL_PIXELFORMAT_RGBA32,
            sdl3.SDL_TEXTUREACCESS_STATIC,
            blurred.width, blurred.height)

        sdl3.SDL_UpdateTexture(texture, None, data, blurred.width * 4)

        sdl3.SDL_SetTextureBlendMode(texture, sdl3.SDL_BLENDMODE_BLEND)
        sdl3.SDL_RenderTexture(self.__renderer, texture, None, None)

        return texture
    
    def build_texture(self, w, h, draw, state = None) -> None:
        texture = sdl3.SDL_CreateTexture(
            self.__renderer,
            sdl3.SDL_PIXELFORMAT_RGBA32,
            sdl3.SDL_TEXTUREACCESS_TARGET,
            w, h)
        
        sdl3.SDL_SetTextureScaleMode(texture, sdl3.SDL_SCALEMODE_LINEAR)

        old_target = sdl3.SDL_GetRenderTarget(self.__renderer)
        sdl3.SDL_SetRenderTarget(self.__renderer, texture)

        sdl3.SDL_SetRenderDrawColor(self.__renderer, 0, 0, 0, 0)
        sdl3.SDL_RenderClear(self.__renderer)

        if state:
            draw(state)
        else:
            draw()

        sdl3.SDL_SetRenderTarget(self.__renderer, old_target)
        
        return texture
    
    def set_texture(self, texture, x, y, w, h) -> None:
        dest = sdl3.SDL_FRect(x, y, w, h)
        sdl3.SDL_RenderTexture(self.__renderer, texture, None, dest)
