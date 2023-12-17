<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create a leading indicator/macroeconomic model that (1) predicts a recession (based on a recession index published by James D. Hamilton that is premised on GDP) and (2) using the recession index as well as a number of other leading indicators calculate the 3-month returns on a series of sector ETF's

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

ABOUT THE PROJECT: Project is broken down into 3 steps:
1) Data ingest - from various sources FRED, FactSet, EIA, and OECD
2) Data transformation - clean up data using transformations such as:
	a) Convert quarterly, monthly, and daily data into monthly data
	b) Filter data according to most practical and relevant time period 2000+
	b) First difference time series data so data is covariance stationary
	c) Normalize data - certain data series are "windowed" in the sense they are normalized over a time window to exagerrate movements over a 'x'-year window - data is standardized using a z-scaler
	d) Apply shifts to data so the feature input is time lagged to the most correlated time step
3) Data model - three models were attempted: Neural Network, Random Forest (other file), and LASSO multivariate linear regression

Principles of the algorithm were loosely based on a paper written by Karatas and Hirsa (2021) “Two-Stage Sector Rotation Methodology Using Machine Learning and Deep Learning Techniques”

Features List:
FRED – Federal Reserve Economic Data - St.Louis FED
GDP
-Gross Domestic Product, Billions of Dollars, Quarterly, Seasonally Adjusted Annual Rate
-Real Gross Domestic Product, Billions of Chained 2017 Dollars, Quarterly, Seasonally Adjusted Annual Rate
-Percent Change from Preceding Period,Seasonally Adjusted Annual Rate
Employment
-Unemployment Rate, Percent, Monthly, Seasonally Adjusted
-All Employees, Total Nonfarm (PAYEMS)
Price Indexes - CPI – PPI – PCE
-Personal Consumption Expenditures, Billions of Dollars, Monthly, Seasonally Adjusted Annual Rate
-Producer Price Index by Commodity: All Commodities, Index 1982=100, Monthly, Not Seasonally Adjusted
-Median Consumer Price Index, Percent Change at Annual Rate, Monthly, Seasonally Adjusted
Mortgage Rate
-30-Year Fixed Rate Mortgage Average in the United States, Percent, Weekly, Not Seasonally Adjusted
Interest Rates – FED funds 
-Federal Funds Effective Rate, Percent, Monthly, Not Seasonally Adjusted
Retail Sales – retail trade
-Retail Sales: Retail Trade, Millions of Dollars, Monthly, Seasonally Adjusted
Trade Balance
Trade Balance: Goods and Services, Balance of Payments Basis, Millions of Dollars, Monthly, Seasonally Adjusted

Credit Spreads
-Moody's Seasoned Baa Corporate Bond Minus Federal Funds Rate, Percent, Daily, Not Seasonally Adjusted
-ICE BofA US High Yield Index Option-Adjusted Spread, Percent, Daily, Not Seasonally Adjusted
-Delinquency Rate on Credit Card Loans, All Commercial Banks
-Consumer Loans: Credit Cards and Other Revolving Plans, All Commercial Banks
Consumer Health
-Personal Saving Rate (PSAVERT)
Manufacturing
-Capacity Utilization: Total Index (TCU)
-Industrial Production: Total Index (INDPRO)
Money Supply
-M1 (M1SL)
-M2 (M2SL)

Macroeconomics – FactSet
-Average weekly hours
-PMI – manufacturing index
-Oil price – WTI
-Gas price - HH
-Interest Rates – inversion – aka term spread
-New Privately Owned Housing Starts, SAAR, Thous Houses - United States
-Unemployment Insurance Initial Claims, SA - United States / 1000
Macroeconomics – OECD
-Consumer and Business confidence index
Macroeconomics – EIA
-Refinery utilization
-Gas consumption
-Oil consumptions
Prices
-S&P 500 P/E
-S&P 500 Volume
-USD dollar index

Data Discovery:
- Correlation matrix was extracted for all features and outputs
- Features with the highest correlation to the output (recession index, and 3-month return) were initially used in the model
- Correlation exercise was run 

<!-- USAGE EXAMPLES -->
## Usage

USAGE: Few functions are built in the body of the code and can be commented in/out depending on usage.

Correlation Matrix:
- Option to calculate correlation matrix for all input/output features for data discovery
- Additional functional built out to calculate correlations for data 

Model Training:
- LASSO Regression - toggle on/off - simple linear regression that penalizes insignificant features
- Neural Network - created a recurrent neural network that recursively passes features from the last time step into the current time step. Simple neural network was trailed as well as LSTM RNN.

Analysis:
- SHAP Analysis - SHAP analysis used to back out significance of features, SHAP is agnostic of model, given the size of the data set using the full training set in the SHAP analysis was not computationally heavy.

<!-- ROADMAP -->
## Roadmap

ROADMAP:


<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

