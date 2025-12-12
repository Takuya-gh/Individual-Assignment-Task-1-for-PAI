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

    def save_reports(self, df: pd.DataFrame) -> int:
        """
        Save reports DataFrame to database.

        Expected DataFrame columns:
        - country_code, country_name, indicator_code, indicator_name, report_date, value

        Args:
            df: DataFrame with normalized schema.

        Returns:
            Number of report rows inserted.
        """
        if not self.conn:
            raise RuntimeError("Database not connected. Call connect() first.")

        cursor = self.conn.cursor()

        try:
            cursor.execute("BEGIN TRANSACTION;")

            # 1. Insert unique countries
            countries = df[["country_code", "country_name"]].drop_duplicates()
            for _, row in countries.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO countries (country_code, country_name, region)
                    VALUES (?, ?, NULL);
                """, (row["country_code"], row["country_name"]))

            # 2. Insert unique indicators
            indicators = df[["indicator_code", "indicator_name"]].drop_duplicates()
            for _, row in indicators.iterrows():
                cursor.execute("""
                    INSERT OR IGNORE INTO indicators (indicator_code, indicator_name, category)
                    VALUES (?, ?, NULL);
                """, (row["indicator_code"], row["indicator_name"]))

            # 3. Insert reports
            report_count = 0
            for _, row in df.iterrows():
                # Lookup indicator_id
                cursor.execute("""
                    SELECT indicator_id FROM indicators WHERE indicator_code = ?;
                """, (row["indicator_code"],))
                indicator_id = cursor.fetchone()[0]

                # Convert report_date to string if needed
                report_date = str(row["report_date"])

                # Insert report
                cursor.execute("""
                    INSERT INTO reports (country_code, indicator_id, report_date, value)
                    VALUES (?, ?, ?, ?);
                """, (row["country_code"], indicator_id, report_date, row["value"]))
                report_count += 1

            cursor.execute("COMMIT;")
            return report_count

        except Exception as e:
            cursor.execute("ROLLBACK;")
            raise

    def query_reports(self, sql: str, params: tuple = ()) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.

        Args:
            sql: SQL query string (use ? for parameters).
            params: Tuple of parameter values for the query.

        Returns:
            DataFrame containing query results.
        """
        if not self.conn:
            raise RuntimeError("Database not connected. Call connect() first.")

        # Execute query and fetch results
        df = pd.read_sql_query(sql, self.conn, params=params)
        return df
