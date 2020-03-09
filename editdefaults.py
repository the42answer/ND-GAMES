#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:37:15 2020

@author: mike
"""

from boundedinput import read_index


def fill(functions: dict):
    results = {}
    for key in functions:
        print(end=f"Enter a value for '{key}'. \n >>> ")
        results[key] = functions[key]()
    return results


def edit_defaults(defaults: dict, functions: dict):
    
    key_list = list(functions)
    key_list.sort()
    
    results = defaults.copy()
    
    while True:
        
        update = read_index(key_list, values=defaults)
        
        if update is None:
            break
        
        print(end=f'Enter a value for {key_list[update]}.')
        defaults[key_list[update]] = functions[key_list[update]]()
   
    return results
