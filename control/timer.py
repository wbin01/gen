#!/usr/bin/env python3
import time

from .control import Control


class Timer(Control):
    """..."""
    def __init__(
            self, call: callable, interval: float = 0.5, cell: Cell = None,
            single_shot: boll = False, init_delay: float = 0.0,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._call = call
        self._interval = interval
        self._cell = cell
        self._single_shot = single_shot
        self._delay = init_delay

        self._active = False
        self._start_time = 0
        self._next_tick = 0
        
    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            f'(interval={self._interval}, tick={self._tick}, '
            f'cell={self.__cell.__class__.__name__})')
    
    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def active(self) -> bool:
        return self._active

    @active.setter
    def active(self, value: bool) -> None:
        if value and not self._active:
            self._start_time = time.monotonic() + self._delay
        
        self._active = value
    
    @property
    def call(self) -> callable:
        """..."""
        return self._call
    
    @call.setter
    def call(self, call: callable) -> None:
        self._call = call

    @property
    def cell(self) -> Cell:
        """..."""
        return self._cell
    
    @cell.setter
    def cell(self, cell: Cell) -> None:
        self._cell = cell
    
    @property
    def init_delay(self) -> float:
        """..."""
        return self._init_delay
    
    @init_delay.setter
    def init_delay(self, value: bool) -> None:
        self._init_delay = value
    
    @property
    def interval(self) -> int:
        """..."""
        return self._interval
    
    @interval.setter
    def interval(self, interval: int) -> None:
        self._interval = interval
    
    @property
    def single_shot(self) -> bool:
        """..."""
        return self._single_shot
    
    @single_shot.setter
    def single_shot(self, value: bool) -> None:
        self._single_shot = value
    
    def _exec(self) -> None:
        if not self._active:
            return
        
        current_time = time.monotonic()
        if current_time < self._start_time:
            return False

        if current_time >= self._next_tick:
            self._next_tick = time.monotonic() + self._interval

            if self._single_shot:
                self._active = False

            if self._cell:
                if self._cell._visible:
                    return self._call()
                return None
            return self._call()

