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


if __name__ == '__main__':
    unittest.main()