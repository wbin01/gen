#!/usr/bin/env python3
from ..mix import Margin, Position, Size
from ..ui import UI


class Cell(Margin, Position, Size, UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        self.__drawer = None

    def __draw(self) -> None:
        pass
