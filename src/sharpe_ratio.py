#!/usr/bin/env python3
"""
risk-adjusted return calculator
"""

import numpy as np


class RiskAdjustedReturnCalculator:
    """risk-adjusted return calculator"""

    def __init__(self, returns, risk_free_rate=0):
        """
        Initialize the calculator with returns and an optional risk-free rate.

        :param returns: Array-like, returns of the investment
        :param risk_free_rate: Float, risk-free rate, default is 0
        """
        self.returns = np.array(returns)
        self.risk_free_rate = risk_free_rate

    def sharpe_ratio(self):
        """
        Calculate the Sharpe Ratio.

        :return: Float, Sharpe Ratio
        """
        excess_returns = self.returns - self.risk_free_rate
        mean_excess_return = np.mean(excess_returns)
        std_excess_return = np.std(excess_returns)
        return mean_excess_return / std_excess_return

    def sortino_ratio(self):
        """
        Calculate the Sortino Ratio.

        :return: Float, Sortino Ratio
        """
        excess_returns = self.returns - self.risk_free_rate
        mean_excess_return = np.mean(excess_returns)
        downside_deviation = np.std(excess_returns[excess_returns < 0])
        return mean_excess_return / downside_deviation


def main():
    """main function"""
    # Example usage:
    returns = [0.01, 0.02, 0.03, -0.01, 0.04, -0.02]
    risk_free_rate = 0.01

    calculator = RiskAdjustedReturnCalculator(returns, risk_free_rate)
    sharpe = calculator.sharpe_ratio()
    sortino = calculator.sortino_ratio()

    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Sortino Ratio: {sortino:.2f}")


if __name__ == "__main__":
    main()
