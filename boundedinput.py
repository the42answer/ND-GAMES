#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 16:34:34 2020

@author: mike
"""

def read_number(dtype, prompt='', floor=None, ceil=None, repeat=False):
    """ Reads a number within specified bounds. """
    
    while True:
    
        try:
            result = dtype(input(prompt))
            if floor is not None and result < floor:
                raise ValueError(f'Number must be no less than {floor}.')
            if ceil is not None and result > ceil:
                raise ValueError(f'Number must be no greater than {ceil}.')
        except ValueError as e:
            print(e)
            result = None
            
        if result is not None or not repeat:
            return result
        

def select_one(options, values=None, prompt='', repeat=False):
    index = read_index(options, values, prompt, repeat)
    return options[index] if index is not None else index
        


# TODO add error handling and repeat support
def read_index(options, values=None, prompt='', repeat=False):

    while True:
                
        try:
            print(prompt)    
            num_width = len(str(len(options)-1))
            
            if values is None:
                for i in range(len(options)):
                    print(f'[{i: >{num_width}}] {options[i]}')
            else:
                key_width = max(map(len, options))
                for i in range(len(options)):
                    print(f'[{i: >{num_width}}] {options[i]: <{key_width}} : {values[options[i]]}')
                
            string = input('Enter your choice.\n >>> ')
            if not string:
                raise ValueError('Empty string.')
            if string:
                result = int(string)
                
        except (ValueError, TypeError) as e:
            print(e)
            result = None
            
        print(result)
            
        if result is not None or not repeat:
            print(result)
            return result
    


def read_float(prompt='', floor=None, ceil=None, repeat=False):
    return read_number(float, prompt, floor, ceil, repeat)



def read_int(prompt='', floor=None, ceil=None, repeat=False):
    return read_number(int, prompt, floor, ceil, repeat)



def read_tuple(prompt='', size=None, floor=None, ceil=None, repeat=False):
    """ Reads a user speficied tuple with some validation. """
    
    while True:
        
        try:
            result = tuple(map(int, input(prompt).split()))
            print(result)
            
            try:
                t_floor = tuple(floor)
                if len(floor) != len(result):
                    raise ValueError(f'Tuple must be length {len(t_floor)} not {len(result)}.')
                for i in range(len(result)):
                    if t_floor[i] > result[i]:
                        raise ValueError(f'Tuple must be no less than {t_floor} elementwise.')
            except (TypeError, ValueError):
                if floor is not None:
                    for elem in result:
                        if floor > elem:
                            raise ValueError(f'Tuple must be no less than {floor} elementwise.')
                        
            try:
                t_ceil = tuple(ceil)
                if len(ceil) != len(result):
                    raise ValueError(f'Tuple must be length {len(t_ceil)} not {len(result)}.')
                for i in range(len(result)):
                    if t_ceil[i] < result[i]:
                        raise ValueError(f'Tuple must be no greater than {t_ceil} elementwise.')
            except (TypeError, ValueError):
                if ceil is not None:
                    for elem in result:
                        if ceil < elem:
                            raise ValueError(f'Tuple must be no greater than {floor} elementwise.')
            
            if size is not None and size != len(result):
                raise ValueError(f'Tuple must be length {size} not {len(result)}.')
            
        except (TypeError, ValueError) as e:
            print(e)
            result = None
            
        if result is not None or not repeat:
            return result