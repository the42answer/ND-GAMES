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
        
        adj_size = (1,) * (4 - len(self.size)) + self.size 
        
        
        for other_coord in it.product(*map(range,adj_size[:-4])):
            
            print(f'Showing coordinates {other_coord} + (*,*,*,*):')
            
            self.print_row_coord(adj_size, width)
            self.print_row_sep(adj_size, width)
            
            for x in range(adj_size[-3]):
                for z in range(adj_size[-1]):
                    
                    self.print_row(
                            adj_size,
                            lambda w, y: func(self[(other_coord+(w,)+(x,)+(y,)+(z,))[-len(self.size):]], width),
                            f'x={x: <{width}} z={z: <{width}}',
                            ' | ', ' | ', ' '
                         )
                    
                self.print_row_sep(adj_size, width)
            print()
            
          
    def print_row(self, size, func, start, border, w_sep, y_sep):
        print(end=f'{start}{border}')
        for w in range(size[-4]):
            if w > 0:
                print(end=w_sep)
            for y in range(size[-2]):
                if y > 0:
                    print(end=y_sep)
                print(end=func(w,y))
        print(border)
        
        
    def print_row_coord(self, size, width):
        self.print_row(size, lambda w, y: f'{w: ^{width}}', f'{"w -> ": <{2*width + 5}}', ' . ', ' . ', ' ')
        self.print_row(size, lambda w, y: f'{y: ^{width}}', f'{"y -> ": <{2*width + 5}}', ' | ', ' | ', ' ')
        
        
    def print_row_sep(self, size, width):
        self.print_row(size, lambda w, y: '-'*width, '-' * (2*width + 5), ' + ', ' + ', '-')