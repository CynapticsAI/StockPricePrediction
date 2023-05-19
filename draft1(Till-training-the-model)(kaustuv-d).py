# -*- coding: utf-8 -*-
"""draft1(kaustuv-d)_MIR.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1LclFXukR48MvoSTce1wUp4Cr49hEukq0

# MIR - **STOCK PRICE PREDICTION**

## Getting the Market Data 
(For the company - ***Apple Inc.***
with Ticker Symbol - **AAPL**)
"""

pip install yfinance

import pandas as pd
import numpy as np
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

apl = yf.Ticker('AAPL')
apl

data = apl.history()
data.head()
#we will be taking the data from 2010, but here it starts from 2023 April , ie, 1 month data.

data.tail()

"""**Taking start date and end date for the company's stock details**

"""

start_time = pd.to_datetime('2010-01-01')
end_time = pd.to_datetime('2023-05-18')
stock = ['AAPL']
data = yf.download(stock, start = start_time, end = end_time)

"""###:The accessed Data of APPLE from (January 1, 2010) to Current Date (May 18, 2023)"""

print(data)

data.reset_index(inplace=True)
data

data.to_csv("AAPL.csv")

"""###Visualizing the Data : (Stock Price --> "Close") """

stk_close = data.reset_index()['Close']
stk_close

Dates = data.reset_index()['Date']
Dates

plt.plot(Dates, stk_close)

"""##Preprocessing the accessed data"""

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))
stk_close= scaler.fit_transform(np.array(stk_close).reshape(-1,1))

print(stk_close)

stk_close

Date01= Dates.to_numpy()
Date = Date01.reshape(3366, 1)

#splitting dataset into train, validation and test datasets
training_size = int(len(stk_close)*0.65)
t_size = len(stk_close)-training_size
valid_size = int(t_size*0.7)
test_size = int(t_size-valid_size)
train_data, valid_data, test_data = stk_close[0:training_size, :], stk_close[training_size:(training_size + valid_size), :], stk_close[(training_size + valid_size):len(stk_close), :]

training_size, valid_size, test_size

import matplotlib.pyplot as plt
plt.plot(Date[0:2187],train_data)
plt.plot(Date[2187:3012],valid_data)
plt.plot(Date[3012:3366], test_data)
plt.legend(['Train','Validation','Test'])

"""**Adding Timesteps**"""

# defining a function to add the required timesteps
def create_dataset(dataset, time_steps=1):
  dataX, dataY= [], []
  for i in range(len(dataset)-time_steps-1):
    a=dataset[i:(i+time_steps), 0]
    dataX.append(a)
    dataY.append(dataset[i+time_steps, 0])
  return np.array(dataX), np.array(dataY)

# taking timesteps and change it accordingly during fine-tuning
time_steps =100

# fittting the train and test sets
X_train, y_train = create_dataset(train_data, time_steps)
X_valid, y_valid = create_dataset(valid_data, time_steps)
X_test, y_test = create_dataset(test_data, time_steps)

print(X_train.shape), print(y_train.shape)

print(X_valid.shape), print(y_valid.shape)

print(X_test.shape), print(y_test.shape)

plt.plot(Date[0:2086], y_train)

"""#Creating the LSTM model"""

# reshaping inputs into 3 dimensions
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1],1)
X_valid = X_valid.reshape(X_valid.shape[0], X_valid.shape[1],1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1],1)

pip install tensorflow

pip install keras

# Creating stacked LSTM model
import tensorflow as tf
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.optimizers import Adam

model = Sequential()
model.add(LSTM(100,return_sequences=True, input_shape=(100,1)))
model.add(Dropout(0.2))
model.add(LSTM(50,return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(50,return_sequences=True))
model.add(Dropout(0.5))
model.add(LSTM(units=50))
model.add(Dropout(0.5))
model.add(Dense(1))
model.compile(loss='mean_squared_error', optimizer='adam')

model.summary()

# fitting the model
history = model.fit(X_train, y_train, validation_data=(X_valid, y_valid),epochs=100, batch_size=64, verbose=1)

"""**Checking Performances**"""

train_predict=model.predict(X_train)
valid_predict=model.predict(X_valid)
test_predict=model.predict(X_test)

len(train_predict)

len(valid_predict)

len(test_predict)

# ReverseScaling to original form
train_predict=scaler.inverse_transform(train_predict)
valid_predict=scaler.inverse_transform(valid_predict)
test_predict=scaler.inverse_transform(test_predict)

import math
from sklearn.metrics import mean_squared_error
math.sqrt(mean_squared_error(y_train, train_predict))

math.sqrt(mean_squared_error(y_valid, valid_predict))

math.sqrt(mean_squared_error(y_test, test_predict))

# Get training and test loss histories
training_loss = history.history['loss']
valid_loss = history.history['loss']
test_loss = history.history['val_loss']

# Create count of the number of epochs
epoch_count = range(1, len(training_loss) + 1)

# Visualize loss history
plt.plot(epoch_count, training_loss)
plt.plot(epoch_count, valid_loss)
plt.plot(epoch_count, test_loss)
plt.legend(['Training Loss','Validation Loss', 'Test Loss'])
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.show()

train_predict=model.predict(X_train).flatten() 

plt.plot(Date[0:2086],train_predict)
plt.plot(Date[0:2086],y_train)
plt.legend(['Training Predictions','Training Observations'])

valid_predict=model.predict(X_valid).flatten()

plt.plot(Date[2187:2911],valid_predict)
plt.plot(Date[2187:2911],y_valid)
plt.legend(['Validation Predictions','Validation Observations'])

test_predict=model.predict(X_test).flatten()

plt.plot(Date[3012:3265], test_predict)
plt.plot(Date[3012:3265], y_test)
plt.legend(['Test Predictions', 'Test Observations' ])

plt.plot(Date[0:2086],train_predict)
plt.plot(Date[0:2086],y_train)
plt.plot(Date[2187:2911],valid_predict)
plt.plot(Date[2187:2911],y_valid)
plt.plot(Date[3012:3265], test_predict)
plt.plot(Date[3012:3265], y_test)
plt.legend(['Training Predictions','Training Observations','Validation Predictions','Validation Observations','Test Predictions', 'Test Observations'])

"""## Future Predictions

"""
