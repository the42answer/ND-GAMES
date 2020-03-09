#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:23:00 2020

@author: mike
"""

from ngrid import NGrid
import random
import itertools as it

class Board(NGrid):
    
    def __init__(self, size):
        
        # Fill in the array with zeros. Numbers will be added later.
        super().__init__(size, 0)
        
        
    def add_numbers(self):
        self.add_numbers_simple()
        
    
    def add_numbers_simple(self):
        amount = random.choice((1,1,2))
        for i in range(amount):
            self[random.randrange(0,len(self))] = random.choice((2,2,4))
            
            
    def move(self, dimension, increase):
        
        for column in it.product(*map(range, self.size[:dimension]), (0,), *map(range, self.size[dimension+1:])):
            print(column)
            
            if increase:
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
                if self[last] == 0 or self[current] == self[last]:
                    self[last] += self[current]
                    self[current] = 0
                    continue
                last[dimension] += offset
                
                
    def print_(self):
        
        self.print_nd(lambda t, w: f'{t: ^{w}}', 2)
                

b = Board((3,4,2))
b.print_()
b.add_numbers()
b.print_()




























