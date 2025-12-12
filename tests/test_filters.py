"""Tests for FilterCriteria."""
import unittest
from analysis.filters import FilterCriteria


class TestFilterCriteria(unittest.TestCase):
    """Test cases for FilterCriteria class."""

    def test_to_sql_where_with_all_filters(self):
        """Test to_sql_where() with country, date_from, and date_to."""
        filters = FilterCriteria(
            country="ABW",
            date_from="2020-01-01",
            date_to="2024-12-31"
        )

        where_clause, params = filters.to_sql_where()

        # Should contain all three conditions
        self.assertIn("country_code", where_clause)
        self.assertIn("report_date", where_clause)
        self.assertIn(">=", where_clause)
        self.assertIn("<=", where_clause)

        # Params should have 3 values
        self.assertEqual(len(params), 3)
        self.assertIn("ABW", params)
        self.assertIn("2020-01-01", params)
        self.assertIn("2024-12-31", params)

    def test_to_sql_where_with_country_only(self):
        """Test to_sql_where() with only country filter."""
        filters = FilterCriteria(country="ABW")

        where_clause, params = filters.to_sql_where()

        self.assertIn("country_code", where_clause)
        self.assertEqual(len(params), 1)
        self.assertEqual(params[0], "ABW")

    def test_to_sql_where_with_no_filters(self):
        """Test to_sql_where() with no filters returns empty clause."""
        filters = FilterCriteria()

        where_clause, params = filters.to_sql_where()

        # Should return empty WHERE clause
        self.assertEqual(where_clause, "")
        self.assertEqual(len(params), 0)


if __name__ == '__main__':
    unittest.main()