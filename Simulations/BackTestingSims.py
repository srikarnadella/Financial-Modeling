import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np
def download_stock_data(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def moving_average_crossover_strategy(stock_data, short_window, long_window):
    signals = pd.DataFrame(index=stock_data.index)
    signals['Price'] = stock_data['Close']
    signals['Short_MA'] = stock_data['Close'].rolling(window=short_window, min_periods=1).mean()
    signals['Long_MA'] = stock_data['Close'].rolling(window=long_window, min_periods=1).mean()
    signals['Signal'] = 0.0
    signals['Signal'][short_window:] = np.where(signals['Short_MA'][short_window:] > signals['Long_MA'][short_window:], 1.0, 0.0)
    signals['Position'] = signals['Signal'].diff()
    
    return signals

# Parameters
ticker = 'AAPL'
start_date = '2021-01-01'
end_date = '2022-12-31'
short_window = 50
long_window = 200

# Run backtesting
stock_data = download_stock_data(ticker, start_date, end_date)
signals = moving_average_crossover_strategy(stock_data, short_window, long_window)

# Plot the backtesting results
plt.figure(figsize=(14, 7))
plt.plot(stock_data['Close'], label='Close Price')
plt.plot(signals['Short_MA'], label='50-day MA')
plt.plot(signals['Long_MA'], label='200-day MA')

# Plot buy signals
plt.plot(signals.loc[signals['Position'] == 1.0].index, 
         signals['Short_MA'][signals['Position'] == 1.0], 
         '^', markersize=10, color='g', lw=0, label='Buy Signal')

# Plot sell signals
plt.plot(signals.loc[signals['Position'] == -1.0].index, 
         signals['Short_MA'][signals['Position'] == -1.0], 
         'v', markersize=10, color='r', lw=0, label='Sell Signal')

plt.title(f'Moving Average Crossover Strategy for {ticker}')
plt.legend()
plt.show()
