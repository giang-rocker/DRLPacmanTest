#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.


class LogFile:
    
    def __init__(self,_logFileName):
        self.logFileName= _logFileName
        self.gameState = self.get_all_game_state()
        self.currentTimeStep = 0
        self.totalGameState = len (self.gameState)
        
    def get_all_game_state(self):
        logFile = open(self.logFileName+'.txt', 'r')
        listGameState=logFile.readlines()
        listGameState.pop(len(listGameState)-1)
        return listGameState
    
    def is_end(self):
        return (self.currentTimeStep == len(self.gameState))
    
    def is_valid(self):
        return (self.currentTimeStep < len(self.gameState)) and (self.currentTimeStep>=0) 
        
    def get_next_state(self):
        self.currentTimeStep+=1
        return self.gameState[self.currentTimeStep-1]
    
    def get_prev_state(self):
        self.currentTimeStep-=1
        return self.gameState[self.currentTimeStep+1]
        
    def get_state(self,_id):
        return self.gameState[_id]
