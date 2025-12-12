"""Tests for CLIController."""
import unittest
from unittest.mock import Mock
from presentation.cli import CLIController


class TestCLIController(unittest.TestCase):
    """Test cases for CLIController class."""

    def test_cli_controller_instantiation(self):
        """Test that CLIController can be instantiated with dependencies."""
        # Create mock dependencies
        mock_repo = Mock()
        mock_analyzer = Mock()
        mock_visualizer = Mock()
        mock_cleaner = Mock()

        # Should instantiate without errors
        try:
            controller = CLIController(
                repo=mock_repo,
                analyzer=mock_analyzer,
                visualizer=mock_visualizer,
                cleaner=mock_cleaner
            )
            self.assertIsNotNone(controller)
        except Exception as e:
            self.fail(f"CLIController instantiation raised {type(e).__name__}: {e}")


if __name__ == '__main__':
    unittest.main()