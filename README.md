
# Stock Price Prediction

This project aims to predict the prices of stocks using historical data and machine learning algorithms. This project is based on Time Series Prediction models like meta's fbprophet and also models based on LSTM (RNN). 

### Project Overview

The stock price prediction project utilizes historical stock market data to build and evaluate machine learning models capable of predicting future stock prices. It is trained on dataset of the stock data from the year 2015-2020. By analyzing patterns and trends in the stock market, we can make informed predictions about the future performance of a particular stock. This project aims to tell whether we will be getting a profit or loss on buying that stock, also returns us the cumulative profit for a period of days.

### Usage
The project provides a set of scripts and Jupyter notebooks for different stages of the stock price prediction pipeline.
For running the model we just need to follow the following steps:

1) Type in the following command in the Command Prompt
```
streamlit run app_mir_1.py
```

or 

(for trying the model on the MIR_app_fd.zip file)

```
streamlit run app_MIR.py
```

(it will open up on a web page)

2) Enter the Company's Stock ticker whose prices we want to predict.

Exceptions to be considered : The stock whose data isn't available on the time period 2015-20 on the yfinance library, the model will raise an error.

