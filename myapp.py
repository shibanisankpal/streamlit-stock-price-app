from yahoofinancials import YahooFinancials
import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

st.write("""
# Stock Price Prediction

Enter the ticker symbol to predict the future stock **closing price**!
""")

# Ask user for ticker symbol
tickerSymbol = st.text_input("Enter ticker symbol")

# Check if ticker symbol is provided
if tickerSymbol:
    try:
        # Get data on the ticker symbol
        tickerData = YahooFinancials(tickerSymbol)

        # Get the historical prices for this ticker
        tickerDf = tickerData.get_historical_price_data(start_date='2010-05-31', end_date='2023-05-31', time_interval='daily')

        # Extract the historical stock prices
        prices = tickerDf[tickerSymbol]['prices']
        df = pd.DataFrame(prices)
        df['date'] = pd.to_datetime(df['formatted_date'])
        df = df[['date', 'close']]
        df = df.set_index('date')

        # Create a new DataFrame with a shifted column for the target variable
        df_shifted = df.shift(-1)

        # Split the data into training and testing sets
        train_data = df.iloc[:-100]  # Use the first n-100 data points for training
        test_data = df.iloc[-100:]  # Use the last 100 data points for testing

        # Scale the data
        scaler = MinMaxScaler()
        train_scaled = scaler.fit_transform(train_data)
        test_scaled = scaler.transform(test_data)

        # Split the data into input features and target variable
        X_train, y_train = train_scaled[:, :-1], train_scaled[:, -1]
        X_test, y_test = test_scaled[:, :-1], test_scaled[:, -1]

        # Reshape the input features to be 3-dimensional for LSTM model
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        # Create an LSTM model
        model = Sequential()
        model.add(LSTM(64, activation='relu', input_shape=(X_train.shape[1], 1)))
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        # Train the model
        model.fit(X_train, y_train, epochs=10, batch_size=32)

        # Make predictions on the test set
        predictions = model.predict(X_test)
        predictions = scaler.inverse_transform(pd.concat([pd.DataFrame(X_test[:, :-1]), pd.DataFrame(predictions)], axis=1))[:, -1]

        # Add the predicted values to the test_data DataFrame
        test_data['predicted_close'] = predictions

        st.write("""
        ## Actual vs. Predicted Closing Price
        """)
        st.line_chart(test_data[['close', 'predicted_close']])

    except KeyError:
        st.write("Invalid ticker symbol. Please enter a valid symbol.")


