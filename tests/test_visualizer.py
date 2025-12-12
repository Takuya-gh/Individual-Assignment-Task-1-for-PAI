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


if __name__ == '__main__':
    unittest.main()