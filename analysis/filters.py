"""Filtering criteria for data queries."""
from typing import Optional, Tuple


class FilterCriteria:
    """Represents filtering criteria for health data queries."""

    def __init__(
        self,
        country: Optional[str] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None
    ) -> None:
        """
        Initialize FilterCriteria.

        Args:
            country: Country code to filter by (e.g., "ABW").
            date_from: Start date in ISO format (e.g., "2020-01-01").
            date_to: End date in ISO format (e.g., "2024-12-31").
        """
        self.country = country
        self.date_from = date_from
        self.date_to = date_to

    def to_sql_where(self) -> Tuple[str, tuple]:
        """
        Generate SQL WHERE clause and parameters.

        Returns:
            Tuple of (where_clause, params):
            - where_clause: SQL WHERE string (or empty if no filters)
            - params: Tuple of parameter values
        """
        conditions = []
        params = []

        if self.country:
            conditions.append("country_code = ?")
            params.append(self.country)

        if self.date_from:
            conditions.append("report_date >= ?")
            params.append(self.date_from)

        if self.date_to:
            conditions.append("report_date <= ?")
            params.append(self.date_to)

        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
            return where_clause, tuple(params)
        else:
            return "", ()