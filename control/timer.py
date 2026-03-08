#!/usr/bin/env python3


class Timer(object):
    def __init__(self, cell: Cell, interval: int, tick: callable) -> None:
        self._cell = cell
        self._interval = interval
        self._tick = tick

        self._next_tick = 0
    
    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(cell={self.__cell.__class__.__name__}, '
            f'interval={self._interval}, tick={self._tick})')
    
    def __str__(self) -> str:
        return f'{self.__class__.__name__}("{self._text}")'
    
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
    def tick(self) -> callable:
        return self._tick
    
    @tick.setter
    def tick(self, tick: callable) -> None:
        self._tick = tick
    
    def _exec(self) -> None:
        if self._cell._visible:
            self._tick()
