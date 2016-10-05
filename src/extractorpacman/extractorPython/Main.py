
from tkinter import *
from Parse import Parse
from LogFile import LogFile
from Frame import Frame

logFile = LogFile("logGame")

listFileName=["a","b","c","d"]


for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))

stateIndex = 50
gameState = Parse.parse_game_state(logFile.get_state(stateIndex))

inputNetWork = Frame.get_input_network(gameState)
scale=6
margin =20

for k in range (0,4):
    canvas = Canvas(width=(Frame.frame_size_y*scale+2*margin), height=(Frame.frame_size_x*scale+2*margin), bg='black')  
    canvas.pack(expand=NO, fill=BOTH)                  


    for i in range (1, Frame.frame_size_x):
                for j in range (0, Frame.frame_size_y):
                    if ( inputNetWork[k].matrix[i][j] ==1 ):
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="blue",width=2)   
                    else:
                        canvas.create_rectangle(margin+j*scale, margin+i*scale, margin+j*scale+scale,margin+i*scale+ scale,fill="grey",width=2) 
 
mainloop()          