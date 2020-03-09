#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 18:37:15 2020

@author: mike
"""

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
    
    print('These are the default options.\nEnter a number to replace one or enter nothing to accept.')
    
    num_width = len(str(len(key_list)-1))
    key_width = max(map(len, key_list))
    
    for i in range(len(key_list)):
        print(f'[{i: >{num_width}}] {key_list[i]: <{key_width}} : {results[key_list[i]]}')
        
    while True:
        string = input('Enter your choice.\n >>> ')
        if not string:
            return results
        if string:
            key = key_list[int(string)]
            print(end=f"Enter a value for '{key}'. \n >>> ")
            results[key] = functions[key]()
   
    return results
    
from boundedinput import read_tuple, read_int, read_float


defaults = {
        'Test tuple': (42,),
        'Test int': None,
        'Test float': 42.0
    }


functions = {
        'Test tuple': lambda: read_tuple(size=2),
        'Test int': lambda: read_int(ceil=0),
        'Test float': read_float
    }


print(edit_defaults(defaults, functions))