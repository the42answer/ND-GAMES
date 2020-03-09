#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 00:50:53 2020

@author: mike
"""

import itertools as it

class NGrid:
    """ Generic n-dimensional board class used across multiple games. """
    
    
    
    def __init__(self, size, array=None):
        self.size = size
        
        if hasattr(array, '__len__'):
            self.array = array
        else:
            length = 1
            for dim in size:
                length *= dim
            self.array = [array] * length
    
    
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
        
    def __setitem__(self, key, value):
        try:
            # Handle iterables as n-dimensional coordinates
            t_key = tuple(key)
            self.array[self.to_linear(t_key)] = value
        except TypeError:
            # Leave anything else to the normal list __getitem__
            self.array[key] = value
        
    def print_nd(self, func, width=3):
        """ Print the n-dimensional board as a series of (up to) 4d grids.
            Each 4d grid is a 2d grid of 2d grids.
            """
        
        adj_size = self.size  + (1,) * (4 - len(self.size))
        
        
        for other_coord in it.product(*map(range,adj_size[4:])):
            
            print(f'Showing coordinates {other_coord} + (*,*,*,*):')
            
            self.print_row_coord(adj_size, width)
            self.print_row_sep(adj_size, width)
            
            for w in range(adj_size[3]):
                for y in range(adj_size[1]):
                    
                    self.print_row(
                            adj_size,
                            lambda z, x: func(self[((z,)+(y,)+(x,)+(w,))[:len(self.size)] + other_coord], width),
                            f'w={w: <{width}} y={y: <{width}}',
                            ' | ', ' | ', ' '
                         )
                    
                self.print_row_sep(adj_size, width)
            print()
            
          
    def print_row(self, size, func, start, border, z_sep, x_sep):
        print(end=f'{start}{border}')
        for x in range(size[2]):
            if x > 0:
                print(end=z_sep)
            for z in range(size[0]):
                if z > 0:
                    print(end=x_sep)
                print(end=func(z,x))
        print(border)
        
        
    def print_row_coord(self, size, width):
        self.print_row(size, lambda z, x: f'{z: ^{width}}', f'{"w -> ": <{2*width + 5}}', ' . ', ' . ', ' ')
        self.print_row(size, lambda z, x: f'{x: ^{width}}', f'{"y -> ": <{2*width + 5}}', ' | ', ' | ', ' ')
        
        
    def print_row_sep(self, size, width):
        self.print_row(size, lambda z, x: '-'*width, '-' * (2*width + 5), ' + ', ' + ', '-')