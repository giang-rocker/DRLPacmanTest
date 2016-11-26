#currently following FullPingPong.py
import sys

from Parse import Parse
from LogFile import LogFile
from Frame import Frame 
from datetime import datetime
from Move import MOVE
import timeit
import socket  
import os
import tensorflow as tf
import sys
import random
import gc
import numpy as np
from collections import deque

GAME = 'pacman' # the name of the game being played for log files
ACTIONS = 4 # number of valid actions
GAMMA = 0.95 # decay rate of past observations
OBSERVE = 200000 # timesteps to observe before traini ng
EXPLORE = 200000 # frames over which to anneal epsilon
FINAL_EPSILON = 0.05 # final value of epsilon
INITIAL_EPSILON = 1 # starting value of epsilon
REPLAY_MEMORY = 200000 # number of previous transitions to remember
BATCH = 64 # size of minibatch
SIZEX = 30
SIZEY=30
NUM_OF_FRAME = 32
TRANING_TIME = 100
LEARNING_RATE =0.0005
SKIP_FRAME = 4
NUM_OF_LEARNED_GAME = 10
NO_NEED_RANDOM = True

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.001, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

def createNetwork():
    W_conv1 = weight_variable([5, 5, NUM_OF_FRAME, 64])
    b_conv1 = bias_variable([64])

    W_conv2 = weight_variable([3, 3, 64, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([2, 2, 64, 64])
    b_conv3 = bias_variable([64])
    
    W_conv4 = weight_variable([2, 2, 64, 64])
    b_conv4 = bias_variable([64])
    
    W_fc1 = weight_variable([1024, 512])
    #W_fc1 = weight_variable([256, 512])
    b_fc1 = bias_variable([512])

    W_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # INPUT LAYER
    input_layer = tf.placeholder("float", [None, SIZEX, SIZEY, NUM_OF_FRAME])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(input_layer, W_conv1, 1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 1) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3, 1) + b_conv3)
    h_pool3 = max_pool_2x2(h_conv3)
    
    h_conv4 = tf.nn.relu(conv2d(h_pool3, W_conv4, 1) + b_conv4)
    #h_conv4 = tf.nn.relu(conv2d(h_conv3, W_conv4, 1) + b_conv4)
    #h_pool4 = max_pool_2x2(h_conv4)

    h_pool4_flat = tf.reshape(h_conv4, [-1,  1024])
    #h_pool4_flat = tf.reshape(h_pool4, [-1, 256])
    
    
    h_fc1 = tf.nn.relu(tf.matmul(h_pool4_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2
    
    #print(h_pool3.get_shape())
    return input_layer, readout, h_fc1
#start



#MAIN

sess = tf.InteractiveSession()
  

# PRE-CALCULATE BLANK MAZE
listFileName=["a","b","c","d"]
for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))
# GET ALL GAME STATES
 

input_layer, readout, h_fc1 = createNetwork()

# MORE VARIABLE
D = deque() # replay memory
a = tf.placeholder("float", [None, ACTIONS])
y = tf.placeholder("float", [None])
readout_action = tf.reduce_sum(tf.mul(readout, a), reduction_indices = 1)    
cost = tf.reduce_mean(tf.square(y - readout_action))
train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost)
saver = tf.train.Saver(max_to_keep=None)


sess.run(tf.initialize_all_variables())

timeStart = timeit.default_timer()
currentTime = timeit.default_timer()
oldCurrentTime =currentTime
 
command ="START_GAME"
gameState = "xxx"
action = 4
 
sock = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
print(host)
port = 22009     
sock.connect(('', port))
sock.send((command +"\n").encode())
terminator=False
gameOver = "OVER"
logGame=[]
#logMove =[]
numOfGame =1146
epsilon = INITIAL_EPSILON
totalTimeStep  =0

 
#LOAD NETWORK INCASE ALREADY LEARNING
checkpoint = tf.train.get_checkpoint_state("saved_networks")
if checkpoint and checkpoint.model_checkpoint_path:
    saver.restore(sess, checkpoint.model_checkpoint_path)
    print ("Successfully loaded:", checkpoint.model_checkpoint_path)
else:
    print ("Could not find old network weights")


#SUPERVISEDLEARNING
#supervised_learning(input_layer, readout, h_fc1, sess, train_step,sock,saver)
#count game
target = open("logCNN/logError.txt", 'r')
numOfGame = sum(1 for line in target)
print(numOfGame)
target.close()

#LOAD LAST GAME STATE
currentGame = numOfGame -1

while(len(D)< REPLAY_MEMORY):
    target = open("logCNN/logGameCNN"+str(currentGame)+".txt", 'r')
    
    logGame=target.readlines()
    
    lenX =  len(logGame)
    originalObject =[]
    originalFrame =[]
    #PARSE GAME STATE - ADD FIRST, LAST AND ALL POS HAVE X Y %4 ==0
    currentObject =Parse.parse_game_state(logGame[0])
    originalObject.append(currentObject)
    originalFrame.append(Frame.get_input_network(currentObject))

    for i in range(1,lenX-1):
        currentObject = Parse.parse_game_state(logGame[i])
        if(currentObject.pacmanWasEaten!="True"):
            pacmanPosX = currentObject.maze.listNode[currentObject.pacman.currentNodeIndex].y
            pacmanPosY = currentObject.maze.listNode[currentObject.pacman.currentNodeIndex].x
            if(pacmanPosX %4!=0 or pacmanPosY%4!=0 ):
                continue
        originalObject.append(currentObject)
        originalFrame.append( Frame.get_input_network (currentObject))

    currentObject =Parse.parse_game_state(logGame[lenX-1])
    originalObject.append(currentObject)
    originalFrame.append(Frame.get_input_network(currentObject))
    # END ADD CURRENT DOMAIN

    lenX = len(originalObject)
    for i in range (0,lenX-1):
        s_t = originalFrame[i]
            #SET ACTION
        terminal = False
        tempReward = 0

        a_t = np.zeros([ACTIONS])
        action_index = originalObject[i+1].pacman.lastMoveMade
        a_t[action_index-1] = 1

        s_t1 = originalFrame[i+1]

        if ( originalObject[i+1].pacmanWasEaten == "True" ):
            tempReward-=1000
            if (originalObject[i+1].pacman.numberOfLivesRemaining> 0 and originalObject[i+1].gameOver=="True"):
                tempReward-=9000
            terminal = True
        if(originalObject[i].currentLevelTime<3999):
            if ( originalObject[i+1].levelCount != originalObject[i].levelCount ):
                tempReward+=1000

        #if(originalObject[i+1].activePill>0 and originalObject[i+1].currentLevelTime>3990):
        #   tempReward-=1000

        if ( originalObject[i].pacman.lastMoveMade == MOVE.get_opposite_move(originalObject[i+1].pacman.lastMoveMade) ):
            tempReward -=10

        r_t = originalObject[i+1].score - originalObject[i].score +tempReward

        if(r_t==0):
            r_t =-2

        #D.append((s_t, a_t, r_t, s_t1, terminal))
        #r_t = finalScore - originalObject[nextFrame].score
        D.append((s_t, a_t, r_t, s_t1, terminal))
        #if len(currentDomain) > REPLAY_CURRENT_MEMORY:
        #   currentDomain.popleft()

        if(terminal):        
            i +=1
    print("DONE LOAD GAME " +str(currentGame)+ " - " + str(len(logGame)) +" - total: " + str(len(D)) )
    currentGame-=1
    target.close ()


#ENDSUPERVISEDLEARNING
print("START  %d %d" %(OBSERVE, EXPLORE))

if(NO_NEED_RANDOM):
    epsilon = FINAL_EPSILON

while(terminator==False):
    gameState = sock.recv(port)
    
    #GAME_OVER
    if(len(gameState)<70):
        print(gameState)
        
        
        # save game state
         
        #tranning_network(input_layer, readout, h_fc1, sess, logGame,train_step,sock,saver,numOfGame)
        
        # ADD GAME STATE TO DOMAIN WHAT EVER
        #totalTimeStep +=len(logGame)
        
        # add all 10k gameState to Domain

        lenX =  len(logGame)
        originalObject = []
        originalFrame = []
        #PARSE GAME STATE - ADD FIRST, LAST AND ALL POS HAVE X Y %4 ==0
        currentObject =Parse.parse_game_state(logGame[0])
        originalObject.append(currentObject)
        originalFrame.append(Frame.get_input_network(currentObject))
            
        for i in range(1,lenX-1):
            currentObject = Parse.parse_game_state(logGame[i])
            if(currentObject.pacmanWasEaten!="True" and currentObject.currentLevelTime!=1):
                pacmanPosX = currentObject.maze.listNode[currentObject.pacman.currentNodeIndex].y
                pacmanPosY = currentObject.maze.listNode[currentObject.pacman.currentNodeIndex].x
                if(pacmanPosX %4!=0 or pacmanPosY%4!=0 ):
                    continue
            originalObject.append(currentObject)
            originalFrame.append( Frame.get_input_network (currentObject))
            
        currentObject =Parse.parse_game_state(logGame[lenX-1])
        originalObject.append(currentObject)
        originalFrame.append(Frame.get_input_network(currentObject))
        # END ADD CURRENT DOMAIN
        
        lenX = len(originalObject)
        currentDomain = deque()
        for i in range (0,lenX-1):
            s_t = originalFrame[i]
            #SET ACTION
            terminal = False
            tempReward = 0
            
            a_t = np.zeros([ACTIONS])
            action_index = originalObject[i+1].pacman.lastMoveMade
            a_t[action_index-1] = 1
        
            s_t1 = originalFrame[i+1]
            
            if ( originalObject[i+1].pacmanWasEaten == "True" ):
                tempReward-=1000
                if (originalObject[i+1].pacman.numberOfLivesRemaining> 0 and originalObject[i+1].gameOver=="True"):
                    tempReward-=9000
                terminal = True
            if(originalObject[i].currentLevelTime<3999):
                if ( originalObject[i+1].levelCount != originalObject[i].levelCount ):
                    tempReward+=1000
            
            #if(originalObject[i+1].activePill>0 and originalObject[i+1].currentLevelTime>3990):
            #   tempReward-=1000
            
            if ( originalObject[i].pacman.lastMoveMade == MOVE.get_opposite_move(originalObject[i+1].pacman.lastMoveMade) ):
                tempReward -=10
            
            r_t = originalObject[i+1].score - originalObject[i].score +tempReward
            
            if(r_t==0):
                r_t =-2
            
            #D.append((s_t, a_t, r_t, s_t1, terminal))
            #r_t = finalScore - originalObject[nextFrame].score
            currentDomain.append((s_t, a_t, r_t, s_t1, terminal))
            #if len(currentDomain) > REPLAY_CURRENT_MEMORY:
            #   currentDomain.popleft()
            
            if(terminal):        
                i +=1
            
        # END OF ADDING
        
        
        #TRANNING CURRENT GAME ANYWAY
        #if(len(D)>OBSERVE):
        
        currentBatch = min(len(currentDomain),BATCH)
        
        error =0
       # TRAINING CURRENT GAME
        for i in range (0,5):
                #socket.send(("TRANNING %.2f" %(i*100.0/tranning_time) +"\n").encode())     
                minibatch = random.sample((currentDomain), currentBatch)

                # get the batch variablesi
                s_j_batch = [d[0] for d in minibatch]
                a_batch = [d[1] for d in minibatch]
                r_batch = [d[2] for d in minibatch]

                #list_s_j1 = [d[3] for d in minibatch]
                s_j1_batch = [d[3] for d in minibatch]
                #for state in list_s_j1:
                #    s_j1_batch.append( Frame.get_input_network ( Parse.parse_game_state(state) )  )

                y_batch = []

                readout_j1_batch = readout.eval(feed_dict = {input_layer : s_j1_batch})

                for k in range(0, len(minibatch)):
                    # if terminal only equals reward
                    if (minibatch[k][4] == True ):
                        y_batch.append(r_batch[k])
                    else:
                        y_batch.append(r_batch[k] + GAMMA * np.max(readout_j1_batch[k]))
                
                error+=cost.eval(feed_dict = {y : y_batch,a : a_batch,input_layer : s_j_batch})
                # perform gradient step
                train_step.run(feed_dict = {
                    y : y_batch,
                    a : a_batch,
                    input_layer : s_j_batch})
                
        # END TRANING CURRENT GAME
       
        #ADD TO CURRENT DOMAIN TO GLOBAL DOMAIN
        for d in currentDomain:
            D.append(d)
            if len(D) > REPLAY_MEMORY:
                D.popleft()
        
        avgError = error/5
        # TRANGIING REPLAY MEMMORY
        if(  NO_NEED_RANDOM == True ):     
            #batch = min(BATCH, len(D))
            #training TRANING_TIME times with BATCH size
            for i in range (0,2*TRANING_TIME):
                #socket.send(("TRANNING %.2f" %(i*100.0/tranning_time) +"\n").encode())     
                minibatch = random.sample((D), BATCH)

                # get the batch variablesi
                s_j_batch = [d[0] for d in minibatch]
                a_batch = [d[1] for d in minibatch]
                r_batch = [d[2] for d in minibatch]

                #list_s_j1 = [d[3] for d in minibatch]
                s_j1_batch = [d[3] for d in minibatch]
                #for state in list_s_j1:
                #    s_j1_batch.append( Frame.get_input_network ( Parse.parse_game_state(state) )  )

                y_batch = []

                readout_j1_batch = readout.eval(feed_dict = {input_layer : s_j1_batch})

                for k in range(0, len(minibatch)):
                    # if terminal only equals reward
                    if (minibatch[k][4] == True ):
                        y_batch.append(r_batch[k])
                    else:
                        y_batch.append(r_batch[k] + GAMMA * np.max(readout_j1_batch[k]))
                
                 
                # perform gradient step
                error+=cost.eval(feed_dict = {y : y_batch,a : a_batch,input_layer : s_j_batch})
                train_step.run(feed_dict = {
                    y : y_batch,
                    a : a_batch,
                    input_layer : s_j_batch})
                    
            avgError = error/(2*TRANING_TIME+5)
                
        if(numOfGame%20==0):
            saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = numOfGame)    
        #print("DONE TRAIN GAME %d th" %numOfGame)
        
        # END OF TRANNING
        """
        #log train
        target = open("logCNN/logTrain"+str(numOfGame)+".txt", 'w')
        target.truncate() # clear it 
        for line in logTrain:
            target.write(line+"\n")
        target.close()
        """ 
        
         
        """
        target = open("logCNN/logMoveCNN"+str(numOfGame)+".txt", 'w')
        for line in logMove:
            target.write(str(ti)+" "+line+"\n")
            ti+=1
        target.close()
        """
        # edit epsilon
        if epsilon >= FINAL_EPSILON and totalTimeStep> OBSERVE:
            print("REDUCE EPSILON")
            epsilon -= FINAL_EPSILON/2
        
        currentTime = timeit.default_timer()
        #print("Time %d - TotalTime: %d " %(currentTime - oldCurrentTime,currentTime - timeStart) )
        oldCurrentTime = currentTime
        
        
        #SAVE LOG GAME
        target = open("logCNN/logGameCNN"+str(numOfGame)+".txt", 'w')
        target.truncate() # clear it 
        for line in logGame:
            target.write(line)
        target.close()
        
        target = open("logCNN/logError.txt", 'a')
        target.write(str(numOfGame)+","+str(avgError)+","+str(currentTime - timeStart)+"\n")
        target.close()
        
        numOfGame +=1
        #print("START_GAME %d with epsilon %.2f" %(numOfGame,epsilon))
        
        logGame=[]
        #logMove=[]
        
        #reset memory
        #if(numOfGame %400==0):
        #    D=[]
        #    D= deque()
            
        
        command ="START_GAME"
        sock.send((command +"\n").encode())
        
    else :
         
        gameStateX = gameState.decode("utf-8") 
        logGame.append(gameStateX)
        
        if random.random() <= epsilon :
            action = "RANDOM"
            #logMove.append("RANDOM")
        else: #or GET THE MAX ACTION FROM CURRENT STATE
            gameObject = Parse.parse_game_state(gameStateX)
            s_t=Frame.get_input_network(gameObject)
            readout_t = readout.eval(feed_dict = {input_layer : [s_t]})[0]
            action = np.argmax(readout_t)+1
            #str1 = " ".join(str(i) for i in readout_t)
            #logMove.append((str1)+ " "+str(action))
            
        #send back to java
        sock.send(("%s" %(action) +"\n").encode())


print("GAME_OVER")
