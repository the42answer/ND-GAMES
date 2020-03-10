#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:32:03 2020

@author: mike
"""

from ngrid import NGrid
import itertools as it


class AdjGrid(NGrid):
    
    def __init__(self, size, adjacency, array=None):
        
        super().__init__(size, array)
        
        self.adjacency = adjacency
        
        # Initialise offsets
        self.offsets = self.get_offsets()
    
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