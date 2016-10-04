#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from Move import MOVE

"""
BLINKY(40, "Blinky"),
PINKY(60, "Pinky"),
INKY(80, "Inky"),
SUE(100, "Sue");
"""

class Ghosts:
    
    def __init__(self, _name,_currentNodeIndex, _edibleTime, _lairTime, _lastMoveMade) :
        self.name =_name
        self.currentNodeIndex = _currentNodeIndex
        self.edibleTime= _edibleTime
        self.lairTime= _lairTime
        self.lastMoveMade = _lastMoveMade
        self.wasEaten=False
   
    def print_ghost(self):
        print ("GhostName: %s" %self.name)
        print ("currentNodeIndex: %d" %self.currentNodeIndex)
        print ("edibleTime: %d" %self.edibleTime)
        print ("lastMoveMade: %s" %self.lastMoveMade)
        print ("wasEaten: %s" %self.wasEaten)
        