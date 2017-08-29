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


class play():
    def __init__(self):
        random.seed(time.time())
        self.ROBOT_IP = "192.168.1.12"
        self.ROBOT_PORT = 9559
        self.action_seqs = [[1, 2, 4, 3, 3, 5, 2, 1, 0, 2, 3, 5, 3, 4, 2, 1, 2, 3, 5, 1, 4, 1, 0, 3, 5],
                       [0, 0, 2, 4, 2, 3, 5, 3, 2, 4, 1, 1, 4, 2, 3, 5, 2, 1, 4, 2, 1, 3, 5, 4, 1],
                       [2, 3, 4, 1, 1, 2, 5, 2, 1, 0, 4, 1, 5, 2, 4, 3, 5, 3, 2, 2, 1, 1, 3, 5, 4],
                       [2, 2, 5, 3, 1, 4, 1, 0, 5, 3, 4, 2, 1, 0, 4, 1, 1, 3, 5, 3, 1, 0, 2, 2, 4],
                       [2, 4, 3, 2, 4, 2, 1, 5, 0, 4, 0, 1, 5, 2, 2, 1, 4, 2, 3, 5, 4, 2, 3, 5, 3],
                       [2, 3, 5, 3, 1, 4, 0, 1, 0, 4, 1, 1, 3, 5, 4, 1, 0, 2, 3, 4, 5, 2, 1, 4, 2],
                       [0, 1, 2, 4, 3, 2, 5, 3, 1, 4, 1, 0, 3, 5, 2, 3, 5, 1, 2, 3, 4, 2, 1, 3, 4],
                       [1, 0, 1, 4, 2, 3, 5, 3, 2, 0, 4, 1, 5, 2, 1, 0, 5, 2, 3, 4, 2, 3, 3, 4, 3],
                       [1, 2, 5, 2, 4, 3, 2, 5, 1, 0, 4, 1, 2, 5, 3, 2, 5, 1, 2, 4, 2, 3, 4, 1, 1],
                       [1, 2, 2, 4, 3, 0, 1, 5, 2, 4, 3, 5, 3, 2, 2, 1, 1, 2, 4, 3, 2, 5, 1, 2, 3],
                       [0, 1, 2, 3, 4, 3, 5, 1, 2, 3, 4, 3, 2, 0, 1, 2, 3, 4, 3, 2, 2, 3, 3, 4, 2],
                       [0, 1, 2, 5, 1, 0, 2, 3, 3, 4, 3, 2, 1, 0, 2, 3, 5, 2, 3, 5, 2, 4, 3, 2, 3]]
        self.positive_success = ["That was great! Keep up the good work!", "Wow, you do great! Go on!",
                            "Awesome! Keep going!"]
        self.positive_failure = ["Oh, that was wrong! Don't give up!", "Oh, you missed it! No problem! Go on!",
                            "Oops, that was not correct! That's OK! Keep going!"]
        self.negative_success = ["Ok, that was easy enough! Let's see now!", "Well, ok! Maybe you were lucky!",
                            "OK, you got it! Was it random??"]
        self.negative_failure = ["Hmmm! I don't think you are paying any attention! Try harder!",
                            "Hey! Are you there? Stay focused!", "Oh, wrong? You need to concentrate more!"]
        self.turn = 1
        self.game = 1


    def connect(self):
        self.tts = ALProxy("ALTextToSpeech", self.ROBOT_IP, self.ROBOT_PORT)  ## For robot to say the text mentioned
        # memory = ALProxy("ALMemory", ROBOT_IP, 9559)
        self.aup = ALProxy("ALAudioPlayer", self.ROBOT_IP, self.ROBOT_PORT)  ## For Robot to play the audio mentioned

    def introduction(self,user_folder,session_id):
        intro = open(user_folder + "session_" + str(session_id) + "/intro",'w')  ## Writes an Intro File (currently empty hence commented)
        server = mps.initialize(intro)
        server.start()

        # Robot Introduction
        """
        self.tts.say("Hi! My name is Stewie!")
        self.tts.say("Let's play a game!")
        time.sleep(0.5)
        self.tts.say("I will say a sequence of letters and you have to repeat it")
        time.sleep(0.5)
        self.tts.say("After the sequence is completed, you will listen to a beep sound!")
        time.sleep(0.9)
        self.aup.playSine(1000, 100, 0, 1)
        time.sleep(1.5)
        self.tts.say("After the sound, you have to respond, by pressing the buttons in the correct order") 
        time.sleep(0.5)
        self.tts.say("Please remember, that you need to give your response after the beep sound!")
        time.sleep(0.5)
        self.tts.say("Use only one hand, and make sure, that each button is pressed properly! Let's try with an example!")
        time.sleep(0.5)

        seq = ["b", "b", "a", "c", "a"]
        for item in seq:
            time.sleep(0.5)
            self.tts.say(item)
        self.aup.playSine(1000, 100, 0, 1)
        sig2 = 1 
        res = []	
        while(sig2):
            res.append(readchar.readkey().lower())
            if len(res) == len(seq):
                sig2 = 0

        time.sleep(0.7)
        self.tts.say("Great! Let's start!")
        """
        intro.close()
        server.stop()
        server.free()