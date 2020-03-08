#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 00:50:53 2020

@author: mike
"""

class NGrid:
    """ Generic n-dimensional board class used across multiple games. """
    
    def __init__(self, size, array):
        self.size = size
        self.array = array
    
    
    def __len__(self):
        return len(self.array)


    def to_linear(self, coord):
        """ The n-dimensional board is stored as a 1-dimensional array
            whose length is the product of the size in each dimension.
            This function converts an n-dimensional coordinate to a
            position on this array.
            """
            
        index = 0
        multiplier = 1
        for dim in range(len(self.size)):
            index += coord[dim] * multiplier
            multiplier *= self.size[dim]
        return index
    
    
    def from_linear(self, index):
        """ Converts an internal array index to an n-dimensional coordinate. """
        
        coord = []
        for dim in range(len(self.size)):
            coord.append(index % self.size[dim])
            index //= self.size[dim]
        return tuple(coord)
    
    
    def __getitem__(self, key):
        """ Allow this class to be indexed.
            Integers and slices can be used like regular lists,
            and iterables can be used to specify n-dimensional coordinates.
            """
            
        try:
            # Handle iterables as n-dimensional coordinates
            t_key = tuple(key)
            return self.array[self.to_linear(t_key)]
        except TypeError:
            # Leave anything else to the normal list __getitem__
            return self.array[key]