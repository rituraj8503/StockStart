import yfinance as yf
import streamlit as st
import pandas as pd
from plotly import graph_objs as go
from datetime import date
from pandas_datareader import data
import csv
import numpy as np


START = "2020-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

def is_bearish_candlestick(candle):
    return candle['close'] < candle['open']


def is_bullish_engulfing(list, index):
    current_day = list[index]
    previous_day = list[index - 1]

    if is_bearish_candlestick(previous_day) \
        and current_day['close'] > previous_day['open'] \
        and current_day['open'] < previous_day['close']:
        return True
    
    return False
  



def candlestick(ticker):
    # dealing with showing candlesticks
    df = data.DataReader(ticker, 'yahoo', START, TODAY)
    df.reset_index(inplace=True)
    fig = go.Figure()
    candlesticks = go.Candlestick(x = df['Date'], low = df['Low'], high = df['High'], close = df['Close'], open = df['Open'], increasing_line_color = 'green', decreasing_line_color = 'red', name="candlesticks")
    fig.add_trace(trace=candlesticks)
    st.plotly_chart(fig)

    # dealing with pattern searching
    yfData = yf.Ticker(ticker)
    dataframe = yfData.history(period="1y")
    dataframe.reset_index(inplace=True)
    csvData = dataframe.to_csv()
    dateData = dataframe['Date']
    closeData = dataframe['Close']
    openData = dataframe['Open']

    dates = []
    close = []
    open = []
    main = []
    for item in dateData:
        dates.append(item)

    for item in closeData:
        close.append(item)

    for item in openData:
        open.append(item)

    length = len(dates)
    for i in range(length):
        main.append({
            'date': dates[i],
            'close': close[i],
            'open': open[i]
        })
    
    for i in range(length):
        if is_bullish_engulfing(main, i):
            print("{} is a bullish engulfing".format(main[i]['date']))
            st.write("{} is a bullish engulfing".format(main[i]['date']))
        





