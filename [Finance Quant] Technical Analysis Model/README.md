

<!-- OBJECTIVE -->
## OBJECTIVE

OBJECTIVE: Create a model to predict an up/down movement in a stock price using technical indicators.

<!-- ABOUT THE PROJECT -->
## ABOUT THE PROJECT

Technical analysis is the study of a collective market sentiment, it assumes inefficient markets and that there are trends, patterns, and repeatability in stock price behavior. The output is whether the stock price moves up or down in 1-day, 7-days, 30-days, or 90-days. This model does not attempt to predict stock price itself because of the number of exogenous factors that contribute to stock price. The following a technical indicators used in the model:

- **Stochastic Oscillator** - a momentum based indicator that measures the price of a stock relative to the highest high and lowest low in a selected time frame  = [(Price - Lowest Low)/(Highest High - Lowest Low)]
- **William %R** - a variant of a stochastic oscillator = [(Highest High - Price)/(Highest High - Lowest Low)]
- **Relative Strength Index (RSI)** - is a momentum based indicator that measures the rolling gain or losses over a time period. RSI can be calculated on price or on volume.  = 100 - (100/ (1 + (previousAvgGain/previousAvgLoss*-1)))
- **Simple Moving Average** - measures the price of a stock relative to a moving average of the price, typically measured against the 20 or 50 day averages
- **Exponential Moving Average** - similar to a simple moving average, but puts more weight on current data
- **Moving Average Convergence/Divergence (MACD)** - a momentum indicator that measures the difference between two moving average lines, in this instance the 50/200 using simple moving average and exponential moving average lines was used
- **Bollinger Bands** - a technical indicator that calculates a top and bottom band based on a number of standard deviations away from a moving average line

Most data is normalized using a standardized scaler, certain data is normalized using kernel smoothing - which standardized the data of a moving window.


<!-- USAGE EXAMPLES -->
## Usage


<!-- ROADMAP -->
## Roadmap


<!-- CONTACT -->
## Contact

Tommy Chu - www.linkedin.com/in/ttchu - tommy.chu3@gmail.com

