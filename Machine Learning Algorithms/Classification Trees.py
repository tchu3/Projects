# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 09:47:24 2020

@author: tommych
"""

def getSplit(index, currentMeasure, data):
    # classificationMeasure = measure that determines how to split the data "Yes"/"No"
    # index is the particular column feature from the original dataset that is being split and compared to i.e. weather temp
    # rowData is the passed through data from the orginal raw data
    
    # Create temporary lists to hold data for the left node of the split and the right node of the split
    leftNode, rightNode = list(),list()
    
    # Iterate through each row in the data set and compare the value to the classification measure passed through
    for x in data:
        if x[index] < currentMeasure:
            leftNode.append(x)
        if x[index] > currentMeasure:
            rightNode.append(x)
    return leftNode, rightNode

def getGiniIndex(classifiedGroups, numClassifications):
    # classifiedGroups is a 'x' by 2 matrix with the left and right nodes
    # Classification is the number of kind of features
    
    # Count the # of instances of a particular classification in a group and sum them together for number of total instances
    # i.e. a 10 row dataset will have 9 - since the current analyzed row is taken away
    # nets any rows that are exactly equal to current row - provide zero additional information
    numInstances = float(sum([len(group) for group in classifiedGroups]))
    
    # Initialize a gini index
    giniIndex = 0.0
    
    for group in classifiedGroups:
        groupSize = float(len(group))
        
        # Test if a group size is 0 continue to the next loop
        if groupSize == 0:
            continue
        
        # Initialize a gini Score
        giniScore = 0
        
        # Score the group based on the score in each classification
        for feature in numClassifications:
            # Simply counts the classifications in a particular feature = [count[-1] for count in group].count(classification)
            # count[-1] looks at the last column - the target variable
            # i.e. 4 kids in a group 10 people or 6 adults in 10 people
            proportion = [count[-1] for count in group].count(feature) / groupSize
            # Gini Index is the square of proportion
            giniScore += proportion * proportion
            
        # Weight the group score by its relative size to the total samples
        giniIndex += (1-giniScore)*(groupSize/numInstances)
    
    return giniIndex
    
def splitData(data):
    # Get the number of features in the last column of the data set
    # Create a set and cast into a list for instance if its binary [0,1]
    targetFeatures = list(set(row[-1] for row in data))
    
    # Initialize variables to hold data from the split
    splitIndex, splitValue, lowestIndex, splitGroups = 999, 999, 999, None
    
    # Loop through each column
    for x in range(len(dataset[0])-1):
    # Loop through each row in the dataset
        for row in data:
            # split Data, iterate through each row and split a feature the current value in the row 
            splitData = getSplit(x, row[x], data)
            # Calculate that gini score by splitting a feature by the current value in the row
            giniIndex = getGiniIndex(splitData, targetFeatures)
            
            # If the current score of the Gini Index is lower than it's previous best score, update "best" gini index
            if giniIndex < lowestIndex:
                splitIndex, splitValue, lowestIndex, splitGroups = x, row[x], giniIndex, splitData
    
    # Return the index of the split, value it split on, and the two groups it split up
    return {'splitIndex':splitIndex, 'value':splitValue, 'groups':splitGroups}

def terminateNode(nodeGroup):
    # Collect the results from the node
    results = [x[-1] for x in nodeGroup]
    # Return the result with the max counts
    return (max(set(results), key=results.count))

def recursiveSplit(node, depth):
    # Hyperparameters
    maxDepth = 2
    minSize = 2
    
    # Break out the left and right groups from the previous node
    leftNode, rightNode = node['groups']
    del(node['groups'])
    
    # Check for max depth
    if depth >= maxDepth:
        node['leftNode'], node['rightNode'] = terminateNode(leftNode), terminateNode[rightNode]
        return
    
    # Continue to split the left child
    if len(leftNode) <= minSize:
        node['leftNode'] = terminateNode(leftNode)
        return
    else:
        node['left'] = splitData(leftNode)
        recursiveSplit(node['left'], depth+1)
        return
    
    # Continue to split the right child
    if len(rightNode) <= minSize:
        node['rightNode'] = terminateNode(rightNode)
        return
    else:
        node['right'] = splitData(rightNode)
        recursiveSplit(node['right'], depth+1)
        return
    
def buildTree(orginalData):
    treeRoot = splitData(orginalData)
    recursiveSplit(treeRoot, 1)
    return treeRoot

dataset = [[2.771244718,1.784783929,0],
	[1.728571309,1.169761413,0],
	[3.678319846,2.81281357,0],
	[3.961043357,2.61995032,0],
	[2.999208922,2.209014212,0],
	[7.497545867,3.162953546,1],
	[9.00220326,3.339047188,1],
	[7.444542326,0.476683375,1],
	[10.12493903,3.234550982,1],
	[6.642287351,3.319983761,1]]

split = splitData(dataset)