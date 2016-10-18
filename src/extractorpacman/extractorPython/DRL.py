#currently following FullPingPong.py
import sys
from tkinter import *
from Parse import Parse
from LogFile import LogFile
from Frame import Frame
from datetime import datetime
from Move import MOVE
import timeit

import tensorflow as tf
import sys
import random
import numpy as np

GAME = 'pacman' # the name of the game being played for log files
ACTIONS = 5 # number of valid actions
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 500. # timesteps to observe before training
EXPLORE = 500. # frames over which to anneal epsilon
FINAL_EPSILON = 0.05 # final value of epsilon
INITIAL_EPSILON = 1.0 # starting value of epsilon
REPLAY_MEMORY = 590000 # number of previous transitions to remember
BATCH = 100 # size of minibatch
K = 1 # only select an action every Kth frame, repeat prev for others
SIZEX = 30
SIZEY=30
NUM_OF_FRAME = 34
TRANING_TIME = 5


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
    W_conv1 = weight_variable([5, 5, NUM_OF_FRAME, 32])
    # number of output
    b_conv1 = bias_variable([32])

    W_conv2 = weight_variable([3, 3, 32, 64])
    b_conv2 = bias_variable([64])

    W_conv3 = weight_variable([2, 2, 64, 64])
    b_conv3 = bias_variable([64])

    W_fc1 = weight_variable([256, 256])
    b_fc1 = bias_variable([256])

    W_fc2 = weight_variable([256, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # INPUT LAYER
    input_layer = tf.placeholder("float", [None, SIZEX, SIZEY, NUM_OF_FRAME])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(input_layer, W_conv1, 2) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 1) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3, 1) + b_conv3)
    h_pool3 = max_pool_2x2(h_conv3)

    h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    # 1600 how many sate ?
    #h_conv3_flat = tf.reshape(h_conv3, [-1, 256])

    h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return input_layer, readout, h_fc1

#start

def tranning_network(s, readout, h_fc1, sess, gameState):
    print("START OF TRAINING NETWORK")
    a = tf.placeholder("float", [None, ACTIONS])
    y = tf.placeholder("float", [None])
    readout_action = tf.reduce_sum(tf.mul(readout, a), reduction_indices = 1)
    
    cost = tf.reduce_mean(tf.square(y - readout_action))
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)
    
    sess.run(tf.initialize_all_variables())
    
    #first state
    timeStep = 0
    s_t = gameState[timeStep]
    D=[]
    print("ADD GAME STATE TO DOMAIN")
    # add all 10k gameState to Domain
    for i in range(1, len(gameState)):
        
        #SET ACTION
        a_t = np.zeros([ACTIONS])
        action_index = 0
        gameStateObjectNext = Parse.parse_game_state(gameState[timeStep+1])
        action_index = gameStateObjectNext.pacman.lastMoveMade
        a_t[action_index] = 1
        
        # SET REWARD
        r_t = gameStateObjectNext.score
        
        # SET NEXTSTATE
        s_t1 = gameState[timeStep+1]
        
        # if GAME OVER SET TERMINAL
        terminal = (gameStateObjectNext.pacman.numberOfLivesRemaining >0) 
        
        #ADD TO DOMAIN
        D.append((s_t, a_t, r_t, s_t1, terminal))
        
        # NEXT STATE IN SEQUENCE
        s_t = s_t1
        timeStep += 1
        
        
    print("DONE ADD GAME STATE TO DOMAIN")
    print("START TO TRAINING BATCH")
    #training 1k times with BATCH size
    for i in range (0,TRANING_TIME):
        print ("Training Time %d " %i )
        #random BATCH gamestate in Domain D
        minibatch = random.sample(D, BATCH)

        # get the batch variables
        
        list_s_j = [d[0] for d in minibatch]
        s_j_batch = []
        for state in list_s_j:
            s_j_batch.append( Frame.get_input_network ( Parse.parse_game_state(state) )  )
        
        
        a_batch = [d[1] for d in minibatch]
        r_batch = [d[2] for d in minibatch]
        
        list_s_j1 = [d[3] for d in minibatch]
        s_j1_batch = []
        for state in list_s_j1:
            s_j1_batch.append( Frame.get_input_network ( Parse.parse_game_state(state) )  )

        y_batch = []
        
        readout_j1_batch = readout.eval(feed_dict = {s : s_j1_batch})
        
        for k in range(0, len(minibatch)):
            # if terminal only equals reward
            if minibatch[i][4]:
                y_batch.append(r_batch[k])
            else:
                y_batch.append(r_batch[k] + GAMMA * np.max(readout_j1_batch[k]))

        # perform gradient step
        train_step.run(feed_dict = {
            y : y_batch,
            a : a_batch,
            input_layer : s_j_batch})
            
        print ("DONE")


    
        
    print("DONE TRAIN ONE GAME")   
    
    
    return 


#GET GAME STATE

timeStart = timeit.default_timer()
sess = tf.InteractiveSession()

logFile = LogFile("logGame")

# PRE-CALCULATE BLANK MAZE
listFileName=["a","b","c","d"]
for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))
# GET ALL GAME STATES
gameState = logFile.get_all_game_state()
 

input_layer, readout, h_fc1 = createNetwork()
tranning_network(input_layer, readout, h_fc1, sess, gameState)
 
timeEnd =start = timeit.default_timer()

print ( str(timeEnd-timeStart)+ " seconds to train %d " %TRANING_TIME + " batch of %d " %BATCH )