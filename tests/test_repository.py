"""Tests for DatabaseRepository."""
import unittest
import os
import tempfile
import sqlite3
from data.repository import DatabaseRepository


class TestDatabaseRepository(unittest.TestCase):
    """Test cases for DatabaseRepository class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.repo = DatabaseRepository(self.db_path)

    def tearDown(self):
        """Clean up test fixtures."""
        self.repo.disconnect()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_connect_creates_database_file(self):
        """Test that connect() creates the database file."""
        self.repo.connect()
        self.assertTrue(os.path.exists(self.db_path))

    def test_init_schema_creates_tables(self):
        """Test that init_schema() creates required tables."""
        self.repo.connect()
        self.repo.init_schema()

        # Query sqlite_master to check tables exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()

        self.assertIn("countries", tables)
        self.assertIn("indicators", tables)
        self.assertIn("reports", tables)

    def test_save_reports_inserts_data(self):
        """Test that save_reports() inserts data into all tables."""
        import pandas as pd
        
        self.repo.connect()
        self.repo.init_schema()

        # Create sample DataFrame with normalized schema
        df = pd.DataFrame([
            {"country_code": "ABW", "country_name": "Aruba", 
            "indicator_code": "SP.DYN.LE00.IN", "indicator_name": "Life expectancy",
            "report_date": "1960-01-01", "value": 64.049},
            {"country_code": "ABW", "country_name": "Aruba",
            "indicator_code": "SP.DYN.LE00.IN", "indicator_name": "Life expectancy",
            "report_date": "1961-01-01", "value": 64.215},
            {"country_code": "AFG", "country_name": "Afghanistan",
            "indicator_code": "SP.DYN.LE00.IN", "indicator_name": "Life expectancy",
            "report_date": "1960-01-01", "value": 32.799}
        ])

        # Save reports
        row_count = self.repo.save_reports(df)

        # Should return 3 (number of report rows inserted)
        self.assertEqual(row_count, 3)

        # Verify countries table has 2 rows
        cursor = self.repo.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM countries")
        self.assertEqual(cursor.fetchone()[0], 2)

        # Verify indicators table has 1 row
        cursor.execute("SELECT COUNT(*) FROM indicators")
        self.assertEqual(cursor.fetchone()[0], 1)

        # Verify reports table has 3 rows
        cursor.execute("SELECT COUNT(*) FROM reports")
        self.assertEqual(cursor.fetchone()[0], 3)


if __name__ == '__main__':
    unittest.main()