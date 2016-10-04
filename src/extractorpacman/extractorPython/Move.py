#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from enum import IntEnum

class MOVE (IntEnum):
    DOWN = 0 
    LEFT = 1
    UP = 2 
    RIGHT = 3
    NEUTRAL = 4
    
    @staticmethod
    def get_move (_move):
        if(_move == "DOWN") or (_move ==0):
            return MOVE.DOWN
        elif(_move == "LEFT") or (_move ==1):
            return MOVE.LEFT
        elif(_move == "UP") or (_move ==2):
            return MOVE.UP
        elif(_move == "RIGHT") or (_move ==3):
            return MOVE.RIGHT
        else:
            return MOVE.NEUTRAL
        
     