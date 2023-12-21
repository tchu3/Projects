################################################################################
############################  DATA  IMPORTS  ###################################
################################################################################
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shap
import os
from sklearn.preprocessing import StandardScaler
from sklearn import linear_model
from sklearn.metrics import r2_score
from keras.models import Sequential
from keras.layers import SimpleRNN, Dense, LSTM, BatchNormalization
from sklearn.model_selection import train_test_split
from tensorflow.keras.layers import Dropout
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
from keras.callbacks import History 
from scipy import stats
from keras import optimizers
inputScaler = StandardScaler()
outputScaler = StandardScaler()

# Import raw data
workbookNames = ["\[RAW DATA] Factset.xlsx","\[RAW DATA] FRED.xlsx","\[RAW DATA] EIA.xlsx","\[RAW DATA] RECESSION INDICATOR.xls","\[RAW DATA] OECD.xlsx"]
mainDirectory = os.getcwd()
consolidatedData = pd.DataFrame()
predictionDF = []
actualDF = []

featureDF = pd.read_excel(mainDirectory + '\[MODEL] FEATURE LIST.xlsx', sheet_name = "FEATURES")
timeLagsDF = pd.read_excel(mainDirectory + '\[MODEL] FEATURE LIST.xlsx', sheet_name = "TIME LAGS")

# Ignore deprecation errors in console
import warnings
warnings.filterwarnings('ignore')

################################################################################
##########################  PREPARATION OF DATA  ###############################
################################################################################

# Consolidate all data into a single dataframe
for workbook in workbookNames:
    timeIntervals = ["Prices","Quarterly","Monthly","Weekly","Daily"]
    
    for interval in timeIntervals:
        try:
            tempSheet = pd.read_excel(mainDirectory + workbook, sheet_name = interval)
            tempSheet['Date'] = pd.to_datetime(tempSheet['Date'])
            
            # Linearly interpolate any quarterly data
            if interval == "Quarterly":
                tempSheet['Date'] = tempSheet['Date'].shift(periods=1)
                tempSheet['Date'] = pd.to_datetime(tempSheet['Date']).dt.to_period('M')
                tempSheet = tempSheet.set_index('Date').resample('M').interpolate().reset_index()
                tempSheet['Date'] = tempSheet['Date'].dt.to_timestamp()
            
            # Group data into monthly, take an average of all data
            tempSheet = tempSheet.groupby(pd.Grouper(key = 'Date', freq='M')).mean().reset_index()
            tempSheet['Date'] = tempSheet['Date'] + pd.offsets.MonthBegin(-1)
            
            # Append data to a consolidated data table
            if consolidatedData.empty:
                consolidatedData = tempSheet
            else:
                consolidatedData = pd.merge(consolidatedData, tempSheet, left_on='Date', right_on='Date', how='left')
            
        except:
            next

consolidatedData['Month'] = pd.DatetimeIndex(consolidatedData['Date']).month

consolidatedData.to_csv(mainDirectory + r"\SUMMARY.csv")

tickerList = ['XLE-US','XLI-US','XLC-US','XLP-US','XLV-US','XLU-US','XLK-US','XLY-US','XLF-US','XLB-US','XLRE-US','R.2000','SP50','IVE-US','IVW-US']

for ticker in tickerList:
    returnWindow = 3
    consolidatedData[ticker + ' - 1 Month Return'] = consolidatedData[ticker].pct_change()    
    consolidatedData[ticker + ' - ' + str(returnWindow) + ' Month Return'] = consolidatedData[ticker + ' - 1 Month Return'] + 1
    consolidatedData[ticker + ' - ' + str(returnWindow) + ' Month Return'] = consolidatedData[ticker + ' - ' + str(returnWindow) + ' Month Return'].rolling(window=returnWindow).apply(np.prod, raw=True)-1
    consolidatedData[ticker + ' - ' + str(returnWindow) + ' Month Return'] = consolidatedData[ticker + ' - ' + str(returnWindow) + ' Month Return'].shift(periods=1-returnWindow)
    
featureList = [
                'Refinery Utilization', 
                'Natural Gas Consumption', 
                'Oil Consumption', 
                'Oil Imports',
                'CMTUS1M-FDS', 
                'CMTUS2Y-FDS', 
                'CMTUS5Y-FDS', 
                'CMTUS10Y-FDS', 
                'SP50 PE', 
                'SP50 Volume', 
                '2-5yr Inversion', 
                '5-10yr Inversion', 
                'Leading Indicators, Average Weekly Working Hours In Manufacturing - United States', 
                'ISM Manufacturing PMI - United States', 
                'New Privately Owned Housing Starts, SAAR, Thous Houses - United States',
                'Leading Indicators, ISM New Orders, Diffusion Index - United States',
                'Manufacturers Inventories',
                'Unemployment Insurance Initial Claims',
                'WTI-FDS', 
                'HHGAS-FDS', 
                'DXY.Z', 
                'GOLD-FDS',
                'COPP-FDS',
                'BAAFF', 
                'ICE BofA US High Yield Index Option-Adjusted Spread, Percent, Daily, Not Seasonally Adjusted',                
                'Unemployment Rate', 
                'Median CPI', 
                'PPI - Commodities', 
                'PCE', 
                'FEDFUNDS', 
                'US Retail Sales - Retail Trade', 
                'Trade Balance: Goods and Services', 
                'Real GDP', 
                'Nominal GDP', 
                'GDP % Seasonally Adjusted',
                'Delinquency Rate on Credit Card Loans, All Commercial Banks, Percent, Quarterly, Seasonally Adjusted',
                'PSAVERT',
                'M1SL',
                'M2SL',
                'University of Michigan: Consumer Sentiment',
                'All Employees, Total Nonfarm',
                'Capacity Utilization: Total Index',
                'Industrial Production: Total Index',
                'MORTGAGE30US',
                'Consumer Loans: Credit Cards and Other Revolving Plans, All Commercial Banks',
                'Consumer Confidence Index', 
                'JTSJOL',
                'Month'
]

outputList = [
#               'XLE-US' + ' - %s Month Return' % (returnWindow), 
#               'XLI-US' + ' - %s Month Return' % (returnWindow), 
#               'XLC-US' + ' - %s Month Return' % (returnWindow), 
#               'XLP-US' + ' - %s Month Return' % (returnWindow), 
#               'XLV-US' + ' - %s Month Return' % (returnWindow), 
#               'XLU-US' + ' - %s Month Return' % (returnWindow), 
#               'XLK-US' + ' - %s Month Return' % (returnWindow), 
#               'XLY-US' + ' - %s Month Return' % (returnWindow), 
#               'XLF-US' + ' - %s Month Return' % (returnWindow), 
#               'XLB-US' + ' - %s Month Return' % (returnWindow), 
#               'XLRE-US' + ' - %s Month Return' % (returnWindow), 
#               'R.2000' + ' - %s Month Return' % (returnWindow), 
#               'SP50' + ' - %s Month Return' % (returnWindow), 
#               'IVE-US' + ' - %s Month Return' % (returnWindow), 
#               'IVW-US' + ' - %s Month Return' % (returnWindow), 
              'Recession Index'
]

dateList = ['Date']

firstDifferenceList = [
               'M1SL',
               'M2SL',
               'Oil Consumption',           
               'Manufacturers Inventories',
               'PPI - Commodities', 
               'PCE', 
               'US Retail Sales - Retail Trade',   
               'Real GDP',
               'Nominal GDP',    
               'All Employees, Total Nonfarm',              
               'Consumer Loans: Credit Cards and Other Revolving Plans, All Commercial Banks', 
               'JTSJOL'
]

rollingWindowList = [    
               'M1SL',
               'M2SL',
               'Oil Consumption',           
               'Manufacturers Inventories',
               'PPI - Commodities', 
               'PCE', 
               'US Retail Sales - Retail Trade',   
               'Real GDP',
               'Nominal GDP',    
               'All Employees, Total Nonfarm',              
               'Consumer Loans: Credit Cards and Other Revolving Plans, All Commercial Banks',          
               'JTSJOL'
]

# First differencing to address time series data that goes up
for column in firstDifferenceList:
    differenceWindow = 1
    consolidatedData[column] = consolidatedData[column].pct_change()
    consolidatedData[column] = consolidatedData[column] + 1
    consolidatedData[column] = consolidatedData[column].rolling(window=differenceWindow).apply(np.prod, raw=True)-1

# Calculate the rolling z-score using kernel smoothing
for column in featureList:
    rollingWindow = 36
    if column in rollingWindowList:
        col_mean = consolidatedData[column].rolling(window=rollingWindow).mean()
        col_std = consolidatedData[column].rolling(window=rollingWindow).std()
        consolidatedData[column] = (consolidatedData[column] - col_mean)/col_std
    if (column == 'Date'):
        consolidatedData[column] = consolidatedData[column]
    else:
        consolidatedData[column] = inputScaler.fit_transform(consolidatedData[column].values.reshape(-1, 1))

################################################################################
#########################  CORRELATION MATRIX  #################################
################################################################################
'''
# Compute the correlation matrix
filteredList = featureList + outputList
filteredDF = consolidatedData[filteredList]
corr = filteredDF.corr()

# Generate a mask for the upper triangle
mask = np.triu(np.ones_like(corr, dtype=bool))

# Set up the matplotlib figure
f, ax = plt.subplots(figsize=(11, 9))

# Draw the heatmap with the mask and correct aspect ratio
sns.heatmap(corr, mask=mask)

# Calculate correlation for various lags on the recession indicator
# output = 'IVW-US' + ' - %s Month Return' % (returnWindow)
output = 'Business Confidence Index'
filteredList = featureList + [output]
tempDF = consolidatedData[filteredList]
for i in range (-12,13):
    tempDF[output + str(i) + '-shift'] = tempDF[output].shift(periods=i)

corrTimeSeries = tempDF.corr()
'''
################################################################################
###############################  MODELLING  ####################################
################################################################################

# Iterate through all the tickers
for output in outputList:
    # Get the feature list
    ticker = output.replace(' - %s Month Return' % (returnWindow), '')
    featureList = featureDF[ticker].dropna()
    featureList = featureList.tolist()
    
    # Fit the output variable to a scaler
    # consolidatedData['Recession Index'] = outputScaler.fit_transform(consolidatedData['Recession Index'].values.reshape(-1, 1))
    consolidatedData[output] = outputScaler.fit_transform(consolidatedData[output].values.reshape(-1, 1))
    
    # Consolidate lists            
    filteredList = dateList + featureList + [output]
    # filteredList = featureList + output
    filteredDF = consolidatedData[filteredList]
    
    # Add extra date rows to the bottom of the dataframe
    for i in range(0,4):
        # Incremental date for the new row
        last_date = pd.to_datetime(filteredDF['Date'].iloc[-1])
        new_date = last_date + relativedelta(months=1)

        # New row data
        new_row = {'Date': new_date.strftime('%Y-%m-%d')}
        filteredDF = pd.concat([filteredDF, pd.DataFrame([new_row])], ignore_index=True)
    
    filteredDF['Date'] = pd.to_datetime(filteredDF['Date']).dt.date
        
    
    # Time shift attributes according to strongest correlation with time lags
    for feature in featureList:
        timeLag = timeLagsDF[['Feature', ticker]][(timeLagsDF['Feature'] == feature)].iloc[0][ticker]
        timeLag = max(timeLag, 5)
        filteredDF[feature] = filteredDF[feature].shift(periods=timeLag)
        
    ## DROP ALL NA ROWS ##
    unfilteredDF = filteredDF
    filteredDF = filteredDF.dropna()
    unfilteredDF['Date'] = pd.to_datetime(unfilteredDF['Date']).dt.date
    tempTestDF = unfilteredDF[(unfilteredDF['Date'] >= date(2005, 3, 1))]
    
    
    ## LASSO REGRESSION ##
    # clf = linear_model.Lasso(alpha=0.1)
    # clf.fit(filteredDF[featureList], filteredDF[output])
    # xTest = tempTestDF[featureList]
    # yTest = tempTestDF[output]
    # y_pred = clf.predict(xTest).reshape(-1, 1)
    
    # prediction = outputScaler.inverse_transform(y_pred)
    # r2 = r2_score(filteredDF[output], y_pred)
    # print(r2)
    
    
    ## RECURRENT NEURAL NETWORK ##
    model = Sequential()
    
    # SPLIT OUT TRAINING AND TEST DATA
    # xTrain, xTest, yTrain, yTest = train_test_split(filteredDF[featureList], filteredDF[output], test_size=0.2, random_state = 42)
    date_cutoff = date(2023, 1, 1)
    tempTrainDF = filteredDF[(filteredDF['Date'] <= date_cutoff)]
    xTrain = tempTrainDF[featureList]
    yTrain = tempTrainDF[output]
    
    xTest = tempTestDF[featureList]
    yTest = tempTestDF[output]
    
    # Reshape to add the third dimension for timesteps - using 1 for a single additional timestep being added into the RNN
    xTrain = xTrain.values.reshape((xTrain.shape[0], xTrain.shape[1], 1))
    data_dim = xTrain.shape[1]
    
    # RECURRENT NEURAL NETWORK SETUP
    #model.add(SimpleRNN(units=8, input_shape=(data_dim, 1)))
    # model.add(Dense(units=6, activation='relu'))
    # model.add(Dropout(0.2)) # SHOULD NOT USE DROPOUT FOR RNN
    # model.add(Dense(units=4, activation='relu'))
    # model.add(Dense(1, activation='linear'))
    
    # LSTM NEURAL NETWORK SETUP
    model.add(LSTM(units=8, input_shape=(data_dim, 1)))
    model.add(Dense(units=4, activation='relu'))
    model.add(Dense(1, activation='linear'))
    
    model.summary()
    history = History()
    
    # Compile the keras model
    adams = optimizers.Adam(lr=0.03)
    model.compile(loss='mean_squared_error', optimizer=adams)
    
    # fit the keras model on the dataset
    history = model.fit(xTrain, yTrain, epochs=150)
    
    # Get training and test loss histories
    training_loss = history.history['loss']
    #test_loss = history.history['val_loss']
    
    # Create count of the number of epochs
    epoch_count = range(1, len(training_loss) + 1)
    
    # Visualize loss history
    plt.plot(epoch_count, training_loss, 'r--')
    #plt.plot(epoch_count, test_loss, 'b-')
    plt.legend(['Training Loss', 'Test Loss'])
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.show();
    
    # Evaluate the keras model
    model.evaluate(xTrain, verbose=2)
    
    # Reshape to add the third dimension for timesteps - using 1 for a single additional timestep being added into the RNN
    xTest = xTest.values.reshape((xTest.shape[0], xTest.shape[1], 1))
    # Run prediction on the test data
    prediction = model.predict(xTest)
    
    predictionDF.append(outputScaler.inverse_transform(prediction).ravel().tolist())
    actualDF.append(outputScaler.inverse_transform(yTest.values.reshape(-1,1)).ravel().tolist())

predictionDF = pd.DataFrame(predictionDF).T
actualDF = pd.DataFrame(actualDF).T
predictionDF.columns = outputList
actualDF.columns = outputList

################################################################################
##############################  OUTPUTS  ######################################
################################################################################

#featureDF = consolidatedData[featureList]
#outputDF = consolidatedData[outputList]
#featureDF.to_csv(mainDirectory + r"\FEATURE_SUMMARY.csv")
#outputDF.to_csv(mainDirectory + r"\OUTPUT_SUMMARY.csv")

# filteredDF.to_csv(mainDirectory + r"\FILTERED_SUMMARY.csv")


################################# SHAP ANALYSIS #################################
    # Prints the feature importances based on SHAP values in an ordered way
    # shap_values -> The SHAP values calculated from a shap.Explainer object
    # features -> The name of the features, on the order presented to the explainer
'''
# Fits the explainer
testSample = tempTestDF[featureList]#.iloc[:15000] # shorten the list of 
explainer = shap.Explainer(model.predict, testSample)

# Calculates the SHAP values
shap_values = explainer(testSample)
#shap.plots.waterfall(shap_values.values[0])

shapOutputs = pd.DataFrame(shap_values.values[0], index = testSample.columns)

# Beeswarm
shap.plots.beeswarm(shap_values)
'''


