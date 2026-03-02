#!/usr/bin/env python3

class Theme:
    classes = {
        'DEFAULT': {
            'BASE': {
                'text': (200, 200, 200, 255),
                'background': (66, 66, 86, 255),
                'border': (60, 100, 150, 255),
                },
            'HOVER': {
                'text': (200, 200, 200, 255),
                'background': (66, 66, 86, 255),
                'border': (60, 100, 150, 255),
                },
            'PRESSED': {
                'text': (200, 200, 200, 255),
                'background': (50, 90, 140, 255),
                'border': (60, 100, 150, 255),
                },
            }
    }

    Frame = {
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
    
    Button = {
        'BASE': {
            'text': (200, 200, 200, 255),
            'background': (40, 40, 40, 255),
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
            'background': (60, 100, 150, 255),
            'border': (60, 100, 150, 255),
            },
        }
    
    Empty = {
        'BASE': {
            'background': (40, 40, 40, 255),
            'border': (80, 80, 80, 255),
            'radius': 6,
            'padding': 10
            },
        'HOVER': {
            'background': (50, 50, 50, 255),
            'border': (60, 100, 150, 255),
            },
        'PRESSED': {
            'background': (60, 100, 150, 255),
            'border': (60, 100, 150, 255),
            },
        }
