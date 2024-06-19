import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

# Black-Scholes formula for calculating option prices and Greeks
def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Calculates the Black-Scholes price and Greeks for a European option.

    Parameters:
    S : float : Current stock price
    K : float : Strike price
    T : float : Time to maturity (in years)
    r : float : Risk-free interest rate
    sigma : float : Volatility of the stock
    option_type : str : 'call' or 'put'

    Returns:
    price, delta, gamma, theta, vega, rho : tuple : Option price and Greeks
    """
    # Calculate d1 and d2 for the Black-Scholes formula
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == 'call':
        # Call option price
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        # Call option Greeks
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2)
        vega = S * norm.pdf(d1) * np.sqrt(T)
        rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == 'put':
        # Put option price
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        # Put option Greeks
        delta = norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
        theta = -(S * norm.pdf(d1) * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2)
        vega = S * norm.pdf(d1) * np.sqrt(T)
        rho = -K * T * np.exp(-r * T) * norm.cdf(-d2)
    return price, delta, gamma, theta, vega, rho

# Parameters for the Black-Scholes model
S = 100  # Current stock price
K = 100  # Strike price
T = 1    # Time to maturity in years
r = 0.05 # Risk-free interest rate
sigma = 0.2 # Volatility

# Calculate option prices and Greeks for call options
call_price, call_delta, call_gamma, call_theta, call_vega, call_rho = black_scholes(S, K, T, r, sigma, option_type='call')
# Calculate option prices and Greeks for put options
put_price, put_delta, put_gamma, put_theta, put_vega, put_rho = black_scholes(S, K, T, r, sigma, option_type='put')

# Print the results for call options
print(f"Call Option Price: {call_price:.2f}")
print(f"Call Option Delta: {call_delta:.2f}")
print(f"Call Option Gamma: {call_gamma:.2f}")
print(f"Call Option Theta: {call_theta:.2f}")
print(f"Call Option Vega: {call_vega:.2f}")
print(f"Call Option Rho: {call_rho:.2f}")

# Print the results for put options
print(f"Put Option Price: {put_price:.2f}")
print(f"Put Option Delta: {put_delta:.2f}")
print(f"Put Option Gamma: {put_gamma:.2f}")
print(f"Put Option Theta: {put_theta:.2f}")
print(f"Put Option Vega: {put_vega:.2f}")
print(f"Put Option Rho: {put_rho:.2f}")

# Sensitivity analysis: Option price as a function of stock price
S_range = np.linspace(50, 150, 100)  # Range of stock prices from 50 to 150
call_prices = [black_scholes(S, K, T, r, sigma, option_type='call')[0] for S in S_range]
put_prices = [black_scholes(S, K, T, r, sigma, option_type='put')[0] for S in S_range]

# Plot option prices as a function of stock price
plt.figure(figsize=(14, 7))

# Plot Call Option Prices
plt.subplot(1, 2, 1)
plt.plot(S_range, call_prices, label='Call Option Price')
plt.xlabel('Stock Price')
plt.ylabel('Option Price')
plt.title('Call Option Price vs Stock Price')
plt.legend()

# Plot Put Option Prices
plt.subplot(1, 2, 2)
plt.plot(S_range, put_prices, label='Put Option Price')
plt.xlabel('Stock Price')
plt.ylabel('Option Price')
plt.title('Put Option Price vs Stock Price')
plt.legend()

plt.tight_layout()
plt.show()

# Sensitivity analysis: Greeks as functions of volatility
vol_range = np.linspace(0.01, 1.0, 100)  # Range of volatilities from 0.01 to 1.0
call_deltas = [black_scholes(S, K, T, r, sigma, option_type='call')[1] for sigma in vol_range]
call_gammas = [black_scholes(S, K, T, r, sigma, option_type='call')[2] for sigma in vol_range]
call_vegas = [black_scholes(S, K, T, r, sigma, option_type='call')[4] for sigma in vol_range]

# Plot Greeks as functions of volatility
plt.figure(figsize=(14, 7))

# Plot Call Option Delta
plt.subplot(1, 3, 1)
plt.plot(vol_range, call_deltas, label='Call Delta')
plt.xlabel('Volatility')
plt.ylabel('Delta')
plt.title('Call Delta vs Volatility')
plt.legend()

# Plot Call Option Gamma
plt.subplot(1, 3, 2)
plt.plot(vol_range, call_gammas, label='Call Gamma')
plt.xlabel('Volatility')
plt.ylabel('Gamma')
plt.title('Call Gamma vs Volatility')
plt.legend()

# Plot Call Option Vega
plt.subplot(1, 3, 3)
plt.plot(vol_range, call_vegas, label='Call Vega')
plt.xlabel('Volatility')
plt.ylabel('Vega')
plt.title('Call Vega vs Volatility')
plt.legend()

plt.tight_layout()
plt.show()
