
from yahoofinancials import YahooFinancials
import streamlit as st
import pandas as pd


st.write("""
# Simple Stock Price App

Enter the ticker symbol to see the stock **closing price** and **volume** of the stock!

""")

# Ask user for ticker symbol
tickerSymbol = st.text_input("Enter ticker symbol")

# Check if ticker symbol is provided
if tickerSymbol:
    try:
        # Get data on the ticker symbol
        tickerData = YahooFinancials(tickerSymbol)

        # Get the historical prices for this ticker
        tickerDf = tickerData.get_historical_price_data(start_date='2010-05-31', end_date='2020-05-31', time_interval='daily')

        # Extract the historical stock prices
        prices = tickerDf[tickerSymbol]['prices']
        df = pd.DataFrame(prices)
        df['date'] = pd.to_datetime(df['formatted_date'])

        st.write("""
        ## Closing Price
        """)
        st.line_chart(df['close'])

        st.write("""
        ## Volume Price
        """)
        st.line_chart(df['volume'])

    except KeyError:
        st.write("Invalid ticker symbol. Please enter a valid symbol.")


