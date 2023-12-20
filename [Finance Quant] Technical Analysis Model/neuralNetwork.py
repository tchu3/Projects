# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:22:35 2020

@author: Tommy Chu
"""

from pandas_datareader import data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
from sys import stdout
from sklearn.preprocessing import StandardScaler
import joblib
mainDirectory = os.getcwd()
outputScaler_filename = mainDirectory + "\Scalers\outputScaler.save"
inputScaler_filename = mainDirectory + "\Scalers\inputScaler.save"
inputScaler = StandardScaler()
outputScaler = StandardScaler()

from scipy.signal import savgol_filter
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error, r2_score

from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json

################################################################################
####################### NEURAL NETWORK FUNCTIONS  ##############################
################################################################################       
def trainModel(inputData, outputData):
    ## STANDARDIZE DATA ##
    inputScaler.fit(inputData)
    outputScaler.fit(outputData)
    scaledInputData = inputScaler.transform(inputData)
    scaledOutputData = outputScaler.transform(outputData)
    scaledInputData = pd.DataFrame(scaledInputData, columns = inputData.columns)
    scaledOutputData = pd.DataFrame(scaledOutputData, columns = outputData.columns)
        
    model = Sequential()
    model.add(Dense(len(inputData.columns), input_dim=len(inputData.columns), activation='relu'))
    model.add(Dense(len(inputData.columns), activation='relu'))
    model.add(Dense(1, activation='linear'))
    
    model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mae'])
    model.fit(inputData, outputData, epochs=1000, shuffle=True, validation_split = 0.7)
    _, metric = model.evaluate(scaledInputData, scaledOutputData)
    print('MAE: %.2f' % (metric))
    return model

def saveModel(model):
    ### SAVE NN Model ###
    modelJSON = model.to_json()
    with open(mainDirectory + r'\Neural Network Config\nnStockModel.json', "w") as json_file:
        json_file.write(modelJSON)
    model.save_weights(mainDirectory + r"\Neural Network Config\nnStockModel.h5")
    joblib.dump(outputScaler, outputScaler_filename) 
    joblib.dump(inputScaler, inputScaler_filename) 
    print("##################    Model Saved    ##################")

def loadModel():
    ### LOAD PREVIOUS NN Model ###
    modelFile = open(mainDirectory + r'\Neural Network Config\nnStockModel.json', 'r')
    loadedModelJSON = modelFile.read()
    modelFile.close()
    loadedModel = model_from_json(loadedModelJSON)
    loadedModel.load_weights(mainDirectory + r"\Neural Network Config\nnStockModel.h5")
    outputScaler = joblib.load(outputScaler_filename)
    inputScaler = joblib.load(inputScaler_filename)
    print("##################    Model Loaded    ##################")
    return [loadedModel, outputScaler, inputScaler]


################################################################################
##########################   NON-FUNCTION CODE   ###############################
################################################################################

# Load technical data run from script getTrainingData
technicalData = pd.read_csv(mainDirectory + r'\technicalData.csv', header = 0)  

##### SPLIT INPUT DATA FROM OUTPUT DATA #####
outputData = pd.DataFrame()
inputData = pd.DataFrame()

# Choose features for the neural network
inputData['Volume RSI'] = technicalData['Volume RSI']
#inputData['Price RSI'] = technicalData['Price RSI']
inputData['20 SMA'] = technicalData['20 SMA']
inputData['50 SMA'] = technicalData['50 SMA']
#inputData['50 EMA'] = technicalData['50 EMA']
#inputData['200 EMA'] = technicalData['200 EMA']
#inputData['50/200 MACD SMA'] = technicalData['50/200 MACD SMA']
#inputData['50/200 MACD EMA'] = technicalData['50/200 MACD EMA']
inputData['BOLU'] = technicalData['BOLU']
#inputData['BOLD'] = technicalData['BOLD']
inputData['VIX'] = technicalData['VIX']
# inputData['Dividend Yield'] = technicalData['Dividend Yield']
# inputData['P/E'] = technicalData['P/E']
#inputData['P/Book'] = technicalData['P/Book']

outputData['Up/Down Indicator'] = technicalData['Up/Down Indicator']


### TRAIN MODEL ###
model = trainModel(inputData, outputData)
saveModel(model)
##################

### LOAD MODEL ###
loader = loadModel()
model = loader[0]
outputScaler = loader[1]
inputScaler = loader[2]
inputData = inputScaler.transform(inputData)
outputData = outputScaler.transform(outputData)
model.compile(loss='mean_squared_error', optimizer='rmsprop', metrics=['mse'])
_, metric = model.evaluate(inputData, outputData)
print('MSE: %.2f' % (metric))
predictedOutput = pd.DataFrame(data=model.predict(inputData), columns=['Up/Down Indicator'])
predictedOutput = outputScaler.inverse_transform(predictedOutput)
rawOutput = outputScaler.inverse_transform(outputData)
##################


