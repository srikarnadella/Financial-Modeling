import tkinter as tk
from tkinter import messagebox
import requests
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Alpha Vantage API key (replace with your own)
API_KEY = '1HWUXYCQ7PG95ZM9'


def fetch_stock_data(symbol):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        if 'Time Series (Daily)' in data:
            return data['Time Series (Daily)']
        else:
            messagebox.showerror('Error', 'Invalid response from API')
    except requests.exceptions.RequestException as e:
        messagebox.showerror('Error', f'Error fetching data: {e}')


def plot_price_chart(symbol):
    stock_data = fetch_stock_data(symbol)
    if stock_data:
        dates = list(stock_data.keys())[:30]  # Last 30 days
        close_prices = [float(stock_data[date]['4. close']) for date in dates]
        
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(dates, close_prices, marker='o', linestyle='-', color='b', label='Close Price')
        ax.set_title(f'{symbol} Price Chart (Last 30 Days)')
        ax.set_xlabel('Date')
        ax.set_ylabel('Price')
        ax.grid(True)
        ax.legend()
        
        # Rotate x-axis labels and set them at appropriate intervals
        ax.set_xticks(np.arange(0, len(dates), 5))  # Show every 5th date
        ax.set_xticklabels([dates[i] for i in range(0, len(dates), 5)], rotation=45, ha='right')  # Rotate labels
        
        return fig


def display_stock_analysis(symbol):
    stock_data = fetch_stock_data(symbol)
    if stock_data:
        # Fetch latest data point
        latest_date = max(stock_data.keys())
        latest_close_price = float(stock_data[latest_date]['4. close'])
        volume = int(stock_data[latest_date]['5. volume'])
        
        # Calculate technical indicators (mock data for demonstration)
        moving_average_50 = np.mean([float(stock_data[date]['4. close']) for date in list(stock_data.keys())[:50]])
        moving_average_200 = np.mean([float(stock_data[date]['4. close']) for date in list(stock_data.keys())[:200]])
        rsi = 60.0  # Example value
        macd = 0.02  # Example value
        support_level = latest_close_price * 0.9
        resistance_level = latest_close_price * 1.1
        
        # Mock fundamental analysis data (replace with actual calculation)
        eps = 2.5
        pe_ratio = 20.0
        dividend_yield = 1.5
        debt_equity_ratio = 0.5
        roe = 15.0
        revenue = 1000000
        net_income = 150000
        
        # Mock sentiment analysis data (replace with actual analysis)
        news_sentiment = 'Positive'
        social_media_sentiment = 'Neutral'
        analyst_ratings = 'Buy'
        
        # Mock comparative analysis data (replace with actual comparison)
        peer_comparison = 'Outperforming peers'
        industry_comparison = 'Above industry average'
        
        # Mock risk analysis data (replace with actual calculation)
        beta = 1.2
        volatility = 0.15
        var = 0.05
        
        # Update GUI elements with fetched data
        label_price.config(text=f'Price: ${latest_close_price}')
        label_volume.config(text=f'Volume: {volume}')
        label_ma_50.config(text=f'50-Day MA: ${moving_average_50:.2f}')
        label_ma_200.config(text=f'200-Day MA: ${moving_average_200:.2f}')
        label_rsi.config(text=f'RSI: {rsi}')
        label_macd.config(text=f'MACD: {macd}')
        label_support.config(text=f'Support Level: ${support_level:.2f}')
        label_resistance.config(text=f'Resistance Level: ${resistance_level:.2f}')
        label_eps.config(text=f'EPS: ${eps}')
        label_pe_ratio.config(text=f'P/E Ratio: {pe_ratio}')
        label_dividend_yield.config(text=f'Dividend Yield: {dividend_yield}%')
        label_debt_equity.config(text=f'Debt/Equity Ratio: {debt_equity_ratio}')
        label_roe.config(text=f'ROE: {roe}%')
        label_revenue.config(text=f'Revenue: ${revenue}')
        label_net_income.config(text=f'Net Income: ${net_income}')
        label_news_sentiment.config(text=f'News Sentiment: {news_sentiment}')
        label_social_media_sentiment.config(text=f'Social Media Sentiment: {social_media_sentiment}')
        label_analyst_ratings.config(text=f'Analyst Ratings: {analyst_ratings}')
        label_peer_comparison.config(text=f'Peer Comparison: {peer_comparison}')
        label_industry_comparison.config(text=f'Industry Comparison: {industry_comparison}')
        label_beta.config(text=f'Beta: {beta}')
        label_volatility.config(text=f'Volatility: {volatility}')
        label_var.config(text=f'Value at Risk (VaR): {var}')


def get_stock_info():
    symbol = entry_symbol.get().strip().upper()
    if symbol:
        display_stock_analysis(symbol)
        plot = plot_price_chart(symbol)
        if plot:
            canvas = FigureCanvasTkAgg(plot, master=frame_chart)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, sticky=tk.NSEW)
    else:
        messagebox.showwarning('Warning', 'Please enter a stock symbol')


# Create the main window
root = tk.Tk()
root.title('Stock Analysis HUD')

# Create GUI elements
label_symbol = tk.Label(root, text='Enter Stock Symbol:')
label_symbol.grid(row=0, column=0, padx=10, pady=10)

entry_symbol = tk.Entry(root, width=10)
entry_symbol.grid(row=0, column=1, padx=10, pady=10)

button_get_info = tk.Button(root, text='Get Stock Info', command=get_stock_info)
button_get_info.grid(row=0, column=2, padx=10, pady=10)

# Frame for displaying price chart
frame_chart = tk.Frame(root)
frame_chart.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky=tk.W+tk.E)

# Labels for displaying stock analysis data
label_price = tk.Label(root, text='Price: ')
label_price.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

label_volume = tk.Label(root, text='Volume: ')
label_volume.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

label_ma_50 = tk.Label(root, text='50-Day MA: ')
label_ma_50.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

label_ma_200 = tk.Label(root, text='200-Day MA: ')
label_ma_200.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)

label_rsi = tk.Label(root, text='RSI: ')
label_rsi.grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)

label_macd = tk.Label(root, text='MACD: ')
label_macd.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

label_support = tk.Label(root, text='Support Level: ')
label_support.grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)

label_resistance = tk.Label(root, text='Resistance Level: ')
label_resistance.grid(row=5, column=1, padx=10, pady=5, sticky=tk.W)

label_eps = tk.Label(root, text='EPS: ')
label_eps.grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)

label_pe_ratio = tk.Label(root, text='P/E Ratio: ')
label_pe_ratio.grid(row=6, column=1, padx=10, pady=5, sticky=tk.W)

label_dividend_yield = tk.Label(root, text='Dividend Yield: ')
label_dividend_yield.grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)

label_debt_equity = tk.Label(root, text='Debt/Equity Ratio: ')
label_debt_equity.grid(row=7, column=1, padx=10, pady=5, sticky=tk.W)

label_roe = tk.Label(root, text='ROE: ')
label_roe.grid(row=8, column=0, padx=10, pady=5, sticky=tk.W)

label_revenue = tk.Label(root, text='Revenue: ')
label_revenue.grid(row=8, column=1, padx=10, pady=5, sticky=tk.W)

label_net_income = tk.Label(root, text='Net Income: ')
label_net_income.grid(row=9, column=0, padx=10, pady=5, sticky=tk.W)

label_news_sentiment = tk.Label(root, text='News Sentiment: ')
label_news_sentiment.grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)

label_social_media_sentiment = tk.Label(root, text='Social Media Sentiment: ')
label_social_media_sentiment.grid(row=10, column=1, padx=10, pady = 5, sticky=tk.W)

label_analyst_ratings = tk.Label(root, text='Analyst Ratings: ')
label_analyst_ratings.grid(row=11, column=0, padx=10, pady = 5, sticky=tk.W)

label_peer_comparison = tk.Label(root, text='Peer Comparison: ')
label_peer_comparison.grid(row=11, column=1, padx=10, pady = 5, sticky=tk.W)

label_industry_comparison = tk.Label(root, text='Industry Comparison: ')
label_industry_comparison.grid(row=12, column=0, padx=10, pady = 5, sticky=tk.W)

label_beta = tk.Label(root, text='Beta: ')
label_beta.grid(row=12, column=1, padx=10, pady = 5, sticky=tk.W)

label_volatility = tk.Label(root, text='Votality: ')
label_volatility.grid(row=13, column=0, padx=10, pady = 5, sticky=tk.W)

label_var = tk.Label(root, text='Variance: ')
label_var.grid(row=13, column=1, padx=10, pady = 5, sticky=tk.W)
root.mainloop()