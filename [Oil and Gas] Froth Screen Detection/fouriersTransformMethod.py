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
import csv
from shapely.geometry import LineString, Point
from sklearn.preprocessing import StandardScaler

from matplotlib import pyplot as plt
from scipy.signal import butter, sosfilt, sosfreqz
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

#text_file = open("upsetFreq.txt", "w", newline='')
#writer = csv.writer(text_file, delimiter = '\t')


##### LOAD VIDEO #####

def getFrames():
    # https://www.analyticsvidhya.com/blog/2018/09/deep-learning-video-classification-python/
    # Open mkv video - this video is a 5 FPS video
    frothVideo = cv2.VideoCapture(r'E:\Froth Screen Videos\[UPSET] 06-03-2020 0306AM.mkv')
    # Path to save the frames
    path = r'E:\[UPSET 06-03-2020 0306AM] Frames 15fps'
    
    # Intialize frame rate for 
    frameRate = frothVideo.get(cv2.CAP_PROP_FPS)
    # Frame rate is 15 - adjust to get every 5th frame
    recordFPS = frameRate / 15
    # Initialize frame counter that will be used to save frames
    count = 0
    
    # Start collecting frames
    while(frothVideo.isOpened()):
        frameNum = frothVideo.get(1)
        retFrame, frame = frothVideo.read()
        if (retFrame != True):
            break
        # Floor is the number rounded down
        if (frameNum % math.floor(recordFPS) == 0):
            fileName = "frame%d.jpg" % count
            count += 1
            cv2.imwrite(os.path.join(path , fileName), frame)
    frothVideo.release()

# Define high pass filter - inclusive of nyquist frequency which states the highest frequency that a sampled signal can unamiguously represent
def butter_highpass(lowcut, fs, order):
    nyq = 0.5 * fs # Defined as half the sampling rate
    low = lowcut / nyq
    #high = 10 # highcut / nyq
    #sos = butter(order, [low, high], analog=False, btype='band', output='sos')

    sos = butter(order, low, 'hp', fs=fs, output='sos')
    return sos

def butter_highpass_filter(data, lowcut, fs, order):
    sos = butter_highpass(lowcut, fs, order=order)
    filteredData = sosfilt(sos, data)
    return filteredData

def movingaverage (values, window):
    # Convolution is two arrays convolved over each other aka multiplied then summed
    # Weights is simply the an array of 1's over the defined window size
    weights = np.repeat(1.0, window)/window
    sma = np.convolve(values, weights, 'valid')
    return sma

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
    #print(leftIntersect)
    
    # THIS RUNS if the right line couldn't be found - when the default right line is the just the right point
    if E[0] == F[0]:    
        rightIntersect = (E[0],E[1])
    # Calculate the intersect of the bottom line and the right line
    else:
        _xIntersect = (botIntercept-rightIntercept)/(rightSlope-botSlope)
        rightIntersect = (_xIntersect,botSlope*_xIntersect+botIntercept)
        
    #print(rightIntersect)
    
    # Calculate the distance between the two intersects
    distance = np.sqrt((leftIntersect[1]-rightIntersect[1])**2+(leftIntersect[0]-rightIntersect[0])**2)
    #print(distance)
    
    # Calculate a crop point starting 20% of the length of the bottom edge
    tempCropPoint = LineString([leftIntersect, rightIntersect]).interpolate(distance*0.3)
    
    return (tempCropPoint.x, height - tempCropPoint.y)

# Function to process image lines from Hughe's Transform and Canny
def processLines(imageLines, image):
    width, height = image.size
    
    # Initialize some variables to hold the line that characterizes the froth box
    bottomBox = [0,0,10,1]
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
        if (slope < bottomSlope * 2.0) and (slope >= 0):
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
        
        
        rightBox = np.array([width, int(tempCropPoint), width - 20, int(tempCropPoint) - 12])
    
    filteredLines = [bottomBox, leftBox, rightBox]
    cropBox = getCroppedBox(bottomBox, leftBox, rightBox)
    return [cropBox, imageLines, filteredLines]
        
##### IMAGE PREPROCESSING #####
def imagePreProcessing(frothImage):
    # Converting image to a grayscale + process image with brightness and contrast
    #imgUpsetBW = imgUpset.convert('L')
    frothImageBW = ImageEnhance.Contrast(frothImage)
    frothImageBW = frothImageBW.enhance(1.3)
    frothImageBW = ImageEnhance.Brightness(frothImageBW)
    frothImageBW = frothImageBW.enhance(0.7)
    
    return frothImageBW

##### DYNAMIC CROPPER #####
def dynamicCropper(frothImageP):
    # Convert image to CV2 format and RGB2BGR for processing through Canny
    img = cv2.cvtColor(np.array(frothImageP), cv2.COLOR_RGB2BGR)
    
    # Convert image to gray scale for processing
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Preblur the image before canny - since canny only uses a 5x5 blur
    blurImage = cv2.blur(grayImage,(3,3))
    cv2.imwrite('BlurImage.jpg', blurImage)
    
    # Apply canny edge detection algorithm on image
    # Argument 1 and 2 = threshold parameter 1 and 2 respectively
    # Argument 3 = aperature size for sorbel filter
    edgeImage = cv2.Canny(blurImage, 70, 120, 5)
    cv2.imwrite('EdgeImage.jpg', edgeImage)
    
    # Use Hughes Transform to get lines
    imageLines = cv2.HoughLinesP(edgeImage, 1, np.pi/180, threshold = 1, minLineLength = 40, maxLineGap = 5)
    
    # Pass lines through to the line processing function
    cropBoxStartPoints = processLines(imageLines, frothImage)
    
    # Draw all the lines found in green 
    for index, line in enumerate(cropBoxStartPoints[1]):
        x1,y1,x2,y2 = line[0]
        #print(str(index) + ': ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2)) 
        cv2.line(img, (x1,y1), (x2,y2), (0,255,0), 2)
    # Draw all filtered lines found in red
    for index, line in enumerate(cropBoxStartPoints[2]):
        x1,y1,x2,y2 = line
        cv2.line(img, (x1,y1), (x2,y2), (0,0,255), 2)
    cv2.imwrite('LinedImage.jpg', img)
    
    # Create the startpoint and endpoint for the cropbox
    startPoint = (int(cropBoxStartPoints[0][0]),int(cropBoxStartPoints[0][1]))
    endPoint = (int(cropBoxStartPoints[0][0] + width*0.03), int(cropBoxStartPoints[0][1] - height*0.1))
    
    cv2.rectangle(img, startPoint, endPoint, (255,0,0), 2) 
    cv2.imwrite('BoxImage.jpg', img)
    
    #### Create a check to confirm the correlation of the last image is reasonable to the last one if not run cropper again ####

    return [startPoint[0], endPoint[1], endPoint[0], startPoint[1]]


##### Convolutional Neural Network #####
def convLayer(image, filt, bias, stride=1):
    # Process and store the filter height and width
    filtDepth, filtHeight, filtWindowSize, _ = filt.shape
    
    # Process and store the image height and width
    imageHeight, imageWidth, _ = image.shape
    
    # Calculate the output dimensions given the filter size
    outputDim = int((imageWidth - filtWindowSize)/stride) + 1
    
    # Create a matrix to hold the output of the conv layer
    outputMatrix = np.zeros(outputDim, outputDim, filtDepth)
    
    # Loop to conolve filter over the image
    for i in range(filtDepth):
        # Start from top of the image
        yCoord = yOutCoord = 0
        # Iterate until the filter reaches the bottom of the image
        while yCoord + filtWindowSize <= imageHeight:
            xCoord = xOutCoord = 0
            
            # Iterate until the filter reaches the side of the image
            while xCoord + filtWindowSize <= imageWidth:
                
                # Perform convolution operation
                outputMatrix[yOutCoord, xOutCoord, i] = np.sum(filt[i] * image[yCoord : yCoord + filtWindowSize, xCoord : xCoord + filtWindowSize, :]) + bias[i]
                xOutCoord += 1
                xCoord += stride
                
            yOutCoord += 1
            yCoord += stride
            
    return outputMatrix

def avgPoolLayer(image, filtWindowSize=2, stride=2):
    
    # Process and store the image height and width
    try:
        imageHeight, imageWidth, filtDepth = image.shape
    except:
        imageHeight, imageWidth = image.shape
        filtDepth = 1
    
    # Calculate the output dimensions given the filter size
    outputHeight = int((imageHeight - filtWindowSize)/stride) + 1
    outputWidth = int((imageWidth - filtWindowSize)/stride) + 1
    
    # Create a matrix to hold the output of the conv layer
    # Add dimension for RGB downsample  np.zeros([outputHeight, outputWidth, filtDepth])
    outputMatrix = np.zeros([outputHeight, outputWidth])
    
    # Slide the window over the entire image with a stride
    for i in range(0,filtDepth):
        # Start from top of the image
        yCoord = yOutCoord = 0
        # Iterate until the filter reaches the bottom of the image
        while yCoord + filtWindowSize <= imageHeight:
            xCoord = xOutCoord = 0
            
            # Iterate until the filter reaches the side of the image
            while xCoord + filtWindowSize <= imageWidth:
                
                # Perform convolution operation
                # Add dimensions for filter depth outputMatrix[yOutCoord, xOutCoord, i] = np.round(np.average(image[yCoord : yCoord + filtWindowSize, xCoord : xCoord + filtWindowSize, :]))
                outputMatrix[yOutCoord, xOutCoord] = np.round(np.average(image[yCoord : yCoord + filtWindowSize, xCoord : xCoord + filtWindowSize]))
                #outputMatrix[yOutCoord, xOutCoord] = sigmoid(outputMatrix[yOutCoord, xOutCoord])*255
                xOutCoord += 1
                xCoord += stride
                
            yOutCoord += 1
            yCoord += stride
            
    return outputMatrix

def sigmoid (x):
    return 1 / (1 + np.exp (-x+127.5))

def flattenLayer(image):
    # Process and store the image height and width
    try:
        imageHeight, imageWidth, filtDepth = image.shape
    except:
        imageHeight, imageWidth = image.shape
        filtDepth = 1
    
    # Create a matrix to hold the output of the conv layer
    outputMatrix = np.zeros([0, 1])
    
    # Concatenate all the vectors into a single array
    
    # Loop through each depth layer
    #for j in range(0,image.shape[2]):
    # Loop through each column
    for i in range(0,imageWidth):
        outputMatrix = np.concatenate((outputMatrix,image[:,i:(i + 1)]))
    
    return outputMatrix

def standardDeviationMethod(processedImages):
    frameSpan = 20 # 20 frame standard deviation
    for i in range(frameSpan,1):
        transformArray = results[i,:]

#### LOOP OVER PICTURE DATABASE FRAME BY FRAME ####

# Initialize variables for result storage
results = np.array([])
outputs = []

for i in range(0,300): # initially just process 300 frames
    path = r'E:\[UPSET 06-03-2020 0306AM] Frames 15fps\frame%d.jpg' % i
    frothImage = Image.open(path)
    
    # Store the original image size for later preprocessing
    width, height = frothImage.size
    
    # Put image through preprocessing
    frothImage = imagePreProcessing(frothImage)
      
    # Run cropper every 300 frames or on the first frame 
    if (i % 300 == 0) or (i == 0):
        # Run dynamic cropper
        cropPoints = dynamicCropper(frothImage)
        
    # Crop the image according to the rectangle and return cropped image
    # Crop is the form of (left, top, right, bottom)
    croppedImage = frothImage.crop((cropPoints[0], cropPoints[1], cropPoints[2], cropPoints[3]))
    croppedImage = croppedImage.convert('L')
    
    # Downsample image using max pool
    #croppedImage = avgPoolLayer(np.array(croppedImage),2,2) #IGNORE DOWN SAMPLE FOR NOW - CHANGE flatten size back to shape
    
    # Flatten and convert to a numpy array
    outputMatrix = flattenLayer(np.asarray(croppedImage)) # REMOVE AS ARRAY IF USING CROPPED IMAGE
    outputMatrix = np.array(outputMatrix)
    
    # Concatenate the results along the column
    if results.size: # Conconate if the results matrix is not empty
        results = np.concatenate((results, outputMatrix), axis=1)
    else: # Initialize results matrix with assignment if empty
        results = outputMatrix


for i in range(0,1):
    transformArray = results[i,:]
    '''
    scaler = StandardScaler()
    transformArray = scaler.fit_transform(transformArray.reshape(-1, 1) )
    transformArray = np.reshape(transformArray, transformArray.size)
    '''
    transformArray = movingaverage(transformArray,5)
    
    # Subtract the mean of the signal to remove the DC signal
    arrayMean = np.mean(transformArray)
    for x in range(0,len(transformArray)):
        transformArray[x] = transformArray[x] - arrayMean
    
    ### Filter Data ###
    #https://medium.com/analytics-vidhya/how-to-filter-noise-with-a-low-pass-filter-python-885223e5e9b7
    # Sample rate of 5fps
    transformArray = butter_highpass_filter(transformArray, 0.5, order = 5, fs = 15)
    
    # Calculate the frequency and the magnitude of the fourier signals
    magnitude = np.fft.fft(transformArray)
    frequency = np.fft.fftfreq(len(transformArray)) * 5
    frequency = frequency.tolist()
    
    # Abs gets us the amplitude of the signal
    amplitude = np.abs(magnitude).tolist()
    
    '''
    frameNum = []
    for i in range(0,len(transformArray)):
        frameNum.append(i*0.2) # 0.2 for 1 seconds/5 frames = 5 fps
    '''
    # Plot frequency stem plot
    fig, ax = plt.subplots()
    ax.stem(frequency, amplitude)
    
r'''
    # Concatenate the results along the column
    outputs.append(amplitude)
temp = []
for i in range(0,len(outputs[0])):
    temp.append(i)
outputs.append(temp)
outputs = np.array(outputs)
outputs = outputs.T
writer.writerows(outputs)
    
    

    text_file.write(str(i) + "\t")
    for j in range(0,len(outputMatrix)):
        text_file.write(str(outputMatrix[j][0]) + "\t")
    text_file.write("\n")
    
    
    #### PRINT HISTOGRAM ####
    # Convert crop image to an array for histogram
    croppedImage = np.array(croppedImage)
    
    histogram,bins = np.histogram(croppedImage.ravel(),256,[0,256])
    plt.bar(bins[:-1], histogram, width = 3, alpha = 0.7, label=("Frame #%d" % i))
    plt.legend()
    #print('Mean: ' + str(croppedImage.mean()))
    #print('Standard Deviation: ' + str(croppedImage.std()))
   
    
    #### PRINT FOURIER TRANSFORMS ####
    fourierImage = np.fft.fft2(croppedImage)
    fourierImage = np.fft.fftshift(fourierImage)
    fourierImage = 20*np.log(np.abs(fourierImage))
    
    tempSubPlotNum = 1+i
    plt.subplot(3,3,tempSubPlotNum), plt.imshow(np.log(1+np.abs(fourierImage)), "gray") , plt.title("Frame #%d" % i)
    
    
    #### RAW IMAGES ####
    tempSubPlotNum = 1+i
    plt.subplot(3,3,tempSubPlotNum), plt.imshow(croppedImage, cmap='gray', vmin = 0, vmax =255), plt.title("Frame #%d" % i)
'''

# Tight layout fixes the padding of the subplots
#plt.tight_layout()

#text_file.close()
    




    