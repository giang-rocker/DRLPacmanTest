#currently following FullPingPong.py
import sys
import os
from tkinter import *
from Parse import Parse
from LogFile import LogFile
from Frame import Frame
from datetime import datetime
from Move import MOVE
import timeit
import socket  

import tensorflow as tf
import sys
import random
import numpy as np
GAME = 'pacman' # the name of the game being played for log files
ACTIONS = 4 # number of valid actions
GAMMA = 0.99 # decay rate of past observations
OBSERVE = 40000 # timesteps to observe before traini ng
EXPLORE = 40000 # frames over which to anneal epsilon
FINAL_EPSILON = 0.05 # final value of epsilon
INITIAL_EPSILON = 1 # starting value of epsilon
REPLAY_MEMORY = 50000 # number of previous transitions to remember
BATCH = 32 # size of minibatch
K = 1 # only select an action every Kth frame, repeat prev for others
SIZEX = 30
SIZEY=30
NUM_OF_FRAME = 31
TRANING_TIME = 100
SAVING_STEP =20
LEARNING_RATE =0.0025
SKIP_FRAME = 1
NUM_OF_LEARNED_GAME = 10
TRANING_CURRENT_TIME = 1


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
    input_layer = tf.placeholder("float", [1,SIZEX, SIZEY, NUM_OF_FRAME])

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



def calculate_value_game_state(input_layer, readout, h_fc1, sess, gameState):
    
    gameObject = Parse.parse_game_state(gameState)
    s_t=Frame.get_input_network(gameObject)
    
    print(s_t.shape)
    
    print(len(s_t))
    for st in s_t[3]:
        print (st.shape)
        #print(st)
    
    print(len(s_t))
    readout_t = readout.eval(feed_dict = {input_layer : [s_t]})[0]
    action_index = np.argmax(readout_t)
    
   
    
    print("State" + str(gameObject.totalTime))
    print(readout_t)
    return action_index

# END OF RUNING GAME

#GET GAME STATE


sess = tf.InteractiveSession()

   

# PRE-CALCULATE BLANK MAZE
listFileName=["a","b","c","d"]
for i in range (0 , 4):
    Parse.maze.append(Parse.parse_maze_info(listFileName[i]))
# GET ALL GAME STATES


 

input_layer, readout, h_fc1 = createNetwork()

# MORE VARIABLE
saver = tf.train.Saver()
gameState=[]
gameState.append("0,44,100,44,0,934,LEFT,3,false,498,0,0,NEUTRAL,1292,0,16,NEUTRAL,1292,0,36,NEUTRAL,1292,0,56,NEUTRAL,1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000111111111111111111111111111111111111111111111111111111111111111111111111,1111,-1,false,false,false,false,false,false,false")
#gameState.append("0,45,100,45,0,933,LEFT,3,false,498,0,0,NEUTRAL,1292,0,15,NEUTRAL,1292,0,35,NEUTRAL,1292,0,55,NEUTRAL,1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111110000000000111111111111111111111111111111111111111111111111111111111111111111111111,1111,-1,false,false,false,false,false,false,false")
#gameState.append("0,46,110,46,0,932,LEFT,3,false,498,0,0,NEUTRAL,1292,0,14,NEUTRAL,1292,0,34,NEUTRAL,1292,0,54,NEUTRAL,1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000111111111111111111111111111111111111111111111111111111111111111111111111,1111,-1,false,false,false,false,false,true,false")
#gameState.append("0,48,110,48,0,930,LEFT,3,false,498,0,0,NEUTRAL,1292,0,12,NEUTRAL,1292,0,32,NEUTRAL,1292,0,52,NEUTRAL,1111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111100000000000111111111111111111111111111111111111111111111111111111111111111111111111,1111,-1,false,false,false,false,false,false,false")


sess.run(tf.initialize_all_variables())

checkpoint = tf.train.get_checkpoint_state("saved_networks")
if checkpoint and checkpoint.model_checkpoint_path:
    saver.restore(sess, checkpoint.model_checkpoint_path)
    print ("Successfully loaded:%s", checkpoint.model_checkpoint_path)
else:
    print ("Could not find old network weights")


print("AFTER LOAD NET")
for gt in gameState:
    calculate_value_game_state(input_layer, readout, h_fc1, sess, gt)



print("GAME_OVER")

