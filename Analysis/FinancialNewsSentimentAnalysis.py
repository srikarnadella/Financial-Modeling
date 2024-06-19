import requests
from bs4 import BeautifulSoup
import pandas as pd
from transformers import pipeline
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize sentiment analysis model
sentiment_model = pipeline('sentiment-analysis')

# Function to scrape news articles from multiple sources
def get_news_articles(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('h2', class_='headline')
    return [article.get_text() for article in articles]

# URLs of financial news websites
urls = [
    'https://www.reuters.com/finance',
    'https://www.cnbc.com/finance/',
    'https://www.bloomberg.com/markets'
]

# Scrape news articles
articles = []
for url in urls:
    articles.extend(get_news_articles(url))

# Perform sentiment analysis using BERT model
sentiments = [sentiment_model(article)[0] for article in articles]

# Create a DataFrame with articles and their sentiment scores
data = {
    'Article': articles,
    'Sentiment': [sentiment['label'] for sentiment in sentiments],
    'Score': [sentiment['score'] for sentiment in sentiments]
}
df = pd.DataFrame(data)

# Visualize sentiment distribution
plt.figure(figsize=(10, 6))
sns.countplot(x='Sentiment', data=df)
plt.title('Sentiment Distribution of Financial News Articles')
plt.show()

# Correlate sentiment scores with stock price movements
stock_data = yf.download('AAPL', start='2022-01-01', end=datetime.today().strftime('%Y-%m-%d'))
stock_data['Sentiment'] = df['Sentiment'].map({'POSITIVE': 1, 'NEGATIVE': -1, 'NEUTRAL': 0}).mean()

# Plot sentiment trends and stock prices
fig, ax1 = plt.subplots(figsize=(12, 8))

ax1.set_xlabel('Date')
ax1.set_ylabel('Stock Price', color='tab:blue')
ax1.plot(stock_data.index, stock_data['Close'], color='tab:blue', label='Stock Price')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx()
ax2.set_ylabel('Sentiment Score', color='tab:red')
ax2.plot(stock_data.index, stock_data['Sentiment'], color='tab:red', label='Sentiment Score', alpha=0.6)
ax2.tick_params(axis='y', labelcolor='tab:red')

fig.tight_layout()
plt.title('Stock Price and Sentiment Score Over Time')
plt.show()
