#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

from PacMan import PacMan
from Ghosts import Ghosts
from Maze import Maze
from Maze import GameState
from Move import MOVE
from LogFile import LogFile
from Nodes import Node,Pill,PowerPill

class Parse:
 
    maze =[] 
    @staticmethod
    def parse_game_state( gameStateInput ):
        index=0
        # Game information
        values = gameStateInput.split(",")
        mazeIndex = int (values[index])
        currentMaze = Parse.maze[mazeIndex]

        index+=1
        totalTime =  int (values[index])
        index+=1
        score =  int (values[index])
        index+=1
        currentLevelTime =  int (values[index])
        index+=1
        levelCount =  int (values[index])
        index+=1

        #PacMan information
        currentNodeIndex = int (values[index])
        index+=1
        lastMoveMade = MOVE.get_move (values[index])
        index+=1
        numberOfLivesRemaining = int (values[index])
        index+=1
        hasReceivedExtraLife =  (values[index].capitalize())
        index+=1
        pacman = PacMan (currentNodeIndex,lastMoveMade,numberOfLivesRemaining,hasReceivedExtraLife)

        #GHOST information
        listGhostName =["Blinky","Pinky","Inky","Sue"]
        listGhost=[]
        for ghostId in range(0, 4):
            ghostName = listGhostName[ghostId]
            ghostCurrentNodeIndex = int (values[index])
            index+=1
            edibleTime = int (values[index])
            index+=1
            lairTime = int (values[index])
            index+=1
            lastMoveMade = MOVE.get_move (values[index])
            index+=1
            ghost = Ghosts(ghostName,ghostCurrentNodeIndex,edibleTime,lairTime,lastMoveMade)
            listGhost.append(ghost)

        #pill info
        numberOfPill = currentMaze.numberOfPill
        listPillStatus=[]
        for i in range (0, numberOfPill):
                if (values[index][i] == '1') :
                    listPillStatus.append(True)
                else:
                    listPillStatus.append(False)
        index+=1

        #Power pill info
        numberOfPowerPill = currentMaze.numberOfPowerPill
        listPowerPillStatus=[]
        for i in range (0, numberOfPowerPill):
                if (values[index][i] == '1') :
                    listPowerPillStatus.append(True)
                else:
                    listPowerPillStatus.append(False)
        index+=1



        timeOfLastGlobalReversal = int(values[index])
        index+=1
        pacmanWasEaten = (values[index].capitalize());
        index+=1

        for ghostId in range(0, 4):
            listGhost[ghostId].wasEaten = (values[index].capitalize())
            index+=1


        pillWasEaten = (values[index].capitalize());
        index+=1
        powerPillWasEaten = (values[index].capitalize());
        index+=1

        # create maze by information
        gameState = GameState(currentMaze,mazeIndex,totalTime,score,currentLevelTime,levelCount,pacman,listGhost,listPillStatus,listPowerPillStatus,timeOfLastGlobalReversal,pacmanWasEaten,pillWasEaten,powerPillWasEaten)
        #gameState.print_game_state()    
        return gameState
        

    @staticmethod    
    def parse_maze_info(mazeName):
        # create entire maze graph. From original map infomation mazeIndex.txt

        #open file mazeIndex.txt
        mazeFile = open("mazes/"+mazeName+'.txt', 'r')
        lines=mazeFile.readlines()

        mazeInfo = lines[0].split("\t")
        mazeName = mazeInfo[0]
        initialPacManNodeIndex = int(mazeInfo[1])
        lairNodeIndex = int(mazeInfo[2])
        initialGhostNodeIndex = int(mazeInfo[3])
        numberOfNode = int(mazeInfo[4])
        numberOfPill = int(mazeInfo[5])
        numberOfPowerPill =int(mazeInfo[6])
        numberOfJucntion = int(mazeInfo[7])

        mazeX = Maze(mazeName,initialPacManNodeIndex,lairNodeIndex,initialGhostNodeIndex,numberOfNode,numberOfPill,numberOfPowerPill,numberOfJucntion)

        #parse NODE DETAIL

        for i in range (1,numberOfNode+1):
            nodeInfo = lines[i].split("\t")

            nodeIndex = int (nodeInfo[0])
            x = int (nodeInfo[1])
            y = int (nodeInfo[2])
            pillIndex = int (nodeInfo[7])
            powerPillIndex = int (nodeInfo[8])

            node = Node(nodeIndex,x,y,pillIndex,powerPillIndex)
            
            mazeX.listNode[nodeIndex] = node
            
            if (pillIndex!=-1):
                pill = Pill(nodeIndex,pillIndex,x,y)
                mazeX.listPill[pillIndex] = pill
            if (powerPillIndex!=-1):
                powerPill = PowerPill(nodeIndex,powerPillIndex,x,y)
                mazeX.listPowerPill[powerPillIndex] = powerPill

        mazeX.print_maze()
        return mazeX
 
 
