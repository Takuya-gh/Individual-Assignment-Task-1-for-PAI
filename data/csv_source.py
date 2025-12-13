"""CSV data source for loading health data files."""
import pandas as pd
import os


class CSVDataSource:
    """Loads and validates CSV files in World Bank WDI format."""

    def __init__(self, file_path: str) -> None:
        """
        Initialize CSVDataSource with a file path.

        Args:
            file_path: Path to the CSV file.
        """
        self.file_path = file_path

    def validate(self) -> bool:
        """
        Validate that the CSV file exists and is readable.

        Returns:
            True if file is valid, False otherwise.
        """
        try:
            # Check if file exists
            if not os.path.exists(self.file_path):
                return False
            
            # Check if file is not empty
            if os.path.getsize(self.file_path) == 0:
                return False
            
            # Try reading the file
            pd.read_csv(self.file_path, skiprows=4, nrows=0)
            return True
        except Exception:
            return False

    def load(self) -> pd.DataFrame:
        """
        Load CSV file into a pandas DataFrame.

        Skips the first 4 metadata rows of World Bank CSV format.

        Returns:
            DataFrame containing the CSV data.

        Raises:
            ValueError: If the file cannot be validated or loaded.
        """
        if not self.validate():
            raise ValueError(f"Cannot load CSV file: {self.file_path}")
        
        # Load CSV with skiprows=4 to skip World Bank metadata rows
        df = pd.read_csv(self.file_path, skiprows=4)
        return df