"""Tests for Analyzer."""
import unittest
import pandas as pd
from analysis.analyzer import Analyzer


class TestAnalyzer(unittest.TestCase):
    """Test cases for Analyzer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = Analyzer()

    def test_summary_stats_calculates_correctly(self):
        """Test that summary_stats() calculates mean, min, max, count."""
        df = pd.DataFrame({
            "country_code": ["ABW", "AFG", "ALB"],
            "value": [64.0, 32.0, 58.0]
        })

        result = self.analyzer.summary_stats(df, value_col="value")

        # Check that all keys exist
        self.assertIn("mean", result)
        self.assertIn("min", result)
        self.assertIn("max", result)
        self.assertIn("count", result)

        # Check values are correct
        self.assertAlmostEqual(result["mean"], 51.333, places=2)
        self.assertEqual(result["min"], 32.0)
        self.assertEqual(result["max"], 64.0)
        self.assertEqual(result["count"], 3)


if __name__ == '__main__':
    unittest.main()