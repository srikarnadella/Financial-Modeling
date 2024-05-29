import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Define the date range
start = "2012-01-01"
end = "2020-04-17"


#Bring in each dataframe
tesla = yf.download("TSLA", start=start, end=end)
if tesla.empty:
    raise ValueError("No data fetched, the DataFrame is empty.")
tesla = tesla.apply(pd.to_numeric, errors='coerce')

ford = yf.download("F", start=start, end=end)
if ford.empty:
    raise ValueError("No data fetched, the DataFrame is empty.")
ford = ford.apply(pd.to_numeric, errors='coerce')

gm = yf.download("GM", start=start, end=end)
if gm.empty:
    raise ValueError("No data fetched, the DataFrame is empty.")
gm = gm.apply(pd.to_numeric, errors='coerce')


tesla['Open'].plot(label='Tesla Open Price', title='Tesla Stock Price', figsize = (15,7))
gm['Open'].plot(label='GM Open Price')
ford['Open'].plot(label='Ford Open Price')
plt.title("Stock Prices")
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()


tesla['Volume'].plot(label='Tesla Volume', figsize = (15,7))
gm['Volume'].plot(label='GM Volume')
ford['Volume'].plot(label='Ford Volume')
plt.title("Trading Volume")
plt.xlabel('Date')
plt.ylabel('Volume')
plt.legend()
plt.show()


tesla['Total Traded'] = tesla['Open'] * tesla['Volume']
ford['Total Traded'] = ford['Open'] * ford['Volume']
gm['Total Traded'] = gm['Open'] * gm['Volume']

