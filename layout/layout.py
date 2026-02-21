#!/usr/bin/env python3
from ..ui import UI


class Layout(UI):
    """Organizes the positioning of the elements."""
    def __init__(self, *args, **kwargs) -> None:
        self.__drawer = None
