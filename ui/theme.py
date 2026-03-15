#!/usr/bin/env python3

class Theme:
    Frame = {
        'BASE': {
            'background-color': (20, 20, 20, 240),
            'border': 1,
            'border-color': (55, 55, 55, 200),
            'radius': 8,
            'accent-color': (60, 100, 150, 255),
            },
        'INACTIVE': {
            'background-color': (20, 20, 20, 240),
            'border-color': (55, 55, 55, 200),
            },
        }
    
    Layout = {
        'BASE': {
            'background-color': (10, 10, 10, 240),
            'border': 1,
            'border-color': (10, 10, 10, 240),
            'radius': 8,
            },
        }
    
    Button = {
        'BASE': {
            'font-color': (200, 200, 200, 255),
            'background-color': (35, 35, 35, 255),
            'border-color': (55, 55, 55, 200),
            'border': 1,
            'font': 'DejaVuSans.ttf',
            'font-size': 12,
            'padding': 10,
            'radius': 6,
            },
        'HOVER': {
            'font-color': (200, 200, 200, 255),
            'background-color': (40, 45, 55, 255),
            'border-color': (45, 70, 100, 255),
            },
        'CLICKED': {
            'font-color': (200, 200, 200, 255),
            'background-color': (50, 63, 88, 255),
            'border-color': (60, 100, 150, 255),
            },
        }
    
    Empty = {
        'BASE': {
            'background-color': (35, 35, 35, 255),
            'border-color': (55, 55, 55, 200),
            'border': 1,
            'radius': 6,
            },
        'HOVER': {
            'background-color': (40, 45, 55, 255),
            'border-color': (45, 70, 100, 255),
            },
        'CLICKED': {
            'background-color': (50, 63, 88, 255),
            'border-color': (60, 100, 150, 255),
            },
        }
    
    Input = {
        'BASE': {
            'font-color': (200, 200, 200, 255),
            'selection-color': (60, 100, 150, 100),
            'background-color': (17, 17, 17, 240),
            'border-color': (55, 55, 55, 200),
            'border': 1,
            'font': 'DejaVuSans.ttf',
            'font-size': 14,
            'padding': 8,
            'radius': 6,
            },
        'HOVER': {
            'font-color': (200, 200, 200, 255),
            'background-color': (10, 10, 10, 240),
            'border-color': (60, 100, 150, 255),
            },
        'CLICKED': {
            'font-color': (200, 200, 200, 255),
            'background-color': (10, 10, 10, 240),
            'border-color': (80, 120, 170, 255),
            },
        }
    
    classes = {
        'CHECKED': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (30, 35, 40, 255),
                'border-color': (40, 70, 120, 255),
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (30, 35, 40, 255),
                'border-color': (60, 100, 150, 255),
                },
            'CLICKED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (50, 63, 88, 255),
                'border-color': (60, 100, 150, 255),
                },
            },

        'DEFAULT': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (40, 50, 70, 255),
                'border-color': (60, 100, 150, 255),
                'border': 2,
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (50, 63, 88, 255),
                'border-color': (60, 100, 150, 255),
                },
            'CLICKED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (60, 80, 100, 255),
                'border-color': (60, 100, 150, 255),
                },
            },
        
        'DISABLED': {
            'BASE': {
                'font-color': (100, 100, 100, 255),
                'background-color': (40, 40, 40, 255),
                'border-color': (60, 60, 60, 255),
                },
            'HOVER': {
                'font-color': (100, 100, 100, 255),
                'background-color': (40, 40, 40, 255),
                'border-color': (60, 60, 60, 255),
                },
            'CLICKED': {
                'font-color': (100, 100, 100, 255),
                'background-color': (40, 40, 40, 255),
                'border-color': (60, 60, 60, 255),
                },
            },
        
        'ERROR': {
            'BASE': {
                'font-color': (200, 200, 200, 255),
                'background-color': (90, 40, 45, 255),
                'border-color': (150, 70, 70, 255),
                },
            'HOVER': {
                'font-color': (200, 200, 200, 255),
                'background-color': (98, 52, 60, 255),
                'border-color': (150, 70, 70, 255),
                },
            'CLICKED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (120, 60, 75, 255),
                'border-color': (150, 70, 70, 255),
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
            'CLICKED': {
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
            'CLICKED': {
                'font-color': (200, 200, 200, 255),
                'background-color': (80, 80, 40, 255),
                'border-color': (110, 95, 35, 255),
                },
            },
        }
