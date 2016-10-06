import sys
from tkinter import *
from Parse import Parse
from LogFile import LogFile
from Frame import Frame
from datetime import datetime
from Move import MOVE
import timeit


def draw_frame(frame):
    canvas = Canvas(width=(Frame.frame_size_y*scale+2*margin), height=(Frame.frame_size_x*scale+2*margin), bg='black')  
    canvas.pack(side="left",expand=YES, fill=BOTH)
    

    for i in range (1, Frame.frame_size_x):
                for j in range (0, Frame.frame_size_y):
                    if ( frame[i][j] ==1 ):
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="blue",width=2)   
                    elif  ( frame[i][j] ==-1 ):
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="red",width=2) 
                    else :
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="grey",width=2) 
    
    mainloop()   


start = timeit.default_timer()

logFile = LogFile("logGame")

listFileName=["a","b","c","d"]
print(sys.getsizeof(1))
print("START")
for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))

 
 
gameState = logFile.get_all_game_state()

inputNetWork = []

for gamestate in gameState:
    inputNetWork.append( Frame.get_input_network ( Parse.parse_game_state(gamestate) )  )


print("DONE parse %d game State" %len (gameState))
stop = timeit.default_timer()

#print ("Size of all input: %d Bytes"  %( sys.getsizeof(inputNetWork[0][0]) ))
print ( str(stop-start)+ " seconds/%d" %len(gameState ))
print ("avg: %f/%d state" %((float)((stop-start)/ len(gameState)),1))
 
scale=6
margin =20
 
print("%d" %(len (inputNetWork)))
       
