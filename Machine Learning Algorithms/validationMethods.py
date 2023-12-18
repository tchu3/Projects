# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 11:20:58 2020

@author: TommyCh
"""
#### Define Imports ####
import pandas as pd
import numpy as np

# Imports for confusion matrix
import seaborn as sn
import matplotlib.pyplot as plt

# Import raw data via pandas
rawData = pd.read_excel (r'\\cnrl.com\cnrl\users\tommych\Desktop\TOMMY CHU\(7) MOC + Projects\(6) YB - PSC Interface\YB PSC Interface (Raw Data).xlsx', sheet_name ='Validation')

def calcPrecision(predicted, target):
    # Recall also known as the positive predictive value
    # Define a variable to hold true positives and false positives
    truePositive = 0
    falsePositive = 0
    
    for i in range(0,len(predicted)):
        # Flag if the result is a true positive
        if str(target[i]).lower() == "true" and str(predicted[i]).lower() == str(target[i]).lower():
            truePositive += 1
        # Flag if the result is a false positive
        elif str(predicted[i]).lower() == "true" and str(predicted[i]).lower() != str(target[i]).lower():
            falsePositive += 1
        # Catch all other true negative and false negative results
        else:
            continue
    
    return truePositive / (truePositive + falsePositive)

def calcRecall(predicted, target):
    # Recall also known as the negative predictive value
    # Define a variable to hold true positives and false positives
    truePositive = 0
    falseNegative = 0
    
    for i in range(0,len(predicted)):
        # Flag if the result is a true positive
        if str(target[i]).lower() == "true" and str(predicted[i]).lower() == str(target[i]).lower():
            truePositive += 1
        # Flag if the result is a false negative
        elif str(predicted[i]).lower() == "false" and str(predicted[i]).lower() != str(target[i]).lower():
            falseNegative += 1
        # Catch all other true negative and false positives results
        else:
            continue
    
    return truePositive / (truePositive + falseNegative)

def F1Score (precision, recall):
    # Harmonic mean of the recall and precision 
    return 2*(precision*recall)/(precision+recall)

def calcAccuracy(predicted, target):
    # Accuracy is the overall success rate
    # Define a variable to hold true matches
    trueMatch = 0
    
    for i in range(0,len(predicted)):
        # Flag if the result is a match
        if str(predicted[i]).lower() == str(target[i]).lower():
            trueMatch += 1
    
    return trueMatch / len(predicted)

def jaccardIndex(predicted, target):
    # Interpreted as the ratio of the estimated true classes intersection to their union
    # Define a variable to hold true positives and false positives
    truePositive = 0
    falseNegative = 0
    falsePositive = 0
    
    for i in range(0,len(predicted)):
        # Flag if the result is a true positive
        if str(target[i]).lower() == "true" and str(predicted[i]).lower() == str(target[i]).lower():
            truePositive += 1
        # Flag if the result is a false negative
        elif str(predicted[i]).lower() == "false" and str(predicted[i]).lower() != str(target[i]).lower():
            falseNegative += 1
        # Flag if the result is a false positive
        elif str(predicted[i]).lower() == "true" and str(predicted[i]).lower() != str(target[i]).lower():
            falsePositive += 1
        # Catch all other true negative and false positives results
        else:
            continue
    
    return truePositive / (truePositive + falseNegative + falsePositive)

def classificationOfSuccessIndex(predicted, target):
    # Defined as 1 minus the sum of the type 1 and type 2 errors
    # Define a variable to hold true positives and false positives
    falseNegative = 0
    falsePositive = 0
    
    for i in range(0,len(predicted)):
        # Flag if the result is a false negative
        if str(predicted[i]).lower() == "false" and str(predicted[i]).lower() != str(target[i]).lower():
            falseNegative += 1
        # Flag if the result is a false positive
        elif str(predicted[i]).lower() == "true" and str(predicted[i]).lower() != str(target[i]).lower():
            falsePositive += 1
            
    return 1 - (falseNegative/len(predicted)) - (falsePositive/len(predicted))

# Plot confusion matrix
#confusionMatrix = pd.crosstab(targetData, predictedData, rownames=['Actual'], colnames=['Predicted'])
#sn.heatmap(confusionMatrix, annot=True)
#plt.show()

#### TEST DATA - TEMP DELETE ####
predictedData = rawData['Interface Found (sigmoid)']
predictedData = predictedData.reset_index().values
predictedData = predictedData[:,1]
targetData = rawData['Interface Found (human)'] 
targetData = targetData.reset_index().values
targetData = targetData[:,1]

print('Sigmoid Method')
precision = calcPrecision(predictedData,targetData)
print('Precision: ' + str(precision))
recall = calcRecall(predictedData,targetData)
print('Recall: ' + str(recall))
print('F1 Score: ' + str(F1Score(precision, recall)))
print('Accuracy: ' + str(calcAccuracy(predictedData,targetData)))

predictedData = rawData['Interface Found (slope)']
predictedData = predictedData.reset_index().values
predictedData = predictedData[:,1]

print('Slope Method')
precision = calcPrecision(predictedData,targetData)
print('Precision: ' + str(precision))
recall = calcRecall(predictedData,targetData)
print('Recall: ' + str(recall))
print('F1 Score: ' + str(F1Score(precision, recall)))
print('Accuracy: ' + str(calcAccuracy(predictedData,targetData)))


