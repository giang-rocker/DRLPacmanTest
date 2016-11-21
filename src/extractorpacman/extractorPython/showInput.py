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
REPLAY_MEMORY = 400000 # number of previous transitions to remember
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

    
    s_t_original,s_t=Frame.get_input_network_debug(gameObject)
    
    for st in s_t_original:
        print(st)
    
     
    readout_t = readout.eval(feed_dict = {input_layer : [s_t]})[0]
    print(readout_t)
    action_index = np.argmax(readout_t)
     
    return action_index

# END OF RUNING GAME


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
 
command ="START_GAME"
gameState = "xxx"
action = 4
print("Loading network weights")
#LOAD NETWORK INCASE ALREADY LEARNING
checkpoint = tf.train.get_checkpoint_state("saved_networks")
if checkpoint and checkpoint.model_checkpoint_path:
    saver.restore(sess, checkpoint.model_checkpoint_path)
    print ("Successfully loaded:", checkpoint.model_checkpoint_path)
else:
    print ("Could not find old network weights")

print("Done loading network")
while(1):
    string = input()
    values = string.split(" ")    
    game = int(values[0])
    stateIndex = int(values[1])
    print("Game: " + str(game) + " State " + str(stateIndex))
    directory = 'logCNN'
    nameLogFile =directory+"/logGameCNN"+ str(game)
    logFile = LogFile(nameLogFile)
        
    listGameState = logFile.get_all_game_state()
    
    if(stateIndex > len(listGameState)):
        print ("State out of Range")
    else:
        gameState = listGameState[stateIndex]
        print(gameState)
        calculate_value_game_state(input_layer, readout, h_fc1, sess, gameState)
        
    print ("-NEXT-")
    
    
     
 
