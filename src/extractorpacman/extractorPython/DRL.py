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
BATCH = 50 # size of minibatch
K = 1 # only select an action every Kth frame, repeat prev for others
SIZEX = 30
SIZEY=30
NUM_OF_FRAME = 34

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

    W_fc1 = weight_variable([256, 512])
    b_fc1 = bias_variable([512])

    W_fc2 = weight_variable([512, ACTIONS])
    b_fc2 = bias_variable([ACTIONS])

    # INPUT LAYER
    input_layer = tf.placeholder("float", [None, SIZEX, SIZEY, NUM_OF_FRAME])

    # hidden layers
    h_conv1 = tf.nn.relu(conv2d(input_layer, W_conv1, 2) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2, 1) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    h_conv3 = tf.nn.relu(conv2d(h_conv2, W_conv3, 1) + b_conv3)
    h_pool3 = max_pool_2x2(h_conv3)

    #h_pool3_flat = tf.reshape(h_pool3, [-1, 256])
    # 1600 how many sate ?
    h_conv3_flat = tf.reshape(h_conv3, [-1, 256])

    h_fc1 = tf.nn.relu(tf.matmul(h_conv3_flat, W_fc1) + b_fc1)

    # readout layer
    readout = tf.matmul(h_fc1, W_fc2) + b_fc2

    return input_layer, readout, h_fc1

#start

def calculate_value_game_state(s, readout, h_fc1, sess, gameState):
    
    a = tf.placeholder("float", [None, ACTIONS])
    y = tf.placeholder("float", [None])
    readout_action = tf.reduce_sum(tf.mul(readout, a), reduction_indices = 1)
    
    cost = tf.reduce_mean(tf.square(y - readout_action))
    train_step = tf.train.AdamOptimizer(1e-6).minimize(cost)
    
    sess.run(tf.initialize_all_variables())
    
    
    s_t=[]
    s_t.append(Frame.get_input_network(Parse.parse_game_state(gameState[400])))
    s_t.append(Frame.get_input_network(Parse.parse_game_state(gameState[401])))
    
    # initial
    for i in range (0,2):
        readout_t = readout.eval(feed_dict = {s : [s_t[i]]})[0]
        action_index = np.argmax(readout_t)
        print(readout_t)
        print(action_index)
        
    
    readout_j1_batch = readout.eval(feed_dict = {s : [s_t[1]]})[0]
    reward = 3
    a_t = np.zeros([ACTIONS])
    a_t[Parse.parse_game_state(gameState[401]).pacman.lastMoveMade] = 1
     
    y_batch=[]
    a_batch=[]
    s_j_batch=[]  
    
    y_batch.append(reward + GAMMA * np.max(readout_j1_batch))    
    a_batch.append(a_t)  
    print(Parse.parse_game_state(gameState[401]).pacman.lastMoveMade)
    s_j_batch.append(s_t[0])
    
    train_step.run(feed_dict = {
                y : y_batch,
                a : a_batch,
                input_layer : s_j_batch})
        
        
    print("DONE TRAIN")   
    
    s_t=[]
    s_t.append(Frame.get_input_network(Parse.parse_game_state(gameState[400])))
    s_t.append(Frame.get_input_network(Parse.parse_game_state(gameState[401])))
    
    # initial
    for i in range (0,2):
        readout_t = readout.eval(feed_dict = {s : [s_t[i]]})[0]
        action_index = np.argmax(readout_t)
        print(readout_t)
        print(action_index)
        
    return 


#GET GAME STATE


sess = tf.InteractiveSession()

logFile = LogFile("logGame")

# PRE-CALCULATE BLANK MAZE
listFileName=["a","b","c","d"]
for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))
# GET ALL GAME STATES
gameState = logFile.get_all_game_state()
 

input_layer, readout, h_fc1 = createNetwork()
calculate_value_game_state(input_layer, readout, h_fc1, sess, gameState)
 