"""Main entry point for the Health Insights Dashboard."""
from data.repository import DatabaseRepository
from data.cleaner import DataCleaner
from analysis.analyzer import Analyzer
from presentation.visualizer import Visualizer
from presentation.cli import CLIController
from utils.config import DEFAULT_DB_PATH


def main():
    """Initialize and run the CLI application."""
    # Initialize dependencies
    repo = DatabaseRepository(DEFAULT_DB_PATH)
    repo.connect()
    repo.init_schema()
    
    cleaner = DataCleaner()
    analyzer = Analyzer()
    visualizer = Visualizer()
    
    # Create and run CLI controller
    cli = CLIController(
        repo=repo,
        analyzer=analyzer,
        visualizer=visualizer,
        cleaner=cleaner
    )
    
    try:
        cli.run()
    finally:
        repo.disconnect()


if __name__ == "__main__":
    main()