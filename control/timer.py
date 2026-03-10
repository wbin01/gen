#!/usr/bin/env python3
from .control import Control


class Timer(Control):
    def __init__(
            self, call: callable, interval: int = 0.5, cell: Cell = None,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._call = call
        self._interval = interval
        self._cell = cell

        self._next_tick = 0
    
    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(interval={self._interval}, tick={self._tick}, '
            f'cell={self.__cell.__class__.__name__})')
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
    
    @property
    def cell(self) -> Cell:
        return self._cell
    
    @cell.setter
    def cell(self, cell: Cell) -> None:
        self._cell = cell
    
    @property
    def interval(self) -> int:
        return self._interval
    
    @interval.setter
    def interval(self, interval: int) -> None:
        self._interval = interval

    @property
    def call(self) -> callable:
        return self._call
    
    @call.setter
    def call(self, call: callable) -> None:
        self._call = call
    
    def _exec(self) -> None:
        if self._cell and self._cell._visible:
            return self._call()
        return self._call()
