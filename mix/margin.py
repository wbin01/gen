#!/usr/bin/env python3


class Margin(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__margin = (0, 0, 0, 0)
        self.__base_margin = (0, 0, 0, 0)
        
        self.__margin_x = 0
        self.__margin_y = 0
    
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
        return self.__margin
    
    @margin.setter
    def margin(self, margin: tuple | int) -> None:
        if not isinstance(margin, (tuple, int)):
            raise TypeError(
                'The value must be an "int" or a "tuple" of integers.')
        
        if isinstance(margin, int):
            self.__margin_x = margin * 2
            self.__margin_y = margin * 2
            self.__margin = margin, margin, margin, margin
            self.__base_margin = self.__margin
        else:
            self.__margin_x = margin[1] + margin[3]
            self.__margin_y = margin[0] + margin[2]
            self.__margin = margin
            self.__base_margin = margin
