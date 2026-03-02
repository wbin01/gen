#!/usr/bin/env python3

class Theme:
    classes = {}

    frame = {
        'BASE': {
            'text': (200, 200, 200, 255),
            'background': (20, 20, 20, 240),
            'border': (55, 55, 55, 200),
            'radius': 8,
            'font': 'DejaVuSans.ttf',
            'font-size': 12,
            'padding': 10
            },
        }
    
    button = {
        'BASE': {
            'text': (200, 200, 200, 255),
            'background': (40, 40, 40, 250),
            'border': (80, 80, 80, 255),
            'radius': 6,
            'font': 'DejaVuSans.ttf',
            'font-size': 12,
            'padding': 10
            },
        'HOVER': {
            'text': (200, 200, 200, 255),
            'background': (50, 50, 50, 255),
            'border': (60, 100, 150, 255),
            },
        'PRESSED': {
            'text': (200, 200, 200, 255),
            'background': (60, 100, 150, 50),
            'border': (60, 100, 150, 255),
            },
        }
    
    empty = {
        'BASE': {
            'background': (40, 40, 40, 250),
            'border': (80, 80, 80, 255),
            'radius': 6,
            'padding': 10
            },
        'HOVER': {
            'background': (50, 50, 50, 255),
            'border': (60, 100, 150, 255),
            },
        'PRESSED': {
            'background': (60, 100, 150, 50),
            'border': (60, 100, 150, 255),
            },
        }
