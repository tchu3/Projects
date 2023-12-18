# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:05:43 2021

@author: tommych
"""

# Import Tkinter for GUI interface 
import tkinter as tk
from PIL import Image, ImageTk
import cv2

import numpy as np
frameStack = []

class frothWindow:
    def __init__(self, window):
        self.window = window
        self.window.title('Froth Screen Detection Tool')
        
        # Initialize buttons and labels
        self.title=tk.Label(window, text='Froth Screen Detection Tool', font = ('Arial Narrow', 16, 'bold'))
        
        self.vid = videoCapture(r'\\cnrl.com\cnrl\users\tommych\Downloads\[UPSET] 07-10-2020 0817PM.mkv')
        
        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()
        
        self.delay = 15
        self.update()
        
        self.window.mainloop()
    
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.getFrame()
        
        if ret:
            # Pass current frame to crossingFrequency Method 
            crossFreq = crossingFrequencyMethod(frame)
            
            # Rescale crossing freq filter from 0-255
            crossFreqScale = crossFreq/50
            crossFreqFilter = 1*(crossFreq>30)
            
            # Adjust RBG index
            frame[:,:,0][frame[:,:,0]*crossFreqFilter > 0] = 255
            frame[:,:,1][frame[:,:,0]*crossFreqFilter > 0] = 0
            frame[:,:,2][frame[:,:,0]*crossFreqFilter > 0] = 0
            
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
            
            
        self.window.after(self.delay, self.update)

class videoCapture:    
    def __init__(self, videoSource):
         # Open Video
        self.vid = cv2.VideoCapture(videoSource)
        
        if not self.vid.isOpened():
            print("Unable to open video source")
        
        # Get video height and width
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        print(self.width)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        print(self.height)
        
            
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()
    
    def getFrame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, frame)
            else:
                return (ret, None)
        else:
            return (ret, None)
         
def crossingFrequencyMethod(currentFrame):
    frameSpan = 50 # 20 frame moving average span        
    currentFrame = cv2.cvtColor(currentFrame, cv2.COLOR_BGR2GRAY)
    
    # Initialize variables for result storage
    tempCrossFreqArray = np.zeros((currentFrame.shape[0],currentFrame.shape[1]))
    
    # Append to frameStack unless 50 frames have already been collected
    if len(frameStack) < frameSpan:
        frameStack.append(currentFrame)
    else:
        frameStack.pop(0)
        frameStack.append(currentFrame)
        
        # Define moving average array
        movingAverage = np.zeros((currentFrame.shape[0],currentFrame.shape[1]))
        # Iterate over each frame to get the moving average
        for i in range(frameSpan-1,0,-1):
            iterFrame = np.array(frameStack[i])
            movingAverage = movingAverage + iterFrame
        movingAverage = movingAverage/frameSpan
        
        # Iterate over each frame to determine if the mean was crossed
        for i in range(1,frameSpan - 1):
            currentPosition = (frameStack[i]-movingAverage) # Current position relative to the mean
            previousPosition = (frameStack[i - 1]-movingAverage) # Previous position relative to the mean
            productArray = np.multiply(currentPosition,previousPosition)
            tempCrossFreqArray = 1*(productArray<0) + tempCrossFreqArray
        #tempCrossFreqArray = 1*(productArray>40)
        
    return tempCrossFreqArray
        


### INITIALIZE GUI ###
frothWindow(tk.Tk())

    