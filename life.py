#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:18:26 2020

@author: mike
"""


from adjgrid import AdjGrid
from time import sleep


class Board(AdjGrid):
    
    def __init__(self, size, adjacency, rules, array=None):
        
        self.rules = rules
        super().__init__(size, adjacency, array)
   
    
    def update(self):
        
        array2 = self.array.copy()
        
        for i in range(len(self)):
            
            neighbours = self.get_neighbours(self.from_linear(i))
            
            adj = 0
            for neighbour in neighbours:
                if self[neighbour]:
                    adj += 1
            
            array2[i] = self.rules(self.size, self.adjacency, adj, self.array[i])
        
        self.array = array2

# Life functions: (dims, adjacency, surrounding, state) -> state
        

# The rules for Conway's Game of Life (the common 2d version)
def conway(dims, adj, surr, st):    
    return surr == 3 or st and surr == 2
    


configs = {
        'conway': conway
    }


b = Board((10,10), 2, conway, False)

fill = (
        (0,1), (1,1), (2,1),  # Blinker
        (0,6), (1,6), (2,6), (1,7), (2,7), (3,7)  # Toad
    )

for coord in fill:
    b[coord] = True

for i in range(10):
    
    b.update()
    b.print_nd(lambda a, b: f'{"#" if a else ".": ^{b}}')
   
    sleep(1)