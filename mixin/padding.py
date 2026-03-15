#!/usr/bin/env python3


class Padding(object):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._padding = (0, 0, 0, 0)
        self._base_padding = (0, 0, 0, 0)
        
        self._padding_x = 0
        self._padding_y = 0
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return self.__class__.__name__
    
    @property
    def padding(self) -> tuple:
        """The paddings.

        The paddings are clockwise. To configure, use an integer tuple with the 
        values of the four paddings (top, right, bottom, and left), or a single 
        integer representing all paddings.
        
        Example:

            padding = 8

            padding = 8, 8, 8, 8
        
        Returns:

            A tuple of integers.
        
        """
        return self._padding
    
    @padding.setter
    def padding(self, padding: tuple | int) -> None:
        if not isinstance(padding, (tuple, int)):
            raise TypeError(
                'The value must be an "int" or a "tuple" of integers.')
        
        if isinstance(padding, int):
            self._padding_x = padding * 2
            self._padding_y = padding * 2
            self._padding = padding, padding, padding, padding
            self._base_padding = self._padding
        else:
            self._padding_x = padding[1] + padding[3]
            self._padding_y = padding[0] + padding[2]
            self._padding = padding
            self._base_padding = padding
