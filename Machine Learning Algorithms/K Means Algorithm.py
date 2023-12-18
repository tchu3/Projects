# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 16:00:53 2020

@author: tommych
"""

import numpy as np
import random as rd
import linalg as la

def KMeans(numClusters, data):
    # Initialize a list to hold the centroids
    centroids = np.array([]).reshape(numClusters,0)
    
    # Initialize a dictionary to hold the clusters
    outputClusters = {}
    # For each cluster initialize a list within the dictionary
    for i in range(numClusters):
        outputClusters[i] = []
        
    # Randomly select a data from the dataset as a centroid
    for i in range(0,numClusters):
        
        # Select a random integer from 0 up to the # of rows in the dataset
        random = rd.randint(0,len(data)-1)
        
        # np.c_ concatenates slices along a list i.e. [1,2,3] and [1,2,3] to ([1,2,3],[1,2,3])
        centroids = np.c_[centroids,data[random]]
        
    # Calculate Euclidian distances from each point to all the centroids
    for x in data:
        # Using linear algebra library the norm is the absolute sum along a vector
        # Iterate through each centroid and calculate the distance store in _tempDistnace
        _tempDistance = [la.norm(x-centroids[y] for y in centroids)]
        # Get the minimum distance and store the data index into the cluster
        _clusterClassification = _tempDistance.index(min(_tempDistance))
        outputClusters[_clusterClassification].append(x)
        
    # Update the centroids
    for x in outputClusters:
        centroids[x] = np.average(outputClusters[x], axis = 0)
        
    
        