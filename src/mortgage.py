#!/usr/bin/env python3
"""
mortgage.py: A simple mortgage
 calculator that generates an
   amortization schedule and visualizations.
"""

import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd

# Load environment variables
load_dotenv("mortgage_info.env")

# Constants
LOAN_AMOUNT = float(os.getenv("LOAN_AMOUNT"))
ANNUAL_INTEREST_RATE = float(os.getenv("ANNUAL_INTEREST_RATE")) / 100
LOAN_TERM_YEARS = int(os.getenv("LOAN_TERM_YEARS"))
LOAN_START_YEAR = int(os.getenv("LOAN_START_YEAR"))


class MortgageCalculator:
    """mortgage.py: A simple
    mortgage calculator that
      generates an amortization schedule and visualizations."""

    def __init__(
        self, loan_amount, annual_interest_rate, loan_term_years, loan_start_year
    ):
        self.loan_amount = loan_amount
        self.annual_interest_rate = annual_interest_rate
        self.loan_term_years = loan_term_years
        self.loan_start_year = loan_start_year
        self.monthly_interest_rate = annual_interest_rate / 12
        self.total_months = loan_term_years * 12
        self.monthly_payment = self.calculate_monthly_payment()
        self.schedule = []

    def calculate_monthly_payment(self):
        """Calculate the monthly mortgage payment."""
        return (
            self.loan_amount
            * (
                self.monthly_interest_rate
                * (1 + self.monthly_interest_rate) ** self.total_months
            )
            / ((1 + self.monthly_interest_rate) ** self.total_months - 1)
        )

    def generate_amortization_schedule(self):
        """Generate the amortization schedule."""
        remaining_balance = self.loan_amount
        for month in range(1, self.total_months + 1):
            interest_payment = remaining_balance * self.monthly_interest_rate
            principal_payment = self.monthly_payment - interest_payment
            remaining_balance -= principal_payment
            self.schedule.append(
                {
                    "Month": month,
                    "Year": self.loan_start_year + (month - 1) // 12,
                    "Monthly Payment": self.monthly_payment,
                    "Principal Payment": principal_payment,
                    "Interest Payment": interest_payment,
                    "Remaining Balance": max(0, remaining_balance),
                }
            )
        return self.schedule

    def create_dataframe(self):
        """Create a DataFrame from the amortization schedule."""
        return pd.DataFrame(self.schedule)

    def generate_yearly_summary(self, df):
        """Generate a yearly summary from the amortization DataFrame."""
        return (
            df.groupby("Year")
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

    def generate_visuals(self, df, yearly_summary):
        """Generate visualizations for the amortization schedule and yearly summary."""
        # Remaining Balance Over Time
        plt.figure(figsize=(10, 6))
        plt.plot(df["Month"], df["Remaining Balance"], label="Remaining Balance")
        plt.title("Loan Balance Over Time")
        plt.xlabel("Months")
        plt.ylabel("Remaining Balance (DKK)")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Principal vs Interest Payments Over Time
        plt.figure(figsize=(10, 6))
        plt.plot(df["Month"], df["Principal Payment"], label="Principal Payment")
        plt.plot(df["Month"], df["Interest Payment"], label="Interest Payment")
        plt.title("Principal vs. Interest Payments Over Time")
        plt.xlabel("Months")
        plt.ylabel("Payment Amount (DKK)")
        plt.grid(True)
        plt.legend()
        plt.show()

        # Total Payments vs Remaining Balance
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

    def print_summary(self, df):
        """Print a summary of the mortgage calculations."""
        total_interest_paid = df["Interest Payment"].sum()
        total_paid = df["Monthly Payment"].sum()
        final_payment_year = self.loan_start_year + self.loan_term_years

        print(f"Monthly Payment: {self.monthly_payment:.2f} DKK")
        print(f"Total Interest Paid: {total_interest_paid:.2f} DKK")
        print(f"Total Amount Paid: {total_paid:.2f} DKK")
        print(f"Loan Fully Paid Off By: {final_payment_year}")


def main():
    """Run the mortgage calculator."""
    calculator = MortgageCalculator(
        LOAN_AMOUNT,
        ANNUAL_INTEREST_RATE,
        LOAN_TERM_YEARS,
        LOAN_START_YEAR,
    )
    schedule = calculator.generate_amortization_schedule()
    df = calculator.create_dataframe()
    yearly_summary = calculator.generate_yearly_summary(df)
    calculator.generate_visuals(df, yearly_summary)
    calculator.print_summary(df)


if __name__ == "__main__":
    main()
