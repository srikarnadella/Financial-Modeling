import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def download_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)['Close']
    return data

def calculate_portfolio_performance(weights, mean_returns, cov_matrix):
    returns = np.sum(mean_returns * weights) * 252
    std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights))) * np.sqrt(252)
    return returns, std_dev

def simulated_annealing(tickers, start_date, end_date, num_iterations, initial_temperature):
    data = download_data(tickers, start_date, end_date)
    mean_returns = data.pct_change().mean()
    cov_matrix = data.pct_change().cov()

    num_assets = len(tickers)
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    
    best_weights = weights
    best_return, best_std_dev = calculate_portfolio_performance(weights, mean_returns, cov_matrix)
    best_sharpe = best_return / best_std_dev
    
    temperature = initial_temperature
    for i in range(num_iterations):
        new_weights = np.random.random(num_assets)
        new_weights /= np.sum(new_weights)
        new_return, new_std_dev = calculate_portfolio_performance(new_weights, mean_returns, cov_matrix)
        new_sharpe = new_return / new_std_dev
        
        if new_sharpe > best_sharpe or np.exp((new_sharpe - best_sharpe) / temperature) > np.random.rand():
            best_weights = new_weights
            best_return = new_return
            best_std_dev = new_std_dev
            best_sharpe = new_sharpe
        
        temperature *= 0.99  # Cool down the temperature

    return best_weights, best_return, best_std_dev, best_sharpe

# Parameters
tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']
start_date = '2021-01-01'
end_date = '2022-12-31'
num_iterations = 1000
initial_temperature = 1000

# Run Simulated Annealing for Portfolio Optimization
best_weights, best_return, best_std_dev, best_sharpe = simulated_annealing(tickers, start_date, end_date, num_iterations, initial_temperature)

print("Optimal Weights:", best_weights)
print("Expected Return:", best_return)
print("Expected Volatility:", best_std_dev)
print("Sharpe Ratio:", best_sharpe)
