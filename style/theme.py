#!/usr/bin/env python3

class Theme:
    classes = {}

    frame = {
        'NORMAL': {
            'text': (200, 200, 200, 255),
            'background': (20, 20, 20, 255),
            'border': (55, 55, 55, 255),
            'radius': 8,
            'font': 'DejaVuSans.ttf',
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
        }
    
    button = {
        'NORMAL': {
            'text': (200, 200, 200, 255),
            'background': (40, 40, 40, 255),
            'border': (80, 80, 80, 255),
            'radius': 4,
            'font': 'DejaVuSans.ttf',
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
        }
