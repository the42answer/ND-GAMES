#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 15:18:26 2020

@author: mike
"""


from adjgrid import AdjGrid


class Board(AdjGrid):
    
    def __init__(self, size, adjacency, rules, array=None):
        
        super().__init__(self, size, adjacency, array)
        

configs = {
        'conway': {}
    }