# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 15:41:35 2020

@author: tommych
"""

import numpy as np

class supportVectorMachine:
    
    def fit(self, X, y):
        
        ### INITIALIZATION ###
        # Regularization strength is equal to the alpha in the Lagrangian 
        regStrength = 10000
        # Learning rate is how big of a step during gradient descent
        learningRate = 0.001
        
        
        def calculateCost(W, X, Y):
            # Calculate hinge loss for the entire data set
            # The W vector is the weights, X is the samples, Y is the -1/+1 factors (decide which side of the boundary it is on)
            
            # N will be the length of the matrix along the sample size "X"
            N = X.shape[0]
            
            # Standard formula to calculate the distance from a sample to the hyperplane given a width
            # the intercept term beta is included in the weight vector
            distanceVector = 1 - Y *(np.dot(X,W))
            
            # List comprehension to convert all distances to max(0, distance)
            distanceVector[distanceVector < 0] = 0
            
            # Calculate the hinge loss
            # Regularization is a hyperparameter - known as alpha in the Langranian equation
            hingeLoss = regStrength * (np.sum(distanceVector)/N)
            
            # Recall the cost function as described the the distance from the hyperplane is equal to 1/2||W||^2 + second part of the equation
            # Returns the entire Langrangian cost function
            return (1/2)*np.dot(W,W) + hingeLoss
        
        
        def gradientDescent(W, xBatch, yBatch):
            # X is the input matrix
            # Y is the output matrix being trained on
            # W is the width from the hyperplane
            # Perform gradient descent 
            
            # Calculate the distance 
            distanceVector = 1 - yBatch *(np.dot(xBatch,W))
            
            # Initialize the Langranian output vector as the length of # of weights
            lagrangianFunc = np.zeros(len(W))
            
            # Enumerate through each distance index in the distanceVector to calculate each Lagrangian term
            # Number of indexes should equal # of samples
            for ind, x in enumerate(distanceVector):
                # For the case when the index is between the boundaries set it by default to the plane
                if max(0,x) == 0:
                    summationTerm = W
                # Else for each other distance that is on the right side of the hyperplane -
                # Calculate the term via multiplication of (X,Y,regressionStrength)
                else:
                    summationTerm = W - (regStrength * yBatch[ind] * xBatch[ind])
            
                # Add the current term to Langrangian summation
                lagrangianFunc += summationTerm
            
            # Divide by "N" terms for the final summation
            lagrangianFunc = lagrangianFunc/len(yBatch)
            
            return lagrangianFunc
        
        def Train (featureMatrix, outputMatrix):
            maxEpochs = 5000
            # Hyperparameter - exponent for when to check the convergence
            n = 0
            # Initialize an initial previousCost - set to infinity to indiciate infinite error
            prevCost = float("inf")
            # Threshold hyperparameter in %
            costThreshold = 0.01
            
            # Define a weight matrix that is the hyperplane that is the dimensions of # of features
            weightMatrix = np.zeros(featureMatrix.shape[1])
            
            # Stochastic gradient descent 
            for epoch in range(1, maxEpochs):
                # Iterate through each sample "x"
                # Enumerate is an interable tuple in a matrix
                for index, x in enumerate (X):
                    descent = gradientDescent(weightMatrix, x, outputMatrix[index])
                    weightMatrix = weightMatrix - (learningRate * descent)
            
                # Create criteria to stop the training if stop converging
                # Check on every 2^n i.e. 1,2,4,8,16,32.... + last epoch
                if epoch == 2 ** n or epoch == maxEpochs - 1:
                    cost = calculateCost(weightMatrix, featureMatrix, outputMatrix)
                    
                    # costThreshold * prevCost = percent change in previous value
                    # If it is below the threshold return the weights and exit the training function
                    if abs(prevCost - cost) <  costThreshold * prevCost:
                            return weightMatrix
                    prevCost = cost
                    n += 1
            
            return weightMatrix
            
            