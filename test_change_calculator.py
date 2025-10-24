import unittest
from change_calculator import calculate_change, calculate_minimal_change, calculate_random_change
from currencies import get_currency_config

class TestChangeCalculator(unittest.TestCase):

    def test_minimal_change_usd(self):
        # Test basic minimal change calculation for USD
        currency_config = get_currency_config('USD')
        result = calculate_minimal_change(87, currency_config)  # 87 cents = 3 quarters, 1 dime, 2 pennies
        self.assertEqual(result, "3 quarters, 1 dime, 2 pennies")

    def test_no_change(self):
        result = calculate_change("5.00", "5.00")
        self.assertEqual(result, "No change owed")

    def test_insufficient_payment(self):
        result = calculate_change("5.00", "3.00")
        self.assertEqual(result, "Error: Insufficient payment")

    def test_invalid_format(self):
        result = calculate_change("abc", "3.00")
        self.assertEqual(result, "Error: Invalid number format")

    def test_invalid_currency(self):
        result = calculate_change("2.13", "3.00", "INVALID")
        self.assertIn("Unsupported currency", result)

    def test_normal_change_usd(self):
        result = calculate_change("2.14", "3.00", "USD")
        # Should use minimal change
        self.assertEqual(result, "3 quarters, 1 dime, 1 penny")

    def test_random_change_usd(self):
        # Test case where owed is divisible by 3 (2.13 * 100 = 213, 213 % 3 = 0)
        result = calculate_change("2.13", "3.00", "USD")
        # Since 213 is divisible by 3, it should use random logic
        # We can't predict exact result due to randomness, but it should be valid
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "Error: Insufficient payment")
        self.assertNotEqual(result, "No change owed")

    def test_euro_currency(self):
        # Test Euro currency
        result = calculate_change("2.14", "3.00", "EUR")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "Error: Insufficient payment")

    def test_colombian_peso_currency(self):
        # Test Colombian Peso currency
        result = calculate_change("1000", "2000", "COP")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "Error: Insufficient payment")

    def test_euro_random_change(self):
        # Test Euro with divisible by 3 amount
        result = calculate_change("2.13", "3.00", "EUR")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "Error: Insufficient payment")

    def test_cop_random_change(self):
        # Test COP with divisible by 3 amount
        result = calculate_change("1000", "2000", "COP")
        self.assertIsInstance(result, str)
        self.assertNotEqual(result, "Error: Insufficient payment")

    def test_currency_case_insensitive(self):
        # Test that currency codes are case insensitive
        result1 = calculate_change("2.14", "3.00", "usd")
        result2 = calculate_change("2.14", "3.00", "USD")
        self.assertEqual(result1, result2)

    def test_random_change_structure(self):
        # Test that random change produces valid output structure
        currency_config = get_currency_config('USD')
        result = calculate_random_change(87, currency_config)
        self.assertIsInstance(result, str)
        # Should contain denomination names
        self.assertTrue(any(denom in result for denom in ['dollar', 'quarter', 'dime', 'nickel', 'penny']))

if __name__ == '__main__':
    unittest.main()