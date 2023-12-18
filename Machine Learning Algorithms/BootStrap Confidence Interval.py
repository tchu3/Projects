# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 15:48:28 2020

@author: tommych
"""
import numpy as np
import pandas as pd

# Data imports for the raw data and the adjoining data table that indicates the mode of operation - join the two tables
rawData = pd.read_excel (r'\\cnrl.com\cnrl\users\tommych\Desktop\TOMMY CHU\(7) MOC + Projects\(22) PSC Control Logic Review\2.0 Improve the Front End\Apron Feeder\Monitoring Dashboard (Raw Data).xlsx', sheet_name ='Raw Data Pull', headers = [0])
modeTable = pd.read_excel (r'\\cnrl.com\cnrl\users\tommych\Desktop\TOMMY CHU\(7) MOC + Projects\(22) PSC Control Logic Review\2.0 Improve the Front End\Apron Feeder\Test Schedule.xlsx', sheet_name ='Sheet1', headers = [0])
rawData = rawData.merge(modeTable, on='Date', how='left')

# Bootstrapping is a statistical method used to determine the confidence interval of statistical measures by holding out data (i.e. the P25-P75 confidence interval of the mean) 
def bootstrapConfidenceInterval(data, numIterations, holdout):
    # Declare a dataframe to hold sample statistics
    sampleData = pd.DataFrame(columns = ['mean','median','p25','p75'])
    mean = np.zeros((numIterations,1))
    median = np.zeros((numIterations,1))
    p25 = np.zeros((numIterations,1))
    p75 = np.zeros((numIterations,1))
    
    # Iterate number of times passed through in the arguments
    for i in range (0,numIterations):
        # Holdout a portion of the data
        sample = data.sample(frac=1-holdout)
        # For each iteration add the mean, median, 25th and 75th percentile
        sampleData.loc[i] = sample.mean() + sample.median() + sample.quantile(0.25) + sample.quantile(0.75)
        '''
        mean[i] = sample.mean()
        median[i] = sample.median()
        p25[i] = sample.quantile(0.25)
        p75[i] = sample.quantile(0.75)
        '''

    return sampleData

# Create masks for the two modes of operation
tph2Filter = rawData["Mode"] == "2 tph"
tph5Filter = rawData["Mode"] == "5 tph"

# Mask to drop all 0 entries
dropZero = rawData["BFC 2 Tonnage Lost"] != 0

# Filter data
tph2Data = rawData[tph2Filter & dropZero]
tph2Data = tph2Data.dropna()
tph5Data = rawData[tph5Filter & dropZero]
tph5Data = tph5Data.dropna()

# Run bootstrap condfidence intervals 
bootstrap2tphData = bootstrapConfidenceInterval(tph2Data["BFC 2 Tonnage Lost"], 1000, 0.1)
print("2tph Median:" + str(bootstrap2tphData['median'].median()) + "95% Confidence Interval: " + str(bootstrap2tphData['median'].quantile(0.025)) + " - " + str(bootstrap2tphData['median'].quantile(0.975)))
bootstrap5tphData = bootstrapConfidenceInterval(tph5Data["BFC 2 Tonnage Lost"], 1000, 0.1)
print("5tph Median:" + str(bootstrap5tphData['median'].median()) + "95% Confidence Interval: " + str(bootstrap5tphData['median'].quantile(0.025)) + " - " + str(bootstrap5tphData['median'].quantile(0.975)))