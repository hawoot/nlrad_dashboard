"""
Timeline data model.

Handles querying and processing of ingestor timeline data.
"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any
from backend.lib.errors import DataAccessError

# ==============================================================================
# TIMELINE CONFIGURATION
# ==============================================================================

TIMELINE_DESKS = ["Options", "Exotics", "Inflation", "LDFX", "FXG"]

# ==============================================================================
# MODEL IMPLEMENTATION
# ==============================================================================


class IngestorTimelineModel:
    """
    Model for ingestor timeline data.

    Provides methods to:
    - Query timeline data by desk and date
    - Process and transform raw data
    - Return structured results
    """

    def __init__(self):
        """Initialize model."""
        # Note: No database connection yet - user hasn't specified DB
        # Will use mock data for now
        pass

    def get_timeline_data(
        self,
        desk,
        date
    ):
        """
        Query timeline data for a specific desk and date.

        Args:
            desk: Desk name (Options, Exotics, Inflation, LDFX, FXG)
            date: Query date

        Returns:
            DataFrame with columns: TS, COB, data, overwrite

        Raises:
            DataAccessError: If query fails
        """
        # TODO: Replace with actual database query
        # For now, return mock data
        return self._get_mock_data(desk, date)

    def _get_mock_data(self, desk, date):
        """
        Generate mock timeline data for testing.

        This is a placeholder until database is configured.

        Args:
            desk: Desk name
            date: Query date

        Returns:
            Mock DataFrame with correct schema
        """
        # Generate sample timestamps throughout the day
        num_records = 10
        timestamps = [
            date + timedelta(hours=i)
            for i in range(num_records)
        ]

        # Create mock data
        data = {
            'TS': timestamps,
            'COB': [date.date()] * num_records,
            'data': [f'/NLRAD/{desk}/path_{i}' for i in range(num_records)],
            'overwrite': [bool(i % 2) for i in range(num_records)]
        }

        df = pd.DataFrame(data)

        return df

    def process_timeline_data(self, df):
        """
        Process raw timeline data and add analytics.

        Args:
            df: Raw timeline DataFrame

        Returns:
            Dictionary with:
                - records: List of record dictionaries
                - summary: Summary statistics
                - metadata: Query metadata
                - dataframe: Original DataFrame for UI rendering
        """
        # Convert DataFrame to records
        records = df.to_dict('records')

        # Calculate summary statistics
        summary = {
            'total_records': len(df),
            'overwrite_count': int(df['overwrite'].sum()) if len(df) > 0 else 0,
            'date_range': {
                'earliest': df['TS'].min().isoformat() if len(df) > 0 else None,
                'latest': df['TS'].max().isoformat() if len(df) > 0 else None,
            }
        }

        return {
            'records': records,
            'summary': summary,
            'dataframe': df  # Include for UI rendering
        }
