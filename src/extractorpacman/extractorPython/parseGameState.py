#!/usr/bin/env python2
#encoding: UTF-8

# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

"""
def parseGameState( gameState ) {
         
    
        _setPills(currentMaze = mazes[mazeIndex]);

        for (int i = 0; i < values[index].length(); i++)
            if (values[index].charAt(i) == '1')
                pills.set(i);
            else
                pills.clear(i);

        index++;

        for (int i = 0; i < values[index].length(); i++)
            if (values[index].charAt(i) == '1')
                powerPills.set(i);
            else
                powerPills.clear(i);

        timeOfLastGlobalReversal = Integer.parseInt(values[++index]);
        pacmanWasEaten = Boolean.parseBoolean(values[++index]);

        ghostsEaten = new EnumMap<GHOST, Boolean>(GHOST.class);

        for (GHOST ghost : GHOST.values())
            ghostsEaten.put(ghost, Boolean.parseBoolean(values[++index]));

        pillWasEaten = Boolean.parseBoolean(values[++index]);
        powerPillWasEaten = Boolean.parseBoolean(values[++index]);
    }
    
"""    
    
from PacMan import PacMan
from Ghosts import Ghosts
from Maze import Maze
from Maze import GameState
from Move import MOVE
 
maze =[] 

def parse_game_state( gameState ):
    index=0
    # Game information
    values = gameState.split(",")
    mazeIndex = int (values[index])
    currentMaze = maze[mazeIndex]
    
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
    
    gameState.print_game_state()
    
    
def parse_maze_info(mazeName):
    # create entire maze graph. From original map infomation mazeIndex.txt
    #fixed size of maze
    defaultWidth = 108;
    defaultHeight = 116; 
    graphNode = [[0 for x in range(defaultWidth)] for y in range(defaultHeight)]
    
    #open file mazeIndex.txt
    mazeFile = open("mazes/"+mazeName+'.txt', 'r')
    lines=mazeFile.readlines()
    
    mazeInfo = lines[0].split("\t");
    mazeName = mazeInfo[0];
    initialPacManNodeIndex = int(mazeInfo[1])
    lairNodeIndex = int(mazeInfo[2]);
    initialGhostNodeIndex = int(mazeInfo[3])
    numberOfNode = int(mazeInfo[4])
    numberOfPill = int(mazeInfo[5])
    numberOfPowerPill =int(mazeInfo[6])
    numberOfJucntion = int(mazeInfo[7])
    
    maze = Maze(mazeName,initialPacManNodeIndex,lairNodeIndex,initialGhostNodeIndex,numberOfNode,numberOfPill,numberOfPowerPill,numberOfJucntion)
   # maze.print_maze();
    
    return maze



 
logFile = open('logGame.txt', 'r')

listFileName=["a","b","c","d"]
for i in range (0 , 4):
  maze.append(parse_maze_info(listFileName[i]))

i = 0
for line in logFile:
    if(line=="\n"):
        break
    print ("State %d" %i)
    
    parse_game_state(line)
    print("")
     
    i+=1
       

 
 
