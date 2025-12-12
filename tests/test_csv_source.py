"""Tests for CSVDataSource."""
import unittest
import os
from data.csv_source import CSVDataSource


class TestCSVDataSource(unittest.TestCase):
    """Test cases for CSVDataSource class."""

    def setUp(self):
        """Set up test fixtures."""
        self.sample_csv_path = "data/world_bank_sample.csv"
        self.missing_file_path = "data/nonexistent.csv"

    def test_validate_returns_true_for_valid_csv(self):
        """Test that validate() returns True for a valid CSV file."""
        source = CSVDataSource(self.sample_csv_path)
        self.assertTrue(source.validate())

    def test_load_returns_dataframe(self):
        """Test that load() returns a pandas DataFrame."""
        source = CSVDataSource(self.sample_csv_path)
        df = source.load()
        self.assertIsNotNone(df)
        self.assertGreater(len(df.columns), 0)

    def test_load_returns_correct_row_count(self):
        """Test that load() returns correct number of data rows."""
        source = CSVDataSource(self.sample_csv_path)
        df = source.load()
        # Sample CSV has 3 data rows (after skipping 2 metadata rows and 1 header row)
        self.assertEqual(len(df), 4)


if __name__ == '__main__':
    unittest.main()