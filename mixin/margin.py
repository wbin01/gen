#!/usr/bin/env python3


class Margin(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._margin = (0, 0, 0, 0)
        self._base_margin = (0, 0, 0, 0)
        
        self._margin_x = 0
        self._margin_y = 0
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def margin(self) -> tuple:
        """The margins.

        The margins are clockwise. To configure, use an integer tuple with the 
        values of the four margins (top, right, bottom, and left), or a single 
        integer representing all margins.
        
        Example:

            margin = 8

            margin = 8, 8, 8, 8
        
        Returns:

            A tuple of integers.
        
        """
        return self._margin
    
    @margin.setter
    def margin(self, margin: tuple | int) -> None:
        if not isinstance(margin, (tuple, int)):
            raise TypeError(
                'The value must be an "int" or a "tuple" of integers.')
        
        if isinstance(margin, int):
            self._margin_x = margin * 2
            self._margin_y = margin * 2
            self._margin = margin, margin, margin, margin
            self._base_margin = self._margin
        else:
            self._margin_x = margin[1] + margin[3]
            self._margin_y = margin[0] + margin[2]
            self._margin = margin
            self._base_margin = margin
