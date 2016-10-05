#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

class Frame:
    
    frame_size_x = 30
    frame_size_y = 28
    numberOfFrame  = 32
    
    def __init__(self,_frameName,_matrix):
        self.frameName = _frameName
        self.matrix = _matrix
    
    @staticmethod
    def get_input_network(_gameState):
        frames = [Frame]* Frame.numberOfFrame
        
        frames[0] =Frame ("Path",Frame.create_frame_path(_gameState))
        frames[1] =Frame ("Pill",Frame.create_frame_pill(_gameState))
        frames[2] =Frame ("PowerPill",Frame.create_frame_power_pill(_gameState))
        frames[3] =Frame ("PacManPosition",Frame.create_frame_paman_position(_gameState))

        for i in range (4, Frame.numberOfFrame):
            frames[i] =Frame ("PacManPosition",Frame.create_frame_paman_position(_gameState))
        
        return frames
        
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
        framePacMan =[[0 for x in range(Frame.frame_size_y)] for y in range(Frame.frame_size_x)] 
        
        x = int(_gameState.maze.listNode[_gameState.pacman.currentNodeIndex].y / 4)
        y = int(_gameState.maze.listNode[_gameState.pacman.currentNodeIndex].x  / 4)
                  
        framePacMan[x][y] = 1;
            
        return framePacMan
    
    def print_frame(self):
        for i in range (0, Frame.frame_size_x):
            for j in range (0, Frame.frame_size_y):
                print (  self.matrix[i][j])
