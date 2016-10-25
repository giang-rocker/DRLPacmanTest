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
OBSERVE = 20 # timesteps to observe before training
EXPLORE = 20 # frames over which to anneal epsilon
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

gameState="3,8674,21280,1705,3,226,LEFT,3,true,218,47,0,RIGHT,1129,47,0,RIGHT,440,47,0,DOWN,167,47,0,DOWN,000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001000111000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,0000,8576,false,false,false,false,false,false,false"

sess.run(tf.initialize_all_variables())
print("BEFORE LOAD NET")
calculate_value_game_state(input_layer, readout, h_fc1, sess, gameState)

directory = 'LogGameFile'

numOfLogGameFile = len([item for item in os.listdir(directory) if os.path.isfile(os.path.join(directory, item))])

print("%d Files" %numOfLogGameFile )


for i in range (1, numOfLogGameFile+1):
    nameLogFile ="F0000"[:-len(str(i))] + str(i)
    print(nameLogFile)
  
checkpoint = tf.train.get_checkpoint_state("saved_networks")
if checkpoint and checkpoint.model_checkpoint_path:
    saver.restore(sess, checkpoint.model_checkpoint_path)
    print ("Successfully loaded:%s", checkpoint.model_checkpoint_path)
else:
    print ("Could not find old network weights")

saver.save(sess, 'saved_networks/' + GAME + '-dqn', global_step = 1)    
    

print("AFTER LOAD NET")
calculate_value_game_state(input_layer, readout, h_fc1, sess, gameState)



print("GAME_OVER")

