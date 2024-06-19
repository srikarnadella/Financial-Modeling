import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

def download_stock_data(ticker, start_date, end_date):
    """
    Downloads historical stock data from Yahoo Finance.
    
    Parameters:
    ticker (str): Stock ticker symbol
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    
    Returns:
    pd.DataFrame: DataFrame containing stock data
    """
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data

def calculate_moving_averages(stock_data, short_window=50, long_window=150):
    """
    Calculates short and long term moving averages.
    
    Parameters:
    stock_data (pd.DataFrame): DataFrame containing stock data
    short_window (int): Window size for short term moving average
    long_window (int): Window size for long term moving average
    
    Returns:
    pd.DataFrame: DataFrame with moving averages added
    """
    stock_data['SMA50'] = stock_data['Close'].rolling(window=short_window).mean()
    stock_data['SMA150'] = stock_data['Close'].rolling(window=long_window).mean()
    return stock_data

def calculate_relative_strength(stock_data, benchmark_data):
    """
    Calculates the relative strength of a stock compared to a benchmark.
    
    Parameters:
    stock_data (pd.DataFrame): DataFrame containing stock data
    benchmark_data (pd.DataFrame): DataFrame containing benchmark data
    
    Returns:
    pd.Series: Series containing the relative strength values
    """
    relative_strength = stock_data['Close'] / benchmark_data['Close']
    return relative_strength

def plot_stock_analysis(stock_data, ticker):
    """
    Plots stock price with moving averages and relative strength.
    
    Parameters:
    stock_data (pd.DataFrame): DataFrame containing stock data
    ticker (str): Stock ticker symbol
    """
    plt.figure(figsize=(14, 7))
    
    # Plot stock price and moving averages
    plt.subplot(2, 1, 1)
    plt.plot(stock_data['Close'], label='Close Price')
    plt.plot(stock_data['SMA50'], label='50-day SMA')
    plt.plot(stock_data['SMA150'], label='150-day SMA')
    plt.title(f'{ticker} Stock Price and Moving Averages')
    plt.legend()
    
    # Plot relative strength
    plt.subplot(2, 1, 2)
    plt.plot(stock_data['RelativeStrength'], label='Relative Strength')
    plt.title(f'{ticker} Relative Strength')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def mark_minervini_analysis(ticker, benchmark_ticker, start_date, end_date):
    """
    Performs Mark Minervini's stock analysis.
    
    Parameters:
    ticker (str): Stock ticker symbol
    benchmark_ticker (str): Benchmark ticker symbol (e.g., SPY for S&P 500)
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    """
    # Download stock and benchmark data
    stock_data = download_stock_data(ticker, start_date, end_date)
    benchmark_data = download_stock_data(benchmark_ticker, start_date, end_date)
    
    # Calculate moving averages
    stock_data = calculate_moving_averages(stock_data)
    
    # Calculate relative strength
    stock_data['RelativeStrength'] = calculate_relative_strength(stock_data, benchmark_data)
    
    # Plot the analysis
    plot_stock_analysis(stock_data, ticker)

# Parameters
ticker = 'AAPL'  # Example stock ticker
benchmark_ticker = 'SPY'  # S&P 500 as benchmark
start_date = '2021-01-01'  # Start date for analysis
end_date = '2022-12-31'  # End date for analysis

# Perform Mark Minervini's stock analysis
mark_minervini_analysis(ticker, benchmark_ticker, start_date, end_date)
