"""unittests for the mortgage module."""
import unittest

from mortgage import MortgageCalculator


class TestMortgageCalculator(unittest.TestCase):
    """unittests for the mortgage module."""
    def setUp(self):
        self.loan_amount = 300000
        self.annual_interest_rate = 0.05
        self.loan_term_years = 30
        self.loan_start_year = 2023
        self.calculator = MortgageCalculator(
            self.loan_amount,
            self.annual_interest_rate,
            self.loan_term_years,
            self.loan_start_year,
        )

    def test_monthly_payment(self):
        """Test the calculation of the monthly payment."""
        expected_payment = (
            1610.46  # This value should be calculated based on the formula
        )
        self.assertAlmostEqual(
            self.calculator.calculate_monthly_payment(), expected_payment, places=2
        )

    def test_amortization_schedule(self):
        """Test the amortization schedule generation."""
        schedule = self.calculator.generate_amortization_schedule()
        self.assertEqual(len(schedule), self.loan_term_years * 12)
        self.assertAlmostEqual(schedule[-1]["Remaining Balance"], 0, places=2)

    def test_dataframe_creation(self):
        """test the creation of a DataFrame from the amortization schedule."""
        schedule = self.calculator.generate_amortization_schedule()
        df = self.calculator.create_dataframe()
        self.assertEqual(len(df), len(schedule))
        self.assertListEqual(
            list(df.columns),
            [
                "Month",
                "Year",
                "Monthly Payment",
                "Principal Payment",
                "Interest Payment",
                "Remaining Balance",
            ],
        )

    def test_yearly_summary(self):
        """test the generation of a yearly summary from the amortization DataFrame."""
        _ = self.calculator.generate_amortization_schedule()
        df = self.calculator.create_dataframe()
        yearly_summary = self.calculator.generate_yearly_summary(df)
        self.assertEqual(len(yearly_summary), self.loan_term_years)
        self.assertListEqual(
            list(yearly_summary.columns),
            [
                "Year",
                "Monthly Payment",
                "Principal Payment",
                "Interest Payment",
                "Remaining Balance",
            ],
        )


if __name__ == "__main__":
    unittest.main()
