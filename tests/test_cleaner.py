"""Tests for DataCleaner."""
import unittest
import pandas as pd
from data.cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):
    """Test cases for DataCleaner class."""

    def setUp(self):
        """Set up test fixtures."""
        self.cleaner = DataCleaner()

    def test_normalize_schema_world_bank_format(self):
        """Test normalization of World Bank wide-format CSV to common schema."""
        # Create sample wide-format DataFrame (World Bank style)
        df = pd.DataFrame({
            "Country Name": ["Aruba", "Afghanistan"],
            "Country Code": ["ABW", "AFG"],
            "Indicator Name": ["Life expectancy", "Life expectancy"],
            "Indicator Code": ["SP.DYN.LE00.IN", "SP.DYN.LE00.IN"],
            "1960": ["64.049", "32.799"],
            "1961": ["64.215", "33.291"],
            "1962": ["", "33.757"]
        })

        # Normalize to common schema
        result = self.cleaner.normalize_schema(df, dataset="world_bank")

        # Assert output columns are correct
        expected_columns = ["country_code", "country_name", "indicator_code", 
                          "indicator_name", "report_date", "value"]
        self.assertListEqual(list(result.columns), expected_columns)

        # Assert number of rows (2 countries × 3 years = 6 rows)
        self.assertEqual(len(result), 6)

        # Assert report_date is in ISO format
        self.assertTrue(result["report_date"].iloc[0].startswith("196"))
        self.assertIn("-01-01", result["report_date"].iloc[0])

        # Assert value column is numeric (empty strings become NaN)
        self.assertTrue(pd.api.types.is_numeric_dtype(result["value"]))

    def test_handle_missing_drop_strategy(self):
        """Test handle_missing with 'drop' strategy removes rows with NaN."""
        df = pd.DataFrame({
            "country_code": ["ABW", "AFG", "ALB"],
            "value": [64.0, None, 58.0]
        })

        result = self.cleaner.handle_missing(df, strategy="drop")

        # Should have 2 rows (AFG row dropped)
        self.assertEqual(len(result), 2)
        self.assertListEqual(list(result["country_code"]), ["ABW", "ALB"])

    def test_handle_missing_fill_zero_strategy(self):
        """Test handle_missing with 'fill_zero' strategy replaces NaN with 0."""
        df = pd.DataFrame({
            "country_code": ["ABW", "AFG", "ALB"],
            "value": [64.0, None, 58.0]
        })

        result = self.cleaner.handle_missing(df, strategy="fill_zero")

        # Should have 3 rows, with AFG value = 0
        self.assertEqual(len(result), 3)
        self.assertEqual(result.loc[1, "value"], 0.0)


if __name__ == '__main__':
    unittest.main()