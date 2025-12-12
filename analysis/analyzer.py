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