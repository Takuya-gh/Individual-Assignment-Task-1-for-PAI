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

    def plot_line(self, df: pd.DataFrame, x: str, y: str, title: str) -> Figure:
        """
        Create a line plot.

        Args:
            df: DataFrame to plot.
            x: Column name for x-axis.
            y: Column name for y-axis.
            title: Plot title.

        Returns:
            Matplotlib Figure object.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df[x], df[y], marker='o', linewidth=2)
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig

    def plot_bar(self, df: pd.DataFrame, x: str, y: str, title: str) -> Figure:
        """
        Create a bar plot.

        Args:
            df: DataFrame to plot.
            x: Column name for x-axis.
            y: Column name for y-axis.
            title: Plot title.

        Returns:
            Matplotlib Figure object.
        """
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(df[x], df[y], color='steelblue')
        ax.set_xlabel(x)
        ax.set_ylabel(y)
        ax.set_title(title)
        ax.grid(True, alpha=0.3, axis='y')
        plt.xticks(rotation=45)
        plt.tight_layout()
        return fig