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

    def test_trend_over_time_groups_by_date(self):
        """Test that trend_over_time() groups and sorts by date."""
        df = pd.DataFrame({
            "report_date": ["2020-01-01", "2021-01-01", "2020-01-01", "2021-01-01"],
            "value": [64.0, 65.0, 32.0, 33.0]
        })

        result = self.analyzer.trend_over_time(df, date_col="report_date", value_col="value")

        # Should have 2 rows (one per unique date)
        self.assertEqual(len(result), 2)

        # Should be sorted by date
        self.assertEqual(result.iloc[0]["report_date"], "2020-01-01")
        self.assertEqual(result.iloc[1]["report_date"], "2021-01-01")

        # Should have mean values
        self.assertAlmostEqual(result.iloc[0]["value"], 48.0)  # mean of 64.0 and 32.0
        self.assertAlmostEqual(result.iloc[1]["value"], 49.0)  # mean of 65.0 and 33.0

    def test_group_aggregate_groups_by_country(self):
        """Test that group_aggregate() groups by specified columns."""
        df = pd.DataFrame({
            "country_code": ["ABW", "ABW", "AFG", "AFG"],
            "value": [64.0, 65.0, 32.0, 33.0]
        })

        result = self.analyzer.group_aggregate(df, group_cols=["country_code"], agg_col="value")

        # Should have 2 rows (one per country)
        self.assertEqual(len(result), 2)

        # Check aggregated values (mean)
        abw_row = result[result["country_code"] == "ABW"]
        afg_row = result[result["country_code"] == "AFG"]
        
        self.assertAlmostEqual(abw_row["value"].iloc[0], 64.5)  # mean of 64.0 and 65.0
        self.assertAlmostEqual(afg_row["value"].iloc[0], 32.5)  # mean of 32.0 and 33.0


if __name__ == '__main__':
    unittest.main()