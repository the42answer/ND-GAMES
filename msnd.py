#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:48:07 2020

@author: mike
"""

from ngrid import NGrid

import itertools as it
import random
from boundedinput import read_tuple, read_int, read_float

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

class Board(NGrid):
    """ An n-dimensional minesweeper board. """
    
    def __init__(self, size, max_adj, mine_frac):
        
        self.size = size
        self.max_adj = max_adj
        
        # Determine number of squares
        length = 1
        for dim in size: length *= dim
        
        # Create board
        board = []
        for i in range(length):
            board.append(Tile(random.random()<mine_frac, 0))
        
        # Initialise the NGrid superclass
        super().__init__(size, board)
        
        # Initialise offsets
        self.offsets = self.get_offsets()
        
        # Set neighbours
        for i in range(len(self)):
            neighbours = self.get_neighbours(self.from_linear(i))
            for neighbour in neighbours:
                neighbour = self[neighbour]
                self[i].neighbours.append(neighbour)
                if neighbour.is_mine:
                    self[i].mines += 1
    
    
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
            
    
    def sweep(self, update=None):
        """ Mark as visible any square whose neighbour has no adjacent mines.
            For efficiency, the update parameter can be used to mark the tiles
            that have been updated, allowing the function to ignore the others.
            """
        
        # If the updated tiles are not specified, assume that they may all be updated
        if update is None:
            update = set(self)
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
        
        
    def is_won(self):
        """ Check if all non-mine squares are cleared. """
        for tile in self:
            if not tile.is_mine and tile.visibility != 1:
                return False
        return True
    
    
    def print_(self):
        self.print_nd(lambda t, w: t.__str__(w), 3)



# TODO make this user friendly
def play():
    
    size = read_tuple(floor=0, prompt="Enter the board's dimensions:\n >>> ")
    upper_bound = tuple(map(lambda x: x-1, size))
    
    adjacency = read_int(floor=1, prompt="Enter offset limit:\n >>> ")
    
    mine_frac = read_float(floor=0, ceil=1, prompt="Enter the mine fraction:\n >>> ")
    
    board = Board(size, adjacency, mine_frac)
    
    while True:
        
        board.print_()
        
        if board.is_won():
            print('You win')
            break
        
        move = read_tuple(floor=0, ceil=upper_bound, prompt='Enter a move:\n >>> ')
    
        if board[move].is_mine:
            print('You lose')
            break
    
        board[move].visibility = True
        board.sweep()
    
    for i in range(len(board)):
        board[i].visibility = 1
        
    board.print_()



if __name__ == '__main__':
    play()


























