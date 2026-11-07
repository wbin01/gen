#!/usr/bin/env python3
import math


def darken_rgba(color: tuple, step: int = 10) -> tuple:
    """Darken rgba color."""
    return tuple(
        [0 if x - step < 0 else x - step for x in color[:-1]] + [color[-1]])


def darken_hex(color: str, step: int = 10) -> str:
    """Darken hex color."""
    rgba_dark = darken_rgba(hex_to_rgba(color), step)
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        rgba_dark[3], rgba_dark[0], rgba_dark[1], rgba_dark[2])


def hex_to_rgba(color: str) -> tuple:
    """Convert hex color to rgba color."""
    color = color.lstrip('#')
    len_color = len(color)

    if len_color == 3:
        color = 'FF' + color + color
    elif len_color == 6:
        color = 'FF' + color
    
    return tuple(int(color[:8][x:x + 2], 16) for x in (2, 4, 6, 0))


def is_dark(color: tuple) -> bool:
    """If color is dark."""
    r, g, b, _ = color
    hsp = math.sqrt(0.299 * (r * r) + 0.587 * (g * g) + 0.114 * (b * b))
    return False if hsp > 127.5 else True


def lighten_rgba(color: tuple, step: int = 10) -> tuple:
    """Lighten rgba color."""
    return tuple(
        [255 if x + step > 255 else x + step for x in color[:-1]] +
        [color[-1]])


def lighten_hex(color: str, step: int = 10) -> str:
    """Lighten hex color."""
    rgba_light = lighten_rgba(hex_to_rgba(color), step)
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        rgba_light[3], rgba_light[0], rgba_light[1], rgba_light[2])


def rgba_str_to_tuple(rgba_str: str) -> tuple:
    """Convert rgba string to tuple.

    :param rgba_str: "* rgba(0, 0, 0, 0) *" or "(0, 0, 0, 0)" or "0, 0, 0, 0"
    """
    if '(' in rgba_str:
        rgba_str = rgba_str.replace(
            ' ', '').split('(')[-1].split(')')[0]

    rgba_str = rgba_str.split(',')
    if rgba_str[-1].startswith('0.'):
        alpha = round(int('0.95'.lstrip('0.')) * 2.55)
    elif rgba_str[-1].endswith('.0'):
        alpha = 255
    else:
        alpha = int(rgba_str[-1])

    return rgba_str[0], rgba_str[1], rgba_str[2], alpha


def rgba_to_hex(color: tuple) -> str:
    """Convert rgba color to hex color."""
    return "#{:02x}{:02x}{:02x}{:02x}".format(
        color[3], color[0], color[1], color[2])


def plasma_color_to_hex(plasma_rgba: str, alternative_hex: str = None) -> str:
    """Convert KDE Plasma color config to valid hex color."""
    if ',' not in plasma_rgba:
        return alternative_hex
    
    color = plasma_rgba.split(',')
    len_color = len(color)

    if len_color == 3:
        color = int(color[0]), int(color[1]), int(color[2]), 255
    else:
        color = int(color[0]), int(color[1]), int(color[2]), int(color[3])
    return rgba_to_hex(color)
