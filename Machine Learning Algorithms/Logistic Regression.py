# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 08:35:49 2020

@author: tommych
"""

import numpy as np

# Define a function for the sigmoid
def sigmoid(x):
    return 1/(1+np.exp(-x))

# Define a function for the log likelihood function
def logLikelihood(featureMatrix, targetMatrix, weightMatrix):
    return np.sum(targetMatrix*np.dot(weightMatrix*featureMatrix) - np.log(1+ np.exp(np.dot(weightMatrix,featureMatrix))))

def logisticRegression(featureMatrix, targetMatrix):
    ### INITIALIZATION ###
    maxEpochs = 5000
    # Learning rate is how big of a step during gradient descent
    learningRate = 0.001
    
    # Initialize a weight matrix which is equal to the length of the feature matrix
    weightMatrix = np.zeros(featureMatrix.shape[1])
    
    # Iterate through each sample 
    for x in range(0,maxEpochs):
        predictionMatrix = sigmoid(featureMatrix,weightMatrix)
        
        # Update the weights
        errorMatrix = targetMatrix - predictionMatrix
        gradientMatrix = np.dot(featureMatrix.t, errorMatrix)
        weightMatrix += learningRate * gradientMatrix
        
    return weightMatrix
        
        
            