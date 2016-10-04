#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from Move import MOVE

class PacMan:
    
    def __init__(self, _currentNodeIndex,_lastMoveMade,_numberOfLivesRemaining,_hasReceivedExtraLife):
        self.currentNodeIndex = _currentNodeIndex
        self.lastMoveMade = _lastMoveMade
        self.numberOfLivesRemaining = _numberOfLivesRemaining
        self.hasReceivedExtraLife = _hasReceivedExtraLife
        
    def print_pacman(self):
        print("PacMan currentNodeIndex: %d"  %self.currentNodeIndex)
        print("PacMan numberOfLivesRemaining: %d"  %self.numberOfLivesRemaining )
        print("PacMan lastMoveMade: %s"  %(MOVE.get_move(self.lastMoveMade)))
        print("PacMan hasReceivedExtraLife: %s"  %self.hasReceivedExtraLife)