#!/usr/bin/env python3
"""
portfolio.py: A simple portfolio tracker that fetches stock prices and
calculates the total value of a stock portfolio over time.
"""

import os
import yfinance as yf
import matplotlib.pyplot as plt
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv("portfolio.env")
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# Portfolio details (ticker symbols and shares owned)
portfolio = {
    "AAPL": 50,   # Apple
    "TSLA": 20,   # Tesla
    "MSFT": 30,   # Microsoft
    "GOOGL": 10,  # Alphabet
    "AMZN": 5     # Amazon
}

def fetch_stock_data(tickers):
    """Fetch stock prices for the given tickers using Yahoo Finance."""
    data = yf.download(list(tickers.keys()), period="1y", interval="1d")
    return data["Adj Close"]

def calculate_portfolio_value(prices, portfolio):
    """Calculate the portfolio value over time."""
    portfolio_df = prices.copy()
    for ticker, shares in portfolio.items():
        portfolio_df[ticker] = portfolio_df[ticker] * shares
    portfolio_df["Total Value"] = portfolio_df.sum(axis=1)
    return portfolio_df

# Fetch stock prices
prices = fetch_stock_data(portfolio)

# Calculate portfolio value
portfolio_df = calculate_portfolio_value(prices, portfolio)

# KPIs
current_value = portfolio_df["Total Value"].iloc[-1]
initial_value = portfolio_df["Total Value"].iloc[0]
total_gain = current_value - initial_value
percent_gain = (total_gain / initial_value) * 100

# Generate Visuals

# 1. Portfolio Value Over Time
plt.figure(figsize=(10, 6))
plt.plot(portfolio_df.index, portfolio_df["Total Value"], label="Total Portfolio Value")
plt.title("Portfolio Value Over Time")
plt.xlabel("Date")
plt.ylabel("Portfolio Value (USD)")
plt.grid(True)
plt.legend()
plt.show()

# 2. Individual Stock Performance
plt.figure(figsize=(10, 6))
for ticker in portfolio.keys():
    plt.plot(prices.index, prices[ticker], label=ticker)
plt.title("Individual Stock Performance")
plt.xlabel("Date")
plt.ylabel("Stock Price (USD)")
plt.grid(True)
plt.legend()
plt.show()

# 3. Portfolio Allocation (Pie Chart)
latest_prices = prices.iloc[-1]
allocation = {ticker: shares * latest_prices[ticker] for ticker, shares in portfolio.items()}
plt.figure(figsize=(8, 8))
plt.pie(allocation.values(), labels=allocation.keys(), autopct='%1.1f%%', startangle=140)
plt.title("Portfolio Allocation")
plt.show()

# Display KPIs
print(f"Initial Portfolio Value: ${initial_value:,.2f}")
print(f"Current Portfolio Value: ${current_value:,.2f}")
print(f"Total Gain: ${total_gain:,.2f} ({percent_gain:.2f}%)")