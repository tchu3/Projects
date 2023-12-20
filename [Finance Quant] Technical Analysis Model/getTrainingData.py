# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 16:22:35 2020

@author: Tommy Chu
"""

from pandas_datareader import data
import yfinance as yf
yf.pdr_override()
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import math
import os
from sys import stdout
from sklearn.preprocessing import StandardScaler
import joblib
mainDirectory = os.getcwd()

################################################################################
###########################  STOCK  FUNCTIONS  #################################
################################################################################

### PRICE RATE OF CHANGE ###
def priceRateOfChange(data, period):
    # Create temp dataframe to hold calculations
    tempData = pd.DataFrame()
    
    tempData['Past Price'] = data.shift(periods=-1)
    
    return (data - tempData['Past Price'])/tempData['Past Price']

### STOCHASTIC OSCILLATOR ###
def stochasticOscillator(data, period):
    # Create temp dataframe to hold calculations
    tempData = pd.DataFrame()
    
    # Create a dataframe for the percentage gain
    tempData['highestHigh'] = data.rolling(window=period).max()
    tempData['lowestLow'] = data.rolling(window=period).min()
    tempData['stochasticOscillator'] = (data - tempData['lowestLow'])/(tempData['highestHigh']-tempData['lowestLow'])*100
    
    return tempData['stochasticOscillator']

### WILLIAMS %R ###
def williamsR(data, period):
    # Create temp dataframe to hold calculations
    tempData = pd.DataFrame()
    
    # Create a dataframe for the percentage gain
    tempData['highestHigh'] = data.rolling(window=period, min_periods=1).max()
    tempData['lowestLow'] = data.rolling(window=period, min_periods=1).min()
    tempData['stochasticOscillator'] = (tempData['highestHigh'] - data)/(tempData['highestHigh']-tempData['lowestLow'])*100
    
    return tempData['stochasticOscillator']

### CALCULATE VOLUME RELATIVE STRENGTH INDEX (RSI) ###
### CALCULATE PRICE RELATIVE STRENGTH INDEX (RSI) ###
def calcRSI(previousAvgGain, previousAvgLoss, currentGain, currentLoss):
    try:
        if math.isnan(float(currentGain)):
            currentGain = 0 
    except:
        currentGain = 0
    try:
        if math.isnan(float(currentLoss)):
            currentLoss = 0
    except:
        currentLoss = 0
    #return 100 - (100/ (1 + (previousAvgGain + currentGain)/ (-1*(previousAvgLoss + currentLoss))))
    return 100 - (100/ (1 + (previousAvgGain/previousAvgLoss*-1)))

def RSI(data, period):
    # Convert volume data to a percent change day-to-day
    data = data.pct_change()
    # Create temp dataframe to hold calculations
    tempData = pd.DataFrame()
    
    # Create a dataframe for the percentage gain
    tempData['percentageGain'] = data.apply(lambda x: x if x > 0 else None)
    tempData['percentageLoss'] = data.apply(lambda x: x if x < 0 else None)
    tempData['rollingGain'] = tempData['percentageGain'].rolling(window=period, min_periods=1).mean()
    tempData['rollingLoss'] = tempData['percentageLoss'].rolling(window=period, min_periods=1).mean()
    tempData['RSI'] = tempData.apply(lambda row: calcRSI(row['rollingGain'],row['rollingLoss'],row['percentageGain'],row['percentageLoss']), axis = 1)
    
    return tempData['RSI']
    
### CALCULATE 50-DAY MOVING DAY AVERAGE ###
### CALCULATE 200-DAY MOVING DAY AVERAGE ###
def movingAverage(data, period):
    return data.rolling(window=period, min_periods=1).mean()

def simpleMovingAverage(data, period):
    return data.rolling(window=period, min_periods=1).mean()-data

### CALCULATE 50-DAY EXPONENTIAL DAY AVERAGE ###
### CALCULATE 200-DAY EXPONENTIAL DAY AVERAGE ###
def expMovingAverage(data, period):
    return data.ewm(span=period, adjust=False).mean()-data

def exponentialMovingAverage(data, period):
    return data.ewm(span=period, adjust=False).mean()

### MACD 50-DAY MOVING DAY AVERAGE - 200-DAY MOVING DAY AVERAGE ###
### MACD 50-DAY EXPONENTIAL DAY AVERAGE - 200-DAY EXPONENTIAL DAY AVERAGE ###
def movingAverageMACD(data, period1, period2, mode):
    # Create temp dataframe to hold calculations
    tempData = pd.DataFrame()
    
    # get Averages
    if mode == "SMA":
        tempData['period1Average'] = movingAverage(data, period1)
        tempData['period2Average'] = movingAverage(data, period2)
    else:
        tempData['period1Average'] = expMovingAverage(data, period1)
        tempData['period2Average'] = expMovingAverage(data, period2)
    
    return tempData['period1Average']-tempData['period2Average']

### BOLLINGER BANDS ###
def bollingerBands(high, low, close, period = 20, deviations = 2):
    tempData = pd.DataFrame()
    tempData['typicalPrice'] = (high + low + close)/3
    tempData['Standard Deviation'] = tempData['typicalPrice'].rolling(window=period, min_periods=1).std()
    tempData['typicalPriceSMA'] = movingAverage(tempData['typicalPrice'], period)
    
    tempData['topBollingerBand'] = tempData['typicalPriceSMA'] + (deviations * tempData['Standard Deviation'])
    tempData['botBollingerBand'] = tempData['typicalPriceSMA'] - (deviations * tempData['Standard Deviation'])
    
    return (tempData['topBollingerBand']-close, close-tempData['botBollingerBand'])

def rawBollingerBands(high, low, close, period = 20, deviations = 2):
    tempData = pd.DataFrame()
    tempData['typicalPrice'] = (high + low + close)/3
    tempData['Standard Deviation'] = tempData['typicalPrice'].rolling(window=period, min_periods=1).std()
    tempData['typicalPriceSMA'] = movingAverage(tempData['typicalPrice'], period)
    
    tempData['topBollingerBand'] = tempData['typicalPriceSMA'] + (deviations * tempData['Standard Deviation'])
    tempData['botBollingerBand'] = tempData['typicalPriceSMA'] - (deviations * tempData['Standard Deviation'])
    
    return (tempData['topBollingerBand'], tempData['botBollingerBand'])

################################################################################
####################### NEURAL NETWORK FUNCTIONS  ##############################
################################################################################
def getData(tickers, start_date, end_date):
    technicalData = pd.DataFrame()
    
    ## Read in VIX data
    vixData = data.DataReader('^VIX', start_date, end_date)
    #vixData = data.get_data_yahoo('^VIX', start_date, end_date)

    ## READ IN FINANCIAL STATEMENT DATA ##
    financialData = pd.read_excel(mainDirectory + r'\S&P500\S&P500 - Index Fundamentals.xlsx')
    # stockFundamentalData = pd.read_excel(mainDirectory + r'\S&P500\S&P500 - Stock Fundamentals.xlsx') ## CURRENTLY UNAVAILABLE
        
    for index, x in enumerate(tickers):
        print(x)
        tempData = data.DataReader(x, start_date, end_date)
        #tempData = data.get_data_yahoo(x, start_date, end_date)
        tempData['Year'] = pd.DatetimeIndex(tempData.index).year
        tempData['Month'] = pd.DatetimeIndex(tempData.index).month
        tempData['Symbol'] = x
        tempData['VIX'] = vixData['Close']
        
        ## JOIN DATA ##
        # Join the index fundamental financial data       
        tempData = tempData.merge(financialData, left_on=['Date'], right_on=['Date'])
        # Join the stock fundamental financial data       
        # tempTechnicalData = tempData.merge(stockFundamentalData, left_on=['Date', 'Symbol'], right_on=['Date', 'Symbol'])
        
        tempTechnicalData = pd.DataFrame()
        tempTechnicalData['Date'] = tempData['Date']
        tempTechnicalData['Price'] = tempData['Close']
        tempTechnicalData['Symbol'] = tempData['Symbol']
        
        tempTechnicalData['Volume RSI'] = RSI(tempData['Volume'], 14)
        tempTechnicalData['Price RSI'] = RSI(tempData['Close'], 14)
        tempTechnicalData['20 SMA'] = simpleMovingAverage(tempData['Close'], 20)
        tempTechnicalData['50 SMA'] = simpleMovingAverage(tempData['Close'], 50)
        tempTechnicalData['(x) 20 SMA'] = movingAverage(tempData['Close'], 20)
        tempTechnicalData['(x) 50 SMA'] = movingAverage(tempData['Close'], 50)
        tempTechnicalData['50 EMA'] = expMovingAverage(tempData['Close'], 50)
        tempTechnicalData['200 EMA'] = expMovingAverage(tempData['Close'], 200)
        tempTechnicalData['(x) 50 EMA'] = exponentialMovingAverage(tempData['Close'], 50)
        tempTechnicalData['(x) 200 EMA'] = exponentialMovingAverage(tempData['Close'], 200)
        tempTechnicalData['50/200 MACD SMA'] = movingAverageMACD(tempData['Close'], 50, 200, "SMA")
        tempTechnicalData['50/200 MACD EMA'] = movingAverageMACD(tempData['Close'], 50, 200, "EMA")
        tempTechnicalData['BOLU'] = bollingerBands(tempData['High'], tempData['Low'], tempData['Close'])[0]
        tempTechnicalData['BOLD'] = bollingerBands(tempData['High'], tempData['Low'], tempData['Close'])[1]
        tempTechnicalData['(x) BOLU'] = rawBollingerBands(tempData['High'], tempData['Low'], tempData['Close'])[0]
        tempTechnicalData['(x) BOLD'] = rawBollingerBands(tempData['High'], tempData['Low'], tempData['Close'])[1]
        tempTechnicalData['Price Rate of Change'] = priceRateOfChange(tempData['Close'], 5)
        tempTechnicalData['Stochastic Oscillator'] = stochasticOscillator(tempData['Close'], 14)
        tempTechnicalData['Williams R'] = williamsR(tempData['Close'], 14)
        tempTechnicalData['VIX'] = tempData['VIX']
        
        # Pull over S&P 500 fundamental data
        tempTechnicalData['Index Dividend Yield'] = tempData['Div Yld - NTM']
        tempTechnicalData['Index P/E'] = tempData['PE - NTM']
        tempTechnicalData['Index P/Book'] = tempData['PBK - NTM']
        
        # Calculate the rolling z-score using kernel smoothing
        # for column in tempTechnicalData:
        #     if (column == 'Volume RSI') or (column == 'Price RSI') or (column == '20 SMA') or (column == '50 SMA') or (column == '50 EMA') or (column == '200 EMA') or (column == '50/200 MACD SMA') or (column == '50/200 MACD EMA') or (column == 'BOLU') or (column == 'BOLD') or (column == 'Price Rate of Change') or (column == 'Price Rate of Change') or (column == 'Stochastic Oscillator') or (column == 'Williams R') or (column == 'VIX') or (column == 'Index Dividend Yield') or (column == 'Index P/E') or (column == 'Index P/Book') or (column == 'P/S') or (column == 'P/E') or (column == 'P/Book'):
        #         col_mean = tempTechnicalData[column].rolling(window=60).mean()
        #         col_std = tempTechnicalData[column].rolling(window=60).std()
        #         tempTechnicalData[column] = (tempTechnicalData[column] - col_mean)/col_std
        
        
        #tempTechnicalData['Dividend Yield'] = tempData['Dividend']/tempData['Close']
        #tempTechnicalData['P/E'] = tempData['Close']/tempData['EPS']
        #tempTechnicalData['P/Book'] = tempData['Close']/(tempData['Book Value']/tempData['Shares Outstanding'])
        
        ## PREDICTION COLUMNS
        tempTechnicalData['1 Day Return'] = tempData['Close'].pct_change()
        tempTechnicalData['Gain/Loss Flag'] = tempTechnicalData['1 Day Return'].apply(lambda x: 1 if x > 0 else -1)
        # Up/down indicator for 7 days
        tempTechnicalData['Up/Down Indicator'] = tempTechnicalData['Gain/Loss Flag'].rolling(window=7, min_periods=7).sum()
        tempTechnicalData['Up/Down Indicator'] = tempTechnicalData['Up/Down Indicator'].shift(periods=-7)
        tempTechnicalData['1 Day Return'] = tempTechnicalData['1 Day Return'].shift(periods=-1)
        
        tempTechnicalData['7 Day Return'] = tempTechnicalData['1 Day Return'] + 1
        tempTechnicalData['7 Day Return'] = tempTechnicalData['7 Day Return'].rolling(window=7).apply(np.prod, raw=True)-1
        tempTechnicalData['7 Day Return'] = tempTechnicalData['7 Day Return'].shift(periods=-6)
        
        tempTechnicalData['30 Day Return'] = tempTechnicalData['1 Day Return'] + 1
        tempTechnicalData['30 Day Return'] = tempTechnicalData['30 Day Return'].rolling(window=30).apply(np.prod, raw=True)-1
        tempTechnicalData['30 Day Return'] = tempTechnicalData['30 Day Return'].shift(periods=-29)

        tempTechnicalData['90 Day Return'] = tempTechnicalData['1 Day Return'] + 1
        tempTechnicalData['90 Day Return'] = tempTechnicalData['90 Day Return'].rolling(window=90).apply(np.prod, raw=True)-1
        tempTechnicalData['90 Day Return'] = tempTechnicalData['90 Day Return'].shift(periods=-89)        
            
        ## DROP ALL NA ROWS ##
        tempTechnicalData = tempTechnicalData.dropna()
        
        if index == 0:
            technicalData = tempTechnicalData
        else:
            technicalData = pd.concat([technicalData,tempTechnicalData])
        ## SAVE TECHNICAL DATA ##
        technicalData.to_csv ( mainDirectory + r'\technicalData.csv', header=True)
        
    return technicalData

################################################################################
##########################   NON-FUNCTION CODE   ###############################
################################################################################

# Override S&P 500 ticker list with the manual list below
tickers = ['ENB.TO', 'PPL.TO', 'IPL.TO', 'TRP.TO']
# tickerList = pd.read_excel(mainDirectory + r'\S&P500\S&P500 - Ticker List.xlsx')  
# tickers = tickerList['Symbol'].tolist()

# Define start and end date of the data pulled
start_date = '2016-01-01'
end_date = '2021-12-25'
technicalData = getData(tickers, start_date, end_date)
