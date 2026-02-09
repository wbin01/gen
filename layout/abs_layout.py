#!/usr/bin/env python3
import sdl3

from ctypes import c_int


class Cell:
    pass


class AbsLayout(object):
    """..."""
    def __init__(self, parent, padding=10, fill=False) -> None:
        """..."""
        self.__parent = parent
        self.__pad = padding
        self.__fill = fill

        self.__dirty = True
        self.__cells = []
        self.__x = 0 + self.__pad
        self.__y = 10
        self.__w = c_int()
        self.__h = c_int()

        self.__spacing = 10

    def add(self, cell: Cell, fill=None) -> Cell:
        """..."""
        self.__cells.append(cell)
        cell.parent = self

        if fill is not None:
            self.__fill = fill
        return cell
    
    def __invalidate(self) -> None:
        for cell in self.__cells:
            cell._Cell__dirty = True

        self.__dirty = True
    
    def __update(self) -> None:
        """..."""
        sdl3.SDL_GetWindowSize(self.__parent, self.__w, self.__h)

        for cell in self.__cells:
            name = f'_{cell.__class__.__name__}'
            setattr(cell, name + '__x', self.__x)
            setattr(cell, name + '__y', self.__y)
            if self.__fill:
                setattr(cell, name + '__w', self.__w.value - (self.__pad * 2))
            # setattr(cell, name + '__h', self.__h.value)
            self.__y += getattr(cell, name + '__h') + self.__spacing
        
        self.__x = 0 + self.__pad
        self.__y = 10

    def __redraw(self) -> None:
        """..."""
        for cell in self.__cells:
            if cell._Cell__dirty:
                name = f'_{cell.__class__.__name__}'
                getattr(cell, name + '__draw')()
                cell._Cell__dirty = False
                # print('Render', name)

        self.__dirty = False
