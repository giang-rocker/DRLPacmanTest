import sys
from tkinter import *
from Parse import Parse
from LogFile import LogFile
from Frame import Frame
from datetime import datetime
import timeit

start = timeit.default_timer()

logFile = LogFile("logGame")

listFileName=["a","b","c","d"]
print(sys.getsizeof(1))
print("START")
for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))

stateIndex = 50
inputNetWork=[]
for stateIndex in range (0,55):
    #print ("Parse Game State %d" %stateIndex)
    gameState = Parse.parse_game_state(logFile.get_state(stateIndex))

    inputNetWork.append(Frame.get_input_network(gameState))
print("DONE parse %d game State" %stateIndex)
stop = timeit.default_timer()

#print ("Size of all input: %d Bytes"  %( sys.getsizeof(inputNetWork[0][0]) ))
print ( str(stop-start)+ " seconds/%d" %stateIndex )
print ("avg: %f/%d state" %((float)((stop-start)/stateIndex),1))

stateIndex = 50
scale=12
margin =20

for k in range (0,4):
    canvas = Canvas(width=(Frame.frame_size_y*scale+2*margin), height=(Frame.frame_size_x*scale+2*margin), bg='black')  
    canvas.pack(side="left",expand=YES, fill=BOTH)
    

    for i in range (1, Frame.frame_size_x):
                for j in range (0, Frame.frame_size_y):
                    if ( inputNetWork[stateIndex][k].matrix[i][j] ==1 ):
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="blue",width=2)   
                    else:
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="grey",width=2) 
 
mainloop()          
