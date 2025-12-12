"""Data visualization and display."""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


class Visualizer:
    """Handles data visualization and table display."""

    def show_table(self, df: pd.DataFrame, max_rows: int = 20) -> None:
        """
        Display DataFrame as a formatted table.

        Args:
            df: DataFrame to display.
            max_rows: Maximum number of rows to show.
        """
        print("\n" + "=" * 80)
        print("DATA TABLE")
        print("=" * 80)
        print(df.to_string(max_rows=max_rows, index=False))
        print("=" * 80)
        print(f"Total rows: {len(df)}")
        print()