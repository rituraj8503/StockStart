import yfinance as yf
import streamlit as st



def show_futher_stats(ticker):
    company = yf.Ticker(ticker)
    st.write(company.info)
    st.image(company.info["logo_url"])
    st.write("Sector: " + company.info["sector"])
    st.write("Industry: " + company.info["industry"])
    st.write("Current Price " + str(company.info["currentPrice"]))
    st.write("Day High: $" + str(company.info["dayHigh"]))
    st.write("Day Low: $" + str(company.info["dayLow"]))
    st.write("Earnings Growth: " + str(company.info["earningsGrowth"]))
    st.write("Quarterly Earnings Growth: " + str(company.info["earningsQuarterlyGrowth"]))
    st.write("Profit Margins: " + str(company.info["profitMargins"]))
    volume = st.write("Volume: " + str(company.info["volume"]))
    avg_volume = st.write("Average Volume: " + str(company.info["averageVolume"]))
    button = st.button("View Financials")

    if button:
        close = st.button("Close Financials")
        st.write(company.financials)
        if close:
            button = False