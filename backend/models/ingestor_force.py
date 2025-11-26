"""
Force load model.

Handles force load configuration and execution.
"""
from typing import List, Dict, Any
from backend.lib.errors import ParameterValidationError, BusinessLogicError

# ==============================================================================
# FORCE LOAD CONFIGURATION
# ==============================================================================

FORCE_LOAD_TABLES = {
    "Inflation Env": {
        "description": "Inflation environment configuration",
        "data": [
            {'configName': 'Config1', 'key': 'inflation.rate', 'group': 'ENV'},
            {'configName': 'Config2', 'key': 'inflation.curve', 'group': 'ENV'},
            {'configName': 'Config3', 'key': 'inflation.spread', 'group': 'ENV'},
        ]
    },
    "Options ScenarioGamma": {
        "description": "Options scenario gamma configuration",
        "data": [
            {'configName': 'Gamma1', 'key': 'gamma.scenario.base', 'group': 'OPTS'},
            {'configName': 'Gamma2', 'key': 'gamma.scenario.stress', 'group': 'OPTS'},
        ]
    },
}

# ==============================================================================
# MODEL IMPLEMENTATION
# ==============================================================================


class IngestorForceModel:
    """
    Model for force load operations.

    Handles:
    - Validating table configurations
    - Processing force load requests
    - Returning success/error states
    """

    def __init__(self):
        """Initialize model."""
        pass

    def get_default_config(self, table_name):
        """
        Get default configuration for a predefined table.

        Args:
            table_name: Name of predefined table

        Returns:
            List of configuration dictionaries with column data

        Raises:
            ParameterValidationError: If table name not found
        """
        if table_name not in FORCE_LOAD_TABLES:
            raise ParameterValidationError(
                f"Table '{table_name}' not found in configuration",
                user_message=f"Unknown table: {table_name}"
            )

        table_config = FORCE_LOAD_TABLES[table_name]
        return table_config['data']

    def get_table_schema(self, table_name):
        """
        Get the schema for a predefined table.

        Args:
            table_name: Name of predefined table

        Returns:
            Dictionary with table configuration including description and data

        Raises:
            ParameterValidationError: If table name not found
        """
        if table_name not in FORCE_LOAD_TABLES:
            raise ParameterValidationError(
                f"Table '{table_name}' not found in configuration",
                user_message=f"Unknown table: {table_name}"
            )

        return FORCE_LOAD_TABLES[table_name]

    def validate_config(self, config_data):
        """
        Validate configuration data.

        Args:
            config_data: List of config dictionaries

        Raises:
            ParameterValidationError: If config is invalid
        """
        if not config_data:
            raise ParameterValidationError(
                "Configuration data cannot be empty",
                user_message="Please provide at least one configuration row"
            )

        for i, row in enumerate(config_data):
            # Check required keys
            required_keys = ['configName', 'key', 'group']
            missing_keys = [k for k in required_keys if k not in row]

            if missing_keys:
                raise ParameterValidationError(
                    f"Row {i} missing required keys: {missing_keys}",
                    user_message=f"Row {i+1} is missing required fields"
                )

            # Check for empty values (skip empty rows)
            all_empty = all(not row.get(k) for k in required_keys)
            some_empty = any(not row.get(k) for k in required_keys)

            if some_empty and not all_empty:
                raise ParameterValidationError(
                    f"Row {i} has incomplete data",
                    user_message=f"Row {i+1} must have all fields filled or be empty"
                )

    def execute_force_load(
        self,
        table_name,
        config_data
    ):
        """
        Execute force load operation.

        Args:
            table_name: Table to load
            config_data: Configuration data

        Returns:
            Dictionary with:
                - success: True/False
                - message: Result message
                - rows_processed: Number of rows processed

        Raises:
            BusinessLogicError: If force load fails
        """
        # TODO: Replace with actual force load logic
        # For now, simulate success

        # Filter out empty rows
        valid_rows = [
            row for row in config_data
            if any(row.get(k) for k in ['configName', 'key', 'group'])
        ]

        return {
            'success': True,
            'message': f'Successfully loaded {len(valid_rows)} configurations to {table_name}',
            'rows_processed': len(valid_rows),
            'table_name': table_name
        }
