#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from Move import MOVE
import numpy as np
class Frame:
    
    frame_size_x = 30
    frame_size_y = 30
    numberOfFrame  = 34
    
    def __init__(self,_frameName,_matrix):
        self.frameName = _frameName
        self.matrix = _matrix
    
    @staticmethod
    def get_input_network(_gameState):
        frames = []
        
        frameMatrix=[]
        
        frames.append(Frame ("Path",Frame.create_frame_path(_gameState)))
        frameMatrix.append(Frame.create_frame_path(_gameState))
        frames.append(Frame ("Pill",Frame.create_frame_pill(_gameState)))
        frameMatrix.append(Frame.create_frame_pill(_gameState))
        frames.append(Frame ("PowerPill",Frame.create_frame_power_pill(_gameState)))
        frameMatrix.append(Frame.create_frame_power_pill(_gameState))
        
        #9 frame of pacman Position [3-11]
        framePacman =Frame.create_frame_paman_position(_gameState)
        for i in range (0,9):
            frames.append( Frame("PacmanPosition", framePacman[i]))
            frameMatrix.append(framePacman[i])

        #5 frame of pacman last Move  [12-16]
        framePacman = Frame.create_frame_paman_lastMove(_gameState)
        for i in range (0,5):
            frames.append( Frame("PacmanLastMove", framePacman[i]))
            frameMatrix.append(framePacman[i])
        
            
        #9 frame of pacman Position [17-25]
        framePacman =Frame.create_frame_ghost_position(_gameState)
        for i in range (0,9):
            frames.append( Frame("GhostPosition", framePacman[i]))
            frameMatrix.append(framePacman[i])

        #5 frame of pacman last Move  [26-30]
        framePacman = Frame.create_frame_ghost_lastMove(_gameState)
        for i in range (0,5):
            frames.append( Frame("GhostLastMove", framePacman[i])) 
            frameMatrix.append(framePacman[i])
        
        #1 edible Time    31
        frames.append(Frame ("edibleTime",Frame.create_frame_edible_time(_gameState)))
        frameMatrix.append(Frame.create_frame_edible_time(_gameState))
        #1 CurrentLevel Level    32
        frames.append(Frame ("currentLevel",Frame.create_frame_current_time(_gameState)))
        frameMatrix.append(Frame.create_frame_current_time(_gameState))
        #1 Current Time    33
        frames.append(Frame ("currentTime",Frame.create_frame_current_level(_gameState)))
        frameMatrix.append(Frame.create_frame_current_level(_gameState))
        
        frameMatrixReturn = np.stack(frameMatrix, axis = 2)
        
        return frameMatrixReturn
        
    @staticmethod
    def create_frame_path(_gameState):
        frameMiniMap =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        
        for  i in range (0, _gameState.maze.numberOfNode):
            if (_gameState.maze.listNode[i].y %4 ==0 ) and (_gameState.maze.listNode[i].x %4==0 ):
                x = int(_gameState.maze.listNode[i].y / 4)
                y = int(_gameState.maze.listNode[i].x  / 4)
                 
                frameMiniMap[x][y] = 1;
            
        return frameMiniMap
    
    @staticmethod
    def create_frame_pill(_gameState):
        framePill =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        
        for  i in range (0, _gameState.maze.numberOfPill):
            if (_gameState.listPillStatus[i]==True) and (_gameState.maze.listPill[i].y %4 ==0 ) and (_gameState.maze.listPill[i].x %4==0 ):
                
                x = int(_gameState.maze.listPill[i].y / 4)
                y = int(_gameState.maze.listPill[i].x  / 4)
                
                framePill[x][y] = 1;
            
        return framePill
    
    @staticmethod
    def create_frame_power_pill(_gameState):
        framePowerPill =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        
        for  i in range (0, _gameState.maze.numberOfPowerPill):
            if (_gameState.maze.listPowerPill[i].y %4 ==0 ) and (_gameState.maze.listPowerPill[i].x %4==0 ):
                x = int(_gameState.maze.listPowerPill[i].y / 4)
                y = int(_gameState.maze.listPowerPill[i].x  / 4)
                  
                framePowerPill[x][y] = 1;
            
        return framePowerPill
        
    @staticmethod
    def create_frame_paman_position(_gameState):
        framePacMan =[[[0 for col in range(Frame.frame_size_y)]for row in range(Frame.frame_size_x)] for x in range(9)]
        
        x = int(_gameState.maze.listNode[_gameState.pacman.currentNodeIndex].y / 4)
        y = int(_gameState.maze.listNode[_gameState.pacman.currentNodeIndex].x  / 4)
        
        realPosX = _gameState.maze.listNode[_gameState.pacman.currentNodeIndex].y
        realPosY = _gameState.maze.listNode[_gameState.pacman.currentNodeIndex].x
                  
        framePacMan[0][x][y] = 1;
        framePacMan[1+(realPosX % 4)][x][y] = 1; 
        framePacMan[5+(realPosY % 4)][x][y] = 1;
        return framePacMan 
             
    @staticmethod
    def create_frame_paman_lastMove(_gameState):
        framePacMan =[[[0 for col in range(Frame.frame_size_y)]for row in range(Frame.frame_size_x)] for x in range(5)]
        
        x = int(_gameState.maze.listNode[_gameState.pacman.currentNodeIndex].y / 4)
        y = int(_gameState.maze.listNode[_gameState.pacman.currentNodeIndex].x  / 4)
        
        
        move = _gameState.pacman.lastMoveMade
        framePacMan[move%5][x][y] = 1;
        return framePacMan
    
    @staticmethod
    def create_frame_ghost_position(_gameState):
        frameGhost =[[[0 for col in range(Frame.frame_size_y)]for row in range(Frame.frame_size_x)] for x in range(9)]
        
        for i in range (0,4):
            x = int(_gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].y / 4)
            y = int(_gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].x  / 4)

            realPosX = _gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].y
            realPosY = _gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].x
            
            value = 0
            if (_gameState.ghosts[i].edibleTime >0):
                value = -1
            else:
                value = 1
            
            #print("%d %d" %(x,y))
            frameGhost[0][x][y] = value;
            frameGhost[1+(realPosX % 4)][x][y] = value; 
            frameGhost[5+(realPosY % 4)][x][y] = value;
            
        return frameGhost 
             
    @staticmethod
    def create_frame_ghost_lastMove(_gameState):
        frameGhost =[[[0 for col in range(Frame.frame_size_y)]for row in range(Frame.frame_size_x)] for x in range(5)]
        
        for i in range (0,4):
            x = int(_gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].y / 4)
            y = int(_gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].x  / 4)

            move = _gameState.ghosts[i].lastMoveMade
            #print("%s  " %MOVE.get_move(move))
            
            frameGhost[move%5][x][y] = 1;
            
        return frameGhost
    
    @staticmethod
    def create_frame_edible_time(_gameState):
        frameGhost =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        
        for i in range (0,4):
            x = int(_gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].y / 4)
            y = int(_gameState.maze.listNode[_gameState.ghosts[i].currentNodeIndex].x  / 4)

            edibleTime = _gameState.ghosts[i].edibleTime 
            frameGhost [x][y] = edibleTime;
            
        return frameGhost
    
    @staticmethod
    def create_frame_current_time(_gameState):
        frame =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        time = _gameState.totalTime
        
        for i in range (0, Frame.frame_size_x):
            for j in range (0, Frame.frame_size_y):
                frame[i][j] = time
            
        return frame
    
    @staticmethod
    def create_frame_current_level(_gameState):
        frame =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        level = _gameState.levelCount
        
        for i in range (0, Frame.frame_size_x):
            for j in range (0, Frame.frame_size_y):
                frame[i][j] = level
            
        return frame
    
    def print_frame(self):
        for i in range (0, Frame.frame_size_x):
            for j in range (0, Frame.frame_size_y):
                print (  self.matrix[i][j])
