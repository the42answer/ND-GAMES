#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:23:00 2020

@author: mike
"""

from ngrid import NGrid
import random
import itertools as it
from boundedinput import read_tuple, read_int, read_float, select_one

class Board(NGrid):
    
    def __init__(self, size, number_gen):
        
        self.number_gen = number_gen
        
        # Fill in the array with zeros. Numbers will be added later.
        super().__init__(size, 0)
        
        
    # TODO handle lack of space
    def add_numbers(self):
        
        numbers = self.number_gen()
        
        empty_indices = set()
        
        for i in range(len(self)):
            if self[i] == 0:
                empty_indices.add(i)
        
        for number in numbers[:len(empty_indices)]:
            index = random.choice(list(empty_indices))
            self[index] = number
            empty_indices.remove(index)
            
            
    def move(self, dimension, increase):
        
        for column in it.product(*map(range, self.size[:dimension]), (0,), *map(range, self.size[dimension+1:])):
            
            if not increase:
                start = 0
                offset = 1
                end = self.size[dimension] - 1
            else:
                start = self.size[dimension] - 1
                offset = -1
                end = 0
            
            last = list(column)
            last[dimension] = start
            current = list(last)
            
            while current[dimension] != end:
                current[dimension] += offset
                if self[current] == 0:
                    continue
                if not (self[last] == 0 or self[current] == self[last]):
                    last[dimension] += offset
                if last != current:
                    combined = self[last] != 0
                    self[last] += self[current]
                    self[current] = 0
                    if combined:
                        last[dimension] += offset
                
                
    def print_(self):
        
        self.print_nd(lambda t, w: f'{"." if t==0 else t: ^{w}}', 2)
        
        
number_gens = {
        'Easy 2s': lambda: 2,
        'Normal': lambda: random.choice(((2,), (2,), (4,), (2,2))),
        'Hard': lambda: random.choice(((2,), (2,), (4,), (2,2), (2,4))),
        '2-type easy': lambda: random.choice(((2,), (3,))),
        '2-type normal': lambda: random.choice(((2,), (3,), (4,), (2,3))),
        '3-type easy': lambda: random.choice(((2,), (3,), (5,))),
        '4-type easy': lambda: random.choice(((2,), (3,), (5,), (7,)))
    }
 

def play():
    
    size = read_tuple(floor=0, prompt="Enter the board's dimensions:\n >>> ", repeat=True)
    
    number_gen = number_gens[select_one(list(number_gens), values=number_gens, repeat=True)]
    
    board = Board(size, number_gen)
    
    while True:
        
        board.add_numbers()
        board.print_()
        
        move = read_int('Enter a move:\n >>> ', floor=-len(board.size), ceil=len(board.size), repeat=True)
        
        # Pass move
        if move == 0:
            continue
        
        move = (abs(move) - 1, move > 0)
        
        board.move(*move)
        

if __name__ == '__main__':
    play()               

























