import numpy as np
import pandas as pd
from pandas_datareader import data as web
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import norm
import yfinance as yf

#https://www.investopedia.com/terms/m/montecarlosimulation.asp
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#Read the concepts in this website
'''
The purpose of the monte carlo simulation is to model a range of possible outcomes. 
Typically it is done using lots of variables, here we are only using the Adj Close.
Regarding stock values it also shows risk in regards to potential gain to lose.
'''
start = "2007-01-01"

def simulate(ticker, name):

    data = yf.download(ticker, start=start)
    if data.empty:
        raise ValueError("No data fetched, the DataFrame is empty.")
    
    data = data['Adj Close']

    data = data.apply(pd.to_numeric, errors='coerce')

    log_returns = np.log(1 + data.pct_change())

    mean = log_returns.mean()

    var = log_returns.var()

    #change of average value of the stock price over time, key to a monte carlo simulation
    drift = mean - (0.5 * var)

    stdev = log_returns.std()

    #How far in the future do we want to go in days
    t_intervals = 365

    #How many simulations:
    iterations = 10

    daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(t_intervals, iterations)))

    S0 = data.iloc[-1]

    price_list = np.zeros_like(daily_returns)
    price_list[0] = S0

    for i in range(1, t_intervals):
       price_list[i] = price_list[i-1] * daily_returns[i]
    
    current_price = data.iloc[-1] 


    plt.figure(figsize=(16,8))
    plt.title(f"Monte Carlo Simulation for: {ticker} over {t_intervals} days")
    plt.xlabel("TIme in days")
    plt.ylabel("Price ($)")
    plt.plot(price_list)
    plt.scatter(0, current_price , color='black', label='Point', s = 100)
    plt.text(0,current_price , f'(Current Price)', fontsize=12, ha='right')

    plt.show()

simulate("SPY", "S&P 500")  


