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

# Fetch data from .env file
current_pension = float(os.getenv("CURRENT_PENSION"))
contribution_goal = float(os.getenv("CONTRIBUTION_GOAL"))
retirement_age = int(os.getenv("RETIREMENT_AGE"))
current_age = int(os.getenv("CURRENT_AGE"))
annual_growth_rate = float(os.getenv("ANNUAL_GROWTH_RATE")) / 100
annual_contribution = float(os.getenv("ANNUAL_CONTRIBUTION"))

# Calculations
years_to_retirement = retirement_age - current_age
remaining_contributions = contribution_goal - current_pension
total_years = years_to_retirement
years = list(range(1, total_years + 1))

# Simulate fund growth with contributions
fund_values = []
fund = current_pension
for year in years:
    fund += annual_contribution
    fund += fund * annual_growth_rate  # Growth on the total fund
    fund_values.append(fund)

# Check if the goal is met
goal_met_year = next(
    (
        year
        for year, value in zip(
            years,
            fund_values,
        )
        if value >= contribution_goal
    ),
    None,
)

# Create DataFrame for visualization
df = pd.DataFrame(
    {
        "Year": [current_age + year for year in years],
        "Fund Value (DKK)": fund_values,
        "Contribution Goal (DKK)": [contribution_goal] * total_years,
    }
)

# Generate Visuals

# 1. Retirement Fund Growth Over Time
plt.figure(figsize=(10, 6))
plt.plot(df["Year"], df["Fund Value (DKK)"], label="Fund Value")
plt.axhline(contribution_goal, color="red", linestyle="--", label="Contribution Goal")
plt.title("Retirement Fund Growth Over Time")
plt.xlabel("Year")
plt.ylabel("Fund Value (DKK)")
plt.grid(True)
plt.legend()
plt.show()

# 2. Contributions vs. Goal
plt.figure(figsize=(10, 6))
plt.bar(df["Year"], df["Fund Value (DKK)"], label="Fund Value")
plt.axhline(contribution_goal, color="red", linestyle="--", label="Contribution Goal")
plt.title("Contributions vs. Goal")
plt.xlabel("Year")
plt.ylabel("Fund Value (DKK)")
plt.grid(True)
plt.legend()
plt.show()

# Summary Metrics
print(f"Current Pension Value: {current_pension:,.2f} DKK")
print(f"Contribution Goal: {contribution_goal:,.2f} DKK")
print(f"Years to Retirement: {years_to_retirement} years")
print(
    f"Goal Met By Year: {goal_met_year + current_age if goal_met_year else 'Not Achievable'}"
)
