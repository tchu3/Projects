# -*- coding: utf-8 -*-
"""
Created on Mon Apr 27 12:49:08 2020

@author: Tommy Chu
"""

#### DEFINE IMPORTS ####
import cv2
import numpy as np
import math
import os
import shapely
from shapely.geometry import LineString, Point

from matplotlib import pyplot as plt
plt.rcParams["figure.figsize"] = (10,5)

# Import skimage for imageio
import imageio
from skimage import transform
import scipy as sp

# Import PIL libraries - Python Image Library
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
########################

mainDirectory = os.getcwd()

##### LOAD IMAGE & VIDEO #####

r'''
# Open mp4 video - this code is used to generate the frames
imgUpsetVideo = cv2.VideoCapture(mainDirectory + r'\1# 249-XT-0033 MRM-Froth-ScreenA@2020-04-27T060959.510Z.mkv')

path = mainDirectory + r'\Frames'
frameRate = imgUpsetVideo.get(5)
count = 0

while(imgUpsetVideo.isOpened()):
    frameNum = imgUpsetVideo.get(1)
    retFrame, frame = imgUpsetVideo.read()
    if (retFrame != True):
        break
    # Floor is the number rounded down
    if (frameNum % math.floor(frameRate) == 0):
        fileName = "frame%d.jpg" % count
        count += 1
        cv2.imwrite(os.path.join(path , fileName), frame)
imgUpsetVideo.release()
'''

# Image array gives the value of each pixel in the image
# imgSK = imageio.imread('x175-1030x816.jpg')
imgClean = Image.open(mainDirectory + r'\Images\249-XT-0032 MRM-Froth-ScreenA_04_13_2020 11_56_42 PM.jpg')
imgUpset = Image.open(mainDirectory + r'\Images\249-XT-0032 MRM-Froth-ScreenA_04_13_2020 11_56_42 PM.jpg')

# Store the original image size for later preprocessing
width, height = imgClean.size

# Function to return crop box
def getCroppedBox(bottomBox, leftBox, rightBox):
    
    # Get intersect of bottom box and left box
    # Convert and store all points of the froth box in A,B,C,D,E,F
    A = (leftBox[0], height - leftBox[1])
    B = (leftBox[2], height - leftBox[3])
    C = (bottomBox[0], height - bottomBox[1])
    D = (bottomBox[2], height - bottomBox[3])
    E = (rightBox[0], height - rightBox[1])
    F = (rightBox[2], height - rightBox[3])
    
    # Left line equation
    leftSlope = (B[1] - A[1])/(B[0] - A[0])
    leftIntercept = A[1] - (A[0]*leftSlope)
    
    # Right line equation
    rightSlope = (F[1] - E[1])/(F[0] - E[0])
    rightIntercept = E[1] - (E[0]*rightSlope)
    
    # Bottom line equation       
    botSlope = (D[1] - C[1])/(D[0] - C[0])
    botIntercept = C[1] - (C[0]*botSlope)
    
    # Calculate the intersect of the bottom line and the left line
    _xIntersect = (botIntercept-leftIntercept)/(leftSlope-botSlope)
    leftIntersect = (_xIntersect,botSlope*_xIntersect+botIntercept)
    print(leftIntersect)
    
    # THIS RUNS if the right line couldn't be found - when the default right line is the just the right point
    if E[0] == F[0]:    
        rightIntersect = (E[0],E[1])
    # Calculate the intersect of the bottom line and the right line
    else:
        _xIntersect = (botIntercept-rightIntercept)/(rightSlope-botSlope)
        rightIntersect = (_xIntersect,botSlope*_xIntersect+botIntercept)
        
    print(rightIntersect)
    
    # Calculate the distance between the two intersects
    distance = np.sqrt((leftIntersect[1]-rightIntersect[1])**2+(leftIntersect[0]-rightIntersect[0])**2)
    print(distance)
    
    # Calculate a crop point starting 20% of the length of the bottom edge
    tempCropPoint = LineString([leftIntersect, rightIntersect]).interpolate(distance*0.2)
    
    return (tempCropPoint.x, height - tempCropPoint.y)

# Function to process image lines from Hughe's Transform and Canny
def processLines(imageLines, image):
    width, height = image.size
    
    # Initialize some variables to hold the line that characterizes the froth box
    bottomBox = [0,0,0,0]
    bottomLength = 0
    bottomSlope = 0.029
    leftBox = [0,0,0,0]
    leftLength = 0
    leftSlope = 0.86
    rightBox = [0,0,0,0]
    rightLength = 0
    rightSlope = -0.60
    
    # Calculate the slope of each line
    for index, line in enumerate(imageLines): 
        x1,y1,x2,y2 = line[0]
        
        # Calculate slope and distance
        if x2 == x1: # If it is a single point skip
            continue
        slope = (-y2+y1)/(x2-x1)
        distance = np.sqrt((y2-y1)**2+(x2-x1)**2)
        
        # Check if slopes are comparable + longer length line + relative regionality of image
        # Slopes have a margin built in
        if (slope < bottomSlope * 1.5) and (slope > bottomSlope * 0.50):
            # Bottom slope SHOULD be on the bottom 75%  of the image
            if (y1 > 0.25 * height) and (y2 > 0.25 * height):
                if (distance > bottomLength) or (min(line[0][1],line[0][3]) > bottomBox[1]):
                    bottomLength = distance
                    bottomBox = line[0]
                    
        if (slope < leftSlope * 1.3) and (slope > leftSlope * 0.7):
            # Left slope SHOULD be on the left half of the screen
            if (x1 < 0.40 * width) and (x2 < 0.40 * width):
                # Pick the left line that is further down - selects the bottom bar on the left side
                if (max(line[0][1],line[0][3]) > max(leftBox[1],leftBox[3])):
                #if distance > leftLength or (min(line[0][0],line[0][2]) > leftBox[0]):
                    leftLength = distance
                    leftBox = line[0]
                    
        if (slope > rightSlope * 1.4) and (slope < rightSlope * 0.6):
            if (x1 > 0.60 * width) and (x2 > 0.60 * width):
                if (min(line[0][0],line[0][2])  < min(rightBox[0],rightBox[1])):
                #if distance > rightLength or (min(line[0][0],line[0][2])  < rightBox[0]):
                    rightLength = distance
                    rightBox = line[0]
                    
    # Create a generic right point at the end of the screen if no right line is found
    if rightLength == 0:
        C = (bottomBox[0],bottomBox[1])
        D = (bottomBox[2],bottomBox[3])
        
        # Bottom line equation       
        botSlope = (D[1] - C[1])/(D[0] - C[0])
        botIntercept = C[1] - (C[0]*botSlope)
        tempCropPoint = width*botSlope + botIntercept
        
        rightBox = np.array([width, int(tempCropPoint), width, int(tempCropPoint)])
    
    cropBox = getCroppedBox(bottomBox, leftBox, rightBox)
    #cropBox = [bottomBox, leftBox, rightBox]
    return cropBox
        

##### IMAGE PREPROCESSING #####

# Converting image to a grayscale + process image with brightness and contrast
#imgUpsetBW = imgUpset.convert('L')
imgUpsetBW = ImageEnhance.Contrast(imgUpset)
imgUpsetBW = imgUpsetBW.enhance(1.3)
imgUpsetBW = ImageEnhance.Brightness(imgUpsetBW)
imgUpsetBW = imgUpsetBW.enhance(0.7)


##### DYNAMIC CROPPER #####

img = cv2.cvtColor(np.array(imgUpsetBW), cv2.COLOR_RGB2BGR)
img2 = img.copy()

# Convert image to gray scale for processing
# Convert image into CV2 format
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Preblur the image before canny - since canny only uses a 5x5 blur
blurImage = cv2.blur(grayImage,(3,3))

# Apply canny edge detection algorithm on image
# Argument 1 and 2 = threshold parameter 1 and 2 respectively
# Argument 3 = aperature size for sorbel filter
edgeImage = cv2.Canny(blurImage, 70, 120, 5)
cv2.imwrite('EdgeImage.jpg', edgeImage)

# Use Hughes Transform to get lines
imageLines = cv2.HoughLinesP(edgeImage, 1, np.pi/180, threshold = 1, minLineLength = 40, maxLineGap = 5)

cropBoxStart = processLines(imageLines, imgUpset)
startPoint = (int(cropBoxStart[0]),int(cropBoxStart[1]))
endPoint = (int(cropBoxStart[0] + width*0.1), int(cropBoxStart[1] - height*0.2))
cv2.rectangle(img, startPoint, endPoint, (0,255,0), 2) 

cv2.imwrite('LinedImage.jpg', img)



    