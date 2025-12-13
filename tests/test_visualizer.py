"""Tests for Visualizer."""
import unittest
import pandas as pd
from presentation.visualizer import Visualizer


class TestVisualizer(unittest.TestCase):
    """Test cases for Visualizer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.visualizer = Visualizer()

    def test_show_table_does_not_raise_exception(self):
        """Test that show_table() runs without errors."""
        df = pd.DataFrame({
            "country_code": ["ABW", "AFG", "ALB"],
            "value": [64.0, 32.0, 58.0]
        })

        # Should not raise any exception
        try:
            self.visualizer.show_table(df, max_rows=20)
        except Exception as e:
            self.fail(f"show_table raised {type(e).__name__}: {e}")

    def test_plot_line_returns_figure(self):
        """Test that plot_line() returns a matplotlib Figure."""
        df = pd.DataFrame({
            "report_date": ["2020-01-01", "2021-01-01", "2022-01-01"],
            "value": [64.0, 65.0, 66.0]
        })

        fig = self.visualizer.plot_line(df, x="report_date", y="value", title="Test Line Plot")

        # Should return a Figure object
        self.assertIsNotNone(fig)
        # Close figure to avoid memory leak
        import matplotlib.pyplot as plt
        plt.close(fig)

    def test_plot_bar_returns_figure(self):
        """Test that plot_bar() returns a matplotlib Figure."""
        df = pd.DataFrame({
            "country_code": ["ABW", "AFG", "ALB"],
            "value": [64.0, 32.0, 58.0]
        })

        fig = self.visualizer.plot_bar(df, x="country_code", y="value", title="Test Bar Plot")

        # Should return a Figure object
        self.assertIsNotNone(fig)
        # Close figure to avoid memory leak
        import matplotlib.pyplot as plt
        plt.close(fig)


if __name__ == '__main__':
    unittest.main()