#!/usr/bin/env python3


class Cell:
    pass


class Layout(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__dirty = True
        self.__cells = []
        self.__x = 100
        self.__y = 10
        self.__spacing = 10

    def add(self, cell: Cell) -> None:
        """..."""
        self.__cells.append(cell)
        cell.parent = self
    
    def __invalidate(self) -> None:
        for cell in self.__cells:
            cell._Cell__dirty = True

        self.__dirty = True
    
    def __update(self) -> None:
        """..."""
        for cell in self.__cells:
            name = f'_{cell.__class__.__name__}__'
            setattr(cell, name + 'x', self.__x)

            name = f'_{cell.__class__.__name__}__'
            setattr(cell, name + 'y', self.__y)
            self.__y += getattr(cell, name + 'h') + self.__spacing
        
        self.__x = 100
        self.__y = 10

    def __redraw(self) -> None:
        """..."""
        for cell in self.__cells:
            if cell._Cell__dirty:
                name = f'_{cell.__class__.__name__}__'
                getattr(cell, name + 'draw')()
                cell._Cell__dirty = False

        self.__dirty = False
