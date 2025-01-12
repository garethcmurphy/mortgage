#!/usr/bin/env python3
"""
portfolio.py: A simple portfolio tracker that fetches stock prices and
calculates the total value of a stock portfolio over time.
"""

import os

import matplotlib.pyplot as plt
import yfinance as yf
from dotenv import load_dotenv

# Constants
ENV_FILE = "portfolio.env"
API_KEY_NAME = "ALPHA_VANTAGE_API_KEY"
PORTFOLIO = {
    "AAPL": 50,  # Apple
    "TSLA": 20,  # Tesla
    "MSFT": 30,  # Microsoft
    "GOOGL": 10,  # Alphabet
    "AMZN": 5,  # Amazon
}


class PortfolioManager:
    """Initialize the Portfolio with ticker symbols and shares owned."""

    def __init__(self, portfolio):
        """Initialize the Portfolio with ticker symbols and shares owned."""
        self.portfolio = portfolio
        self.prices = None
        self.portfolio_df = None

        # Load API key from .env file
        load_dotenv(ENV_FILE)
        self.api_key = os.getenv(API_KEY_NAME)

    def fetch_stock_data(self):
        """Fetch stock prices for the given tickers using Yahoo Finance."""
        self.prices = yf.download(
            list(self.portfolio.keys()),
            period="1y",
            interval="1d",
        )["Adj Close"]

    def calculate_portfolio_value(self):
        """Calculate the portfolio value over time."""
        self.portfolio_df = self.prices.copy()
        for ticker, shares in self.portfolio.items():
            self.portfolio_df[ticker] = self.portfolio_df[ticker] * shares
        self.portfolio_df["Total Value"] = self.portfolio_df.sum(axis=1)

    def generate_visuals(self):
        """Generate and display visuals for the portfolio."""
        # 1. Portfolio Value Over Time
        plt.figure(figsize=(10, 6))
        plt.plot(
            self.portfolio_df.index,
            self.portfolio_df["Total Value"],
            label="Total Portfolio Value",
        )
        plt.title("Portfolio Value Over Time")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value (USD)")
        plt.grid(True)
        plt.legend()
        plt.show()

        # 2. Individual Stock Performance
        plt.figure(figsize=(10, 6))
        for ticker in self.portfolio.keys():
            plt.plot(self.prices.index, self.prices[ticker], label=ticker)
        plt.title("Individual Stock Performance")
        plt.xlabel("Date")
        plt.ylabel("Stock Price (USD)")
        plt.grid(True)
        plt.legend()
        plt.show()

        # 3. Portfolio Allocation (Pie Chart)
        latest_prices = self.prices.iloc[-1]
        allocation = {
            ticker: shares * latest_prices[ticker]
            for ticker, shares in self.portfolio.items()
        }
        plt.figure(figsize=(8, 8))
        plt.pie(
            allocation.values(),
            labels=allocation.keys(),
            autopct="%1.1f%%",
            startangle=140,
        )
        plt.title("Portfolio Allocation")
        plt.show()

    def display_kpis(self):
        """Display key performance indicators for the portfolio."""
        current_value = self.portfolio_df["Total Value"].iloc[-1]
        initial_value = self.portfolio_df["Total Value"].iloc[0]
        total_gain = current_value - initial_value
        percent_gain = (total_gain / initial_value) * 100

        print(f"Initial Portfolio Value: ${initial_value:,.2f}")
        print(f"Current Portfolio Value: ${current_value:,.2f}")
        print(f"Total Gain: ${total_gain:,.2f} ({percent_gain:.2f}%)")


if __name__ == "__main__":
    portfolio_manager = PortfolioManager(PORTFOLIO)
    portfolio_manager.fetch_stock_data()
    portfolio_manager.calculate_portfolio_value()
    portfolio_manager.generate_visuals()
    portfolio_manager.display_kpis()
