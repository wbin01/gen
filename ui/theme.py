#!/usr/bin/env python3

class Theme:
    classes = {
        'DEFAULT': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (40, 50, 70, 255),
                'border-color': (60, 100, 150, 255),
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (50, 63, 88, 255),
                'border-color': (60, 100, 150, 255),
                },
            'PRESSED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (60, 80, 100, 255),
                'border-color': (60, 100, 150, 255),
                },
            },
        
        'ERROR': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (70, 40, 50, 255),
                'border-color': (150, 60, 100, 255),
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (88, 50, 63, 255),
                'border-color': (150, 60, 100, 255),
                },
            'PRESSED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (100, 60, 80, 255),
                'border-color': (150, 60, 100, 255),
                },
            },
        
        'SUCCESS': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (40, 70, 50, 255),
                'border-color': (60, 150, 100, 255),
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (50, 88, 63, 255),
                'border-color': (60, 150, 100, 255),
                },
            'PRESSED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (60, 100, 80, 255),
                'border-color': (60, 150, 100, 255),
                },
            },
        
        'WARNING': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (55, 55, 30, 255),
                'border-color': (110, 95, 35, 255),
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (65, 65, 32, 255),
                'border-color': (110, 95, 35, 255),
                },
            'PRESSED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (80, 80, 40, 255),
                'border-color': (110, 95, 35, 255),
                },
            },
    }

    Frame = {
        'BASE': {
            'background-color': (20, 20, 20, 240),
            'border': 1,
            'border-color': (55, 55, 55, 200),
            'radius': 8,
            },
        }
    
    Button = {
        'BASE': {
            'background-color': (40, 40, 40, 255),
            'border': 1,
            'border-color': (80, 80, 80, 255),
            'radius': 6,
            'font': 'DejaVuSans.ttf',
            'font-size': 12,
            'font-color': (200, 200, 200, 255),
            'padding': 10
            },
        'HOVER': {
            'font-color': (200, 200, 200, 255),
            'background-color': (40, 45, 55, 255),
            'border-color': (60, 100, 150, 255),
            },
        'PRESSED': {
            'font-color': (200, 200, 200, 255),
            'background-color': (50, 63, 88, 255),
            'border-color': (60, 100, 150, 255),
            },
        }
    
    Empty = {
        'BASE': {
            'background-color': (40, 40, 40, 255),
            'border': 1,
            'border-color': (80, 80, 80, 255),
            'radius': 6,
            },
        'HOVER': {
            'background-color': (50, 50, 50, 255),
            'border-color': (60, 100, 150, 255),
            },
        'PRESSED': {
            'background-color': (60, 100, 150, 255),
            'border-color': (60, 100, 150, 255),
            },
        }
