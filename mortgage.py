#!/usr/bin/env python3
"""
mortgage.py: A simple mortgage calculator that generates an amortization
schedule and visualizations.
"""

import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv("mortgage_info.env")

# Fetch data from the .env file
loan_amount = float(os.getenv("LOAN_AMOUNT"))
annual_interest_rate = float(os.getenv("ANNUAL_INTEREST_RATE")) / 100
loan_term_years = int(os.getenv("LOAN_TERM_YEARS"))
loan_start_year = int(os.getenv("LOAN_START_YEAR"))

# Calculate monthly interest rate and total months
monthly_interest_rate = annual_interest_rate / 12
total_months = loan_term_years * 12

# Calculate monthly payment
monthly_payment = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months)
    / ((1 + monthly_interest_rate) ** total_months - 1)
)

# Generate amortization schedule
schedule = []
remaining_balance = loan_amount
for month in range(1, total_months + 1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment - interest_payment
    remaining_balance -= principal_payment
    schedule.append(
        {
            "Month": month,
            "Year": loan_start_year + (month - 1) // 12,
            "Monthly Payment": monthly_payment,
            "Principal Payment": principal_payment,
            "Interest Payment": interest_payment,
            "Remaining Balance": max(0, remaining_balance),
        }
    )

# Create DataFrame
amortization_df = pd.DataFrame(schedule)

# Yearly summary
yearly_summary = (
    amortization_df.groupby("Year")
    .agg(
        {
            "Monthly Payment": "sum",
            "Principal Payment": "sum",
            "Interest Payment": "sum",
            "Remaining Balance": "last",
        }
    )
    .reset_index()
)

# Generate visuals

# 1. Remaining Balance Over Time
plt.figure(figsize=(10, 6))
plt.plot(
    amortization_df["Month"],
    amortization_df["Remaining Balance"],
    label="Remaining Balance",
)
plt.title("Loan Balance Over Time")
plt.xlabel("Months")
plt.ylabel("Remaining Balance (DKK)")
plt.grid(True)
plt.legend()
plt.show()

# 2. Principal vs Interest Payments Over Time
plt.figure(figsize=(10, 6))
plt.plot(
    amortization_df["Month"],
    amortization_df["Principal Payment"],
    label="Principal Payment",
)
plt.plot(
    amortization_df["Month"],
    amortization_df["Interest Payment"],
    label="Interest Payment",
)
plt.title("Principal vs. Interest Payments Over Time")
plt.xlabel("Months")
plt.ylabel("Payment Amount (DKK)")
plt.grid(True)
plt.legend()
plt.show()

# 3. Total Payments vs Remaining Balance
plt.figure(figsize=(10, 6))
plt.plot(
    yearly_summary["Year"],
    yearly_summary["Remaining Balance"],
    label="Remaining Balance",
)
plt.bar(
    yearly_summary["Year"],
    yearly_summary["Principal Payment"],
    alpha=0.6,
    label="Principal Paid",
)
plt.bar(
    yearly_summary["Year"],
    yearly_summary["Interest Payment"],
    bottom=yearly_summary["Principal Payment"],
    alpha=0.6,
    label="Interest Paid",
)
plt.title("Yearly Payments and Remaining Balance")
plt.xlabel("Year")
plt.ylabel("Amount (DKK)")
plt.grid(True)
plt.legend()
plt.show()

# Display summary
total_interest_paid = amortization_df["Interest Payment"].sum()
total_paid = amortization_df["Monthly Payment"].sum()
final_payment_year = loan_start_year + loan_term_years

print(f"Monthly Payment: {monthly_payment:.2f} DKK")
print(f"Total Interest Paid: {total_interest_paid:.2f} DKK")
print(f"Total Amount Paid: {total_paid:.2f} DKK")
print(f"Loan Fully Paid Off By: {final_payment_year}")
