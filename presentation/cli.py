"""Command-line interface controller."""
import pandas as pd
from typing import Optional
from data.repository import DatabaseRepository
from data.cleaner import DataCleaner
from data.csv_source import CSVDataSource
from analysis.analyzer import Analyzer
from analysis.filters import FilterCriteria
from presentation.visualizer import Visualizer
import matplotlib.pyplot as plt


class CLIController:
    """Manages the CLI menu and user interactions."""

    def __init__(
        self,
        repo: DatabaseRepository,
        analyzer: Analyzer,
        visualizer: Visualizer,
        cleaner: DataCleaner
    ) -> None:
        """
        Initialize CLIController with dependencies.

        Args:
            repo: DatabaseRepository instance.
            analyzer: Analyzer instance.
            visualizer: Visualizer instance.
            cleaner: DataCleaner instance.
        """
        self.repo = repo
        self.analyzer = analyzer
        self.visualizer = visualizer
        self.cleaner = cleaner
        self.current_df: Optional[pd.DataFrame] = None

    def run(self) -> None:
        """Run the main CLI loop."""
        print("\n" + "=" * 60)
        print("Public Health Data Insights Dashboard")
        print("=" * 60)

        while True:
            print("\nMenu:")
            print("1. Import data from CSV")
            print("2. Filter data")
            print("3. View summary statistics")
            print("4. Visualise trend")
            print("5. Exit")

            choice = input("\nChoose option: ").strip()

            if choice == "1":
                self.menu_import()
            elif choice == "2":
                self.menu_filter()
            elif choice == "3":
                self.menu_analyze()
            elif choice == "4":
                self.menu_visualize()
            elif choice == "5":
                print("Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1-5.")

    def menu_import(self) -> None:
        """Handle CSV import."""
        csv_path = input("Enter CSV file path (or press Enter for default): ").strip()
        if not csv_path:
            csv_path = "data/API_SP.DYN.LE00.IN_DS2_en_csv_v2_2505.csv"

        try:
            print(f"Loading CSV from: {csv_path}")
            source = CSVDataSource(csv_path)
            
            if not source.validate():
                print("Error: Invalid CSV file.")
                return

            # Load raw data
            df_raw = source.load()
            print(f"Loaded {len(df_raw)} rows from CSV.")

            # Normalize schema
            print("Normalizing schema...")
            df_normalized = self.cleaner.normalize_schema(df_raw, dataset="world_bank")
            print(f"Normalized to {len(df_normalized)} rows (long format).")

            # Handle missing values
            df_clean = self.cleaner.handle_missing(df_normalized, strategy="drop")
            print(f"After cleaning: {len(df_clean)} rows.")

            # Save to database
            print("Saving to database...")
            row_count = self.repo.save_reports(df_clean)
            print(f"Successfully imported {row_count} reports to database.")

            self.current_df = df_clean

        except Exception as e:
            print(f"Error during import: {e}")

    def menu_filter(self) -> None:
        """Handle data filtering."""
        country = input("Enter country code (or press Enter to skip): ").strip() or None
        date_from = input("Enter start date YYYY-MM-DD (or press Enter to skip): ").strip() or None
        date_to = input("Enter end date YYYY-MM-DD (or press Enter to skip): ").strip() or None

        try:
            filters = FilterCriteria(country=country, date_from=date_from, date_to=date_to)
            where_clause, params = filters.to_sql_where()

            if where_clause:
                sql = f"SELECT * FROM reports {where_clause}"
            else:
                sql = "SELECT * FROM reports"

            df = self.repo.query_reports(sql, params)
            print(f"Found {len(df)} matching rows.")
            self.current_df = df

        except Exception as e:
            print(f"Error during filtering: {e}")

    def menu_analyze(self) -> None:
        """Handle summary statistics."""
        if self.current_df is None or len(self.current_df) == 0:
            print("No data loaded. Please import or filter data first.")
            return

        try:
            stats = self.analyzer.summary_stats(self.current_df, value_col="value")
            print("\nSummary Statistics:")
            print(f"  Mean:  {stats['mean']:.2f}")
            print(f"  Min:   {stats['min']:.2f}")
            print(f"  Max:   {stats['max']:.2f}")
            print(f"  Count: {stats['count']}")

        except Exception as e:
            print(f"Error during analysis: {e}")

    def menu_visualize(self) -> None:
        """Handle trend visualization."""
        if self.current_df is None or len(self.current_df) == 0:
            print("No data loaded. Please import or filter data first.")
            return

        try:
            trend = self.analyzer.trend_over_time(self.current_df, date_col="report_date", value_col="value")
            
            if len(trend) == 0:
                print("No trend data to visualize.")
                return

            fig = self.visualizer.plot_line(trend, x="report_date", y="value", title="Trend Over Time")
            plt.show()

        except Exception as e:
            print(f"Error during visualization: {e}")