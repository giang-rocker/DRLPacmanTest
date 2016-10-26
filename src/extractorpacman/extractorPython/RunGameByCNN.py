#currently following FullPingPong.py
import sys
from tkinter import *
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
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 19 # timesteps to observe before training
EXPLORE = 19 # frames over which to anneal epsilon
FINAL_EPSILON = 0.05 # final value of epsilon
INITIAL_EPSILON = 1.0 # starting value of epsilon
REPLAY_MEMORY = 590000 # number of previous transitions to remember
BATCH = 100 # size of minibatch
K = 1 # only select an action every Kth frame, repeat prev for others
SIZEX = 30
SIZEY=30
NUM_OF_FRAME = 32
TRANING_TIME = 100
SAVING_STEP =20
LEARNING_RATE =0.00005
SKIP_FRAME = 4
NUM_OF_LEARNED_GAME = 5


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev = 0.01)
    return tf.Variable(initial)

def bias_variable(shape):
    initial = tf.constant(0.01, shape = shape)
    return tf.Variable(initial)

def conv2d(x, W, stride):
    return tf.nn.conv2d(x, W, strides = [1, stride, stride, 1], padding = "SAME")

def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize = [1, 2, 2, 1], strides = [1, 2, 2, 1], padding = "SAME")

def createNetwork():
    # network weights
    # size of filter X, Y , number of input, number of output
    W_conv1 = weight_variable([5, 5, NUM_OF_FRAME, 64])
    # number of output
    b_conv1 = bias_variable([64])

    W_conv2 = weight_variable([3, 3, 64, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([2, 2, 64, 64])
    b_conv3 = bias_variable([64])
    
    W_conv4 = weight_variable([2, 2, 64, 64])
    b_conv4 = bias_variable([64])

    W_fc1 = weight_variable([256, 512])
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
    h_pool4 = max_pool_2x2(h_conv4)

    h_pool4_flat = tf.reshape(h_pool4, [-1, 256])
    # 1600 how many sate ?
    #h_conv3_flat = tf.reshape(h_conv3, [-1, 256])

    h_fc1 = tf.nn.relu(tf.matmul(h_pool4_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2
    
    #print(h_pool3.get_shape())
    return input_layer, readout, h_fc1
#start




def calculate_value_game_state(s, readout, h_fc1, sess, gameState):
    
    
    gameObject = Parse.parse_game_state(gameState)
    
    #print("AT Game Step: %d Score %d" %(gameObject.totalTime, gameObject.score))

    
    s_t=Frame.get_input_network(gameObject)
     
    readout_t = readout.eval(feed_dict = {s : [s_t]})[0]
    
    action_index = np.argmax(readout_t)
     
    return action_index

# END OF RUNING GAME

def tranning_network(s, readout, h_fc1, sess, gameState,train_step, socket,saver,ithGame):
    #LOAD NET
    # saving and loading networks
    
    checkpoint = tf.train.get_checkpoint_state("saved_networks")
    if checkpoint and checkpoint.model_checkpoint_path:
        saver.restore(sess, checkpoint.model_checkpoint_path)
        print ("Successfully loaded:", checkpoint.model_checkpoint_path)
    else:
        print ("Could not find old network weights")
    
    
    
    print("START OF TRAINING GAME %d th" %ithGame)   
     #first state
   
    s_t = Frame.get_input_network ( Parse.parse_game_state(gameState[0]))
    D = deque()
    print(len(gameState))
    # add all 10k gameState to Domain
    
    lastValidMove = MOVE.NEUTRAL
    lastAction  = MOVE.NEUTRAL
    oldScore =0
    for i in range(1, len(gameState)-1):
        
        
        
        #SET ACTION
        a_t = np.zeros([ACTIONS])
        action_index = 0
        for k in range (1,SKIP_FRAME+1):
            gameStateObjectNext = Parse.parse_game_state(gameState[min(len(gameState)-1,(i+k))])
            action_index = gameStateObjectNext.pacman.lastMoveMade
            
            if (action_index==4):
                lastValidMove =  lastAction
                a_t[lastValidMove] =1
            else:
                lastAction = action_index
                a_t[lastAction] =1
            
            if (gameStateObjectNext.pacmanWasEaten  ):
                break
        
        
        
        
         # SET REWARD
        r_t = gameStateObjectNext.score - oldScore
        oldScore = gameStateObjectNext.score
        
        # SET NEXTSTATE
        s_t1 = Frame.get_input_network ( gameStateObjectNext)
        
        # if GAME OVER SET TERMINAL
        terminal = gameStateObjectNext.pacmanWasEaten
        
        #ADD TO DOMAIN
        D.append((s_t, a_t, r_t, s_t1, terminal))
        
        # NEXT STATE IN SEQUENCE
        
        if (terminal):
            i = gameStateObjectNext.totalTime+1
            if(i<len(gameState)-1):
                s_t = Frame.get_input_network ( Parse.parse_game_state(gameState[i]))
        else :
            s_t= s_t1
            
        
         
        # if teminal, skip the next step
        
    #training 1k times with BATCH size
    for i in range (0,TRANING_TIME):
        socket.send(("TRANNING %f" %(i*100.0/TRANING_TIME) +"\n").encode())     
        minibatch = random.sample(list(D), BATCH)
        
        
        
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
        
        readout_j1_batch = readout.eval(feed_dict = {s : s_j1_batch})
        
        for k in range(0, len(minibatch)):
            # if terminal only equals reward
            if minibatch[k][4]:
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

a = tf.placeholder("float", [None, ACTIONS])
y = tf.placeholder("float", [None])
readout_action = tf.reduce_sum(tf.mul(readout, a), reduction_indices = 1)    
cost = tf.reduce_mean(tf.square(y - readout_action))
train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cost)
saver = tf.train.Saver()


sess.run(tf.initialize_all_variables())

 
 
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

#SUPERVISEDLEARNING
#supervised_learning(input_layer, readout, h_fc1, sess, train_step,sock,saver)


while(terminator==False):
    gameState = sock.recv(port)
    
    
    if(len(gameState)<8):
        action = random.randrange(ACTIONS)
      #send back to java
        sock.send(("%d" %(action) +"\n").encode())
        
    elif(len(gameState)<15):
        print(gameState)
        
        #SAVE LOG GAME
        target = open("logGameCNN.txt", 'w')
        target.truncate() # clear it 
        for line in logGame:
            target.write(line)
        target.close()
        # save game state
         
        tranning_network(input_layer, readout, h_fc1, sess, logGame,train_step,sock,saver,numOfGame)
        command ="START_GAME"
        sock.send((command +"\n").encode())
        
        # edit epsilon
        if epsilon > FINAL_EPSILON and numOfGame > OBSERVE:
            epsilon -= (INITIAL_EPSILON - FINAL_EPSILON) / EXPLORE
        
        numOfGame +=1
        print("START_GAME %d" %numOfGame)
        logGame=[]
    else :
         
        gameStateX = gameState.decode("utf-8") 
        logGame.append(gameStateX)
        
        if random.random() <= epsilon or numOfGame <= OBSERVE:
            action = random.randrange(ACTIONS)
        else: #or GET THE MAX ACTION FROM CURRENT STATE
            action  = calculate_value_game_state(input_layer, readout, h_fc1, sess, gameStateX)
    
        #send back to java
        sock.send(("%s" %(action) +"\n").encode())


print("GAME_OVER")
s.close 
    

