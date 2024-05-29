import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Define the date range
start = "2020-01-01"
end = "2020-04-17"

google = yf.download("GOOGL", start=start, end=end)
if google.empty:
    raise ValueError("No data fetched, the DataFrame is empty.")

print(google.head())  # Display the first few rows to ensure data is retrieved correctly
print(google.dtypes)  # Display data types of the DataFrame

# Convert data to numeric if necessary
google = google.apply(pd.to_numeric, errors='coerce')
print(google.dtypes)  # Check data types after conversion

# Plot the data if it was successfully retrieved and converted
if not google.empty:
    google['Open'].plot(label='Google Open Price', title='Google Stock Price', figsize = (15,7))
    google['Close'].plot(label='Google Close Price', title='Google Stock Price')
    plt.title("Google Stock Prices")
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.show()

    google['Volume'].plot(figsize = (17,5))
    plt.title("Google Volume")
    plt.show()

