#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
 


class Maze:
    
    def __init__(self,_mazeName,_initialPacManNodeIndex,_lairNodeIndex,_initialGhostNodeIndex,_numberOfNode,_numberOfPill,_numberOfPowerPill,_numberOfJucntion):
     #initial infomation
        self.mazeName = _mazeName
        self.initialPacManNodeIndex = _initialPacManNodeIndex
        self.lairNodeIndex = _lairNodeIndex
        self.initialGhostNodeIndex = _initialGhostNodeIndex
        self.numberOfNode = _numberOfNode
        self.numberOfPill = _numberOfPill
        self.numberOfPowerPill = _numberOfPowerPill
        self.numberOfJucntion = _numberOfJucntion
    
    def print_maze(self):
        print ( "MazeInfo" )
        print ("Name: %s" %self.mazeName)
        print ("initialPacManNodeIndex: %d" %self.initialPacManNodeIndex)
        print ("lairNodeIndex: %d" %self.lairNodeIndex)
        print ("initialGhostNodeIndex: %d" %self.initialGhostNodeIndex)
        print ("numberOfNode: %d" %self.numberOfNode)
        print ("numberOfPill: %d" %self.numberOfPill)
        print ("numberOfPowerPill: %d" %self.numberOfPowerPill)
        print ("numberOfJucntion: %d" %self.numberOfJucntion)
        

class GameState:
    
    #listPills boolean pillIndex available or not
      
    def __init__(self,_maze,_mazeIndex,_totalTime,_score,_currentLevelTime,_levelCount,_pacman,_listGhost,_listPillStatus,_listPowerPillStatus,_timeOfLastGlobalReversal,_pacmanWasEaten,_pillWasEaten,_powerPillWasEaten):
        
        self.maze= _maze
        self.mazeIndex= _mazeIndex
        self.totalTime =_totalTime
        self.score = _score
        self.currentLevelTime = _currentLevelTime
        self.levelCount = _levelCount
        self.pacman = _pacman
        self.ghosts=_listGhost
       
        self.listPillStatus = _listPillStatus
        self.listPowerPillStatus = _listPowerPillStatus
        
        self.timeOfLastGlobalReversal = _timeOfLastGlobalReversal
        self.pacmanWasEaten = _pacmanWasEaten
        self.pillWasEaten = _pillWasEaten
        self.powerPillWasEaten = _powerPillWasEaten
    
    def print_list_ghost (self):
        for ghost in self.ghosts:
            ghost.print_ghost()
            
    def print_pill_status (self):
        count =0 
        for pill in self.listPillStatus:
            if(pill==True):
                count+=1
        print("AvailablePill: %d Unavailable: %d " %(count ,( len(self.listPillStatus)-count ))  )
    
    def print_power_pill_status (self):
        count =0 
        for pill in self.listPowerPillStatus:
            if(pill==True):
                count+=1
        print("AvailablePowerPill: %d Unavailable: %d " %(count ,( len(self.listPowerPillStatus)-count ))  )
       
        
        
    def print_game_state (self):
        """
        print ("mazeIndex: %d " %self.mazeIndex)
        print ("totalTime: %d" %self.totalTime)
        print ("score: %d" %self.score)
        print ("currentLevelTime: %d" %self.currentLevelTime)
        print ("levelCount: %d" %self.levelCount)
        """
        self.pacman.print_pacman()
        """
        
        self.print_list_ghost()
        self.print_pill_status()
        self.print_power_pill_status()
        
        print ("timeOfLastGlobalReversal: %d" %self.timeOfLastGlobalReversal)
        print ("pacmanWasEaten: %s" %self.pacmanWasEaten)
        print ("pillWasEaten: %s" %self.pillWasEaten)
        print ("powerPillWasEaten: %s" %self.powerPillWasEaten)
        """
    
    