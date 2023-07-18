import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date as dt_date
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

def get_stock_data(symbol, start_date, end_date):
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

def get_company_name(symbol):
    company = yf.Ticker(symbol)
    return company.info['longName']


def train_arima_model(data, prediction_days):
    model = ARIMA(data['Adj Close'], order=(5, 1, 0))
    model_fit = model.fit()

    # Get the forecasted values (including the last actual price)
    forecast = model_fit.forecast(steps=prediction_days)


    # Prepare data for prediction
    last_date = data.index[-1]
    forecast_dates = pd.date_range(start=last_date + timedelta(days=1), periods=prediction_days)

    return model_fit, forecast, forecast_dates



def main():
    st.title("Finance Project with Streamlit")

    # Get user inputs
    symbol = st.text_input("Enter the stock symbol (e.g., AAPL):", "AAPL")
    start_date = st.date_input("Start date:", datetime(2021, 1, 1))

    # Set end_date to today
    end_date = dt_date.today()  # Use dt_date to avoid conflicts

    # Fetch and display stock data
    stock_data = get_stock_data(symbol, start_date, end_date)
    company_name = get_company_name(symbol)

    st.subheader(f"{company_name} ({symbol}) Stock Prices from {start_date} to {end_date}")
    st.line_chart(stock_data["Adj Close"])
    # Stock price prediction using ARIMA
    st.subheader("Stock Price Prediction using ARIMA")
    prediction_days = st.slider("Select the number of days for prediction:", 1, 30, 7)

    # Train the ARIMA model
    model_fit, forecast, forecast_dates = train_arima_model(stock_data, prediction_days)

    # Plot predicted stock prices using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.plot(forecast_dates, forecast, label='Predicted Stock Prices', color='orange')
    plt.xlabel('Date')
    plt.ylabel('Stock Price')
    plt.title(f"Predicted Stock Prices for {company_name} ({symbol})")
    plt.legend()

    # Display predicted prices as text labels on the plot
    for date, price in zip(forecast_dates, forecast):
        plt.text(date, price, f'{price:.2f}', ha='center', va='bottom', color='black')

    st.pyplot(plt)





if __name__ == "__main__":
    main()





