#!/usr/bin/env python3
from ..mix import Margin, Padding
from ..ui import UI


class Cell(Margin, UI):
    """..."""
    def __init__(self) -> None:
        """..."""
        super().__init__()
        self.__drawer = None

    def __draw(self) -> None:
        pass
