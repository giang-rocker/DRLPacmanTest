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
import numpy as np
from collections import deque

GAME = 'pacman' # the name of the game being played for log files
ACTIONS = 4 # number of valid actions
GAMMA = 0.95 # decay rate of past observations
OBSERVE = 500000 # timesteps to observe before traini ng
EXPLORE = 500000 # frames over which to anneal epsilon
FINAL_EPSILON = 0.05 # final value of epsilon
INITIAL_EPSILON = 1 # starting value of epsilon
REPLAY_MEMORY = 200000 # number of previous transitions to remember
REPLAY_CURRENT_MEMORY = 4000 # last 4k step of current game
BATCH = 32 # size of minibatch
K = 1 # only select an action every Kth frame, repeat prev for others
SIZEX = 30
SIZEY=30
NUM_OF_FRAME = 11
TRANING_TIME = 100
SAVING_STEP =20
LEARNING_RATE =0.0005
SKIP_FRAME = 4
NUM_OF_LEARNED_GAME = 10
TRANING_CURRENT_TIME = 1
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



def calculate_value_game_state(input_layer, readout, h_fc1, sess, gameState):
    
    
    gameObject = Parse.parse_game_state(gameState)
    
    #print("AT Game Step: %d Score %d" %(gameObject.totalTime, gameObject.score))

    
    s_t=Frame.get_input_network(gameObject)
     
    readout_t = readout.eval(feed_dict = {input_layer : [s_t]})[0]
    
    action_index = np.argmax(readout_t)
     
    return action_index

# END OF RUNING GAME

def tranning_network(s, readout, h_fc1, sess, gameState,train_step, socket,saver,ithGame):
    #LOAD NET
    # saving and loading networks
        
    print("START OF TRAINING GAME %d th" %ithGame)   
     #first state
   
    
    print(len(gameState))
    # add all 10k gameState to Domain
    
    lastValidMove = MOVE.LEFT
    lastAction  = MOVE.NEUTRAL
    oldScore =0
    lenX =  len(gameState)
    originalObject =[]
    originalFrame =[]
    
    #precalculate
    for i in range(lenX):
        originalObject.append(Parse.parse_game_state(gameState[i]))
        originalFrame.append( Frame.get_input_network ( originalObject[i]))
    
    originalObject.append(Parse.parse_game_state(gameState[lenX-1]))
    originalObject[lenX].pacmanWasEaten="True"
    originalFrame.append( Frame.get_input_network ( originalObject[lenX]))      
    lenX+=1
    
    D = deque()
    #add to domain
    i = 0
    while(i < (lenX-1)):
        s_t = originalFrame[i]
        #SET ACTION
        a_t = np.zeros([ACTIONS])
        action_index = originalObject[i+1].pacman.lastMoveMade

        if (action_index==4) :
            action_index = lastValidMove
        else:
            lastValidMove= action_index

        a_t[action_index-1] = 1

        terminal = False

        if ((i+SKIP_FRAME )< lenX-1):
            nextFrame = i+SKIP_FRAME 
        else :
             nextFrame = lenX-1

        s_t1 = originalFrame[nextFrame]
        if ( originalObject[nextFrame].pacmanWasEaten == "True" ):
            terminal = True

        r_t = originalObject[nextFrame].score - oldScore
        oldScore = originalObject[nextFrame].score
        D.append((s_t, a_t, r_t, s_t1, terminal))


        if(terminal==True):
           i = nextFrame
        i+=1
            
    currentBatch = min(len(D),BATCH)
    #training 1k times with BATCH size
    tranning_time = lenX/100
    for i in range (0,tranning_time):
        #socket.send(("TRANNING %.2f" %(i*100.0/tranning_time) +"\n").encode())     
        minibatch = random.sample(list(D), currentBatch)
        
        # get the batch variablesi
        
        #list_s_j = [d[0] for d in minibatch]
        s_j_batch = [d[0] for d in minibatch]
        
        #for state in list_s_j:
        #    s_j_batch.append( Frame.get_input_network ( Parse.parse_game_state(state) )  )
        
        
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
        train_step.run(feed_dict = {
            y : y_batch,
            a : a_batch,
            input_layer : s_j_batch})
            
    saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = ithGame)    
    print("DONE TRAIN GAME %d th" %ithGame)   
    
    
    return 



def supervised_learning(s, readout, h_fc1, sess, train_step, socket,saver):
    #LOAD NET
    # saving and loading networks
    
    directory = 'LogGameFile'

    numOfLogGameFile = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])
    #NUM_OF_LEARNED_GAME = numOfLogGameFile
    print("START OF TRAINING BY SUPERVISED NETWORK")
     #first state
     
    for i in range (0,NUM_OF_LEARNED_GAME):
        
        nameLogFile =directory+"/F0000"[:-len(str(i))] + str(i)
        logFile = LogFile(nameLogFile)
        
        gameState = logFile.get_all_game_state()
        
        tranning_network(s, readout, h_fc1, sess, gameState,train_step, socket,saver,i)
        
        
        
    print("DONE SUPERVISED LEARNING")   
        
    return 


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
saver = tf.train.Saver()


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
logMove =[]
numOfGame =0
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



#ENDSUPERVISEDLEARNING
print("START  %d %d" %(OBSERVE, EXPLORE))

if(NO_NEED_RANDOM):
    epsilon = FINAL_EPSILON

while(terminator==False):
    gameState = sock.recv(port)
    
    #GAME_OVER
    if(len(gameState)<60):
        print(gameState)
        
        
        # save game state
         
        #tranning_network(input_layer, readout, h_fc1, sess, logGame,train_step,sock,saver,numOfGame)
        
        # ADD GAME STATE TO DOMAIN WHAT EVER
        totalTimeStep +=len(logGame)
        
        # add all 10k gameState to Domain

        lastValidMove = MOVE.LEFT
        lastAction  = MOVE.NEUTRAL
        oldScore =0
        lenX =  len(logGame)
        originalObject =[]
        originalFrame =[]
        count =0 
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
            if(originalObject[i].activePill==1):
                if ( originalObject[i+1].levelCount != originalObject[i].levelCount ):
                    tempReward+=1000
            
            if(originalObject[i+1].activePill>1 and originalObject[i+1].currentLevelTime>3990):
                tempReward-=1000

            r_t = originalObject[i+1].score - originalObject[i].score +tempReward
            if(r_t==0):
                r_t =-1
            
            #D.append((s_t, a_t, r_t, s_t1, terminal))
            #r_t = finalScore - originalObject[nextFrame].score
            currentDomain.insert(0,(s_t, a_t, r_t, s_t1, terminal))
            if len(currentDomain) > REPLAY_CURRENT_MEMORY:
                currentDomain.popleft()
            
                
            if(terminal):        
                i +=1
            
        # END OF ADDING
        
        logTrain =[]
        
        #TRANNING CURRENT GAME ANYWAY
        #if(len(D)>OBSERVE):
        print("START OF TRAINING AT GAME %d th" %numOfGame)   
        # TRANING 10 CURRENT GAME
        #for i in range (0, TRANING_CURRENT_TIME):
        # ONCE TIME ONLY ?
        #minibatch = currentDomain
        s_j_batch = [d[0] for d in currentDomain]
        a_batch = [d[1] for d in currentDomain]
        r_batch = [d[2] for d in currentDomain]
        s_j1_batch = [d[3] for d in currentDomain]
        y_batch = []
        readout_j1_batch = readout.eval(feed_dict = {input_layer : s_j1_batch})
        for k in range(0, len(currentDomain)):
            if (currentDomain[k][4] == True ):
                y_batch.append(r_batch[k])
            else:
                y_batch.append(r_batch[k] + GAMMA * np.max(readout_j1_batch[k]))
            
        for i in range (2):
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
        
        currentDomain=deque()
        
        if(totalTimeStep>OBSERVE or NO_NEED_RANDOM ):         
            #batch = min(BATCH, len(D))
            #training TRANING_TIME times with BATCH size
            for i in range (0,TRANING_TIME):
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
                train_step.run(feed_dict = {
                    y : y_batch,
                    a : a_batch,
                    input_layer : s_j_batch})

            saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = numOfGame)    
            print("DONE TRAIN GAME %d th" %numOfGame)
        
        # END OF TRANNING
        """
        #log train
        target = open("logCNN/logTrain"+str(numOfGame)+".txt", 'w')
        target.truncate() # clear it 
        for line in logTrain:
            target.write(line+"\n")
        target.close()
        """ 
        #SAVE LOG GAME
        target = open("logCNN/logGameCNN"+str(numOfGame)+".txt", 'w')
        target.truncate() # clear it 
        for line in logGame:
            target.write(line)
        target.close()
        ti=0
        target = open("logCNN/logMoveCNN"+str(numOfGame)+".txt", 'w')
        for line in logMove:
            target.write(str(ti)+" "+line+"\n")
            ti+=1
        target.close()
        
        # edit epsilon
        if epsilon >= FINAL_EPSILON and totalTimeStep> OBSERVE:
            print("REDUCE EPSILON")
            epsilon -= FINAL_EPSILON/2
        
        currentTime = timeit.default_timer()
        print("Time %d - TotalTime: %d " %(currentTime - oldCurrentTime,currentTime - timeStart) )
        oldCurrentTime = currentTime
        
        numOfGame +=1
        print("START_GAME %d with epsilon %.2f" %(numOfGame,epsilon))
        
        logGame=[]
        logMove=[]
        
        #reset memory
        if(numOfGame %400==0):
            D=[]
            D= deque()
            
        
        command ="START_GAME"
        sock.send((command +"\n").encode())
        
    else :
         
        gameStateX = gameState.decode("utf-8") 
        logGame.append(gameStateX)
        
        if random.random() <= epsilon :
            action = "RANDOM"
            logMove.append("RANDOM")
        else: #or GET THE MAX ACTION FROM CURRENT STATE
            gameObject = Parse.parse_game_state(gameStateX)
            s_t=Frame.get_input_network(gameObject)
            readout_t = readout.eval(feed_dict = {input_layer : [s_t]})[0]
            action = np.argmax(readout_t)+1
            str1 = " ".join(str(i) for i in readout_t)
            logMove.append((str1)+ " "+str(action))
            
        #send back to java
        sock.send(("%s" %(action) +"\n").encode())


print("GAME_OVER")
