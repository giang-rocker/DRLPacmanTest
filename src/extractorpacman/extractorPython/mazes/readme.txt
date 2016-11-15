The files containing the graphs are structured as follows:

First line is a header that contains information regarding the maze. The information is as follows:

name of maze
start node for Ms Pac-Man
node that corresponds to the lair
start node for the ghosts
number of nodes in the maze
number of pills in the maze
number of power pills in the maze
number of junctions in the maze

All other lines corresponds to individual nodes on the graph. Each node has the following information:

node index 0
x-coordinate	1 
y-coordinate 2 
neighbouring node in UP direction (-1 if none)3 
neighbouring node in RIGHT direction (-1 if none)4 
neighbouring node in DOWN direction (-1 if none)5 
neighbouring node in LEFT direction (-1 if none)6 
pill-index of the node (-1 if none)7 
power-pill index of the node (-1 if none)8