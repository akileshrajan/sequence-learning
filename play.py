#!/usr/bin/python

from naoqi import ALProxy
import numpy as np 
import readchar
import time
from random import randint
import os 
import muse_pyliblo_server as mps
import matplotlib.pyplot as plt
import gc
import random


# initialize random seed
random.seed(time.time())

# NAO parameters
#ROBOT_IP = "129.107.119.134" # ethernet
ROBOT_IP = "192.168.1.12"

tts = ALProxy("ALTextToSpeech", ROBOT_IP, 9559)  ## For robot to say the text mentioned
#memory = ALProxy("ALMemory", ROBOT_IP, 9559)
aup = ALProxy("ALAudioPlayer", ROBOT_IP, 9559)   ## For Robot to play the audio mentioned


# user info and folders
user = raw_input('Enter userID: ')
user_folder = "data/user_" + str(user) + '/'

if os.path.exists(user_folder):
	session_id = len(os.listdir(user_folder)) + 1
else:
	session_id = 1

os.makedirs(user_folder + "session_" + str(session_id)) 
intro = open(user_folder + "session_" + str(session_id) + "/intro", 'w')	## Writes an Intro File (currently empty hence commented)
server = mps.initialize(intro)
server.start()

# Robot Introduction 
"""
tts.say("Hi! My name is Stewie!")
tts.say("Let's play a game!")
time.sleep(0.5)
tts.say("I will say a sequence of letters and you have to repeat it")
time.sleep(0.5)
tts.say("After the sequence is completed, you will listen to a beep sound!")
time.sleep(0.9)
aup.playSine(1000, 100, 0, 1)
time.sleep(1.5)
tts.say("After the sound, you have to respond, by pressing the buttons in the correct order") 
time.sleep(0.5)
tts.say("Please remember, that you need to give your response after the beep sound!")
time.sleep(0.5)
tts.say("Use only one hand, and make sure, that each button is pressed properly! Let's try with an example!")
time.sleep(0.5)

seq = ["b", "b", "a", "c", "a"]
for item in seq:
	time.sleep(0.5)
	tts.say(item)
aup.playSine(1000, 100, 0, 1)
sig2 = 1 
res = []	
while(sig2):
	res.append(readchar.readkey().lower())
	if len(res) == len(seq):
		sig2 = 0

time.sleep(0.7)
tts.say("Great! Let's start!")
"""
intro.close()
server.stop()
server.free()

positive_success = ["That was great! Keep up the good work!", "Wow, you do great! Go on!", "Awesome! Keep going!"]
positive_failure = ["Oh, that was wrong! Don't give up!", "Oh, you missed it! No problem! Go on!", "Oops, that was not correct! That's OK! Keep going!"]
negative_success = ["Ok, that was easy enough! Let's see now!", "Well, ok! Maybe you were lucky!", "OK, you got it! Was it random??"]
negative_failure = ["Hmmm! I don't think you are paying any attention! Try harder!", "Hey! Are you there? Stay focused!", "Oh, wrong? You need to concentrate more!"]
			

rf = 0
server = []
s = 0 
correct = 0 
total = 0 

diff = [3,5,7,9]    # Difficulty level 3,5,7,9 characters of the letters
let = ('a','b','c') # Letters that form the sequence
Actions = ["Easy", "Medium", "Hard", "Positive Feedback", "Negative Feedback"]

dir_name = 'data/user_' + user + '/session_' +  str(session_id) + '/'
turn = 1
game = 1

# 10 sequences of predefined actions for data collection -- maybe find a more formal way to define actions -- e.g., distribution etc.
action_seqs = [[1,2,4,3,3,5,2,1,0,2,3,5,3,4,2,1,2,3,5,1,4,1,0,3,5], [0,0,2,4,2,3,5,3,2,4,1,1,4,2,3,5,2,1,4,2,1,3,5,4,1], [2,3,4,1,1,2,5,2,1,0,4,1,5,2,4,3,5,3,2,2,1,1,3,5,4],
			   [2,2,5,3,1,4,1,0,5,3,4,2,1,0,4,1,1,3,5,3,1,0,2,2,4], [2,4,3,2,4,2,1,5,0,4,0,1,5,2,2,1,4,2,3,5,4,2,3,5,3], [2,3,5,3,1,4,0,1,0,4,1,1,3,5,4,1,0,2,3,4,5,2,1,4,2],
			   [0,1,2,4,3,2,5,3,1,4,1,0,3,5,2,3,5,1,2,3,4,2,1,3,4], [1,0,1,4,2,3,5,3,2,0,4,1,5,2,1,0,5,2,3,4,2,3,3,4,3], [1,2,5,2,4,3,2,5,1,0,4,1,2,5,3,2,5,1,2,4,2,3,4,1,1],
			   [1,2,2,4,3,0,1,5,2,4,3,5,3,2,2,1,1,2,4,3,2,5,1,2,3], [0,1,2,3,4,3,5,1,2,3,4,3,2,0,1,2,3,4,3,2,2,3,3,4,2], [0,1,2,5,1,0,2,3,3,4,3,2,1,0,2,3,5,2,3,5,2,4,3,2,3]]

actions = action_seqs[randint(0,10)]
ps = 0 

total_score = 0 
previous_score = 0 
out = open(dir_name + "/output", 'w')
log_eeg = open(dir_name + "/state_EEG", 'a')
log_session = open(dir_name + "/logfile", 'a')
server = mps.initialize(out)
server.start()

while (turn<=len(actions)): 	
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)
		
	response = []
	res = []
	rf = 0 ## Robot feedback.

	# select action from predefined
	action = actions[turn-1]

	## record EEG signals when robot announces the sequence ##
	out = open(dir_name + "/robot_" + str(turn), 'w')
	server.f = out 
	##########################################################

	if action == 4: 
		rf = 1
		seq = list(np.random.choice(let, Dold))
	elif action == 5: 
		rf = 2
		seq = list(np.random.choice(let, Dold))
	else: 
		seq = list(np.random.choice(let, diff[action]))
		Dold = diff[action]

	length = len(seq)
	
	feedback_id = randint(0,2)
	## Detetrmines if previous user action is success or not and accordingly chooses feedback type.
    ## What statement said is chosen randomly. In the above line "feedback_id"
	if rf == 1: 
		if previous_success == 1: 
			tts.say(positive_success[feedback_id])
		else: 
			tts.say(positive_failure[feedback_id])

	if rf == 2: 
		if previous_success == 1: 
			tts.say(negative_success[feedback_id])
		else: 
			tts.say(negative_failure[feedback_id])

	## Loop to say the sequence of charecters
	for item in seq:
		time.sleep(0.8)
		tts.say(item)

	aup.playSine(1000, 100, 0, 1)       ## play beep sound for user to respond.

	time.sleep(1)

	## record EEG signals when user presses the buttons ##
	out = open(dir_name + "/user_" + str(turn), 'w')
	server.f = out
	######################################################

	# start time to measure response time
	start_time = time.time()

	################### CHECK USER RESPONSE AND CALCULATE SCORE ####################
	sig2 = 1
	first = 0 	
	while(sig2):
		res.append(readchar.readkey().lower())
		if first == 0: 
			reaction_time = time.time() - start_time
			first = 1
		if len(res) == Dold:
			sig2 = 0 
	
	completion_time = time.time() - start_time
	if seq != res:
		success = -1
		score = -1*(diff.index(length)+1)
	else: 
		success = 1
		score = diff.index(length) + 1
		correct += 1
	#################################################################################

	dataline = str(length) + ' ' + str(rf) + ' ' + str(previous_score) + ' robot_' + str(turn) + ' human_' + str(turn) + '\n'	
	log_eeg.write(dataline)
	dataline = str(turn) + ' ' + str(length) + ' ' + str(rf) + ' ' + str(score) + ' ' + str(success) + ' ' + str(reaction_time) + ' ' + str(completion_time) + ' ' + str(seq) + ' ' + str(res) + '\n'
	log_session.write(dataline)

	previous_success = success
	previous_score = score
	previous_rf = rf

	total_score += score
	turn += 1
		
out.close()
log_eeg.close()
log_session.close()
server.stop()

tts.say("That's the end of our session! Thank you for your time!! Hope to see you again!!!")
