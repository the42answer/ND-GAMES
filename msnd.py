#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 19:48:07 2020

@author: mike
"""

import itertools as it
import random
import math

class Tile():
    def __init__(self, is_mine, visibility):
        self.is_mine = is_mine
        self.visibility = visibility
        self.neighbours = []
        self.mines = 0
        
    def __str__(self, width=2):
        if self.visibility == 1:
            out = '!' if self.is_mine else self.mines
        else:
            out = '@' if self.visibility == 2 else '#'
        return f'{out: ^{width}}'

class Board:
    
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
        index = 0
        multiplier = 1
        for dim in range(len(self.size)):
            index += coord[dim] * multiplier
            multiplier *= self.size[dim]
        return index
    
    
    def from_linear(self, index):
        coord = []
        for dim in range(len(self.size)):
            coord.append(index % self.size[dim])
            index //= self.size[dim]
        return tuple(coord)
    
    
    def get_offsets(self):
        
        good_offsets = []
        
        for offset in it.product((-1,0,1), repeat=len(self.size)):
            if 0 < sum(map(abs, offset)) <= self.max_adj:
                good_offsets.append(offset)
                
        return good_offsets
    
    
    def get_neighbours(self, coord):
        neighbours = []
        for offset in self.offsets:
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
    
    def print_row_coord(self, size, width):
        self.print_row(size, lambda x, z: f'{x: ^{width}}', f'{"x -> ": <{2*width + 5}}', ' . ', ' . ', ' ')
        self.print_row(size, lambda x, z: f'{z: ^{width}}', f'{"z -> ": <{2*width + 5}}', ' | ', ' | ', ' ')
        
    def print_row_sep(self, size, width):
        self.print_row(size, lambda x, z: '-'*width, '-' * (2*width + 5), ' + ', ' + ', '-')
        

    def print_row(self, size, func, start, border, x_sep, z_sep):
        print(end=f'{start}{border}')
        for x in range(size[-3]):
            if x > 0:
                print(end=x_sep)
            for z in range(size[-1]):
                if z > 0:
                    print(end=z_sep)
                print(end=func(x,z))
        print(border)
    
    def print_nd(self, width=3):
        
        adj_size = (1,) * (4 - len(self.size)) + self.size 
        
        
        for other_coord in it.product(*map(range,adj_size[:-4])):
            
            print(f'Showing coordinates {other_coord} + (*,*,*,*):')
            
            self.print_row_coord(adj_size, width)
            self.print_row_sep(adj_size, width)
            
            for w in range(adj_size[-4]):
                for y in range(adj_size[-2]):
                    
                    self.print_row(
                            adj_size,
                            lambda x, z: self.board[self.to_linear((other_coord+(w,)+(x,)+(y,)+(z,))[-len(self.size):])].__str__(width),
                            f'w={w: <{width}} y={y: <{width}}',
                            ' | ', ' | ', ' '
                         )
                    
                self.print_row_sep(adj_size, width)
            print()
            
    
    def sweep(self, update=None):
        
        if update is None:
            update = set(self.board)
        
        while update:
            update_next = set()
            for tile in update:
                if tile.visibility == 1 and tile.mines == 0:
                    for neighbour in tile.neighbours:
                        if neighbour.visibility != 1:
                            neighbour.visibility = 1
                            update_next.add(neighbour)
            update = update_next

    def __getitem__(self, key):
        try:
            t_key = tuple(key)
            return self.board[self.to_linear(t_key)]
        except TypeError:
            return self.board[key]
        
    def is_won(self):
        for tile in self.board:
            if not tile.is_mine and tile.visibility != 1:
                return False
        return True

def read_tuple(size=None, floor=None, ceil=None, prompt=''):
    
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


























