#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:48:07 2020

@author: mike
"""

from ngrid import NGrid

import itertools as it
import random
from boundedinput import read_tuple, select_one, read_int, read_float
from editdefaults import fill

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
            if self.is_mine:
                out = '!'
            else:
                out = '.' if self.mines == 0 else self.mines
        else:
            out = '@' if self.visibility == 2 else '#'
        return f'{out: ^{width}}'

class Board(NGrid):
    """ An n-dimensional minesweeper board. """
    
    def __init__(self, size, adjacency, mine_frac):
        
        self.size = size
        self.adjacency = adjacency
        
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
        
        self.update_neighbours()
        
        
    def update_neighbours(self):
        # Set neighbours
        
        for i in range(len(self)):
            self[i].mines = 0
        
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
            if 0 < sum(map(abs, offset)) <= self.adjacency:
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
        
        
    def move(self, coord):
        self[coord].visibility = True
        self.sweep()
        
        
    def first_move(self, coord):
        self[coord].is_mine = False
        for tile in self[coord].neighbours:
            tile.is_mine = False
        self.update_neighbours()
        self.move(coord)
        



configs = {
        'Custom': None,
        
        'Easy 2d': {'size':(10,10), 'mine_frac':0.2, 'adjacency':2},
        'Normal 2d': {'size':(20,15), 'mine_frac':0.25, 'adjacency':2},
        'Hard 2d': {'size':(25,20), 'mine_frac':0.3, 'adjacency':2},
        
        'Easy 4d': {'size':(4,4,3,3), 'mine_frac':0.2, 'adjacency':2},
        'Normal 4d': {'size':(4,4,4,4), 'mine_frac':0.25, 'adjacency':2},
        'Hard 4d': {'size':(5,5,4,4), 'mine_frac':0.3, 'adjacency':2},
        
        'Easy 4d full': {'size':(4,4,3,3), 'mine_frac':0.05, 'adjacency':4},
        'Normal 4d full': {'size':(4,4,4,4), 'mine_frac':0.08, 'adjacency':4},
        'Hard 4d full': {'size':(5,5,4,4), 'mine_frac':0.1, 'adjacency':4},
    }

functions = {
        'size': lambda: read_tuple(floor=0, repeat=True),
        'mine_frac': lambda: read_float(floor=0.0, ceil=1.0, repeat=True),
        'adjacency': lambda: read_int(floor=0, repeat=True)
    }



# TODO make this user friendly
def play():
    
    config = configs[select_one(list(configs), values=configs)]
    
    if config is None:
        config = fill(functions)
    
    board = Board(**config)
    
    upper_bound = tuple(map(lambda x: x-1, board.size))
    
    first_move = True
    
    while True:
        
        
        board.print_()
        
        if board.is_won():
            print('You win')
            break
        
        move = read_tuple(floor=0, ceil=upper_bound, prompt='Enter a move:\n >>> ', repeat=True)
    
        if first_move:
            board.first_move(move)
        else:
            board.move(move)
        first_move = False
    
        if board[move].is_mine:
            print('You lose')
            break
    
    
    for i in range(len(board)):
        board[i].visibility = 1
        
    board.print_()



if __name__ == '__main__':
    play()


























