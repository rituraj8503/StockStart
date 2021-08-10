from prophet.plot import plot
import yfinance as yf
from plotly import graph_objs as go
import pandas as pd
import streamlit as st
from datetime import date
import numpy as np
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

data = yf.download("SENS", START, TODAY)
data.reset_index(inplace=True)
print(data.shape)

fig1 = go.Figure()
# fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close')) 

playData = data
playData = playData[['Close']] #clone of the data so I don't manipulate the actual thing

#Create a variable to predict x days out into the future
future_days = 25
#Create a new column (target)
playData['Prediction'] = playData[['Close']].shift(-future_days)
print(playData.tail())

#Create the feature data set and convert it to a numpy array and remove the last 'x' rows/days
X = np.array(playData.drop(['Prediction'], 1))[:-future_days]
print(X)

#Create the target data set and convert it to a numpy array and get all of the target values except the last x rows
y = np.array(playData['Prediction'])[:-future_days]
print(y)

#split the data into 75% training and 25% testing
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

#Create the models
#Create decision Tree resgressor model
tree = DecisionTreeRegressor().fit(x_train, y_train)
#Create the Linear Regression model
lr = LinearRegression().fit(x_train, y_train)

#get the last x rows of the feature dataset
x_future = playData.drop(['Prediction'], 1)[:-future_days]
x_future = x_future.tail(future_days)
x_future = np.array(x_future)

#Show the model tree prediction
tree_prediction = tree.predict(x_future)
print(tree_prediction)
print()

#Show the model linear regression prediction
lr_prediction = lr.predict(x_future)
print(lr_prediction)

#Visualize the data
predictions = tree_prediction

valid = playData[X.shape[0]:]
valid['Prediction'] = predictions
print(valid)
print(data)
fig1.add_trace(go.Scatter(x=data['Date'].tail(25), y=data['Close'], name='actual'))
fig1.add_trace(go.Scatter(x=data['Date'].tail(25), y=valid['Prediction'], name='tree_regressor'))
# print(playData)

st.plotly_chart(fig1)

fig2 = go.Figure()
predictions_two = lr_prediction
valid_lr = playData[X.shape[0]:]
valid_lr['Prediction'] = predictions_two
fig2.add_trace(go.Scatter(x=data['Date'].tail(25), y=data['Close'], name='actual'))
fig2.add_trace(go.Scatter(x=data['Date'].tail(25), y=valid_lr['Prediction'], name='linear_regression'))
st.plotly_chart(fig2)

