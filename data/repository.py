"""Database repository for storing and querying health data."""
import sqlite3
import pandas as pd
from typing import Optional


class DatabaseRepository:
    """Handles SQLite database operations."""

    def __init__(self, db_path: str) -> None:
        """
        Initialize DatabaseRepository with database path.

        Args:
            db_path: Path to SQLite database file.
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self) -> None:
        """Establish connection to the database."""
        self.conn = sqlite3.connect(self.db_path)
        # Enable foreign key support
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.conn.commit()

    def disconnect(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None

    def init_schema(self) -> None:
        """
        Create database schema (tables and indexes).

        Creates three tables:
        - countries: Country reference data
        - indicators: Indicator reference data
        - reports: Health report data with foreign keys
        """
        if not self.conn:
            raise RuntimeError("Database not connected. Call connect() first.")

        cursor = self.conn.cursor()

        # Create countries table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS countries (
                country_code TEXT PRIMARY KEY,
                country_name TEXT NOT NULL,
                region TEXT
            );
        """)

        # Create indicators table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS indicators (
                indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
                indicator_code TEXT UNIQUE NOT NULL,
                indicator_name TEXT NOT NULL,
                category TEXT
            );
        """)

        # Create reports table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                report_id INTEGER PRIMARY KEY AUTOINCREMENT,
                country_code TEXT NOT NULL,
                indicator_id INTEGER NOT NULL,
                report_date TEXT NOT NULL,
                value REAL,
                FOREIGN KEY (country_code) REFERENCES countries(country_code),
                FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id)
            );
        """)

        # Create index for filtering
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_reports_filters
            ON reports(country_code, indicator_id, report_date);
        """)

        self.conn.commit()
