"""Data analysis and statistical calculations."""
import pandas as pd


class Analyzer:
    """Handles data analysis operations."""

    def summary_stats(self, df: pd.DataFrame, value_col: str = "value") -> dict:
        """
        Calculate summary statistics for a column.

        Args:
            df: Input DataFrame.
            value_col: Name of the column to analyze.

        Returns:
            Dictionary with keys: mean, min, max, count
        """
        stats = df[value_col].agg(["mean", "min", "max", "count"])
        
        # Convert to dict with native Python types
        return {
            "mean": float(stats["mean"]),
            "min": float(stats["min"]),
            "max": float(stats["max"]),
            "count": int(stats["count"])
        }
    
    def trend_over_time(self, df: pd.DataFrame, date_col: str = "report_date", 
                   value_col: str = "value") -> pd.DataFrame:
        """
        Calculate trend over time (mean value per date).

        Args:
            df: Input DataFrame.
            date_col: Name of the date column.
            value_col: Name of the value column.

        Returns:
            DataFrame with columns [date_col, value_col], sorted by date.
        """
        # Group by date and calculate mean
        trend = df.groupby(date_col)[value_col].mean().reset_index()
        
        # Sort by date
        trend = trend.sort_values(by=date_col)
        
        return trend