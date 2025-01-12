#!/usr/bin/env python3
"""
retirement.py: A simple retirement
 calculator that estimates the growth
   of a retirement fund over time.
"""

import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd

# Load environment variables
load_dotenv("retirement.env")

# Constants
CURRENT_PENSION = float(os.getenv("CURRENT_PENSION"))
CONTRIBUTION_GOAL = float(os.getenv("CONTRIBUTION_GOAL"))
RETIREMENT_AGE = int(os.getenv("RETIREMENT_AGE"))
CURRENT_AGE = int(os.getenv("CURRENT_AGE"))
ANNUAL_GROWTH_RATE = float(os.getenv("ANNUAL_GROWTH_RATE")) / 100
ANNUAL_CONTRIBUTION = float(os.getenv("ANNUAL_CONTRIBUTION"))


class RetirementCalculator:
    """A class to calculate
    retirement fund
      growth over time."""

    def __init__(
        self,
        current_pension,
        contribution_goal,
        retirement_age,
        current_age,
        annual_growth_rate,
        annual_contribution,
    ):
        self.current_pension = current_pension
        self.contribution_goal = contribution_goal
        self.retirement_age = retirement_age
        self.current_age = current_age
        self.annual_growth_rate = annual_growth_rate
        self.annual_contribution = annual_contribution
        self.years_to_retirement = retirement_age - current_age
        self.fund_values = []

    def calculate_fund_growth(self):
        """Calculate the growth of the retirement fund over time."""
        fund = self.current_pension
        for year in range(1, self.years_to_retirement + 1):
            fund += self.annual_contribution
            fund += fund * self.annual_growth_rate  # Growth on the total fund
            self.fund_values.append(fund)
        return self.fund_values

    def check_goal_met(self):
        """Check if the contribution goal is met and return the year."""
        for year, value in enumerate(self.fund_values, start=1):
            if value >= self.contribution_goal:
                return year
        return None

    def create_dataframe(self):
        """Create a DataFrame with the fund values and contribution goal."""
        years = list(range(1, self.years_to_retirement + 1))
        return pd.DataFrame(
            {
                "Year": [self.current_age + year for year in years],
                "Fund Value (DKK)": self.fund_values,
                "Contribution Goal (DKK)": [self.contribution_goal]
                * self.years_to_retirement,
            }
        )

    def generate_visuals(self, df):
        """_summary_

        Args:
            df (_type_): _description_
        """
        # Retirement Fund Growth Over Time
        plt.figure(figsize=(10, 6))
        plt.plot(df["Year"], df["Fund Value (DKK)"], label="Fund Value")
        plt.axhline(
            self.contribution_goal,
            color="red",
            linestyle="--",
            label="Contribution Goal",
        )
        plt.title("Retirement Fund Growth Over Time")
        plt.xlabel("Year")
        plt.ylabel("Fund Value (DKK)")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Contributions vs. Goal
        plt.figure(figsize=(10, 6))
        plt.bar(df["Year"], df["Fund Value (DKK)"], label="Fund Value")
        plt.axhline(
            self.contribution_goal,
            color="red",
            linestyle="--",
            label="Contribution Goal",
        )
        plt.title("Contributions vs. Goal")
        plt.xlabel("Year")
        plt.ylabel("Fund Value (DKK)")
        plt.grid(True)
        plt.legend()
        plt.show()

    def print_summary(self, goal_met_year):
        """Print a summary of the retirement fund growth."""
        print(f"Current Pension Value: {self.current_pension:,.2f} DKK")
        print(f"Contribution Goal: {self.contribution_goal:,.2f} DKK")
        print(f"Years to Retirement: {self.years_to_retirement} years")
        print(
            f"""
Goal Met By Year: {goal_met_year + self.current_age if goal_met_year else "Not Achievable"}
"""
        )


def main():
    """Main function to run the retirement calculator."""
    calculator = RetirementCalculator(
        CURRENT_PENSION,
        CONTRIBUTION_GOAL,
        RETIREMENT_AGE,
        CURRENT_AGE,
        ANNUAL_GROWTH_RATE,
        ANNUAL_CONTRIBUTION,
    )
    calculator.calculate_fund_growth()
    goal_met_year = calculator.check_goal_met()
    df = calculator.create_dataframe()
    calculator.generate_visuals(df)
    calculator.print_summary(goal_met_year)


if __name__ == "__main__":
    main()
