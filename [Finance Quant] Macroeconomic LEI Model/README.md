

<!-- OBJECTIVE -->
## OBJECTIVE

**OBJECTIVE**: Create a leading indicator/macroeconomic model that **(1)** predicts a recession (based on a recession index published by James D. Hamilton that is premised on GDP) and **(2)** using the recession index as a feature as well as a number of other leading indicators calculate the 3-month returns on a series of sector ETF's

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

The process is broken down into 3 steps:
1) **Data ingest** - csv's captured from various data sources including: FRED, FactSet, EIA, and OECD (full list included below)
2) **Data transformation** - data cleaned using the following transformations:
	a) Convert quarterly, monthly, and daily data into monthly data
	b) Filter data according to most practical and relevant time period 2000-2022 (264 data points on a monthly basis)
	b) First difference time series data to ensure series is covariance stationary
	c) Normalize data - data is standardized using a normal z-scaler - certain data series are "windowed" so they are normalized over a time window to amplify movements over a 'x'-year window  
	d) Apply shifts to data so the feature input is time lagged to the most correlated time step
3) **Data model** - three models were trained and evaluated: a Neural Network, Random Forest (other file), and LASSO multivariate linear regression

Principles of the algorithm were loosely based on a paper written by Karatas and Hirsa (2021) “Two-Stage Sector Rotation Methodology Using Machine Learning and Deep Learning Techniques”

## FEATURE LIST:

**FRED – Federal Reserve Economic Data - St.Louis FED**
GDP

 - Gross Domestic Product, Billions of Dollars, Quarterly, Seasonally Adjusted Annual Rate
 - Real Gross Domestic Product, Billions of Chained 2017 Dollars, Quarterly, Seasonally Adjusted Annual Rate
 - Percent Change from Preceding Period,Seasonally Adjusted Annual Rate Employment
 - Unemployment Rate, Percent, Monthly, Seasonally Adjusted
 - All Employees, Total Nonfarm (PAYEMS)

Price Indexes - CPI – PPI – PCE

 - Personal Consumption Expenditures, Billions of Dollars, Monthly, Seasonally Adjusted Annual Rate
 - Producer Price Index by Commodity: All Commodities, Index 1982=100, Monthly, Not Seasonally Adjusted
 - Median Consumer Price Index, Percent Change at Annual Rate, Monthly, Seasonally Adjusted 

Mortgage Rate

 - 30-Year Fixed Rate Mortgage Average in the United States, Percent, Weekly, Not Seasonally Adjusted

Interest Rates – FED funds
 - Federal Funds Effective Rate, Percent, Monthly, Not Seasonally Adjusted

Retail Sales – retail trade

 - Retail Sales: Retail Trade, Millions of Dollars, Monthly, Seasonally Adjusted

Trade Balance

 - Trade Balance: Goods and Services, Balance of Payments Basis, Millions of Dollars, Monthly, Seasonally Adjusted

Credit Spreads

 - Moody's Seasoned Baa Corporate Bond Minus Federal Funds Rate, Percent, Daily, Not Seasonally Adjusted 
 - ICE BofA US High Yield Index Option-Adjusted Spread, Percent, Daily, Not Seasonally Adjusted   
 - Delinquency Rate on Credit Card Loans, All Commercial Banks    -Consumer Loans: Credit Cards and Other Revolving Plans, All Commercial Banks

Consumer Health
 - Personal Saving Rate (PSAVERT)

Manufacturing

 - Capacity Utilization: Total Index (TCU)
 - Industrial Production: Total Index (INDPRO)

Money Supply
 - M1 (M1SL)
 - M2 (M2SL)

**Macroeconomics – FactSet**

 - Average weekly hours
 - PMI – manufacturing index
 - Oil price – WTI
 - Gas price - HH
 - Interest Rates – inversion – aka term spread
 - New Privately Owned Housing Starts, SAAR, Thous Houses - United States
 - Unemployment Insurance Initial Claims, SA - United States / 1000

**Macroeconomics – OECD**

 - Consumer and Business confidence index
 
 **Macroeconomics – EIA**

 - Refinery utilization
 - Gas consumption
 - Oil consumptions

**Price Data - Factset**

 - S&P 500 P/E
 - S&P 500 Volume
 - USD dollar index

## Data Discovery
- A correlation matrix was extracted for features and outputs
- Features with the highest correlation to the output variable (recession index and 3-month return) were used in the model
- A correlation exercise was run on various time lags (form -12 to +12 months), and the time lag with the greatest correlation to the output variable was ultimately used. Not all variables are coincident, therefore the time-lagged correlations helped identify leading, coincident, and lagging indicators.

<!-- USAGE EXAMPLES -->
## Usage

A few functions are built in the body of the code and can be commented in/out depending on usage.

**Correlation Matrix**:
- Option to calculate correlation matrix for all input/output features for data discovery
- Additional functional built out to calculate correlations for data 

**Model Training**:
- LASSO Regression - toggle on/off - simple linear regression that penalizes insignificant features
- Neural Network - created a recurrent neural network that recursively passes features from the last time step into the current time step. Multiple variants of a neural network were used such as vanilla neural network, RNN, and LSTM
- 80/20 training/test data set split 
- Model currently trained on 150 epochs, training loss appears to have troughed at 150 - additional epochs caused overfitting of the model

**Analysis**:
- SHAP Analysis - SHAP analysis was used to back out significance of features, SHAP is agnostic of the model, given the size of the data set SHAP was run over the entire training set and was not computationally burdensome.


## INITIAL RESULTS

 LASSO regression suggests that most salient variables that affect the recession index are: S&P 500 Volume, Average Weekly Hours, ISM Manufacturing Index, Credit Spreads, US Retail Sales, and the Business Confidence Index. These features are vetted using first principles to avoid spurious correlations.

 1. S&P 500 Volume (+10.08 Coefficient) - suggests that when recessions are proceeded by a capitulation (aka sell-off) in the stocks
 2. ISM Manufacturing Index (-3.98 Coefficient) - suggests that when manufacturing declines there is a higher probability of a recession, consistent with first principles
 3. Credit Spreads (-3.76 Coefficient) - suggests that as credit spreads widen (more negative) there is a positive correlation to the recession index. This is consistent with what happened in the great recession. Oddly, credit spreads are narrow right now, despite the other indicators suggesting a recession this goes against prior recessions.
 4. US Retail Sales (+1.3 Coefficient) - Data set is first differenced, therefore positive values are M/M increases. First principles suggests that as sales increase there should be a negative correlation with the recession index. This needs to be evaluated further.
 5. Business Confidence Index (-11.59 Coefficient) - Survey based data that polls the sentiment of businesses. This has the strongest correlation, suggests that when business confidence drops there is an incoming recession (since business confidence ripples down to manufacturing, lay offs, etc...) consistent with first principles.

<!-- ROADMAP -->
## ROADMAP
Project is currently functional, out-of-sample accuracy can be improved. Below is a running list of action items for the project.
- Investigate correlation sign mismatch on  US Retail Sales for LASSO regression model
- Explore additional feature engineering, such as Recursive Feature Elimination (RFE) outlined in Karatas and Hirsa (2021) to determine most relevant features to include in neural network as opposed to a simple correlation analysis

<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

