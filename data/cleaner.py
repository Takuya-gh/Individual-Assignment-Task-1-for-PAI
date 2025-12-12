"""Data cleaning and normalization."""
import pandas as pd


class DataCleaner:
    """Handles data cleaning and schema normalization."""

    def normalize_schema(self, df: pd.DataFrame, dataset: str) -> pd.DataFrame:
        """
        Normalize dataset-specific schema to common format.

        Args:
            df: Input DataFrame with dataset-specific columns.
            dataset: Dataset type (e.g., "world_bank").

        Returns:
            DataFrame with normalized schema:
            [country_code, country_name, indicator_code, indicator_name, report_date, value]
        """
        if dataset == "world_bank":
            # Identify year columns (columns that can be parsed as integers)
            year_columns = [col for col in df.columns if col.isdigit()]

            # Rename identifier columns to common schema
            df_renamed = df.rename(columns={
                "Country Name": "country_name",
                "Country Code": "country_code",
                "Indicator Name": "indicator_name",
                "Indicator Code": "indicator_code"
            })

            # Melt wide format to long format
            id_vars = ["country_code", "country_name", "indicator_code", "indicator_name"]
            df_long = pd.melt(
                df_renamed,
                id_vars=id_vars,
                value_vars=year_columns,
                var_name="year",
                value_name="value"
            )

            # Transform year to ISO date format (YYYY-01-01)
            df_long["report_date"] = df_long["year"] + "-01-01"
            df_long = df_long.drop(columns=["year"])

            # Convert value to numeric (empty strings become NaN)
            df_long["value"] = pd.to_numeric(df_long["value"], errors='coerce')

            # Reorder columns
            df_long = df_long[["country_code", "country_name", "indicator_code", 
                              "indicator_name", "report_date", "value"]]

            return df_long
        else:
            raise ValueError(f"Unknown dataset type: {dataset}")
        
    def handle_missing(self, df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
        """
        Handle missing values in the DataFrame.

        Args:
            df: Input DataFrame.
            strategy: Strategy to handle missing values:
                    - "drop": Remove rows with missing values
                    - "fill_zero": Replace missing numeric values with 0

        Returns:
            DataFrame with missing values handled.
        """
        if strategy == "drop":
            # Drop rows with any missing values
            return df.dropna()
        elif strategy == "fill_zero":
            # Fill missing numeric values with 0
            return df.fillna(0)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")