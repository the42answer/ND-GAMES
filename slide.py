#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:23:00 2020

@author: mike
"""

from ngrid import NGrid
import random
import itertools as it
from boundedinput import read_tuple, read_int, read_float

class Board(NGrid):
    
    def __init__(self, size):
        
        # Fill in the array with zeros. Numbers will be added later.
        super().__init__(size, 0)
        
        
    def add_numbers(self):
        self.add_numbers_simple()
        
    
    def add_numbers_simple(self):
        amount = random.choice((1,1,2))
        while amount > 0:
            index = random.randrange(0,len(self))
            if self[index] == 0:
                self[index] = random.choice((2,2,4))
                amount -= 1
            
            
    def move(self, dimension, increase):
        
        for column in it.product(*map(range, self.size[:dimension]), (0,), *map(range, self.size[dimension+1:])):
            print(column)
            
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
 

def play():
    
    size = read_tuple(floor=0, prompt="Enter the board's dimensions:\n >>> ", repeat=True)
    board = Board(size)
    
    while True:
        
        board.add_numbers()
        board.print_()
        
        move = read_int('Enter a move:\n >>> ', floor=-len(board.size), ceil=len(board.size), repeat=True)
        
        # Pass move
        if move == 0:
            continue
        
        move = (abs(move) - 1, move > 0)
        
        board.move(*move)
        board.print_()


if __name__ == '__main__':
    play()               

























