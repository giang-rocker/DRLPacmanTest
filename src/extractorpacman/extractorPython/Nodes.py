#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class Node:
    
    def __init__(self,_nodeIndex,_x,_y,_pillIndex,_powerPillIndex):
        self.nodeIndex = _nodeIndex
        self.x = _x
        self.y = _y
        self.pillIndex=_pillIndex
        self.powerPillIndex = _powerPillIndex
        

class Pill:
     
    def __init__(self,_nodeIndex,_pillIndex,_x,_y):
        self.nodeIndex = _nodeIndex
        self.pillIndex = _pillIndex
        self.x=_x
        self.y = _y
        self.isAvailable = False
    
    
class PowerPill:
     
    def __init__(self,_nodeIndex,_powerPillIndex,_x,_y):
        self.nodeIndex = _nodeIndex
        self.powerPillIndex = _powerPillIndex
        self.x=_x
        self.y = _y
        self.isAvailable = False
    