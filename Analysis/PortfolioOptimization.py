import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from scipy.optimize import minimize
import seaborn as sns
from datetime import datetime

# Fetch historical price data for a diverse set of assets
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TLT', 'IEF']  # Including bonds
data = yf.download(tickers, start='2018-01-01', end=datetime.today().strftime('%Y-%m-%d'))['Adj Close']

# Calculate daily returns
returns = data.pct_change().dropna()

# Calculate mean returns and covariance matrix
mean_returns = returns.mean()
cov_matrix = returns.cov()

# Define the portfolio optimization function considering transaction costs
def portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate=0.01):
    returns = np.sum(mean_returns * weights)
    volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (returns - risk_free_rate) / volatility
    return returns, volatility, sharpe_ratio

# Constraints and bounds
constraints = ({'type': 'eq', 'fun': lambda x: np.sum(x) - 1})
bounds = tuple((0, 0.3) for _ in range(len(tickers)))  # max 30% per asset

# Objective function to minimize (negative Sharpe ratio)
def min_func_sharpe(weights, mean_returns, cov_matrix, risk_free_rate):
    return -portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)[2]

# Initial guess
initial_guess = len(tickers) * [1. / len(tickers)]

# Optimize the portfolio
opt_result = minimize(min_func_sharpe, initial_guess, args=(mean_returns, cov_matrix, 0.01),
                      method='SLSQP', bounds=bounds, constraints=constraints)

# Optimal weights
opt_weights = opt_result.x

# Monte Carlo simulation
def monte_carlo_simulation(mean_returns, cov_matrix, num_portfolios=10000, risk_free_rate=0.01):
    results = np.zeros((4, num_portfolios))
    weights_record = []
    for i in range(num_portfolios):
        weights = np.random.random(len(tickers))
        weights /= np.sum(weights)
        weights_record.append(weights)
        returns, volatility, sharpe_ratio = portfolio_performance(weights, mean_returns, cov_matrix, risk_free_rate)
        results[0,i] = returns
        results[1,i] = volatility
        results[2,i] = sharpe_ratio
        results[3,i] = (returns - risk_free_rate) / volatility  # Sharpe ratio
    return results, weights_record

results, weights_record = monte_carlo_simulation(mean_returns, cov_matrix)

# Plot efficient frontier
plt.figure(figsize=(12, 8))
plt.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis', marker='o')
plt.colorbar(label='Sharpe ratio')
plt.scatter(portfolio_performance(opt_weights, mean_returns, cov_matrix)[1],
            portfolio_performance(opt_weights, mean_returns, cov_matrix)[0], marker='*', color='r', s=500, label='Optimal Portfolio')
plt.title('Efficient Frontier with Monte Carlo Simulation')
plt.xlabel('Volatility')
plt.ylabel('Return')
plt.legend()
plt.show()

# Interactive plot using seaborn
sns.pairplot(pd.DataFrame(results.T, columns=['Return', 'Volatility', 'Sharpe Ratio', 'Risk-Adjusted Return']),
             diag_kind='kde', kind='reg')
plt.show()
