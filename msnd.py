#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:48:07 2020

@author: mike
"""

import itertools as it
import random

class Tile():
    """ A structure representing a single tile, and useful information about it. """
    
    def __init__(self, is_mine, visibility):
        self.is_mine = is_mine
        self.visibility = visibility
        self.neighbours = []
        self.mines = 0
    
    def __str__(self, width=2):
        """ Print the tile in a useful format. """
        
        if self.visibility == 1:
            out = '!' if self.is_mine else self.mines
        else:
            out = '@' if self.visibility == 2 else '#'
        return f'{out: ^{width}}'

class Board:
    """ An n-dimensional minesweeper board. """
    
    def __init__(self, size, max_adj, mine_frac):
        
        self.size = size
        self.max_adj = max_adj
        
        # Determine number of squares
        self.length = 1
        for dim in size: self.length *= dim
        
        # Create board
        self.board = []
        for i in range(self.length):
            self.board.append(Tile(random.random()<mine_frac, 0))
        
        # Initialise offsets
        self.offsets = self.get_offsets()
        
        # Set neighbours
        for i in range(self.length):
            neighbours = self.get_neighbours(self.from_linear(i))
            for neighbour in neighbours:
                neighbour = self.board[self.to_linear(neighbour)]
                self.board[i].neighbours.append(neighbour)
                if neighbour.is_mine:
                    self.board[i].mines += 1
       
        
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
    
    
    def get_offsets(self):
        """ Offsets are coordinates holding -1, 0, or 1 in each place.
            A correct offset must not be all zeros (this points to the same square),
            and must have a total number of changes (-1 or 1) not greater than
            the adjacency limt.
            This function finds all correct offsets. 
            """
        
        good_offsets = []
        
        # Iterate over all possible offsets
        for offset in it.product((-1,0,1), repeat=len(self.size)):
            
            # Test if this is a good offset by checking the number of changes
            if 0 < sum(map(abs, offset)) <= self.max_adj:
                good_offsets.append(offset)
                
        return good_offsets
    
    
    def get_neighbours(self, coord):
        """ Get all neighbours of a given coordinate.
            Neighbours are the squares that count for minesweeper adjacency.
            """
            
        neighbours = []
        
        # Iterate over all good offsets
        for offset in self.offsets:
            
            # Add the offset to the current coordinate,
            # and keep any candidate that is actually on the board
            candidate = list(coord)
            good_candidate = True
            for i in range(len(self.size)):
                candidate[i] += offset[i]
                if not 0 <= candidate[i] < self.size[i]:
                    good_candidate = False
                    break
            if good_candidate:
                neighbours.append(candidate)
                
        return neighbours
    
    
    def print_nd(self, width=3):
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
                            lambda w, y: self.board[self.to_linear((other_coord+(w,)+(x,)+(y,)+(z,))[-len(self.size):])].__str__(width),
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
            
    
    def sweep(self, update=None):
        """ Mark as visible any square whose neighbour has no adjacent mines.
            For efficiency, the update parameter can be used to mark the tiles
            that have been updated, allowing the function to ignore the others.
            """
        
        # If the updated tiles are not specified, assume that they may all be updated
        if update is None:
            update = set(self.board)
        else:
            update = set(update)
        
        while update:
            
            # Apply the sweep algorithm at each updated tile
            update_next = set()
            for tile in update:
                
                # If a tile is visible, and has no adjacent mines, make all neighbours visible
                if tile.visibility == 1 and tile.mines == 0:
                    for neighbour in tile.neighbours:
                        if neighbour.visibility != 1:
                            neighbour.visibility = 1
                            
                            # Mark these neighbours for update next iteration
                            update_next.add(neighbour)
                            
            update = update_next


    def __getitem__(self, key):
        """ Allow this class to be indexed.
            Integers and slices can be used like regular lists,
            and iterables can be used to specify n-dimensional coordinates.
            """
            
        try:
            # Handle iterables as n-dimensional coordinates
            t_key = tuple(key)
            return self.board[self.to_linear(t_key)]
        except TypeError:
            # Leave anything else to the normal list __getitem__
            return self.board[key]
        
        
    def is_won(self):
        """ Check if all non-mine squares are cleared. """
        for tile in self.board:
            if not tile.is_mine and tile.visibility != 1:
                return False
        return True



def read_tuple(size=None, floor=None, ceil=None, prompt=''):
    """ Reads a user speficied tuple with some validation. """
    
    try:
        result = tuple(map(int, input(prompt).split()))
        print(result)
    except TypeError or ValueError:
        print('Malformed expression.\nEnter numbers separated by spaces only.')
        return
    
    try:
        t_floor = tuple(floor)
        if len(floor) != len(result):
            print(f'Tuple must be length {len(t_floor)} not {len(result)}.')
            return
        for i in range(len(result)):
            if t_floor[i] > result[i]:
                print(f'Tuple must be no less than {t_floor} elementwise.')
                return
    except TypeError or ValueError:
        if floor is not None:
            for elem in result:
                if floor > elem:
                    print(f'Tuple must be no less than {floor} elementwise.')
                    return
                
    try:
        t_ceil = tuple(ceil)
        if len(ceil) != len(result):
            print(f'Tuple must be length {len(t_ceil)} not {len(result)}.')
            return
        for i in range(len(result)):
            if t_ceil[i] < result[i]:
                print(f'Tuple must be no greater than {t_ceil} elementwise.')
                return
    except TypeError or ValueError:
        if ceil is not None:
            for elem in result:
                if ceil < elem:
                    print(f'Tuple must be no greater than {floor} elementwise.')
                    return
    
    if size is not None and size != len(result):
        print(f'Tuple must be length {size} not {len(result)}.')
        return
        
    return result
            
            

# TODO make this user friendly
def play():
    
    size = read_tuple(floor=0, prompt="Enter the board's dimensions:\n >>> ")
    upper_bound = tuple(map(lambda x: x-1, size))
    
    board = Board(size, 100, 0.1)
    
    while True:
        
        board.print_nd()
        
        if board.is_won():
            print('You win')
            break
        
        move = read_tuple(floor=0, ceil=upper_bound, prompt='Enter a move:\n >>> ')
        if move is None: continue
    
        if board[move].is_mine:
            print('You lose')
            break
    
        board[move].visibility = True
        board.sweep()
    
    for i in range(len(board.board)):
        board.board[i].visibility = 1
        
    board.print_nd()



if __name__ == '__main__':
    play()


























