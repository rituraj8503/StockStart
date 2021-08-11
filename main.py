import streamlit as st
from datetime import date

import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from mlalgos import show_ml_algos
from furtherstats import show_futher_stats
from candlestick import candlestick

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title("Finance App")
st.sidebar.title("Options")

options = st.sidebar.selectbox("Which dashboard?", ("Stock Predictor", "Visualize Some Basic ML Algos", "Analyze Statistics", "Patterns"))
st.header(options)

stocks = ("AAPL", "GOOG", "MSFT", "SENS")
selected_stock = st.selectbox("Select stock to analyze", stocks)

if options == "Stock Predictor":

    n_years = st.slider("Years of prediction", 1, 4)
    period = n_years * 365

    @st.cache
    def load_data(ticker):
        data = yf.download(ticker, START, TODAY)
        data.reset_index(inplace=True)
        return data

    data_load_state = st.text("Load data...")
    data = load_data(selected_stock)
    data_load_state.text("Loading data...done!")

    st.subheader("Raw Data")
    st.write(data.tail())

    def plot_raw_data():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='stock_open'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='stock_close')) 
        fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)

    plot_raw_data()

    #forecasting
    df_train = data[['Date', 'Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet()
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict (future)

    st.subheader('Forecasted Data')
    st.write(forecast.tail())


    st.write('Forecasted Data')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)
    st.write("Forecast Components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

if options == "Visualize Some Basic ML Algos":
    show_ml_algos(selected_stock)


if options == "Analyze Statistics":
    show_futher_stats(selected_stock)

if options == "Patterns":
    candlestick(selected_stock)